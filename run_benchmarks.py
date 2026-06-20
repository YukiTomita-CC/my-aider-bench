import argparse
import logging
import os
import shlex
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

# ── Logging configuration ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("benchmark_run.log"),
    ],
)
log = logging.getLogger(__name__)

EDIT_FORMATS = ["whole", "diff"]
LANGUAGES = ["python", "cpp"]


# ── Load configuration ──────────────────────────────────────────────────────
def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


# ── Model download ──────────────────────────────────────────────────────────
def download_model(repo: str, gguf_filter: str, local_dir: str) -> None:
    log.info(f"Downloading {repo}  filter={gguf_filter}")
    subprocess.run(
        [
            "hf", "download", repo,
            "--include", gguf_filter,
            "--local-dir", local_dir,
        ],
        check=True,
    )


def find_gguf(local_dir: str) -> str:
    files = list(Path(local_dir).rglob("*.gguf"))
    if not files:
        raise FileNotFoundError(f"No .gguf file found under {local_dir}")
    return str(files[0])


# ── Generate model_settings.yml ─────────────────────────────────────────────
def write_model_settings(alias: str, num_ctx: int, max_tokens: int) -> str:
    settings = [
        {
            "name": f"openai/{alias}",
            "extra_params": {"num_ctx": num_ctx, "max_tokens": max_tokens},
        }
    ]
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".yml", prefix="model_settings_", delete=False
    )
    yaml.dump(settings, tmp)
    tmp.close()
    return tmp.name


# ── Start / wait for / stop llama-server ────────────────────────────────────
def build_server_cmd(
    gguf_path: str, alias: str, server_cfg: dict, server_bin: str
) -> list[str]:
    extra_args = shlex.split(server_cfg.get("extra_args", ""))
    return [server_bin, "-m", gguf_path] + extra_args + ["--alias", alias]


def start_server(
    gguf_path: str, alias: str, server_cfg: dict, server_bin: str
) -> subprocess.Popen:
    cmd = build_server_cmd(gguf_path, alias, server_cfg, server_bin)
    log_path = f"server_{alias}.log"
    log.info(f"Starting llama-server  log={log_path}")
    log.debug("Command: " + " ".join(cmd))
    log_file = open(log_path, "w")
    return subprocess.Popen(cmd, stdout=log_file, stderr=log_file)


def wait_for_server(health_url: str, timeout: int) -> None:
    log.info(f"Waiting for server at {health_url}  timeout={timeout}s ...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(health_url, timeout=2) as resp:
                if resp.status == 200:
                    log.info("Server is ready.")
                    return
        except Exception:
            pass
        time.sleep(3)
    raise TimeoutError(f"Server did not become ready within {timeout}s")


def stop_server(proc: subprocess.Popen) -> None:
    if proc is None or proc.poll() is not None:
        return
    log.info("Stopping llama-server ...")
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        log.warning("Graceful shutdown timed out — killing.")
        proc.kill()
        proc.wait()
    log.info("Server stopped.")


# ── Run benchmark ───────────────────────────────────────────────────────────
def run_benchmark(
    suite_name: str,
    alias: str,
    edit_format: str,
    language: str,
    threads: int,
    model_settings_path: str,
    benchmark_script: str,
) -> None:
    cmd = [
        sys.executable, benchmark_script,
        suite_name,
        "--model", f"openai/{alias}",
        "--edit-format", edit_format,
        "--threads", str(threads),
        "--languages", language,
        "--read-model-settings", model_settings_path,
    ]
    log.info("Running: " + " ".join(cmd))
    subprocess.run(cmd, check=True)


# ── Push results to GitHub ──────────────────────────────────────────────────
def push_results(model_name: str, aider_dir: str, results_dir: str) -> None:
    log.info("Collecting results ...")
    subprocess.run([sys.executable, "collect_results.py"], cwd=aider_dir, check=True)

    log.info("Pushing results to GitHub ...")
    subprocess.run(["git", "add", "."], cwd=results_dir, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Add {model_name} benchmark results"],
        cwd=results_dir,
        check=True,
    )
    subprocess.run(["git", "push"], cwd=results_dir, check=True)
    log.info("Push complete.")


# ── Main loop ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Aider benchmark loop")
    parser.add_argument("config", help="Path to config YAML")
    args = parser.parse_args()

    cfg = load_config(args.config)
    bench = cfg.get("benchmark", {})

    threads         = bench.get("threads", 4)
    models_dir      = bench.get("models_dir", "/workspace/models")
    benchmark_script= bench.get("benchmark_script", "/workspace/aider/benchmark/benchmark.py")
    server_bin      = bench.get("server_bin", "/workspace/llama.cpp/build/bin/llama-server")
    health_url      = bench.get("server_health_url", "http://localhost:8080/health")
    health_timeout  = bench.get("server_health_timeout", 180)
    aider_dir       = bench.get("aider_dir", "/workspace/aider")
    results_dir     = bench.get("results_dir", "/workspace/benchmark-results")

    models = cfg["models"]
    total = len(models) * len(EDIT_FORMATS) * len(LANGUAGES)
    log.info(
        f"Total runs: {total}  "
        f"({len(models)} models × {len(EDIT_FORMATS)} formats × {len(LANGUAGES)} languages)"
    )

    for model_cfg in models:
        name       = model_cfg["name"]
        repo       = model_cfg["repo"]
        gguf_filter= model_cfg["gguf_filter"]
        alias      = model_cfg.get("alias", name)
        server_cfg = model_cfg["server"]
        aider_cfg  = model_cfg["aider"]

        local_dir = os.path.join(models_dir, name)
        os.makedirs(local_dir, exist_ok=True)

        # ① Download model
        download_model(repo, gguf_filter, local_dir)
        gguf_path = find_gguf(local_dir)
        log.info(f"GGUF: {gguf_path}")

        # ② Generate temporary model_settings.yml
        model_settings_path = write_model_settings(
            alias, aider_cfg["num_ctx"], aider_cfg["max_tokens"]
        )

        # ③ Start server (always stopped in finally block)
        proc = start_server(gguf_path, alias, server_cfg, server_bin)
        try:
            wait_for_server(health_url, health_timeout)

            # ④ Benchmark loop (whole/diff × python/cpp)
            for edit_format in EDIT_FORMATS:
                for language in LANGUAGES:
                    suite = f"{name}-{edit_format}-{language}"
                    log.info(f"{'='*60}")
                    log.info(f"Suite: {suite}")
                    log.info(f"{'='*60}")
                    run_benchmark(
                        suite, alias, edit_format, language,
                        threads, model_settings_path, benchmark_script,
                    )

        finally:
            stop_server(proc)
            os.unlink(model_settings_path)

        # Only reached if all 4 runs succeeded
        push_results(name, aider_dir, results_dir)

        # Delete used GGUF to save disk space (keep only one file at a time)
        log.info(f"Deleting GGUF: {gguf_path}")
        os.unlink(gguf_path)

    log.info("All benchmarks completed.")


if __name__ == "__main__":
    main()
