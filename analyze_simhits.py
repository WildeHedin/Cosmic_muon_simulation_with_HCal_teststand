
import uproot # for data loading
import awkward as ak # for data manipulation
import hist # for histogram filling (and some plotting)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
import pylandau
import numpy as np
import matplotlib.ticker as ticker

with uproot.open('check.root') as f:
    events = f['LDMX_Events'].arrays()


pdg_id = events['SimParticles_cosmics.second.pdg_id_']
p_energy = events['SimParticles_cosmics.second.energy_']

muon_mask = (pdg_id == 13) | (pdg_id == -13)

muon_energy = p_energy[muon_mask]
muon_energy_flat = ak.flatten(muon_energy)

#find the vertex of the muon in the event
vtx_x_muon = events['SimParticles_cosmics.second.vtx_x_'][muon_mask]
vtx_y_muon = events['SimParticles_cosmics.second.vtx_y_'][muon_mask]
vtx_z_muon = events['SimParticles_cosmics.second.vtx_z_'][muon_mask]

#find the end point of the muon in the event
end_x_muon = events['SimParticles_cosmics.second.end_x_'][muon_mask]
end_y_muon = events['SimParticles_cosmics.second.end_y_'][muon_mask]
end_z_muon = events['SimParticles_cosmics.second.end_z_'][muon_mask]

#find the momentum of muon in event
px_muon = events['SimParticles_cosmics.second.px_'][muon_mask]
py_muon = events['SimParticles_cosmics.second.py_'][muon_mask]
pz_muon = events['SimParticles_cosmics.second.pz_'][muon_mask]

x_hits = events['HcalSimHits_cosmics.x_']
y_hits = events['HcalSimHits_cosmics.y_']
z_hits = events['HcalSimHits_cosmics.z_']

edep = events['HcalSimHits_cosmics.edep_']

scint_length = 2000
scint_width = 50
scint_thick = 20

num_bars = 8
layer_thickness = 21.5
layer_width = num_bars * scint_width
space_between_sections = 1000

num_layers_alongx_bottom = 4
num_layers_alongz_bottom = 4
num_layers_bottom = num_layers_alongx_bottom + num_layers_alongz_bottom

num_layers_alongx_top = 4
num_layers_alongz_top  = 4
num_layers_top = num_layers_alongx_top + num_layers_alongz_top

dy = (num_layers_top + num_layers_top) * layer_thickness + space_between_sections

first_layer_ypos_bottom = -dy/2
first_layer_scint_ypos_bottom = first_layer_ypos_bottom + scint_thick/2

first_layer_ypos_top = dy/2 - layer_thickness * num_layers_top
first_layer_scint_ypos_top = first_layer_ypos_top + scint_thick/2

first_scint_alongx_zpos = -layer_width/2
first_scint_alongz_xpos = -layer_width/2

x_min=[]
x_max=[]
y_min=[]
y_max=[]
z_min=[]
z_max=[]


for l in range(0,num_layers_bottom,1):
    if l % 2 == 0:
        for i in range(num_bars):
            x_min.append(first_scint_alongz_xpos + i*scint_width)
            x_max.append(first_scint_alongz_xpos + scint_width + i*scint_width)
            y_min.append(first_layer_ypos_bottom + l*layer_thickness)
            y_max.append(first_layer_ypos_bottom + scint_thick + l*layer_thickness)
            z_min.append(-scint_length/2)
            z_max.append(scint_length/2)

    else:
        for i in range(num_bars):
            x_min.append(-scint_length/2)
            x_max.append(scint_length/2)
            y_min.append(first_layer_ypos_bottom + (l)*layer_thickness)
            y_max.append(first_layer_ypos_bottom + scint_thick + (l)*layer_thickness)
            z_min.append(first_scint_alongx_zpos + i*scint_width)
            z_max.append(first_scint_alongx_zpos + scint_width + i*scint_width)


for i in range(0,64):
    mask_x =  (x_hits >= x_min[i]) & (x_hits <= x_max[i])
    mask_y =  (y_hits >= y_min[i]) & (y_hits <= y_max[i])
    mask_z =  (z_hits >= z_min[i]) & (z_hits <= z_max[i])
    mask = mask_x & mask_y & mask_z
    mask_nonempty = ak.num(edep[mask]) > 0
    edep_nonempty = edep[mask][mask_nonempty]
    edep_howlong = ak.num(edep_nonempty)
    edep_twoormore=ak.sum(ak.num(edep_nonempty) > 1)
    edep_flat = ak.flatten(edep[mask])

    #print(edep_twoormore)
    #print(x_min[i], x_max[i], y_min[i], y_max[i], z_min[i], z_max[i])
    
    '''
    fig = plt.figure()
    fig.set_size_inches(8, 6)
    counts, bins = np.histogram(edep_flat, bins=100, range=(0,13))
    plt.step(bins[:-1], counts, where='post', color='orange')
    plt.title(f"Energy deposition in strip {i}, layer 1, section 1", fontsize=17)
    plt.ylim(0,350)
    plt.xlim(0,13)
    plt.ylabel('Counts', fontsize=16)
    plt.xlabel('Energy deposition [MeV]', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()
    '''
