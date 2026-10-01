
import LDMX.Ecal.ecal_hardcoded_conditions 
import LDMX.Hcal.hcal_geometry 
import LDMX.Ecal.ecal_geometry 
import LDMX.Hcal.hcal_hardcoded_conditions

# import processor templates
import LDMX.Hcal.digi as hcal_digi
import LDMX.Hcal.hcal_geometry

from datetime import datetime
current_date = datetime.now().strftime("%Y%m%d")  # Added current date to the filename
output_string = "cosmicEvents/cosmic_events_" + current_date + ".root"

import time

start = time.time()

p.output_files = [output_string]
p.run = 1
p.log_frequency = 1
p.logger.term_level=1


from LDMX.SimCore.simulator import Simulator

sim = Simulator('lhe_cosmics_simulation')

sim.set_detector( 'ldmx-esa-cosmic26-v1' )

import os,sys
full_lhe_file_path = os.path.realpath(sys.argv[1])
print(os.listdir())

from LDMX.SimCore import generators

sim.generators = [ generators.Lhe(full_lhe_file_path)]

p.max_events = 10000

# HcalDigiProducer and/or HcalRecProducer do not work correctly with the data obtained when simulating events with the implemented GDML file "hcal-prototype-cosmics". 
#p.sequence = [ sim , hcal_digi.HcalDigiProducer(), hcal_digi.HcalRecProducer()]
p.sequence = [ sim , hcal_digi.HcalSimpleDigiAndRecProducer()]

