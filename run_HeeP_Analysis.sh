#! /bin/bash

KIN=$1

ANA_DIR="/group/c-kaonlt/USERS/${USER}/simc_gfortran/scripts"

InDATAFilename="Raw_Data_$KIN.root"
InDUMMYFilename="Raw_DummyData_$KIN.root"
InSIMCFilename="Heep_Coin_$KIN.root"
OutDATAFilename="Analysed_Data_$KIN"
OutDUMMYFilename="Analysed_DummyData_$KIN"
OutFullAnalysisFilename="FullAnalysis_$KIN"

cd $ANA_DIR
echo
echo "Analysing data..."
echo
root -l <<EOF 
.x $ANA_DIR/Analysed_COIN.C("$InDATAFilename","$OutDATAFilename")
EOF
echo
echo "Analysing dummy data..."
echo
root -l <<EOF 
.x $ANA_DIR/Analysed_COIN.C("$InDUMMYFilename","$OutDUMMYFilename")
EOF

python3 HeepCoin.py "${OutDATAFilename}.root" "${OutDUMMYFilename}.root" ${InSIMCFilename} ${OutFullAnalysisFilename}

cd ../
evince "OUTPUTS/${OutFullAnalysisFilename}.pdf"