def langau(x, mpv, eta, sigma, A):
        return A * pylandau.langau(x, mpv, eta, sigma)


def plot_edep_alongz_bottom():
    x_min_alongz_bottom=[]
    x_max_alongz_bottom=[]
    y_min_alongz_bottom=[]
    y_max_alongz_bottom=[]
    z_min_alongz_bottom=[]
    z_max_alongz_bottom=[]

    for l in range(0,num_layers_bottom,2):
            for i in range(num_bars):
                x_min_alongz_bottom.append(first_scint_alongz_xpos + i*scint_width)
                x_max_alongz_bottom.append(first_scint_alongz_xpos + scint_width + i*scint_width)
                y_min_alongz_bottom.append(first_layer_ypos_bottom + l*layer_thickness)
                y_max_alongz_bottom.append(first_layer_ypos_bottom + scint_thick + l*layer_thickness)
                z_min_alongz_bottom.append(-scint_length/2)
                z_max_alongz_bottom.append(scint_length/2)

    edep_flat_alongz_bottom=[]
    for i in range(0,len(x_min_alongz_bottom)):
        mask_x =  (x_hits >= x_min_alongz_bottom[i]) & (x_hits <= x_max_alongz_bottom[i])
        mask_y =  (y_hits >= y_min_alongz_bottom[i]) & (y_hits <= y_max_alongz_bottom[i])
        mask_z =  (z_hits >= z_min_alongz_bottom[i]) & (z_hits <= z_max_alongz_bottom[i])
        mask = mask_x & mask_y & mask_z
        edep_masked = edep[mask]
        mask_nonempty = ak.num(edep_masked) > 0
        edep_nonempty = edep_masked[mask_nonempty]
        edep_summed = ak.sum(edep_nonempty, axis=1)
        edep_flat_alongz_bottom.append(edep_summed)
        #edep_flat_alongz_bottom.append(ak.flatten(edep[mask]))

    data = ak.to_numpy(ak.flatten(edep_flat_alongz_bottom))
    counts, edges = np.histogram(data, bins=100, range=(0, 13))
    centers = 0.5 * (edges[:-1] + edges[1:])
    mpv_guess = centers[np.argmax(counts)]
    eta_guess = 0.05 * mpv_guess
    sigma_guess = 0.15 * mpv_guess
    A_guess = max(counts)
    p0 = [mpv_guess, eta_guess, sigma_guess, A_guess]

    fit_mask = (centers > 2.6) & (centers < 13)
    params, cov = curve_fit(langau, centers[fit_mask], counts[fit_mask], p0=p0, maxfev=10000)
    print(f"MVP = {params[0]:.2f}, Amplitude = {params[3]:.2f}, Eta = {params[1]:.2f}, Sigma = {params[2]:.2f}")
    errors = np.sqrt(np.diag(cov))
    print(f"MVPer = {errors[0]:.4f}, Amplitudeer = {errors[3]:.4f}, Etaer = {errors[1]:.4f}, Sigmaer = {errors[2]:.4f}")

    fig = plt.figure()
    fig.set_size_inches(8, 6)
    plt.step(edges[:-1], counts, where='post', color='orange')
    x_fit = np.linspace(0, 13, 500)
    plt.plot(x_fit, langau(x_fit, *params), color="mediumvioletred")
    plt.title(f"Energy deposition in bars along z-axis in bottom section", fontsize=17)
    plt.ylim(0,10000)
    plt.xlim(0,13)
    plt.ylabel('Counts', fontsize=16)
    plt.xlabel('Energy deposition [MeV]', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()


def plot_edep_alongx_bottom():
    x_min_alongx_bottom=[]
    x_max_alongx_bottom=[]
    y_min_alongx_bottom=[]
    y_max_alongx_bottom=[]
    z_min_alongx_bottom=[]
    z_max_alongx_bottom=[]

    for l in range(0,num_layers_bottom,2):
            for i in range(num_bars):
                x_min_alongx_bottom.append(-scint_length/2)
                x_max_alongx_bottom.append(scint_length/2)
                y_min_alongx_bottom.append(first_layer_ypos_bottom + (l+1)*layer_thickness)
                y_max_alongx_bottom.append(first_layer_ypos_bottom + scint_thick + (l+1)*layer_thickness)
                z_min_alongx_bottom.append(first_scint_alongx_zpos + i*scint_width)
                z_max_alongx_bottom.append(first_scint_alongx_zpos + scint_width + i*scint_width)
            

    edep_flat_alongx_bottom=[]
    for i in range(0,len(x_min_alongx_bottom)):
        mask_x =  (x_hits >= x_min_alongx_bottom[i]) & (x_hits <= x_max_alongx_bottom[i])
        mask_y =  (y_hits >= y_min_alongx_bottom[i]) & (y_hits <= y_max_alongx_bottom[i])
        mask_z =  (z_hits >= z_min_alongx_bottom[i]) & (z_hits <= z_max_alongx_bottom[i])
        mask = mask_x & mask_y & mask_z
        edep_masked = edep[mask]
        mask_nonempty = ak.num(edep_masked) > 0
        edep_nonempty = edep_masked[mask_nonempty]
        edep_summed = ak.sum(edep_nonempty, axis=1)
        edep_flat_alongx_bottom.append(edep_summed)
        #edep_flat_alongz_bottom.append(ak.flatten(edep[mask]))

    data = ak.to_numpy(ak.flatten(edep_flat_alongx_bottom))
    counts, edges = np.histogram(data, bins=100, range=(0, 13))
    centers = 0.5 * (edges[:-1] + edges[1:])
    mpv_guess = centers[np.argmax(counts)]
    eta_guess = 0.05 * mpv_guess
    sigma_guess = 0.15 * mpv_guess
    A_guess = max(counts)
    p0 = [mpv_guess, eta_guess, sigma_guess, A_guess]
    
    fit_mask = (centers > 2.6) & (centers < 13)
    params, cov = curve_fit(langau, centers[fit_mask], counts[fit_mask], p0=p0, maxfev=10000)
    print(f"MVP = {params[0]:.2f}, Amplitude = {params[3]:.2f}, Eta = {params[1]:.2f}, Sigma = {params[2]:.2f}")
    errors = np.sqrt(np.diag(cov))
    print(f"MVPer = {errors[0]:.4f}, Amplitudeer = {errors[3]:.4f}, Etaer = {errors[1]:.4f}, Sigmaer = {errors[2]:.4f}")

    fig = plt.figure()
    fig.set_size_inches(8, 6)
    plt.step(edges[:-1], counts, where='post', color='orange')
    x_fit = np.linspace(0, 13, 500)
    plt.plot(x_fit, langau(x_fit, *params), color="mediumvioletred")
    plt.title(f"Energy deposition in bars along x-axis in bottom section", fontsize=17)
    plt.xlim(0,13)
    plt.ylim(0,10000)
    plt.ylabel('Counts', fontsize=16)
    plt.xlabel('Energy deposition [MeV]', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()


def plot_edep_alongz_top():
    x_min_alongz_top=[]
    x_max_alongz_top=[]
    y_min_alongz_top=[]
    y_max_alongz_top=[]
    z_min_alongz_top=[]
    z_max_alongz_top=[]

    for l in range(0,num_layers_top,2):
            for i in range(num_bars):
                x_min_alongz_top.append(first_scint_alongz_xpos + i*scint_width)
                x_max_alongz_top.append(first_scint_alongz_xpos + scint_width + i*scint_width)
                y_min_alongz_top.append(first_layer_ypos_top + l*layer_thickness)
                y_max_alongz_top.append(first_layer_ypos_top + scint_thick + l*layer_thickness)
                z_min_alongz_top.append(-scint_length/2)
                z_max_alongz_top.append(scint_length/2)

    edep_flat_alongz_top=[]
    for i in range(0,len(x_min_alongz_top)):
        mask_x =  (x_hits >= x_min_alongz_top[i]) & (x_hits <= x_max_alongz_top[i])
        mask_y =  (y_hits >= y_min_alongz_top[i]) & (y_hits <= y_max_alongz_top[i])
        mask_z =  (z_hits >= z_min_alongz_top[i]) & (z_hits <= z_max_alongz_top[i])
        mask = mask_x & mask_y & mask_z
        edep_masked = edep[mask]
        mask_nonempty = ak.num(edep_masked) > 0
        edep_nonempty = edep_masked[mask_nonempty]
        edep_summed = ak.sum(edep_nonempty, axis=1)
        edep_flat_alongz_top.append(edep_summed)
        #edep_flat_alongz_bottom.append(ak.flatten(edep[mask]))

    data = ak.to_numpy(ak.flatten(edep_flat_alongz_top))
    counts, edges = np.histogram(data, bins=100, range=(0, 13))
    centers = 0.5 * (edges[:-1] + edges[1:])
    mpv_guess = centers[np.argmax(counts)]
    eta_guess = 0.05 * mpv_guess
    sigma_guess = 0.15 * mpv_guess
    A_guess = max(counts)
    p0 = [mpv_guess, eta_guess, sigma_guess, A_guess]
     
    fit_mask = (centers > 2.6) & (centers < 13)
    params, cov = curve_fit(langau, centers[fit_mask], counts[fit_mask], p0=p0, maxfev=10000)
    print(f"MVP = {params[0]:.2f}, Amplitude = {params[3]:.2f}, Eta = {params[1]:.2f}, Sigma = {params[2]:.2f}")
    errors = np.sqrt(np.diag(cov))
    print(f"MVPer = {errors[0]:.4f}, Amplitudeer = {errors[3]:.4f}, Etaer = {errors[1]:.4f}, Sigmaer = {errors[2]:.4f}")

    fig = plt.figure()
    fig.set_size_inches(8, 6)
    plt.step(edges[:-1], counts, where='post', color='orange', label='Data')
    x_fit = np.linspace(0, 13, 500)
    plt.plot(x_fit, langau(x_fit, *params), color="mediumvioletred", label='Langau fit')
    plt.title(f"Energy deposition in bars along z-axis in top section", fontsize=17)
    plt.xlim(0,13)
    plt.ylim(0,11500)
    plt.ylabel('Counts', fontsize=16)
    plt.xlabel('Energy deposition in bars [MeV]', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=16)
    plt.show()


def plot_edep_alongx_top():
    x_min_alongx_top=[]
    x_max_alongx_top=[]
    y_min_alongx_top=[]
    y_max_alongx_top=[]
    z_min_alongx_top=[]
    z_max_alongx_top=[]

    for l in range(0,num_layers_top,2):
            for i in range(num_bars):
                x_min_alongx_top.append(-scint_length/2)
                x_max_alongx_top.append(scint_length/2)
                y_min_alongx_top.append(first_layer_ypos_top + (l+1)*layer_thickness)
                y_max_alongx_top.append(first_layer_ypos_top + scint_thick + (l+1)*layer_thickness)
                z_min_alongx_top.append(first_scint_alongx_zpos + i*scint_width)
                z_max_alongx_top.append(first_scint_alongx_zpos + scint_width + i*scint_width)
            

    edep_flat_alongx_top=[]
    for i in range(0,len(x_min_alongx_top)):
        mask_x =  (x_hits >= x_min_alongx_top[i]) & (x_hits <= x_max_alongx_top[i])
        mask_y =  (y_hits >= y_min_alongx_top[i]) & (y_hits <= y_max_alongx_top[i])
        mask_z =  (z_hits >= z_min_alongx_top[i]) & (z_hits <= z_max_alongx_top[i])
        mask = mask_x & mask_y & mask_z
        edep_masked = edep[mask]
        mask_nonempty = ak.num(edep_masked) > 0
        edep_nonempty = edep_masked[mask_nonempty]
        edep_summed = ak.sum(edep_nonempty, axis=1)
        edep_flat_alongx_top.append(edep_summed)
        #edep_flat_alongz_bottom.append(ak.flatten(edep[mask]))

    data = ak.to_numpy(ak.flatten(edep_flat_alongx_top))
    counts, edges = np.histogram(data, bins=100, range=(0, 13))
    centers = 0.5 * (edges[:-1] + edges[1:])
    mpv_guess = centers[np.argmax(counts)]
    eta_guess = 0.05 * mpv_guess
    sigma_guess = 0.15 * mpv_guess
    A_guess = max(counts)
    p0 = [mpv_guess, eta_guess, sigma_guess, A_guess]
    
    fit_mask = (centers > 2.6) & (centers < 13)
    params, cov = curve_fit(langau, centers[fit_mask], counts[fit_mask], p0=p0, maxfev=10000)
    print(f"MVP = {params[0]:.2f}, Amplitude = {params[3]:.2f}, Eta = {params[1]:.2f}, Sigma = {params[2]:.2f}")
    errors = np.sqrt(np.diag(cov))
    print(f"MVPer = {errors[0]:.4f}, Amplitudeer = {errors[3]:.4f}, Etaer = {errors[1]:.4f}, Sigmaer = {errors[2]:.4f}")

    fig = plt.figure()
    fig.set_size_inches(8, 6)
    plt.step(edges[:-1], counts, where='post', color='orange', label='Data')
    x_fit = np.linspace(0, 13, 500)
    plt.plot(x_fit, langau(x_fit, *params), color="mediumvioletred", label='Langau fit')
    plt.title(f"Energy deposition in bars along x-axis in top section", fontsize=17)
    plt.xlim(0,13)
    plt.ylim(0,11500)
    plt.ylabel('Counts', fontsize=16)
    plt.xlabel('Energy deposition in bars [MeV]', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=16)
    plt.show()

plot_edep_alongx_top()
plot_edep_alongz_top()
plot_edep_alongx_bottom()
plot_edep_alongz_bottom()

