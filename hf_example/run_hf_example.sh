#!/bin/bash
set -euo pipefail

export HOME="$PWD"
export MPLCONFIGDIR="$PWD/.matplotlib"
mkdir -p "$MPLCONFIGDIR"
mkdir -p Geometry

echo "=== Job information ==="
hostname
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

python - <<'PY'
import torch
print("PyTorch:", torch.__version__)
print("CUDA build:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
print("Low-level CUDA count:", torch._C._cuda_getDeviceCount())
PY

echo
echo "=== Running GaitDynamics HF complete-kinematics example ==="
echo "Height: 1.83 m"
echo "Weight: 71.4 kg"
echo "Treadmill speed: 1.15 m/s"

printf '\n1.83\n71.4\n1.15\n' | \
python run_gaitdynamics.py

echo
echo "=== Output ==="
ls -lh *_grf_pred___.mot
