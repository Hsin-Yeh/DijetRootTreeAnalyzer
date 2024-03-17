#!/bin/bash

########## Config ##########
runMethod=$1 # create/send/merge/status/resend
signame="heavyhiggs" # grav/heavyhiggs
version="2024-03-17"
limitType="1D" # 2D
versionDir="${version}_${signame}_${limitType}"

if [[ ${limitType} == "1D" ]]; then
        couplist=(14 1400 5600)
        masslist=(600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200 2300 2400 2500 2600 2700 2800 2900 3000 3100 3200 3300 3400 3500 3600 3700 3800 3900 4000 4100 4200 4300 4400 4500 4600 4700 4800 4900)
        if [[ ${coupling} == "1p4" ]]; then
                    masslist=(600 611 622 634 645 657 669 681 694 707 719 732 746 759 773 787 801 816 830 845 860 876 892 908 924 940 957 974 992 1009 1027 1046 1064 1083 1102 1122 1142 1162 1183 1204 1225 1247 1269 1291 1314 1337 1361 1385 1409 1434 1459 1485 1511 1537 1564 1592 1619 1648 1677 1706 1736 1766 1797 1828 1860 1893 1926 1959 1993 2028 2064 2099 2136 2173 2211 2249 2288 2328 2368 2410 2451 2494 2537 2581 2626 2671 2718 2765 2812 2861 2910 2961 3012 3064 3117 3171 3225 3281 3338 3395 3454 3513 3574 3636 3698 3762 3827 3893 3960 4028 4097 4167 4239 4312 4386 4462 4538 4616 4696 4776 4858 4942 5000)
        elif [[ ${coupling} == "5p6" ]]; then
                    masslist=(600 625 653 683 713 745 778 812 848 885 924 964 1005 1049 1094 1141 1190 1241 1293 1348 1405 1465 1527 1591 1658 1727 1800 1875 1953 2034 2119 2207 2298 2393 2492 2595 2702 2813 2929 3050 3175 3305 3440 3581 3728 3880 4038 4203 4374 4553 4738 4931 5000)
        fi

elif [[ ${limitType} == "2D" ]]; then
        couplist=(14 361 707 1054 1400 2450 3500 4550 5600)
        masslist=($(seq 600 10 5000))
fi

# couplist=(4550)
# masslist=(1300)
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

        finish_count=0
        empty_count=0
        nonexist_count=0

        echo "==========Checking output status=========="
        for coupling in "${couplist[@]}"; do
                echo ${coupling}
                for mass in "${masslist[@]}"; do
                        resultfile="finalResults_heavyhiggs_${coupling}_${mass}.txt"
                        if [ ! -f ${resultfile} ]; then
                                echo "${resultfile} does not exist" >> status.txt
                                nonexist_count=$((nonexist_count+1))
                        elif [ -f ${resultfile} -a ! -s $resultfile ]; then
                                echo "${resultfile} is empty" >> status.txt
                                empty_count=$((empty_count+1))
                        elif [ -f ${resultfile} -a -s $resultfile ]; then
                                echo "${resultfile} finished" >> status.txt
                                finish_count=$((finish_count+1))
                        fi
                done
        done
        echo "Finish: ${finish_count}, Empty: ${empty_count}, Nonexist: ${nonexist_count}"

########## ResendJobs if output file size is 0 ##########
elif [[ ${runMethod} == "resend" ]]; then
        cd ${versionDir}
        empty_count=0

        echo "==========Resending Jobs=========="
        for coupling in "${couplist[@]}"; do
                echo ${coupling}
                for mass in "${masslist[@]}"; do
                        resultfile="finalResults_heavyhiggs_${coupling}_${mass}.txt"
                        if [ ! -f ${resultfile} ]; then
                                echo "${resultfile} does no exist"
                        elif [ -f ${resultfile} -a ! -s $resultfile ]; then
                                empty_count=$((empty_count+1))
                                echo "${resultfile} is empty"
                                rm ${resultfile}
                                jobDir="${coupling}/${mass}"
                                submitFile="${jobDir}/jobs/limit_${coupling}_${mass}.sub"
                                #echo ${run}
                                chmod 755 ${submitFile}

                                echo "Resending ${submitFile}, ${empty_count} jobs resended"
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
