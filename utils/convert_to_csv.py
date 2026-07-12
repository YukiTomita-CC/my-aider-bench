import sys
import csv
import re
import yaml
from pathlib import Path

DEFAULT_INPUT_DIR = Path(__file__).parent.parent / "results"
OUTPUT_PATH = Path(DEFAULT_INPUT_DIR) /"results.csv"


def extract_language(dirname: str) -> str:
    match = re.search(r"-(python|cpp)$", dirname)
    if match:
        return match.group(1)
    return ""


def load_yaml(filepath: Path) -> list[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def convert(yaml_files: list[Path]) -> None:
    all_rows = []

    for yaml_file in yaml_files:
        entries = load_yaml(yaml_file)
        for entry in entries:
            dirname = entry.pop("dirname", "")
            language = extract_language(dirname)
            row = {"language": language, **entry}
            all_rows.append(row)

    if not all_rows:
        print("No data found to convert.")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    ordered_columns = [
        "model", "language", "edit_format",
        "pass_rate_2", "pass_rate_1", "pass_num_2", "pass_num_1",
        "percent_cases_well_formed", "num_malformed_responses", "num_with_malformed_responses", "syntax_errors", "exhausted_context_windows",
        "error_outputs", "user_asks", "lazy_comments", "indentation_errors", "test_timeouts",
        "total_cost", "seconds_per_case", "prompt_tokens", "completion_tokens",
        "test_cases", "total_tests", "command", "versions", "commit_hash", "date",
    ]
    all_keys = set(all_rows[0].keys())
    known = [c for c in ordered_columns if c in all_keys]
    unknown = [c for c in all_rows[0].keys() if c not in set(ordered_columns)]
    fieldnames = known + unknown
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Done: {len(all_rows)} record(s) -> {OUTPUT_PATH}")


if __name__ == "__main__":
    input_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT_DIR

    if not input_dir.exists():
        print(f"Directory not found: {input_dir}")
        sys.exit(1)

    yaml_files = sorted(input_dir.glob("*.yaml"))

    if not yaml_files:
        print(f"No YAML files found in: {input_dir}")
        sys.exit(1)

    print(f"Processing {len(yaml_files)} YAML file(s) from: {input_dir}")
    convert(yaml_files)
