#!/bin/tcsh

#setenv combmode "samefunfit"
# setenv combmode "diffunfit"
setenv combmode "MultiDimFit"

setenv nominalmodel "dijet"

setenv models "dijet expow1 invpow1 invpowlin1 envelope"

setenv insignames "grav heavyhiggs"

setenv cats "EBEB EBEE"

# Years
# setenv years "2016 2017 2018"
setenv years 2016

setenv musinjected `seq 1 1`
#setenv musinjected `seq 1 5`
# setenv musinjected "0.1 1 2"

# Year first
foreach year ($years)
echo "------------------------"
echo "Year ${year}"

setenv lumi "35.9"
if (${year} == "2017") then
setenv lumi "41.527"
else if (${year} == "2018") then
setenv lumi "59.670"
endif

foreach insigname ($insignames)
echo "------------------------"
echo "insigname ${insigname}"

setenv couplings "0p014 1p4 5p6"
if (${insigname} == "grav") then
setenv couplings "kMpl001 kMpl01 kMpl02"
endif

setenv method "full"
if (${insigname} == "heavyhiggs") then
setenv method "genFiducial"
endif

# Coupling now
foreach coup ($couplings)
echo "------------------------"
echo "Coupling ${coup}"

setenv masses "500 600 700 800 900 1000 1100 1200 1500 1800 2100 2400 2700 3000 3500 4000 4500 5000 5500 6000 6500 7000"
if ($coup == "kMpl001" || $coup == "0p014" || $coup == "1p4" || $coup == "5p6") then
setenv masses "500 600 700 800 900 1000 1100 1200 1500 1800 2100 2400 2700 3000 3500 4000 4500 5000"
endif

# Cat now
foreach cat ($cats)
echo "------------------------"
echo "Cat ${cat}"

#mus injected
foreach muin ($musinjected)
echo "------------------------"
echo "Muin ${muin}"

# Starting the loop through all models
foreach model ($models)
echo "===================================================================================="
echo "Model $model"

#masses
foreach mass ($masses)
echo "------------------------"
echo "Mass ${mass}"

#setenv workpath "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/ParallelForCombine/${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/jobs"
setenv workpath "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/ParallelForCombine/${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/jobs"

setenv runumberslist ` ls ${workpath} | grep .sub `

foreach run  ($runumberslist)

#echo ${run}
chmod 755 ${workpath}/${run}

echo "Sending ${run}"
#bsub -q 8nh -o /tmp/junk ${workpath}/${run}
condor_submit ${workpath}/${run}
echo "condor_submit ${workpath}/${run}"
#bsub -q 8nh -o ${workpath}/../logs/${run}.txt ${workpath}/${run}
#echo "bsub -q 8nh -o /tmp/junk ${workpath}/${run}"

end

end 

end

end 

end

end

end

end
