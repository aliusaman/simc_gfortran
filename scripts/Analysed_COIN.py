#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-03 11:39:47 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

###################################################################################################################################################

# Import relevant packages
import uproot as up
import numpy as np
import root_numpy as rnp
import pandas as pd
import root_pandas as rpd
import ROOT
import scipy
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import sys, math, os, subprocess

##################################################################################################################################################

# Check the number of arguments provided to the script
if len(sys.argv)-1!=1:
    print("!!!!! ERROR !!!!!\n Expected 3 arguments\n Usage is with - ROOTfilePrefix RunNumber MaxEvents \n!!!!! ERROR !!!!!")
    sys.exit(1)

##################################################################################################################################################

# Input params - run number and max number of events
ROOTPrefix = "Kaon_coin_replay_production"
runNum = sys.argv[1]
MaxEvent = "-1"

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
import ltsep as lt 


##############################################################################################################################################
'''
Define and set up cuts
'''

fout = '/DB/CUTS/run_type/simc_coin_heep.cuts'

# defining Cuts
cuts = ["coin_ep_cut_prompt_noRF_nopid"]

proc_root = lt.Root(ROOTPrefix,runNum,MaxEvent,fout,cuts,os.path.realpath(__file__)).setup_ana()
c = proc_root[0] # Cut object
b = proc_root[1] # Dictionary of branches
OUTPATH = proc_root[2] # Get pathing for OUTPATH

#################################################################################################################################################################
UTILPATH = lt.SetPath(os.path.realpath(__file__)).getPath("UTILPATH")
rootName = "%s/ROOTfiles/Analysis/HeeP/%s_%s_%s.root" % (UTILPATH, ROOTPrefix, runNum, MaxEvent)     # Input file location and variables taking
s_tree = up.open(rootName)["TSP"]

P_BCM4A_scalerCharge = s_tree.array("P.BCM4A.scalerCharge")
P_BCM2_scalerCharge = s_tree.array("P.BCM2.scalerCharge")
P_BCM4B_scalerCharge = s_tree.array("P.BCM4B.scalerCharge")
P_BCM1_scalerCharge = s_tree.array("P.BCM1.scalerCharge")
P_BCM4C_scalerCharge = s_tree.array("P.BCM4C.scalerCharge")

P_BCM4A_scalerCurrent = s_tree.array("P.BCM4A.scalerCurrent")
P_BCM2_scalerCurrent = s_tree.array("P.BCM2.scalerCurrent")
P_BCM4B_scalerCurrent = s_tree.array("P.BCM4B.scalerCurrent")
P_BCM1_scalerCurrent = s_tree.array("P.BCM1.scalerCurrent")
P_BCM4C_scalerCurrent = s_tree.array("P.BCM4C.scalerCurrent")

def scalers():
    
    NoCut = [P_BCM4A_scalerCharge,P_BCM4B_scalerCharge,P_BCM4C_scalerCharge,P_BCM2_scalerCharge,P_BCM1_scalerCharge,P_BCM4A_scalerCurrent,P_BCM4B_scalerCurrent,P_BCM4C_scalerCurrent,P_BCM2_scalerCurrent,P_BCM1_scalerCurrent]
        
    Uncut = [(P_BCM4A_scalerCharge,P_BCM4B_scalerCharge,P_BCM4C_scalerCharge,P_BCM2_scalerCharge,P_BCM1_scalerCharge,P_BCM4A_scalerCurrent,P_BCM4B_scalerCurrent,P_BCM4C_scalerCurrent,P_BCM2_scalerCurrent,P_BCM1_scalerCurrent) for (P_BCM4A_scalerCharge,P_BCM4B_scalerCharge,P_BCM4C_scalerCharge,P_BCM2_scalerCharge,P_BCM1_scalerCharge,P_BCM4A_scalerCurrent,P_BCM4B_scalerCurrent,P_BCM4C_scalerCurrent,P_BCM2_scalerCurrent,P_BCM1_scalerCurrent) in zip(*NoCut)]
    
    SCALERS = {
        "scaler" : Uncut,
    }

    return SCALERS

