#!/usr/bin/env python3
"""
Aiderベンチマークの--stats出力からYAML部分だけ抽出し、
benchmark-results/<スイート名>.yaml として保存するスクリプト。

使い方（aiderディレクトリ直下から実行）:
  python collect_results.py
"""
import subprocess
import sys
from pathlib import Path


BENCHMARKS_DIR = Path("tmp.benchmarks")
RESULTS_DIR = Path("benchmark-results")

# --stats出力でスキップすべき行の判定
SKIP_PREFIXES = (
    "\u2500",   # ─ (区切り線)
    "costs:",   # costs: $0.00...
    "Warning:", # Warning: incomplete...
)


def extract_yaml(stats_output: str) -> str:
    """--stats出力からYAMLブロックだけを取り出す。"""
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

    # 末尾の空行を除去
    while yaml_lines and not yaml_lines[-1].strip():
        yaml_lines.pop()

    return "\n".join(yaml_lines) + "\n" if yaml_lines else ""


def suite_name_from_dirname(dirname: str) -> str:
    """
    '2026-06-19-08-08-58--north-diff-python' → 'north-diff-python'
    タイムスタンプ部分（最初の--より前）を除去する。
    """
    parts = dirname.split("--", 1)
    return parts[1] if len(parts) == 2 else dirname


def find_bench_dirs() -> list[Path]:
    """tmp.benchmarks/ 内のベンチマーク結果ディレクトリを返す（polyglot-benchmark等は除外）。"""
    exclude_prefixes = ("polyglot",)
    return sorted(
        d for d in BENCHMARKS_DIR.iterdir()
        if d.is_dir() and not any(d.name.startswith(p) for p in exclude_prefixes)
    )


def main() -> None:
    if not BENCHMARKS_DIR.exists():
        print(f"Error: {BENCHMARKS_DIR} が見つかりません。aiderディレクトリ直下で実行してください。")
        sys.exit(1)

    RESULTS_DIR.mkdir(exist_ok=True)

    bench_dirs = find_bench_dirs()
    if not bench_dirs:
        print("処理対象のベンチマークディレクトリが見つかりませんでした。")
        sys.exit(1)

    print(f"{len(bench_dirs)} 件のベンチマークを処理します。\n")

    for bench_dir in bench_dirs:
        print(f"  処理中: {bench_dir.name}")

        result = subprocess.run(
            ["./benchmark/benchmark.py", "--stats", str(bench_dir)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"    ⚠ --stats コマンドが失敗しました（スキップ）")
            if result.stderr:
                print(f"    stderr: {result.stderr.strip()}")
            continue

        yaml_content = extract_yaml(result.stdout)
        if not yaml_content.strip():
            print(f"    ⚠ YAMLブロックが見つかりませんでした（スキップ）")
            continue

        suite_name = suite_name_from_dirname(bench_dir.name)
        output_path = RESULTS_DIR / f"{suite_name}.yaml"
        output_path.write_text(yaml_content, encoding="utf-8")
        print(f"    ✓ 保存: {output_path}")

    print(f"\n完了。{RESULTS_DIR}/ の内容:")
    for f in sorted(RESULTS_DIR.glob("*.yaml")):
        print(f"  {f}")


if __name__ == "__main__":
    main()
