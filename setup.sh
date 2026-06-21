#!/bin/bash
set -euo pipefail

# ============================================================
# RunPod Benchmark Setup Script
# Usage: bash setup.sh <GitHub_UserID> <GitHub_PAT>
#
# The following environment variables must be set in Pod Template:
#   AIDER_DOCKER=1
#   AIDER_BENCHMARK_DIR=/workspace/aider/tmp.benchmarks
#   OPENAI_API_BASE=http://localhost:8080/v1
#   OPENAI_API_KEY=dummy
# ============================================================

# ----------------------------
# Argument check
# ----------------------------
if [ $# -ne 2 ]; then
  echo "Usage: bash setup.sh <GitHub_UserID> <GitHub_PAT>"
  exit 1
fi

GITHUB_USER="$1"
GITHUB_PAT="$2"

echo "========================================"
echo " Step 0: GitHub PAT & Dependencies"
echo "========================================"

# GitHub credentials
git config --global credential.helper store
echo "https://${GITHUB_USER}:${GITHUB_PAT}@github.com" > ~/.git-credentials
echo "✔ git credentials configured"

# Install dependencies
echo "→ Installing apt packages..."
apt-get update -qq
apt-get install -y -qq libboost-all-dev libtbb-dev cmake tmux
echo "✔ apt packages installed"

echo ""
echo "========================================"
echo " Step 1: Build llama.cpp"
echo "========================================"

cd /workspace
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

echo "→ Running CMake configuration..."
cmake -B build -DGGML_CUDA=ON

echo "→ Building (parallel jobs: $(nproc))..."
cmake --build build --config Release -j$(nproc) -t llama-server
echo "✔ llama-server build complete"

echo ""
echo "========================================"
echo " Step 2: aider + Benchmark Environment"
echo "========================================"

cd /workspace
git clone https://github.com/Aider-AI/aider.git
cd aider

echo "→ Patching benchmark.py paths..."
sed -i \
  's|"/aider/benchmark/npm-test.sh"|"/workspace/aider/benchmark/npm-test.sh"|g; s|"/aider/benchmark/cpp-test.sh"|"/workspace/aider/benchmark/cpp-test.sh"|g' \
  benchmark/benchmark.py
echo "✔ benchmark.py patched"

mkdir -p tmp.benchmarks

echo "→ Cloning polyglot-benchmark..."
git clone https://github.com/Aider-AI/polyglot-benchmark.git tmp.benchmarks/polyglot-benchmark

echo "→ Installing aider[dev]..."
pip install -e ".[dev]"
echo "✔ aider installation complete"

echo ""
echo "========================================"
echo " Step 3: Clone Benchmark Results Repo"
echo "========================================"

cd /workspace
git clone https://github.com/YukiTomita-CC/my-aider-bench.git benchmark-results
echo "✔ benchmark-results cloned"

echo ""
echo "========================================"
echo " Setup complete!"
echo "========================================"