def coin_protons():

    # Define the array of arrays containing the relevant HMS and SHMS info                              

    NoCut_COIN_Protons = [b["H_gtr_yp"],b["H_gtr_xp"],b["H_dc_yp_fp"],b["H_dc_xp_fp"],b["H_dc_y_fp"],b["H_dc_x_fp"],b["P_gtr_yp"],b["P_gtr_xp"],b["P_dc_yp_fp"],b["P_dc_xp_fp"],b["P_dc_y_fp"],b["P_dc_x_fp"],b["P_dc_InsideDipoleExit"],b["H_dc_InsideDipoleExit"],b["H_gtr_beta"],  b["H_gtr_dp"], b["H_gtr_p"], b["H_hod_goodscinhit"], b["H_hod_goodstarttime"], b["H_cal_etotnorm"], b["H_cal_etottracknorm"], b["H_cer_npeSum"], b["CTime_epCoinTime_ROC1"], b["P_gtr_beta"],  b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["MMp"], b["H_RF_Dist"],b["P_RF_Dist"], b["Q2"], b["W"], b["epsilon"], b["ph_q"], b["MandelT"], b["emiss"],b["pmiss"], b["pmiss_x"], b["pmiss_y"], b["pmiss_z"]]

    Uncut_COIN_Protons = [(b["H_gtr_yp"],b["H_gtr_xp"],b["H_dc_yp_fp"],b["H_dc_xp_fp"],b["H_dc_y_fp"],b["H_dc_x_fp"],b["P_gtr_yp"],b["P_gtr_xp"],b["P_dc_yp_fp"],b["P_dc_xp_fp"],b["P_dc_y_fp"],b["P_dc_x_fp"],b["P_dc_InsideDipoleExit"],b["H_dc_InsideDipoleExit"],b["H_gtr_beta"],  b["H_gtr_dp"], b["H_gtr_p"], b["H_hod_goodscinhit"], b["H_hod_goodstarttime"], b["H_cal_etotnorm"], b["H_cal_etottracknorm"], b["H_cer_npeSum"], b["CTime_epCoinTime_ROC1"], b["P_gtr_beta"],  b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["MMp"], b["H_RF_Dist"],b["P_RF_Dist"], b["Q2"], b["W"], b["epsilon"], b["ph_q"], b["MandelT"], b["emiss"],b["pmiss"], b["pmiss_x"], b["pmiss_y"], b["pmiss_z"]) for (b["H_gtr_yp"],b["H_gtr_xp"],b["H_dc_yp_fp"],b["H_dc_xp_fp"],b["H_dc_y_fp"],b["H_dc_x_fp"],b["P_gtr_yp"],b["P_gtr_xp"],b["P_dc_yp_fp"],b["P_dc_xp_fp"],b["P_dc_y_fp"],b["P_dc_x_fp"],b["P_dc_InsideDipoleExit"],b["H_dc_InsideDipoleExit"],b["H_gtr_beta"],  b["H_gtr_dp"], b["H_gtr_p"], b["H_hod_goodscinhit"], b["H_hod_goodstarttime"], b["H_cal_etotnorm"], b["H_cal_etottracknorm"], b["H_cer_npeSum"], b["CTime_epCoinTime_ROC1"], b["P_gtr_beta"],  b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["MMp"], b["H_RF_Dist"],b["P_RF_Dist"], b["Q2"], b["W"], b["epsilon"], b["ph_q"], b["MandelT"], b["emiss"],b["pmiss"], b["pmiss_x"], b["pmiss_y"], b["pmiss_z"]) in zip(*NoCut_COIN_Protons)
        ]

    # Create array of arrays of pions after cuts, all events, prompt and random          

    Cut_COIN_Protons_tmp = NoCut_COIN_Protons
    Cut_COIN_Protons_all_tmp = []

    for arr in Cut_COIN_Protons_tmp:
        Cut_COIN_Protons_all_tmp.append(c.add_cut(arr, "coin_ep_cut_prompt_noRF_nopid"))

    Cut_COIN_Protons_all = [(b["H_gtr_yp"],b["H_gtr_xp"],b["H_dc_yp_fp"],b["H_dc_xp_fp"],b["H_dc_y_fp"],b["H_dc_x_fp"],b["P_gtr_yp"],b["P_gtr_xp"],b["P_dc_yp_fp"],b["P_dc_xp_fp"],b["P_dc_y_fp"],b["P_dc_x_fp"],b["P_dc_InsideDipoleExit"],b["H_dc_InsideDipoleExit"],b["H_gtr_beta"],  b["H_gtr_dp"], b["H_gtr_p"], b["H_hod_goodscinhit"], b["H_hod_goodstarttime"], b["H_cal_etotnorm"], b["H_cal_etottracknorm"], b["H_cer_npeSum"], b["CTime_epCoinTime_ROC1"], b["P_gtr_beta"],  b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["MMp"], b["H_RF_Dist"],b["P_RF_Dist"], b["Q2"], b["W"], b["epsilon"], b["ph_q"], b["MandelT"], b["emiss"],b["pmiss"], b["pmiss_x"], b["pmiss_y"], b["pmiss_z"]) for (b["H_gtr_yp"],b["H_gtr_xp"],b["H_dc_yp_fp"],b["H_dc_xp_fp"],b["H_dc_y_fp"],b["H_dc_x_fp"],b["P_gtr_yp"],b["P_gtr_xp"],b["P_dc_yp_fp"],b["P_dc_xp_fp"],b["P_dc_y_fp"],b["P_dc_x_fp"],b["P_dc_InsideDipoleExit"],b["H_dc_InsideDipoleExit"],b["H_gtr_beta"],  b["H_gtr_dp"], b["H_gtr_p"], b["H_hod_goodscinhit"], b["H_hod_goodstarttime"], b["H_cal_etotnorm"], b["H_cal_etottracknorm"], b["H_cer_npeSum"], b["CTime_epCoinTime_ROC1"], b["P_gtr_beta"],  b["P_gtr_p"], b["P_gtr_dp"], b["P_hod_goodscinhit"], b["P_hod_goodstarttime"], b["P_cal_etotnorm"], b["P_cal_etottracknorm"], b["P_aero_npeSum"], b["P_aero_xAtAero"], b["P_aero_yAtAero"], b["P_hgcer_npeSum"], b["P_hgcer_xAtCer"], b["P_hgcer_yAtCer"], b["MMp"], b["H_RF_Dist"],b["P_RF_Dist"], b["Q2"], b["W"], b["epsilon"], b["ph_q"], b["MandelT"], b["emiss"],b["pmiss"], b["pmiss_x"], b["pmiss_y"], b["pmiss_z"]) in zip(*Cut_COIN_Protons_all_tmp)
        ]

    COIN_Protons = {
        "Uncut_Proton_Events" : Uncut_COIN_Protons,
        "Cut_Proton_Events_All" : Cut_COIN_Protons_all,
        }

    return COIN_Protons

