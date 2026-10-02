import numpy as np
import matplotlib.pyplot as plt

def read_mot(path):
    with open(path) as f:
        lines = f.readlines()
    end = next(i for i,l in enumerate(lines) if 'endheader' in l.lower())
    return np.loadtxt(path, skiprows=end+2)

P = read_mot('STS1_grf_pred___.mot')
M = read_mot('STS1_forces.mot')

tp = P[:,0]
tm = M[:,0]

# GaitDynamics COP
# force1 = right, force2 = left
gd_R_px = P[:,4]
gd_R_pz = P[:,6]
gd_L_px = P[:,13]
gd_L_pz = P[:,15]

# Measured COP, resampled to GaitDynamics timestamps
R_px = np.interp(tp, tm, M[:,4])
R_pz = np.interp(tp, tm, M[:,6])
L_px = np.interp(tp, tm, M[:,13])
L_pz = np.interp(tp, tm, M[:,15])

R_Fy = np.interp(tp, tm, M[:,2])
L_Fy = np.interp(tp, tm, M[:,11])

# COP only meaningful when foot is loaded
R_mask = R_Fy > 20
L_mask = L_Fy > 20

def metrics(pred, meas, mask):
    e = pred[mask] - meas[mask]
    rmse = np.sqrt(np.mean(e**2))
    bias = np.mean(e)
    r = np.corrcoef(pred[mask], meas[mask])[0,1]
    return rmse, bias, r

# X COP
plt.figure(figsize=(11,6))
plt.plot(tp[R_mask], gd_R_px[R_mask], label='GaitDynamics Right COP x')
plt.plot(tp[R_mask], R_px[R_mask], '--', label='Measured Right COP x')
plt.plot(tp[L_mask], gd_L_px[L_mask], label='GaitDynamics Left COP x')
plt.plot(tp[L_mask], L_px[L_mask], '--', label='Measured Left COP x')
plt.xlabel('Time (s)')
plt.ylabel('COP x (m)')
plt.title('Subject 2 STS1: COP x Comparison')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('STS1_COPx_comparison.png', dpi=200)

# Z COP
plt.figure(figsize=(11,6))
plt.plot(tp[R_mask], gd_R_pz[R_mask], label='GaitDynamics Right COP z')
plt.plot(tp[R_mask], R_pz[R_mask], '--', label='Measured Right COP z')
plt.plot(tp[L_mask], gd_L_pz[L_mask], label='GaitDynamics Left COP z')
plt.plot(tp[L_mask], L_pz[L_mask], '--', label='Measured Left COP z')
plt.xlabel('Time (s)')
plt.ylabel('COP z (m)')
plt.title('Subject 2 STS1: COP z Comparison')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('STS1_COPz_comparison.png', dpi=200)

for name, pred, meas, mask in [
    ('R COP x', gd_R_px, R_px, R_mask),
    ('R COP z', gd_R_pz, R_pz, R_mask),
    ('L COP x', gd_L_px, L_px, L_mask),
    ('L COP z', gd_L_pz, L_pz, L_mask),
]:
    rmse, bias, r = metrics(pred, meas, mask)
    print(f'{name}: RMSE={rmse:.4f} m, Bias={bias:.4f} m, r={r:.3f}')

print('\nSaved:')
print('  STS1_COPx_comparison.png')
print('  STS1_COPz_comparison.png')
