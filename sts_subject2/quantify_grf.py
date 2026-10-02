import numpy as np

def read_mot(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    end_idx = next(i for i, line in enumerate(lines)
                   if 'endheader' in line.lower())
    return np.loadtxt(path, skiprows=end_idx + 2)

def metrics(pred, meas):
    err = pred - meas
    rmse = np.sqrt(np.mean(err**2))
    mae_bias = np.mean(err)
    r = np.corrcoef(pred, meas)[0,1]
    return rmse, mae_bias, r

mass = 78.2
BW = mass * 9.81

pred = read_mot('STS1_grf_pred___.mot')
meas = read_mot('STS1_forces.mot')

tp = pred[:,0]
tm = meas[:,0]

# GaitDynamics columns
gd = {
    'R_Fx': pred[:,1],
    'R_Fy': pred[:,2],
    'R_Fz': pred[:,3],
    'L_Fx': pred[:,10],
    'L_Fy': pred[:,11],
    'L_Fz': pred[:,12],
}

# Measured, interpolated to 100 Hz
lab = {
    'R_Fx': np.interp(tp, tm, meas[:,1]),
    'R_Fy': np.interp(tp, tm, meas[:,2]),
    'R_Fz': np.interp(tp, tm, meas[:,3]),
    'L_Fx': np.interp(tp, tm, meas[:,10]),
    'L_Fy': np.interp(tp, tm, meas[:,11]),
    'L_Fz': np.interp(tp, tm, meas[:,12]),
}

foot_vertical = lab['R_Fy'] + lab['L_Fy']
mask_loaded = foot_vertical > 0.5 * BW

print(f'BW = {BW:.1f} N')
print(f'Loaded threshold = {0.5*BW:.1f} N')
print(f'Loaded samples = {mask_loaded.sum()} / {len(mask_loaded)}')
print()

for name in gd:
    rmse, bias, r = metrics(gd[name], lab[name])
    rmse_l, bias_l, r_l = metrics(gd[name][mask_loaded], lab[name][mask_loaded])

    print(name)
    print(f'  FULL:   RMSE={rmse:7.2f} N   Bias={bias:7.2f} N   r={r:6.3f}')
    print(f'  LOADED: RMSE={rmse_l:7.2f} N   Bias={bias_l:7.2f} N   r={r_l:6.3f}')
