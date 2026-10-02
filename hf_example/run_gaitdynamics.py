import runpy
import torch

print("=== PyTorch CUDA compatibility shim ===")
print("Original torch.cuda.device_count():", torch.cuda.device_count())
print("Low-level CUDA count:", torch._C._cuda_getDeviceCount())

# PyTorch 1.13.1 does not correctly parse CHTC's UUID-form
# CUDA_VISIBLE_DEVICES. The CUDA runtime itself sees the allocated GPU.
torch.cuda.device_count = torch._C._cuda_getDeviceCount

print("Patched torch.cuda.device_count():", torch.cuda.device_count())

runpy.run_path(
    "GaitDynamics/example_usage/gait_dynamics.py",
    run_name="__main__"
)
