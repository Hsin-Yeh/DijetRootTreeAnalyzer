#!/bin/bash

version="2023-11-05"
mkdir ${version}
cd ${version}

# couplist=(4550)
# masslist=(1300)
# couplist=(14 361 707 1054 1400 2450 3500 4550 5600)
couplist=(14 1400 5600)
masslist=($(seq 600 10 2000))


echo "==========Creating jobs=========="
for coupling in "${couplist[@]}"; do
    echo ${coupling}
    for mass in "${masslist[@]}"; do
        jobDir="${coupling}/${mass}"
        #Create local structure for jobs
        rm -rf ${jobDir}/output ${jobDir}/jobs ${jobDir}/logs
        mkdir -p ${jobDir}/output ${jobDir}/jobs ${jobDir}/logs
        chmod 755 -R ${jobDir}/output ${jobDir}/jobs ${jobDir}/logs

        submitFile="${jobDir}/jobs/limit_${coupling}_${mass}.sub"
        transferFile="finalResults_grav_${coupling}_${mass}.txt"
        outDir="${jobDir}/output/"


        echo '+JobFlavour = "tomorrow" ' > ${submitFile}
        echo ' ' >> ${submitFile}
        echo "executable  = /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/ParallelForLimits/setupCombine.sh" >> ${submitFile}
        echo "arguments   = "'$(ClusterID) $(ProcId)'" ${outDir} ${coupling} ${mass} " >> ${submitFile}
        echo "output      = ${PWD}/${jobDir}/logs/limit_${coupling}_${mass}.out " >> ${submitFile}
        echo "error       = ${PWD}/${jobDir}/logs/limit_${coupling}_${mass}.err " >> ${submitFile}
        echo "log         = ${PWD}/${jobDir}/logs/limit_${coupling}_${mass}_htc.log " >> ${submitFile}
        echo "transfer_output_files   = ${transferFile} " >> ${submitFile}
        echo 'requirements = (OpSysAndVer =?= "CentOS7") ' >> ${submitFile}
        echo 'max_retries = 1' >> ${submitFile}
        echo "queue 1 " >> ${submitFile}

        chmod 755 ${submitFile}

    done
done
