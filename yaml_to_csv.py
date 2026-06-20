import sys
import csv
import yaml
from pathlib import Path

EDIT_FORMATS = {"whole", "diff"}
LANGUAGES = {"python", "cpp"}


def parse_filename(stem: str) -> tuple[str, str, str]:
    parts = stem.split("-")

    if len(parts) < 3:
        raise ValueError(f"Unparseable filename: '{stem}'")

    language = parts[-1]
    edit_format = parts[-2]
    model = "-".join(parts[:-2])

    if edit_format not in EDIT_FORMATS:
        raise ValueError(f"Unknown edit_format '{edit_format}' (file: '{stem}')")
    if language not in LANGUAGES:
        raise ValueError(f"Unknown language '{language}' (file: '{stem}')")

    return model, edit_format, language


def main():
    results_dir = Path("./results")
    output_path = Path("./results/results.csv")

    if not results_dir.exists():
        print(f"Error: directory '{results_dir}' not found", file=sys.stderr)
        sys.exit(1)

    yaml_files = sorted(results_dir.glob("*.yaml")) + sorted(results_dir.glob("*.yml"))

    if not yaml_files:
        print(f"Error: no YAML files found in '{results_dir}'", file=sys.stderr)
        sys.exit(1)

    rows = []
    for path in yaml_files:
        try:
            model, edit_format, language = parse_filename(path.stem)
        except ValueError as e:
            print(f"Skipping: {e}", file=sys.stderr)
            continue

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        record = data[0] if isinstance(data, list) else data

        rows.append({
            "model": model,
            "edit_format": edit_format,
            "language": language,
            **record,
        })

    if not rows:
        print("No files could be converted", file=sys.stderr)
        sys.exit(1)

    all_keys = list(dict.fromkeys(k for row in rows for k in row))

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ {len(rows)} record(s) written to '{output_path}'")


if __name__ == "__main__":
    main()
