#! /bin/bash

# Runs script in the ltsep python package that grabs current path enviroment
if [[ ${HOSTNAME} = *"cdaq"* ]]; then
    PATHFILE_INFO=`python3 /home/cdaq/pionLT-2021/hallc_replay_lt/UTIL_PION/bin/python/ltsep/scripts/getPathDict.py $PWD` # The output of this python script is just a comma separated string
elif [[ ${HOSTNAME} = *"farm"* ]]; then
    PATHFILE_INFO=`python3 /u/home/${USER}/.local/lib/python3.4/site-packages/ltsep/scripts/getPathDict.py $PWD` # The output of this python script is just a comma separated string
fi

# Split the string we get to individual variables, easier for printing and use later
VOLATILEPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f1` # Cut the string on , delimitter, select field (f) 1, set variable to output of command
ANALYSISPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f2`
HCANAPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f3`
REPLAYPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f4`
UTILPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f5`
PACKAGEPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f6`
OUTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f7`
ROOTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f8`
REPORTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f9`
CUTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f10`
PARAMPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f11`
SCRIPTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f12`
ANATYPE=`echo ${PATHFILE_INFO} | cut -d ','  -f13`
USER=`echo ${PATHFILE_INFO} | cut -d ','  -f14`
HOST=`echo ${PATHFILE_INFO} | cut -d ','  -f15`
SIMCPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f16`

while getopts 'haos' flag; do
    case "${flag}" in
        h) 
        echo "--------------------------------------------------------------"
        echo "./run_HeeP_Analysis.sh -{flags} {variable arguments, see help}"
        echo "--------------------------------------------------------------"
        echo
        echo "The following flags can be called for the heep analysis..."
        echo "    -h, help"
        echo "    -a, analyze"
	echo "        coin -> KIN=arg1"
	echo "        sing -> SPEC=arg1 KIN=arg2 (requires -s flag)"
	echo "    -s, single arm"
	echo "    -o, offset to replay applied"
        exit 0
        ;;
        a) a_flag='true' ;;
        o) o_flag='true' ;;
	s) s_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

if [[ $a_flag = "true" || $o_flag = "true" || $s_flag = "true" ]]; then
    if [[ $s_flag = "true" ]]; then
	spec=$(echo "$2" | tr '[:upper:]' '[:lower:]')
	SPEC=$(echo "$spec" | tr '[:lower:]' '[:upper:]')
	KIN=$3
	ROOTPREFIX=replay_${spec}_heep
    else
	KIN=$2
	ROOTPREFIX=replay_coin_heep
    fi
else
    KIN=$1
    ROOTPREFIX=replay_coin_heep
fi

if [[ $s_flag = "true" ]]; then
    # Hard coded file
    if [[ $SPEC = "HMS" ]]; then
	EffData="hms_heep_HeePSing_efficiency_data_2022_07_28.csv"
    else
	EffData="shms_heep_HeePSing_efficiency_data_2022_07_28.csv"
    fi
    InDATAFilename="Raw_Data_${SPEC}_${KIN}.root"
    InDUMMYFilename="Raw_DummyData_${SPEC}_${KIN}.root"
    InSIMCFilename="Heep_${SPEC}_${KIN}.root"
    OutDATAFilename="Analysed_Data_${SPEC}_${KIN}"
    OutDUMMYFilename="Analysed_DummyData_${SPEC}_${KIN}"
    if [[ $o_flag = "true" ]]; then
	OutFullAnalysisFilename="FullAnalysis_Offset_${SPEC}_${KIN}"
    else
	OutFullAnalysisFilename="FullAnalysis_${SPEC}_${KIN}"
    fi
else
    # Hard coded file
    EffData="coin_production_HeePCoin_efficiency_data_2022_06_13.csv"
    InDATAFilename="Raw_Data_${KIN}.root"
    InDUMMYFilename="Raw_DummyData_${KIN}.root"
    InSIMCFilename="Heep_Coin_${KIN}.root"
    OutDATAFilename="Analysed_Data_${KIN}"
    OutDUMMYFilename="Analysed_DummyData_${KIN}"
    if [[ $o_flag = "true" ]]; then
	OutFullAnalysisFilename="FullAnalysis_Offset_${KIN}"
    else
	OutFullAnalysisFilename="FullAnalysis_${KIN}"
    fi
fi

if [[ $KIN = "10p6" && $s_flag != "true" ]]; then
    declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # All heep coin 10p6 runs
    #    declare -a data=(4827) # Just one test run
    declare -a dummydata=(4864)
elif [[ $KIN = "8p2" ]]; then
    declare -a data=(7974 7975 7976)
    #    declare -a data=(7974) # Just one test run
    declare -a dummydata=(7977)
elif [[ $KIN = "6p2" ]]; then
    declare -a data=(7866 7867)
    declare -a dummydata=(7868)
elif [[ $KIN = "4p9" ]]; then
    declare -a data=(6881 6882)
    declare -a dummydata=(6883)
elif [[ $KIN = "3p8" ]]; then
    declare -a data=(6634 6635)
    declare -a dummydata=(6637)
elif [[ $KIN = "8p2" && $s_flag != "true" ]]; then
    declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863)
    declare -a dummydata=(4864)
elif [[ $KIN = "10p6" && $s_flag = "true" ]]; then
    declare -a data=(4784 4785) # All heep singles 10p6 runs
    declare -a dummydata=(4786)
elif [[ $KIN = "8p2" && $s_flag = "true" ]]; then
    declare -a data=(111)
    declare -a dummydata=(111)    
else
    echo "Invalid kinematic setting, ${KIN}"
    exit 128
fi

if [[ $a_flag = "true" ]]; then
    if [[ $s_flag = "true" ]]; then
	cd "${SIMCPATH}/scripts/SING"
	echo
	echo "Analysing ${SPEC} data..."
	echo

	for i in "${data[@]}"
	do
	    echo
	    echo "-----------------------------"
	    echo "Analysing data run $i..."
	    echo "-----------------------------"
	    echo
	    python3 Analysed_SING.py "$i" ${SPEC}
	    #root -l <<EOF 
	    #.x $SIMCPATH/Analysed_SING.C("$InDATAFilename","$OutDATAFilename")
	    #EOF
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/HeeP"
	echo
	echo "Combining root files..."  
	hadd -f ${OutDATAFilename}.root *_-1_${SPEC}_Raw_Data.root
	rm -f *_-1_${SPEC}_Raw_Data.root

	cd "${SIMCPATH}/scripts/SING"    
	echo
	echo "Analysing ${SPEC} dummy data..."
	echo

	for i in "${dummydata[@]}"
	do
	    echo
	    echo "-----------------------------------"
	    echo "Analysing dummy data run $i..."
	    echo "-----------------------------------"
	    echo
	    python3 Analysed_SING.py "$i" ${SPEC}
	    #root -l <<EOF 
	    #.x $SIMCPATH/Analysed_SING.C("$InDUMMYFilename","$OutDUMMYFilename")
	    #EOF
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/HeeP"
	echo
	echo "Combining root files..."
	hadd -f ${OutDUMMYFilename}.root *_-1_${SPEC}_Raw_Data.root
	rm -f *_-1_${SPEC}_Raw_Data.root	
    else
	cd "${SIMCPATH}/scripts/COIN"
	echo
	echo "Analysing data..."
	echo

	for i in "${data[@]}"
	do
	    echo
	    echo "-----------------------------"
	    echo "Analysing data run $i..."
	    echo "-----------------------------"
	    echo
	    python3 Analysed_COIN.py "$i"
	    #root -l <<EOF 
	    #.x $SIMCPATH/Analysed_COIN.C("$InDATAFilename","$OutDATAFilename")
	    #EOF
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/HeeP"
	echo
	echo "Combining root files..."  
	hadd -f ${OutDATAFilename}.root *_-1_Raw_Data.root
	rm -f *_-1_Raw_Data.root

	cd "${SIMCPATH}/scripts/COIN"    
	echo
	echo "Analysing dummy data..."
	echo

	for i in "${dummydata[@]}"
	do
	    echo
	    echo "-----------------------------------"
	    echo "Analysing dummy data run $i..."
	    echo "-----------------------------------"
	    echo
	    python3 Analysed_COIN.py "$i"
	    #root -l <<EOF 
	    #.x $SIMCPATH/Analysed_COIN.C("$InDUMMYFilename","$OutDUMMYFilename")
	    #EOF
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/HeeP"
	echo
	echo "Combining root files..."
	hadd -f ${OutDUMMYFilename}.root *_-1_Raw_Data.root
	rm -f *_-1_Raw_Data.root
    fi
fi

cd "${SIMCPATH}/scripts"

DataChargeVal=()
DataEffVal=()
echo
echo "Calculating data total charge..."
for i in "${data[@]}"
do
    DataChargeVal+=($(python3 findcharge.py ${ROOTPREFIX} "$i" -1))
    DataEffVal+=($(python3 calculate_efficiency.py "$i" ${EffData}))
    #echo "${DataChargeVal[@]} mC"
done
DataChargeSum=$(IFS=+; echo "$((${DataChargeVal[*]}))") # Only works for integers
echo "${DataChargeSum} uC"

DummyChargeVal=()
DummyEffVal=()
echo
echo "Calculating dummy total charge..."
for i in "${dummydata[@]}"
do
    DummyChargeVal+=($(python3 findcharge.py ${ROOTPREFIX} "$i" -1))
    DummyEffVal+=($(python3 calculate_efficiency.py "$i" ${EffData}))
    #echo "${DummyChargeVal[@]} mC"
done
DummyChargeSum=$(IFS=+; echo "$((${DummyChargeVal[*]}))") # Only works for integers
echo "${DummyChargeSum} uC"

if [[ $s_flag = "true" ]]; then
    cd "${SIMCPATH}/scripts/SING"
    python3 HeepSing.py ${KIN} "${OutDATAFilename}.root" $DataChargeSum "${DataEffVal[*]}" "${OutDUMMYFilename}.root" $DummyChargeSum "${DummyEffVal[*]}" ${InSIMCFilename} ${OutFullAnalysisFilename} ${SPEC}
else
    cd "${SIMCPATH}/scripts/COIN"
    python3 HeepCoin.py ${KIN} "${OutDATAFilename}.root" $DataChargeSum "${DataEffVal[*]}" "${OutDUMMYFilename}.root" $DummyChargeSum "${DummyEffVal[*]}" ${InSIMCFilename} ${OutFullAnalysisFilename}
fi

cd "${SIMCPATH}"
evince "OUTPUT/Analysis/HeeP/${OutFullAnalysisFilename}.pdf"
