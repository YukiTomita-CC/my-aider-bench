from pathlib import Path
import sys

import pandas as pd
import yaml


class ResultsFormatter:
    def __init__(self, fixture_dir=None):
        self.model_map = self._load_model_map(fixture_dir)


    def get_tables(self, csv_path=None) -> dict[str, str]:
        if csv_path is None:
            csv_path = Path(__file__).resolve().parent.parent / "results/results.csv"
            
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

        df["Model"] = df["Model"].map(self._convert_model_name)
        df = df[df["Model"].apply(lambda x: x.lower() in self.model_map or not x.startswith("openai/"))]

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
            "cpp": self._df_to_markdown(cpp_df),
            "python": self._df_to_markdown(python_df),
        }


    def _load_model_map(self, fixture_dir: str | None) -> dict[str, str]:
        model_map = {}
        
        if fixture_dir is None:
            root_dir = Path(__file__).resolve().parent.parent
        else:
            root_dir = fixture_dir
        
        config_path = root_dir / "benchmark_config.yml"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                for model in config.get("models", []):
                    name = model.get("name", "")
                    display_name = model.get("display_name", "")
                    if name and display_name:
                        model_map[f"openai/{name}"] = display_name

        api_config_path = root_dir / "benchmark_config_api.yml"
        if api_config_path.exists():
            with open(api_config_path, "r") as f:
                config = yaml.safe_load(f)
                for model in config.get("models", []):
                    model_string = model.get("model_string", "")
                    if model_string:
                        model_map[model_string] = model_string

        return model_map


    def _convert_model_name(self, name: str) -> str:
        if pd.isna(name):
            return name
        lower_name = name.lower()
        if name.startswith("openai/") and "gpt-5" not in name:
            if lower_name not in self.model_map:
                return name
            return self.model_map[lower_name]
        return name


    def _df_to_markdown(self, df: pd.DataFrame) -> str:
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


if __name__ == "__main__":
    results_formatter = ResultsFormatter()
    
    tables = results_formatter.get_tables()
    
    print("### C++\n")
    print(tables["cpp"])
    print("\n\n")
    print("### Python\n")
    print(tables["python"])
