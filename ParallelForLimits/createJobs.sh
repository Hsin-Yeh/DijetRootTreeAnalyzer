#!/bin/bash

########## Config ##########
runMethod=$1 # create/send/merge
signame="heavyhiggs" # grav/heavyhiggs
version="2024-03-17"
versionDir="${version}_${signame}"
masslist=($(seq 600 10 5000))
# couplist=(4550)
# masslist=(1300)
couplist=(14 361 707 1054 1400 2450 3500 4550 5600)
############################

########## CreateJobs ##########
if [[ ${runMethod} == "create" ]]; then
        mkdir ${versionDir}
        cd ${versionDir}

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
                        transferFile="finalResults_${signame}_${coupling}_${mass}.txt"
                        outDir="${jobDir}/output/"


                        echo '+JobFlavour = "tomorrow" ' > ${submitFile}
                        echo ' ' >> ${submitFile}
                        echo "executable  = /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/ParallelForLimits/setupCombine.sh" >> ${submitFile}
                        echo "arguments   = "'$(ClusterID) $(ProcId)'" ${outDir} ${coupling} ${mass} ${signame} " >> ${submitFile}
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

########## SendJobs ##########
elif [[ ${runMethod} == "send" ]]; then
        cd ${versionDir}

        echo "==========Sending Jobs=========="
        for coupling in "${couplist[@]}"; do
                echo ${coupling}
                for mass in "${masslist[@]}"; do
                        jobDir="${coupling}/${mass}"
                        submitFile="${jobDir}/jobs/limit_${coupling}_${mass}.sub"
                        #echo ${run}
                        chmod 755 ${submitFile}

                        echo "Sending ${submitFile}"
                        condor_submit ${submitFile}
                        # echo "condor_submit ${submitFile}"
                done
        done

########## Check output status ##########
elif [[ ${runMethod} == "status" ]]; then
        cd ${versionDir}
        rm status.txt
        touch status.txt

        echo "==========Checking output status=========="
        for coupling in "${couplist[@]}"; do
                echo ${coupling}
                for mass in "${masslist[@]}"; do
                        resultfile="finalResults_heavyhiggs_${coupling}_${mass}.txt"
                        if [ ! -f ${resultfile} ]; then
                                echo "${resultfile} does no exist" >> status.txt
                        elif [ -f ${resultfile} -a ! -s $resultfile ]; then
                                echo "${resultfile} is empty" >> status.txt
                        elif [ -f ${resultfile} -a -s $resultfile ]; then
                                echo "${resultfile} finished" >> status.txt
                        fi
                done
        done

########## ResendJobs if output file size is 0 ##########
elif [[ ${runMethod} == "resend" ]]; then
        cd ${versionDir}

        echo "==========Resending Jobs=========="
        for coupling in "${couplist[@]}"; do
                echo ${coupling}
                for mass in "${masslist[@]}"; do
                        resultfile="finalResults_heavyhiggs_${coupling}_${mass}.txt"
                        if [ ! -f ${resultfile} ]; then
                                echo "${resultfile} does no exist"
                        elif [ -f ${resultfile} -a ! -s $resultfile ]; then
                                echo "${resultfile} is empty"
                                jobDir="${coupling}/${mass}"
                                submitFile="${jobDir}/jobs/limit_${coupling}_${mass}.sub"
                                #echo ${run}
                                chmod 755 ${submitFile}

                                echo "Resending ${submitFile}"
                                condor_submit ${submitFile}
                                # echo "condor_submit ${submitFile}"
                        fi
                done
        done


########## MergeJobs ##########
elif [[ ${runMethod} == "merge" ]]; then
        cd ${versionDir}
        mkdir results
        mv final*.txt results
        # for coupling in "${couplist[@]}"; do
        #         echo ${coupling}
        #         mkdir -p ${versionDir}/results/${signame}/${coupling}
        #         for mass in "${masslist[@]}"; do
        #                 mv ${versionDir}/finalResults_${signame}_${coupling}_${mass}.txt ${versionDir}/results/${signame}/${coupling}
        #         done

        # done
fi
