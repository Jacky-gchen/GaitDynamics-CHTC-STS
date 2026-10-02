# GaitDynamics CHTC STS Workflow

This repository documents a reproducible CHTC workflow for running the Stanford NMBL GaitDynamics pretrained inference pipeline and adapting it for a sit-to-stand (STS) smoke test.

## Workflow

Official GaitDynamics source and pretrained models
→ Hugging Face complete-kinematics reproduction
→ CHTC Apptainer/GPU setup
→ subject2 STS1 inference
→ predicted bilateral GRFs and COPs
→ comparison against measured force-plate data

## Upstream GaitDynamics

Official repository:

https://github.com/stanfordnmbl/GaitDynamics

Upstream commit used:

8dc5aed58161a129fd2d58ff071cb802f2654be9

The original GaitDynamics inference implementation was not modified for the STS smoke test.

## Verified pretrained model hashes

GaitDynamicsDiffusion.pt

709f7229013313b512585c35a6457155be2a7ce650a7ad08d6e2d85c04c4a260

GaitDynamicsRefinement.pt

34a659ce485ea48eb11e1400dac53c46892e1487bcf347c16c529c463dd011fb

The pretrained model files are not included in this repository.

## Repository structure

- `chtc/` — Apptainer environment definition
- `hf_example/` — CHTC reproduction of the authors' complete-kinematics example
- `sts_subject2/` — subject2 STS smoke-test submission and validation scripts

## Important note

GaitDynamics was developed primarily for walking and running. The STS run in this repository should be treated as an out-of-distribution smoke test, not as a validated STS force-estimation model.
