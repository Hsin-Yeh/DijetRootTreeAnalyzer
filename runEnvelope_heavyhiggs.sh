#!/usr/bin/env sh

export method="genFiducial"
export model="heavyhiggs"
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"
export SignalNormFile="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines_${method}.txt"
export massInterval=10
# masslist={600,613,621,629,637,645,653,662,670,679,687,696,705,714,723,732,741,751,760,770,779,789,799,809,820,830,840,851,862,872,883,894,906,917,929,940,952,964,976,988,1001,1013,1026,1038,1051,1064,1078,1091,1105,1119,1132,1147,1161,1175,1190,1205,1219,1235,1250,1265,1281,1297,1313,1329,1346,1362,1379,1396,1413,1431,1449,1466,1485,1503,1521,1540,1559,1578,1598,1617,1637,1657,1678,1698,1719,1740,1762,1783,1805,1827,1850,1873,1895,1919,1942,1966,1990,2014,2039,2064,2089,2115,2141,2167,2193,2220,2247,2275,2303,2331,2359,2388,2417,2447,2477,2507,2537,2568,2600,2631,2663,2696,2729,2762,2795,2830,2864,2899,2934,2970,3006,3042,3079,3117,3155,3193,3232,3271,3311,3351,3392,3433,3475,3517,3560,3603,3647,3691,3736,3781,3827,3873,3920,3968,4016,4065,4114,4164,4214,4265,4317,4369,4422,4476,4530,4585,4640,4696,4753,4811,4869,4928,4987,5048,5109,5171,5233,5296,5360,5425,5491,5557,5624,5692,5761,5831,5901,5973,6045,6118,6192,6267,6342,6419,6496,6575,6654,6734,6816,6898,6981,7000}

##########################
########## 2016 ##########
##########################
export year=2016
export lumi=35.9
for coup in {"0p014","1p4","5p6"}; do
    for cat in {"EBEB","EBEE"}; do
        for mass in `seq 500 ${massInterval} 5000`; do
            for fitmethod in {"dijet","expow1","invpow1","invpowlin1","envelope"}; do
                mkdir -p output/envelope/${year}/${coup}/${cat}
                time python python/RunDiphotonCombine.py -c config/diphotons_bias_${year}.config -i bkgAltModels/${fitmethod}/blind/FitResults_DiPhotons_${coup}_${cat}_${year}.root -b DiPhotons_${coup}_${cat} --mass ${mass} -m gg -d output/envelope/${year}/${model}/${coup}/${cat} -r 1 --rMin -3 --rMax 3 -l ${lumi} --year ${year} --fit-pdf ${fitmethod} --SigNorm $SigNormFile --method ${method}
            done
        done
    done
done
##########################
########## 2017 ##########
##########################
export year=2017
export lumi=41.527
for coup in {"0p014","1p4","5p6"}; do
    for cat in {"EBEB","EBEE"}; do
        for mass in `seq 500 ${massInterval} 5000`; do
            for fitmethod in {"dijet","expow1","invpow1","invpowlin1","envelope"}; do
                mkdir -p output/envelope/${year}/${coup}/${cat}
                time python python/RunDiphotonCombine.py -c config/diphotons_bias_${year}.config -i bkgAltModels/${fitmethod}/blind/FitResults_DiPhotons_${coup}_${cat}_${year}.root -b DiPhotons_${coup}_${cat} --mass ${mass} -m gg -d output/envelope/${year}/${model}/${coup}/${cat} -r 1 --rMin -3 --rMax 3 -l ${lumi} --year ${year} --fit-pdf ${fitmethod} --SigNorm $SigNormFile --method ${method}
            done
        done
    done
done
##########################
########## 2018 ##########
##########################
export year=2018
export lumi=59.670
for coup in {"0p014","1p4","5p6"}; do
    for cat in {"EBEB","EBEE"}; do
        for mass in `seq 500 ${massInterval} 5000`; do
            for fitmethod in {"dijet","expow1","invpow1","invpowlin1","envelope"}; do
                mkdir -p output/envelope/${year}/${coup}/${cat}
                time python python/RunDiphotonCombine.py -c config/diphotons_bias_${year}.config -i bkgAltModels/${fitmethod}/blind/FitResults_DiPhotons_${coup}_${cat}_${year}.root -b DiPhotons_${coup}_${cat} --mass ${mass} -m gg -d output/envelope/${year}/${model}/${coup}/${cat} -r 1 --rMin -3 --rMax 3 -l ${lumi} --year ${year} --fit-pdf ${fitmethod} --SigNorm $SigNormFile --method ${method}
            done
        done
    done
done
