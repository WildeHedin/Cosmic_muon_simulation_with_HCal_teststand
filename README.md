# Cosmic muon simulation with HCal test-stand
This code was developed for the thesis ["Cosmic muon simulation with a new HCal prototype geometry at LDMX"](https://lup.lub.lu.se/student-papers/search/publication/9246704). In this project I have included a geometry description of the hadronic calorimeter components in [ldmx-sw](https://github.com/LDMX-Software/ldmx-sw) of the test-stand that LDMX will use to measure cosmic muons at SLAC. Cosmic muon simulations have also been performed and the interactions with the detector have been analyzed.  

## Geometry implementation
Two main files have been created and modified during this project: A GDML file, which provides detector information to Geant4, and a python file, which provides detector information to ldmx-sw. These two files can be found in the folder NewGeometry and have been included in ldmx-sw v4.9.2. 

## Generate simulation samples
Before getting started denv must be installed according to https://ldmx-software.github.io/. The version must be v4.9.2 or later. 

### Generate a LHE-file
First an LHE-file with must be created to store initial information about the cosmic muons. 

Run: denv python3 lheData/cosmic_muon_lhe_generator.py --numEvents=xx --detector=HcalCosmic

A simplified description of the HCal test-stand geometry has been added to cosmic_muon_lhe_generator.py (HcalCosmic), so that the generator creates the particles at relevant coordinates. In addition, several if statesments in the generator have been updated because some muons were never assigned a vertex in the previous version. 

### Geant4 simulation
Before performing the simulation, create a folder that will store the ROOT files:

mkdir cosmicEvents

then run:

denv fire cosmic_config_teststand.py lheData/name_of_file.lhe 

### Analyze
The file analyse_rechits.py performs the analysis of the reconstructed data presented in my thesis, while analyse_simhits.py analyses the truth-level data. analyze_simhits.py might have to be modified if future changes are made to the GDML file.

