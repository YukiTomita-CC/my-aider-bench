# my-aider-bench

## Motivation

I'm an indie developer who recently started using Aider. Since the official Aider leaderboard has stopped being updated, I decided to run the benchmarks myself to help with model selection and am sharing the results here.

## TL;DR

As of 2026/06/30, the models I'm currently using are:
- Everyday use: Qwen3.6-35B-A3B (unsloth/Qwen3.6-35B-A3B-MTP-GGUF:UD-Q4_K_XL)
- Tough tasks: Qwen3.6-27B (unsloth/Qwen3.6-27B-MTP-GGUF:UD-Q4_K_XL)

## Results

All results are available in `./results/results.csv`.
All runtime parameters and quantization sizes are listed in `./benchmark_config.yml`.

Results are primarily for models supported by llama.cpp, measured in GGUF format (mainly Q4).
Some results for OpenAI, Claude, and Google API models are also included.

A summary of `results.csv` is shown below. In most cases, open-weight models tend to score higher with `whole` than `diff` edit format.
<!-- BEGIN AUTO-GENERATED MARKDOWN TABLE -->
### C++

| Model | Edit-format | pass@1 | pass@2 |
| --- | --- | --- | --- |
| anthropic/claude-sonnet-4-5-20250929 | diff | 26.9 | 88.5 |
| gemini/gemini-3-flash-preview | diff-fenced | 50 | 84.6 |
| llama.cpp/Qwen3.6-27B | whole | 30.8 | 84.6 |
| llama.cpp/Ornith-1.0-35B | whole | 34.6 | 73.1 |
| llama.cpp/Ornith-1.0-35B(bartowski) | whole | 26.9 | 73.1 |
| llama.cpp/Ornith-1.0-35B(bartowski) | diff | 23.1 | 73.1 |
| openai/gpt-5-mini | diff | 15.4 | 73.1 |
| llama.cpp/Qwen3.6-27B | diff | 23.1 | 69.2 |
| llama.cpp/Qwen3.6-35B-A3B | whole | 23.1 | 69.2 |
| llama.cpp/Ornith-1.0-35B | diff | 30.8 | 65.4 |
| llama.cpp/Qwen3-Coder-Next | diff | 19.2 | 65.4 |
| llama.cpp/Qwen3.6-35B-A3B | diff | 30.8 | 61.5 |
| llama.cpp/Qwen3-Coder-Next | whole | 23.1 | 61.5 |
| openai/gpt-5.2 | diff | 23.1 | 61.5 |
| llama.cpp/Devstral-2-123B-Instruct-2512 | diff | 7.7 | 50 |
| llama.cpp/gemma-4-31B-it | whole | 7.7 | 50 |
| gemini/gemini-2.5-flash | diff-fenced | 7.7 | 46.2 |
| llama.cpp/gemma-4-31B-it | diff | 7.7 | 46.2 |
| llama.cpp/Devstral-2-123B-Instruct-2512 | whole | 11.5 | 42.3 |
| anthropic/claude-haiku-4-5-20251001 | diff | 7.7 | 42.3 |
| llama.cpp/gemma-4-31B-it(no think) | diff | 7.7 | 42.3 |
| llama.cpp/gemma-4-31B-it(no think) | whole | 7.7 | 34.6 |
| llama.cpp/gpt-oss-120b | diff | 3.8 | 30.8 |
| llama.cpp/Qwythos-9B-Claude-Mythos-5 | diff | 0 | 26.9 |
| llama.cpp/Devstral-Small-2-24B-Instruct-2512 | diff | 3.8 | 23.1 |
| llama.cpp/gemma-4-26B-A4B-it | diff | 3.8 | 23.1 |
| llama.cpp/gpt-oss-120b | whole | 0 | 23.1 |
| llama.cpp/North-Mini-Code-1.0 | whole | 0 | 23.1 |
| llama.cpp/Qwythos-9B-Claude-Mythos-5 | whole | 0 | 23.1 |
| llama.cpp/Nex-N2-mini(fix chat-template) | whole | 7.7 | 19.2 |
| llama.cpp/gemma-4-26B-A4B-it | whole | 0 | 19.2 |
| llama.cpp/GLM-4.7-Flash | whole | 0 | 19.2 |
| llama.cpp/North-Mini-Code-1.0 | diff | 3.8 | 15.4 |
| llama.cpp/gemma-4-12B-it | diff | 0 | 15.4 |
| llama.cpp/Devstral-Small-2-24B-Instruct-2512 | whole | 3.8 | 11.5 |
| llama.cpp/gemma-4-12B-it | whole | 0 | 11.5 |
| llama.cpp/Nex-N2-mini | whole | 7.7 | 7.7 |
| llama.cpp/GLM-4.7-Flash | diff | 0 | 7.7 |
| llama.cpp/gpt-oss-20b | diff | 0 | 7.7 |
| llama.cpp/Nex-N2-mini(fix chat-template) | diff | 3.8 | 3.8 |
| llama.cpp/gpt-oss-20b | whole | 0 | 3.8 |
| llama.cpp/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2 | whole | 0 | 0 |
| llama.cpp/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2 | diff | 0 | 0 |
| llama.cpp/Nex-N2-mini | diff | 0 | 0 |


