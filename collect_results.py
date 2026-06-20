import subprocess
import sys
from pathlib import Path


BENCHMARKS_DIR = Path("tmp.benchmarks")
RESULTS_DIR = Path("/workspace/benchmark-results/results")


SKIP_PREFIXES = (
    "\u2500",
    "costs:",
    "Warning:",
)


def extract_yaml(stats_output: str) -> str:
    yaml_lines = []
    in_yaml = False

    for line in stats_output.splitlines():
        if line.startswith("- dirname:"):
            in_yaml = True

        if not in_yaml:
            continue

        if any(line.startswith(p) for p in SKIP_PREFIXES):
            break

        yaml_lines.append(line)

    while yaml_lines and not yaml_lines[-1].strip():
        yaml_lines.pop()

    return "\n".join(yaml_lines) + "\n" if yaml_lines else ""


def suite_name_from_dirname(dirname: str) -> str:
    parts = dirname.split("--", 1)
    return parts[1] if len(parts) == 2 else dirname


def find_bench_dirs() -> list[Path]:
    exclude_prefixes = ("polyglot",)
    return sorted(
        d for d in BENCHMARKS_DIR.iterdir()
        if d.is_dir() and not any(d.name.startswith(p) for p in exclude_prefixes)
    )


def main() -> None:
    if not BENCHMARKS_DIR.exists():
        print(f"Error: {BENCHMARKS_DIR} not found. Please run this from the aider root directory.")
        sys.exit(1)

    RESULTS_DIR.mkdir(exist_ok=True)

    bench_dirs = find_bench_dirs()
    if not bench_dirs:
        print("No benchmark directories found to process.")
        sys.exit(1)

    print(f"Processing {len(bench_dirs)} benchmark(s).\n")

    for bench_dir in bench_dirs:
        print(f"  Processing: {bench_dir.name}")

        result = subprocess.run(
            ["./benchmark/benchmark.py", "--stats", str(bench_dir)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"    ⚠ --stats command failed (skipping)")
            if result.stderr:
                print(f"    stderr: {result.stderr.strip()}")
            continue

        yaml_content = extract_yaml(result.stdout)
        if not yaml_content.strip():
            print(f"    ⚠ No YAML block found (skipping)")
            continue

        suite_name = suite_name_from_dirname(bench_dir.name)
        output_path = RESULTS_DIR / f"{suite_name}.yaml"
        output_path.write_text(yaml_content, encoding="utf-8")
        print(f"    ✓ Saved: {output_path}")

    print(f"\nDone. Contents of {RESULTS_DIR}/:")
    for f in sorted(RESULTS_DIR.glob("*.yaml")):
        print(f"  {f}")


if __name__ == "__main__":
    main()
