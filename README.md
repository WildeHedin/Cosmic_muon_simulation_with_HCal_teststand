# HCal-Prototype-Cosmics
This page is still being edited.
In this project I have implemented a geometry description, in the LDMX software, of the HCal prototype that will be assembled at SLAC to measure cosmic muons. Cosmic muon simulations have also been performed and the interactions with the detector have been analyzed.  

## Geometry implementation
Two main files have been created and modified during this project: A GDML file, which provides detector information to Geant4, and a python file, which provides detector information to ldmx-sw. These two files can be found in the folder NewGeometry and have been included in ldmx-sw v.XXXX. 

## Generate simulation samples
### Generate a LHE-file
An LHE-file contains initial information about the cosmic muons. 

Run: denv python3 lheData/cosmic_muon_lhe_generator_updated.py --numEvents=xx --detector=cosmicHcalPrototype

A simplified description of the Cosmic HCal prototype geometry has been added to cosmic_muon_lhe_generator_updated.py. 
In addition, several if statesments have been updated because some muons were never assigned a vertex in the previous generators. 
This is explained a bit better in my thesis. 

### Geant4 simulation
Create a folder that will store the ROOT files:

mkdir cosmicEvents

Run: just -f ~/ldmx-sw/justfile fire cosmic_config_hcalprototype.py lheData/name_of_file.lhe 

### Analyze
The file AnalyzeRecHits.py performs the analysis of the reconstructed data presented in my thesis, while the AnalyzeSimHits.py analyses the truth-level data. AnalyzeSimHits.py might have to be modified if future changes are made to the GDML file which describes the cosmic HCal geometry. 