### Python

| Model | Edit-format | pass@1 | pass@2 |
| --- | --- | --- | --- |
| gemini/gemini-3-flash-preview | diff-fenced | 76.5 | 97.1 |
| llama.cpp/Qwen3-Coder-Next | whole | 44.1 | 79.4 |
| openai/gpt-5-mini | diff | 23.5 | 79.4 |
| llama.cpp/Qwen3-Coder-Next | diff | 44.1 | 76.5 |
| openai/gpt-5.2 | diff | 38.2 | 76.5 |
| anthropic/claude-sonnet-4-5-20250929 | diff | 29.4 | 76.5 |
| llama.cpp/Qwen3.6-27B | whole | 38.2 | 70.6 |
| llama.cpp/gemma-4-31B-it | diff | 8.8 | 70.6 |
| gemini/gemini-2.5-flash | diff-fenced | 29.4 | 67.6 |
| llama.cpp/gemma-4-31B-it | whole | 14.7 | 64.7 |
| llama.cpp/Qwen3.6-27B | diff | 44.1 | 61.8 |
| llama.cpp/Ornith-1.0-35B(bartowski) | diff | 32.4 | 61.8 |
| llama.cpp/Qwen3.6-35B-A3B | whole | 41.2 | 58.8 |
| llama.cpp/Qwen3.6-35B-A3B | diff | 32.4 | 58.8 |
| llama.cpp/Ornith-1.0-35B | diff | 29.4 | 58.8 |
| llama.cpp/Ornith-1.0-35B | whole | 26.5 | 58.8 |
| llama.cpp/Ornith-1.0-35B(bartowski) | whole | 38.2 | 52.9 |
| llama.cpp/gemma-4-31B-it(no think) | whole | 8.8 | 52.9 |
| anthropic/claude-haiku-4-5-20251001 | diff | 8.8 | 50 |
| llama.cpp/gemma-4-31B-it(no think) | diff | 5.9 | 50 |
| llama.cpp/gpt-oss-120b | diff | 8.8 | 41.2 |
| llama.cpp/Devstral-2-123B-Instruct-2512 | diff | 0 | 38.2 |
| llama.cpp/Devstral-2-123B-Instruct-2512 | whole | 2.9 | 32.4 |
| llama.cpp/gpt-oss-120b | whole | 11.8 | 26.5 |
| llama.cpp/Qwythos-9B-Claude-Mythos-5 | diff | 11.8 | 26.5 |
| llama.cpp/North-Mini-Code-1.0 | whole | 8.8 | 26.5 |
| llama.cpp/Devstral-Small-2-24B-Instruct-2512 | diff | 0 | 23.5 |
| llama.cpp/North-Mini-Code-1.0 | diff | 8.8 | 20.6 |
| llama.cpp/Nex-N2-mini(fix chat-template) | diff | 2.9 | 17.6 |
| llama.cpp/Qwythos-9B-Claude-Mythos-5 | whole | 8.8 | 14.7 |
| llama.cpp/Nex-N2-mini(fix chat-template) | whole | 5.9 | 14.7 |
| llama.cpp/Nex-N2-mini | whole | 5.9 | 11.8 |
| llama.cpp/Nex-N2-mini | diff | 8.8 | 8.8 |
| llama.cpp/Devstral-Small-2-24B-Instruct-2512 | whole | 2.9 | 8.8 |
| llama.cpp/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2 | diff | 5.9 | 5.9 |
| llama.cpp/GLM-4.7-Flash | whole | 2.9 | 5.9 |
| llama.cpp/gemma-4-12B-it | whole | 0 | 5.9 |
| llama.cpp/gemma-4-12B-it | diff | 0 | 5.9 |
| llama.cpp/gemma-4-26B-A4B-it | diff | 0 | 5.9 |
| llama.cpp/gpt-oss-20b | whole | 0 | 5.9 |
| llama.cpp/gemma-4-26B-A4B-it | whole | 0 | 2.9 |
| llama.cpp/GLM-4.7-Flash | diff | 0 | 2.9 |
| llama.cpp/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2 | whole | 0 | 0 |
| llama.cpp/gpt-oss-20b | diff | 0 | 0 |

