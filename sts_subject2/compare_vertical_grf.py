import numpy as np
import matplotlib.pyplot as plt

def read_mot(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    end_idx = next(i for i, line in enumerate(lines)
                   if 'endheader' in line.lower())

    # Skip endheader and column-name row.
    data = np.loadtxt(path, skiprows=end_idx + 2)
    return data

mass = 78.2
BW = mass * 9.81

pred = read_mot('STS1_grf_pred___.mot')
meas = read_mot('STS1_forces.mot')

# GaitDynamics
t_pred = pred[:, 0]
gd_r_fy = pred[:, 2]
gd_l_fy = pred[:, 11]
gd_total = gd_r_fy + gd_l_fy

# Measured force plates
t_meas = meas[:, 0]
r_fy = meas[:, 2]
l_fy = meas[:, 11]
plate3_fy = meas[:, 20]

feet_total = r_fy + l_fy
all3_total = feet_total + plate3_fy

# Resample measured forces to 100-Hz GaitDynamics timestamps
feet_interp = np.interp(t_pred, t_meas, feet_total)
all3_interp = np.interp(t_pred, t_meas, all3_total)

plt.figure(figsize=(11, 6))
plt.plot(t_pred, gd_total, label='GaitDynamics R + L')
plt.plot(t_pred, feet_interp, label='Measured R + L')
plt.plot(t_pred, all3_interp, '--', label='Measured R + L + Plate 3')
plt.axhline(BW, linestyle=':', label=f'Body weight = {BW:.1f} N')

plt.xlabel('Time (s)')
plt.ylabel('Vertical GRF (N)')
plt.title('Subject 2 STS1: GaitDynamics vs Lab Force Plates')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('STS1_vertical_GRF_comparison.png', dpi=200)

print('Saved STS1_vertical_GRF_comparison.png')
print(f'Body weight: {BW:.1f} N')
print(f'GD at t=0: {gd_total[0]:.1f} N')
print(f'Measured feet at t=0: {feet_interp[0]:.1f} N')
print(f'Measured all 3 at t=0: {all3_interp[0]:.1f} N')
print(f'Max plate 3 Fy: {np.max(plate3_fy):.1f} N')
