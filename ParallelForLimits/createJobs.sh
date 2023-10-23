#!/bin/bash

version="2023-10-23"
# couplist=(4550)
# masslist=(1300)
couplist=(14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600)
masslist=($(seq 600 10 5000))

cd ${version}

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


        echo '+JobFlavour = "longlunch" ' > ${submitFile}
        echo ' ' >> ${submitFile}
        echo "executable  = ${PWD}/setupCombine.sh" >> ${submitFile}
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