<!-- END AUTO-GENERATED MARKDOWN TABLE -->
## About the Benchmarks

- Measurement environment:
  - Open-weight models: RunPod (runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04)
  - API models: Docker container as described in the [official Aider repository](https://github.com/aider-ai/aider)
- Measurement method:
  - Follows the benchmark measurement method described in the official Aider repository.
  - For RunPod, the official Docker container environment was reproduced inside a Pod and run directly (not docker-in-docker).
- About pass@1 / pass@2 (from https://arxiv.org/abs/2507.09866):
  - Pass@1: Measures the proportion of coding tasks an LLM completes correctly on its first attempt, as verified by test cases, directly reflecting the one-shot coding accuracy of LLMs.
  - Pass@2: After a failed attempt, LLMs can view their previous code and error messages before trying again, capturing the capacity of LLMs to improve via immediate feedback.

## Usage

Fork this repository and use it as your own. Inside a Pod, you can run the benchmarks with the following commands:

```bash
curl -fsSL https://raw.githubusercontent.com/YukiTomita-CC/my-aider-bench/main/setup.sh | bash -s -- "$GITHUB_USER" "$GITHUB_PAT"

tmux new -s bench

cd /workspace/aider
python /workspace/benchmark-results/run_benchmarks.py /workspace/benchmark-results/benchmark_config.yml
```

`setup.sh` performs the following:
1. Git configuration
2. Clone and build llama.cpp
3. Clone the official Aider repository and install dependencies
4. Clone the benchmark problem repository
5. Clone this repository (for storing results) and place the scripts

Make sure to set the following environment variables inside the container:
- AIDER_DOCKER=1
- AIDER_BENCHMARK_DIR=/workspace/aider/tmp.benchmarks
- OPENAI_API_BASE=http://localhost:8080/v1
- OPENAI_API_KEY=dummy
- GITHUB_USER=yours
- GITHUB_PAT=yours
- GIT_USER_EMAIL=yours
- GIT_USER_NAME=yours

Use a fine-grained PAT with the minimum required scope and a short expiration.
Also, update line 91 of `setup.sh` to match your forked repository name.

To change the target languages, edit the list on line 27 of `run_benchmarks.py`.
As of 2026/06/29, the languages supported by Aider-AI/polyglot-benchmark are:
- cpp
- go
- java
- javascript
- python
- rust

This repository targets C++ and Python, so the libraries required for other languages are not included. If you want to measure other languages, refer to the [official Docker image](https://github.com/Aider-AI/aider/blob/main/benchmark/Dockerfile) and add the necessary setup to `setup.sh`.

If you run into issues, feel free to open an Issue.

## Disclaimer

- All measurements are n=1 and accuracy is not guaranteed.
- The GPU used on RunPod varies (e.g., A6000, A40) depending on availability at the time of measurement.
- Due to budget constraints, results are limited to C++ and Python, which are my primary languages.
