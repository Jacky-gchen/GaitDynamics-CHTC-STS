import numpy as np
import matplotlib.pyplot as plt

def read_mot(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    end_idx = next(i for i, line in enumerate(lines)
                   if 'endheader' in line.lower())

    return np.loadtxt(path, skiprows=end_idx + 2)

pred = read_mot('STS1_grf_pred___.mot')
meas = read_mot('STS1_forces.mot')

# Time
t_pred = pred[:, 0]
t_meas = meas[:, 0]

# GaitDynamics
# force1 = right, force2 = left
gd_R_Fx = pred[:, 1]
gd_R_Fz = pred[:, 3]

gd_L_Fx = pred[:, 10]
gd_L_Fz = pred[:, 12]

# Measured force plates
meas_R_Fx = np.interp(t_pred, t_meas, meas[:, 1])
meas_R_Fz = np.interp(t_pred, t_meas, meas[:, 3])

meas_L_Fx = np.interp(t_pred, t_meas, meas[:, 10])
meas_L_Fz = np.interp(t_pred, t_meas, meas[:, 12])

# -------- X direction --------
plt.figure(figsize=(11, 6))

plt.plot(t_pred, gd_R_Fx, label='GaitDynamics Right Fx')
plt.plot(t_pred, meas_R_Fx, '--', label='Measured Right Fx')

plt.plot(t_pred, gd_L_Fx, label='GaitDynamics Left Fx')
plt.plot(t_pred, meas_L_Fx, '--', label='Measured Left Fx')

plt.axhline(0, linewidth=1)
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
plt.title('Subject 2 STS1: Fx Comparison')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('STS1_Fx_comparison.png', dpi=200)

# -------- Z direction --------
plt.figure(figsize=(11, 6))

plt.plot(t_pred, gd_R_Fz, label='GaitDynamics Right Fz')
plt.plot(t_pred, meas_R_Fz, '--', label='Measured Right Fz')

plt.plot(t_pred, gd_L_Fz, label='GaitDynamics Left Fz')
plt.plot(t_pred, meas_L_Fz, '--', label='Measured Left Fz')

plt.axhline(0, linewidth=1)
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
plt.title('Subject 2 STS1: Fz Comparison')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('STS1_Fz_comparison.png', dpi=200)

print('Saved:')
print('  STS1_Fx_comparison.png')
print('  STS1_Fz_comparison.png')

print('\nRanges:')
print(f'GD Right Fx: {gd_R_Fx.min():.1f} to {gd_R_Fx.max():.1f} N')
print(f'Measured Right Fx: {meas_R_Fx.min():.1f} to {meas_R_Fx.max():.1f} N')

print(f'GD Left Fx: {gd_L_Fx.min():.1f} to {gd_L_Fx.max():.1f} N')
print(f'Measured Left Fx: {meas_L_Fx.min():.1f} to {meas_L_Fx.max():.1f} N')

print(f'GD Right Fz: {gd_R_Fz.min():.1f} to {gd_R_Fz.max():.1f} N')
print(f'Measured Right Fz: {meas_R_Fz.min():.1f} to {meas_R_Fz.max():.1f} N')

print(f'GD Left Fz: {gd_L_Fz.min():.1f} to {gd_L_Fz.max():.1f} N')
print(f'Measured Left Fz: {meas_L_Fz.min():.1f} to {meas_L_Fz.max():.1f} N')
