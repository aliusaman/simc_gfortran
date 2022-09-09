#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-09-09 01:45:54 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
from functools import reduce
import sys,os

###############################################################################################################################################

'''
ltsep package import and pathing definitions
'''

# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
UTILPATH=lt.UTILPATH

################################################################################################################################################
# Define efficiencies

def get_efficiencies(runNum,efficiency_table):

    inp_f = UTILPATH+"/scripts/efficiency/OUTPUTS/%s" % efficiency_table

    # Converts csv data to dataframe
    try:
        eff_data = pd.read_csv(inp_f)
    except IOError:
        print("Error: %s does not appear to exist." % inp_f)
        sys.exit(0)
    #print(eff_data.keys())

    # Redefine table to be only the run number of interest
    eff_data = eff_data[eff_data['Run_Number'] == int(runNum)]
    #print(eff_data)

    # Define dictionary of efficiency values
    effDict ={
        # HMS Detectors
        "HMS_Cer_ALL_Elec_Eff" : eff_data["HMS_Cer_ALL_Elec_Eff"].iloc[0],
        #"HMS_Cer_COIN_Elec_Eff" : eff_data["HMS_Cer_COIN_Elec_Eff"].iloc[0],
        #"HMS_Cer_SING_Elec_Eff" : eff_data["HMS_Cer_SING_Elec_Eff"].iloc[0],
        "HMS_Elec_ALL_TRACK_EFF" : eff_data["HMS_Elec_ALL_TRACK_EFF"].iloc[0],
        #"HMS_Elec_COIN_TRACK_EFF" : eff_data["HMS_Elec_COIN_TRACK_EFF"].iloc[0],
        #"HMS_Elec_SING_TRACK_EFF" : eff_data["HMS_Elec_SING_TRACK_EFF"].iloc[0],
        "HMS_Hodo_3_of_4_EFF" : eff_data["HMS_Hodo_3_of_4_EFF"].iloc[0],
        #"HMS_Hodo_4_of_4_EFF" : eff_data["HMS_Hodo_4_of_4_EFF"].iloc[0],
        # SHMS Detectors
        #"SHMS_Aero_Prot_Eff" : eff_data["SHMS_Aero_Prot_Eff"].iloc[0], # Very low ~40-70%
        #"SHMS_Hadron_ALL_TRACK_EFF" : eff_data["SHMS_Hadron_ALL_TRACK_EFF"].iloc[0],
        "SHMS_Hodo_3_of_4_EFF" : eff_data["SHMS_Hodo_3_of_4_EFF"].iloc[0],
        #"SHMS_Hodo_4_of_4_EFF" : eff_data["SHMS_Hodo_4_of_4_EFF"].iloc[0],
        "SHMS_Prot_ALL_TRACK_EFF" : eff_data["SHMS_Prot_ALL_TRACK_EFF"].iloc[0],
        #"SHMS_Prot_COIN_TRACK_EFF" : eff_data["SHMS_Prot_COIN_TRACK_EFF"].iloc[0],
        #"SHMS_Prot_SING_TRACK_EFF" : eff_data["SHMS_Prot_SING_TRACK_EFF"].iloc[0],
        # Livetimes
        #"COIN_CPULT" : eff_data["COIN_CPULT"].iloc[0], # Using TLT
        #"HMS_CPULT" : eff_data["HMS_CPULT"].iloc[0], # Oddly very low, ~6%
        #"SHMS_CPULT" : eff_data["SHMS_CPULT"].iloc[0], # Oddly very low, ~6%
        "Non_Scaler_EDTM_Live_Time" : eff_data["Non_Scaler_EDTM_Live_Time"].iloc[0],
    }

    # Define dictionary of efficiency uncertainty values
    effErrorDict ={
        # HMS Detectors
        "HMS_Cer_ALL_Elec_Eff_ERROR" : eff_data["HMS_Cer_ALL_Elec_Eff_ERROR"].iloc[0],
        #"HMS_Cer_COIN_Elec_Eff_ERROR" : eff_data["HMS_Cer_COIN_Elec_Eff_ERROR"].iloc[0],
        #"HMS_Cer_SING_Elec_Eff_ERROR" : eff_data["HMS_Cer_SING_Elec_Eff_ERROR"].iloc[0],
        "HMS_Elec_ALL_TRACK_EFF_ERROR" : eff_data["HMS_Elec_ALL_TRACK_EFF_ERROR"].iloc[0],
        #"HMS_Elec_COIN_TRACK_EFF_ERROR" : eff_data["HMS_Elec_COIN_TRACK_EFF_ERROR"].iloc[0],
        "HMS_Elec_SING_TRACK_EFF_ERROR" : eff_data["HMS_Elec_SING_TRACK_EFF_ERROR"].iloc[0],
        # SHMS Detectors
        #"SHMS_Aero_Prot_Eff_ERROR" : eff_data["SHMS_Aero_Prot_Eff_ERROR"].iloc[0],
        #"SHMS_Hadron_ALL_TRACK_EFF_ERROR" : eff_data["SHMS_Hadron_ALL_TRACK_EFF_ERROR"].iloc[0],
        "SHMS_Prot_ALL_TRACK_EFF_ERROR" : eff_data["SHMS_Prot_ALL_TRACK_EFF_ERROR"].iloc[0],
        #"SHMS_Prot_COIN_TRACK_EFF_ERROR" : eff_data["SHMS_Prot_COIN_TRACK_EFF_ERROR"].iloc[0],
        #"SHMS_Prot_SING_TRACK_EFF_ERROR" : eff_data["SHMS_Prot_SING_TRACK_EFF_ERROR"].iloc[0],
        # Livetimes
        #"COIN_CPULT_ERROR" : eff_data["COIN_CPULT_ERROR"].iloc[0],
        #"HMS_CPULT_ERROR" : eff_data["HMS_CPULT_ERROR"].iloc[0],
        #"SHMS_CPULT_ERROR" : eff_data["SHMS_CPULT_ERROR"].iloc[0],
        "Non_Scaler_EDTM_Live_Time_ERROR" : eff_data["Non_Scaler_EDTM_Live_Time_ERROR"].iloc[0],
    }    

    return [effDict,effErrorDict]

def calculate_efficiency(runNum,efficiency_table):

    effDict = get_efficiencies(runNum,efficiency_table)[0] # Efficiency dictionary

    # Calculate total efficiency. The reduce function pretty much iterates on
    # its arguments which in this case is a lambda function. This lambda function
    # takes x,y from the list (ie the list of efficiencies) and multiplies them.
    # This is all pythonic mumbo-jumbo for doing the product of everything in the
    # list. Enjoy!
    tot_efficiency = reduce(lambda x, y: x*y, list(effDict.values()))
    return tot_efficiency