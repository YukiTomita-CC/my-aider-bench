import pandas as pd
import sys

MODEL_MAP = {
    "openai/devstral-small":       "llama.cpp/Devstral-Small-2-24B-Instruct-2512",
    "openai/devstral":             "llama.cpp/Devstral-2-123B-Instruct-2512",
    "openai/gemma4-12b-agentic":   "llama.cpp/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2",
    "openai/gemma4-12b":           "llama.cpp/gemma-4-12B-it",
    "openai/gemma4-26b-a4b":       "llama.cpp/gemma-4-26B-A4B-it",
    "openai/gemma4-31b-no-think":  "llama.cpp/gemma-4-31B-it(no think)",
    "openai/gemma4-31b":           "llama.cpp/gemma-4-31B-it",
    "openai/glm47-flash":          "llama.cpp/GLM-4.7-Flash",
    "openai/gpt-oss-120b":         "llama.cpp/gpt-oss-120b",
    "openai/gpt-oss-20b":          "llama.cpp/gpt-oss-20b",
    "openai/nex-n2-mini-fix":      "llama.cpp/Nex-N2-mini(fix chat-template)",
    "openai/nex-n2-mini":          "llama.cpp/Nex-N2-mini",
    "openai/north-mini-code":      "llama.cpp/North-Mini-Code-1.0",
    "openai/ornith-35b-q4":        "llama.cpp/Ornith-1.0-35B",
    "openai/ornith-35b-bartowski": "llama.cpp/Ornith-1.0-35B(bartowski)",
    "openai/qwen3-coder-next":     "llama.cpp/Qwen3-Coder-Next",
    "openai/qwen36-27b":           "llama.cpp/Qwen3.6-27B",
    "openai/qwen36-35b-a3b":       "llama.cpp/Qwen3.6-35B-A3B",
    "openai/qwythos-9b":           "llama.cpp/Qwythos-9B-Claude-Mythos-5",
}

def convert_model_name(name: str) -> str:
    if pd.isna(name):
        return name
    lower_name = name.lower()
    if lower_name.startswith(("openai/", "sglang/")) and "gpt-5" not in lower_name:
        if lower_name not in MODEL_MAP:
            print(f"Warning: no mapping for '{name}', leaving as-is.", file=sys.stderr)
            return name
        return MODEL_MAP[lower_name]
    return name


def df_to_markdown(df: pd.DataFrame) -> str:
    headers = df.columns.tolist()
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for _, row in df.iterrows():
        formatted_vals = []
        for val in row.tolist():
            if isinstance(val, (int, float)):
                formatted_vals.append(f"{val:g}")
            else:
                formatted_vals.append(str(val))
        lines.append("| " + " | ".join(formatted_vals) + " |")
    return "\n".join(lines)


def get_tables(path: str) -> dict[str, str]:
    df = pd.read_csv(path)
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

    cpp_df = df[df["Language"] == "cpp"].copy()
    python_df = df[df["Language"] == "python"].copy()

    sort_cols = ["pass@2", "pass@1", "Model", "Edit-format"]
    ascending = [False, False, True, False]
    
    def sort_key(col):
        if col.name == "Model":
            return col.str.lower()
        return col

    cpp_df = cpp_df.sort_values(by=sort_cols, ascending=ascending, key=sort_key).reset_index(drop=True).drop(columns="Language")
    python_df = python_df.sort_values(by=sort_cols, ascending=ascending, key=sort_key).reset_index(drop=True).drop(columns="Language")

    return {
        "cpp": df_to_markdown(cpp_df),
        "python": df_to_markdown(python_df),
    }


def main(csv_path: str) -> None:
    tables = get_tables(csv_path)
    print(tables["cpp"])
    print()
    print(tables["python"])


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "./results/results.csv"
    main(path)
