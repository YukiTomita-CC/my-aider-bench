import pandas as pd
import sys

MODEL_MAP = {
    "openai/devstral-small":      "llama.cpp/Devstral-Small-2-24B-Instruct-2512",
    "openai/devstral":            "llama.cpp/Devstral-2-123B-Instruct-2512",
    "openai/gemma4-12b-agentic":  "llama.cpp/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2",
    "openai/gemma4-12b":          "llama.cpp/gemma-4-12B-it",
    "openai/gemma4-26b-a4b":      "llama.cpp/gemma-4-26B-A4B-it",
    "openai/gemma4-31b-no-think": "llama.cpp/gemma-4-31B-it(no think)",
    "openai/gemma4-31b":          "llama.cpp/gemma-4-31B-it",
    "openai/glm47-flash":         "llama.cpp/GLM-4.7-Flash",
    "openai/gpt-oss-120b":        "llama.cpp/gpt-oss-120b",
    "openai/gpt-oss-20b":         "llama.cpp/gpt-oss-20b",
    "openai/nex-n2-mini-fix":     "llama.cpp/Nex-N2-mini(fix chat-template)",
    "openai/nex-n2-mini":         "llama.cpp/Nex-N2-mini",
    "openai/north-mini-code":     "llama.cpp/North-Mini-Code-1.0",
    "openai/ornith-35b-q4":       "llama.cpp/Ornith-1.0-35B",
    "openai/qwen3-coder-next":    "llama.cpp/Qwen3-Coder-Next",
    "openai/qwen36-27b":          "llama.cpp/Qwen3.6-27B",
    "openai/qwen36-35b-a3b":      "llama.cpp/Qwen3.6-35B-A3B",
}

def convert_model_name(name: str) -> str:
    if name.startswith(("openai/", "sglang/")) and "gpt-5" not in name:
        if name not in MODEL_MAP:
            print(f"Warning: no mapping for '{name}', leaving as-is.", file=sys.stderr)
            return name
        return MODEL_MAP[name]
    return name


def df_to_markdown(df: pd.DataFrame) -> str:
    headers = df.columns.tolist()
    col_widths = [max(len(str(h)), df[h].astype(str).map(len).max()) for h in headers]

    def row_str(values):
        return "| " + " | ".join(str(v).ljust(w) for v, w in zip(values, col_widths)) + " |"

    separator = "| " + " | ".join("-" * w for w in col_widths) + " |"

    lines = [row_str(headers), separator]
    for _, row in df.iterrows():
        lines.append(row_str(row.tolist()))

    return "\n".join(lines)


def main(csv_path: str) -> None:
    df = pd.read_csv(csv_path)

    df = df[["model", "language", "edit_format", "pass_rate_1", "pass_rate_2"]].rename(
        columns={
            "model":       "Model",
            "language":    "Language",
            "edit_format": "Edit-format",
            "pass_rate_1": "pass@1",
            "pass_rate_2": "pass@2",
        }
    )

    df["Model"] = df["Model"].map(convert_model_name)

    cpp_df    = df[df["Language"] == "cpp"   ].sort_values("pass@2", ascending=False).reset_index(drop=True).drop(columns="Language")
    python_df = df[df["Language"] == "python"].sort_values("pass@2", ascending=False).reset_index(drop=True).drop(columns="Language")

    print("### C++\n")
    print(df_to_markdown(cpp_df))
    print("\n")
    print("### Python\n")
    print(df_to_markdown(python_df))


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "./results/results.csv"
    main(path)