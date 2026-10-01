
import uproot # for data loading
import awkward as ak # for data manipulation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
import pylandau
import numpy as np

#-------------------------
#OPEN ROOT FILE
#-------------------------

with uproot.open('check.root') as f:
    events = f['LDMX_Events'].arrays()


#Detected energy in bars
dete = events['HcalRecHits_cosmics.energy_']

#strip, layer and section hits
layer_hits = events['HcalRecHits_cosmics.layer_']
strip_hits = events['HcalRecHits_cosmics.strip_']
section_hits = events['HcalRecHits_cosmics.section_']

section1_mask = (section_hits == 1) 
section2_mask = (section_hits == 2) 

#--------------------------------
# HITS SECTIONs AND LAYERS
#--------------------------------

def plot_hits(title, xlabel, data, bins):

    counts, edges = np.histogram(data, bins=bins)
    centers = 0.5 * (edges[:-1] + edges[1:])
    errors = np.sqrt(counts)
    fig = plt.figure()
    fig.set_size_inches(8, 6)
    plt.hist(data, bins=bins, edgecolor='mediumvioletred', linewidth=1.2, color="w")
    plt.errorbar(centers, counts, yerr=errors, fmt='none', color='mediumvioletred', capsize=3)
    plt.title(title, fontsize=17)
    plt.ylabel('Number of hits', fontsize=16)
    plt.xlabel(xlabel, fontsize=16)
    plt.xticks(centers.astype(int), fontsize=14)
    ax = plt.gca()
    ax.yaxis.get_offset_text().set_fontsize(14)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(3,3))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()

section_hits_flat = ak.to_numpy(ak.flatten(section_hits))
bins_section=np.arange(0.5, 3.5, 1)
plot_hits("Hits in sections", "Section", section_hits_flat, bins_section)

layer_hit_flat= ak.to_numpy(ak.flatten(layer_hits))
layer_hit_flat1= ak.to_numpy(ak.flatten(layer_hits[section1_mask]))
layer_hit_flat2= ak.to_numpy(ak.flatten(layer_hits[section2_mask]))
bins_layer = np.arange(0.5, 9.5, 1)

plot_hits("Hits in layers top section", "Layer", layer_hit_flat1, bins_layer)
plot_hits("Hits in layers bottom section", "Layer", layer_hit_flat2, bins_layer)

#--------------------------
#DETECTED ENERGY
#--------------------------

def langau(x, mpv, eta, sigma, A):
        return pylandau.langau(x, mpv, eta, sigma,A)

def plot_dete_bars(title, layermask, sectionmask):
    mask = layermask & sectionmask
    energy_strip = dete[mask]
    energy_nonempty = ak.flatten(energy_strip)
    
    data = ak.to_numpy(energy_nonempty)
    counts, edges = np.histogram(data, bins=100, range=(0, 13))
    centers = 0.5 * (edges[:-1] + edges[1:])
    mpv_guess = centers[np.argmax(counts)]
    eta_guess = 0.05 * mpv_guess
    sigma_guess = 0.15 * mpv_guess
    A_guess = max(counts)
    p0 = [mpv_guess, eta_guess, sigma_guess, A_guess]

    fit_mask = (centers > 1.6) & (centers < 13)
    params, cov = curve_fit(langau, centers[fit_mask], counts[fit_mask], p0=p0, maxfev=10000)

    print(f"MVP = {params[0]:.2f}, Amplitude = {params[3]:.2f}, Eta = {params[1]:.2f}, Sigma = {params[2]:.2f}")
    errors = np.sqrt(np.diag(cov))
    print(f"MVPer = {errors[0]:.4f}, Amplitudeer = {errors[3]:.4f}, Etaer = {errors[1]:.4f}, Sigmaer = {errors[2]:.4f}")

    fig = plt.figure()
    fig.set_size_inches(8, 6)
    plt.step(edges[:-1], counts, where='post', color='orange',  label='Data')
    x_fit = np.linspace(0, 13, 500)
    plt.plot(x_fit, langau(x_fit, *params), color="mediumvioletred",  label='Langau fit')
    plt.title(title, fontsize=17)
    plt.ylabel('Counts', fontsize=16)
    plt.xlabel('Detected energy in bars [MeV]', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=16)
    plt.xlim(0, 13)
    plt.show()