##################################################################################################################################################################

def main():
    
    COIN_Proton_Data = coin_protons()

    Scaler_Data = scalers()

    # This is just the list of branches we use from the initial root file for each dict
    # I don't like re-defining this here as it's very prone to errors if you included (or removed something) earlier but didn't modify it here
    # Should base the branches to include based on some list and just repeat the list here (or call it again directly below)

    COIN_Proton_Data_Header = ["hsyptar","hsxptar","hsypfp","hsxpfp","hsyfp","hsxfp","ssyptar","ssxptar","ssypfp","ssxpfp","ssyfp","ssxfp","P_dc_InsideDipoleExit","H_dc_InsideDipoleExit","H_gtr_eta", "hsdelta", "H_gtr_p", "H_hod_goodscinhit", "H_hod_goodstarttime", "H_cal_etotnorm", "H_cal_etottracknorm", "H_cer_npeSum", "CTime_epCoinTime_ROC1", "P_gtr_eta", "P_gtr_p", "ssdelta", "P_hod_goodscinhit", "P_hod_goodstarttime", "P_cal_etotnorm", "P_cal_etottracknorm", "P_aero_npeSum", "P_aero_xAtAero", "P_aero_yAtAero", "P_hgcer_npeSum", "P_hgcer_xAtCer", "P_hgcer_yAtCer", "MMp", "H_RF_Dist","P_RF_Dist", "Q2", "W", "epsilon", "ph_q", "MandelT", "emiss", "pmiss", "pmx", "pmy", "pmz"]

    Scaler_Data_Header = ["bcm4a_charge","bcm4b_charge","bcm4c_charge","bcm2_charge","bcm1_charge","bcm4a_current","bcm4b_current","bcm4c_current","bcm2_current","bcm1_current"]
    
    # Need to create a dict for all the branches we grab                                                
    data = {}
    for d in (COIN_Proton_Data,Scaler_Data): 
        data.update(d)
    data_keys = list(data.keys()) # Create a list of all the keys in all dicts added above, each is an array of data

    for i in range (0, len(data_keys)):
        if("Proton" in data_keys[i]):
            DFHeader=list(COIN_Proton_Data_Header)
        elif("scaler" in data_keys[i]):
            DFHeader=list(Scaler_Data_Header)
        else:
            continue
            # Uncomment the line below if you want .csv file output, WARNING the files can be very large and take a long time to process!                                                                      
            #pd.DataFrame(data.get(data_keys[i])).to_csv("%s/%s_%s.csv" % (OUTPATH, data_keys[i], runNum), header=DFHeader, index=False) # Convert array to panda dataframe and write to csv with correct header                                                                                                      
        if (i == 0):
            pd.DataFrame(data.get(data_keys[i]), columns = DFHeader, index = None).to_root("%s/%s_%s_Raw_Data.root" % (OUTPATH, runNum, MaxEvent), key ="%s" % data_keys[i])
        elif (i != 0):
            pd.DataFrame(data.get(data_keys[i]), columns = DFHeader, index = None).to_root("%s/%s_%s_Raw_Data.root" % (OUTPATH, runNum, MaxEvent), key ="%s" % data_keys[i], mode ='a')

if __name__ == '__main__':
    main()
print ("Processing Complete")