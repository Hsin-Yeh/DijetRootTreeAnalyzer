#!/bin/tcsh

#setenv combmode "samefunfit"
setenv combmode "diffunfit" 

setenv nominalmodel "dijet"

setenv models "dijet expow1 invpow1 invpowlin1"

#setenv masses `seq 600 100 5000`
setenv masses "600 700 800 900 1000 1100 1200 1500 1800 2100 2400 2700 3000 3500 4000 4500 5000 5500 6000"

# setenv couplings "kMpl001 kMpl01 kMpl02 0p014 1p4 5p6"
setenv couplings "kMpl001 kMpl01 kMpl02"
#setenv couplings "0p014 1p4 5p6"

setenv cats "EBEB EBEE"

#I will change it one at a time
setenv insigname "grav"

# Years 
setenv years "2017"
#setenv years "2018"

setenv musinjected `seq 1 1`
#setenv musinjected `seq 1 5`

# Year first
foreach year ($years)
echo "------------------------"
echo "Year ${year}"

# Coupling now
foreach coup ($couplings)
echo "------------------------"
echo "Coupling ${coup}"

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
setenv workpath "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/ParallelForBias/${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/jobs"

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