plot_dete_bars("Bars along x in top section", (layer_hits % 2 == 0 ), (section_hits == 1))
plot_dete_bars("Bars along z in top section", (layer_hits % 2 != 0 ), (section_hits == 1))
plot_dete_bars("Bars along x in bottom section", (layer_hits % 2 == 0 ), (section_hits == 2))
plot_dete_bars("Bars along z in bottom section", (layer_hits % 2 != 0 ), (section_hits == 2))

#------------------------------
#ANGLE DEPENDENCE
#------------------------------

pdg_id = events['SimParticles_cosmics.second.pdg_id_']
muon_mask = (pdg_id == 13) | (pdg_id == -13)

px_muon = events['SimParticles_cosmics.second.px_'][muon_mask]
py_muon = events['SimParticles_cosmics.second.py_'][muon_mask]
pz_muon = events['SimParticles_cosmics.second.pz_'][muon_mask]

p = np.sqrt(px_muon**2 + py_muon**2 + pz_muon**2)
polar_angle_deg = np.arccos(-py_muon / p)*180/np.pi
azimuthal_angle_deg = np.arctan2(px_muon, pz_muon)*180/np.pi

def plot_dete_vs_polar(title, mask=None):
     if mask is None:
        dete_mask = dete
     else:
        dete_mask = dete[mask]

     polar_angle_expanded = ak.broadcast_arrays(polar_angle_deg[:,0], dete_mask)[0]

     polar_angles = ak.to_numpy(ak.flatten(polar_angle_expanded))
     energies = ak.to_numpy(ak.flatten(dete_mask))

     fig = plt.figure()
     fig.set_size_inches(8, 6)
     plt.hist2d(polar_angles, energies, bins=[100, 100],  range=[[0, 75], [0, 15]],  cmap='plasma')
     plt.title(title, fontsize=17)
     plt.xlabel(r"Polar angle $\theta$ [deg]", fontsize=16)
     plt.ylabel("Detected energy in bars [MeV]", fontsize=16)
     plt.colorbar(label="Counts")
     plt.xticks(fontsize=14)
     plt.yticks(fontsize=14)
     plt.ylim(0, 15)
     plt.show()


def plot_dete_vs_az(title, mask=None):
     if mask is None:
        dete_mask = dete
     else:
        dete_mask = dete[mask]

     azimuthal_angles_expanded_mask = ak.broadcast_arrays(azimuthal_angle_deg[:,0], dete_mask)[0]
     azimuthal_angles_mask = ak.to_numpy(ak.flatten(azimuthal_angles_expanded_mask))
     energies_mask = ak.to_numpy(ak.flatten(dete_mask))

     fig = plt.figure()
     fig.set_size_inches(8, 6)
     plt.hist2d(azimuthal_angles_mask, energies_mask, bins=[100, 100], range=[[-180, 180], [0, 15]], cmap='plasma')
     plt.title(title, fontsize=17)
     plt.xlabel(r"Azimuthal angle $\phi$ [deg]", fontsize=16)
     plt.ylabel("Detected energy in bars [MeV]", fontsize=16)
     plt.colorbar(label="Counts")
     plt.xticks(fontsize=14)
     plt.yticks(fontsize=14)
     plt.ylim(0, 15)
     plt.show()

plot_dete_vs_polar("Detected energy vs Polar Angle")
plot_dete_vs_az("Detected energy vs Azimuthal Angle")
plot_dete_vs_az("Detected energy vs Azimuthal Angle Even Layers", mask = (layer_hits % 2 == 0))
plot_dete_vs_az("Detected energy vs Azimuthal Angle Odd Layers", mask = (layer_hits % 2 != 0))
