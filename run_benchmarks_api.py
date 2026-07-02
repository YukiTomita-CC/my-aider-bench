import argparse
import logging
import os
import subprocess
import sys
import tempfile
import yaml

# ── Logging configuration ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("benchmark_run_api.log"),
    ],
)
log = logging.getLogger(__name__)

LANGUAGES = ["python", "cpp"]


# ── Load configuration ──────────────────────────────────────────────────────
def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


# ── Generate temporary model_settings.yml ──────────────────
def write_custom_model_settings(model_string: str, settings: dict) -> str:
    entry = {"name": model_string, **settings}
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".yml", prefix="model_settings_", delete=False
    )
    yaml.dump([entry], tmp)
    tmp.close()
    log.info(f"Custom model settings written: {tmp.name}")
    return tmp.name


# ── Run benchmark ───────────────────────────────────────────────────────────
def run_benchmark(
    suite_name: str,
    model_string: str,
    language: str,
    benchmark_script: str,
    model_settings_path: str | None = None,
) -> None:

    cmd = [
        sys.executable, benchmark_script,
        suite_name,
        "--model", model_string,
        "--languages", language,
    ]
    if model_settings_path:
        cmd += ["--read-model-settings", model_settings_path]

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
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=results_dir, check=True)
    subprocess.run(["git", "push"], cwd=results_dir, check=True)
    log.info("Push complete.")


# ── Main loop ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Aider benchmark loop (API models)")
    parser.add_argument("config", help="Path to config YAML")
    args = parser.parse_args()

    cfg = load_config(args.config)
    bench = cfg.get("benchmark", {})

    benchmark_script = bench.get("benchmark_script", "/workspace/aider/benchmark/benchmark.py")
    aider_dir        = bench.get("aider_dir", "/workspace/aider")
    results_dir      = bench.get("results_dir", "/workspace/benchmark-results")

    models = [m for m in cfg["models"] if m.get("completed") is not True]
    total = len(models) * len(LANGUAGES)
    log.info(
        f"Total runs: {total}  "
        f"({len(models)} models × {len(LANGUAGES)} languages)"
    )

    for model_cfg in models:
        name            = model_cfg["name"]
        model_string    = model_cfg["model_string"]
        custom_settings = model_cfg.get("model_settings")

        model_settings_path = None
        if custom_settings:
            model_settings_path = write_custom_model_settings(model_string, custom_settings)

        try:
            for language in LANGUAGES:
                suite = f"{name}-{language}"
                log.info(f"{'='*60}")
                log.info(f"Suite: {suite}")
                log.info(f"{'='*60}")
                run_benchmark(
                    suite, model_string, language,
                    benchmark_script, model_settings_path,
                )
        finally:
            if model_settings_path and os.path.exists(model_settings_path):
                os.unlink(model_settings_path)

        push_results(name, aider_dir, results_dir)

    log.info("All benchmarks completed.")


if __name__ == "__main__":
    main()
