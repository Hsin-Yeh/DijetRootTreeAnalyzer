#!/bin/tcsh

#setenv combmode "samefunfit" 
setenv combmode "diffunfit" 

setenv nominalmodel "dijet"

setenv models "dijet expow1 invpow1 invpowlin1"

#setenv masses `seq 600 100 5000`
setenv masses "600 700 800 900 1000 1100 1200 1500 1800 2100 2400 2700 3000 3500 4000 4500 5000 5500 6000" 

#setenv couplings "kMpl001 kMpl01 kMpl02 0p014 1p4 5p6"
setenv couplings "kMpl001 kMpl01 kMpl02"
#setenv couplings "0p014 1p4 5p6"

setenv cats "EBEB EBEE"

#I will change it one at a time
setenv insigname "grav"

# Years 
setenv years "2016"
setenv lumi "35.9"
#setenv lumi "41.527"
#setenv lumi "59.670"

setenv musinjected `seq 1 1`
#setenv musinjected "5 10 15"
#setenv musinjected `seq 1 3`
#setenv musinjected `seq 1 1`
setenv ntoys 1000
setenv theseed 397

#This is for the number of jobs per clusterid
set jobsperclusterchoice=10

setenv PWD `pwd`

# Year first
foreach year ($years)
echo "------------------------"
echo "Year ${year}"

# in/out
setenv inoutpath "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/output/${year}/combine_bias/${insigname}/${combmode}"

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

#Create local structure for the output
rm -rf ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/output ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/jobs ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/logs
mkdir -p ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/output ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/jobs ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/logs
chmod 755 -R ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/output ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/jobs ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/logs

#Output of the job will be here
rm -rf ${inoutpath}/${coup}/${cat}/mu${muin}/${model}/mass${mass}
mkdir -p ${inoutpath}/${coup}/${cat}/mu${muin}/${model}/mass${mass}

#foreach batch (`seq 0 100`)
foreach batch (`seq 0 0`)

echo '+JobFlavour = "tomorrow" ' > bias_$batch.sub
#echo '+JobFlavour = "microcentury" ' > bias_$batch.sub
echo ' ' >> bias_$batch.sub
echo "executable  = ${PWD}/setupCombineBias.sh" >> bias_$batch.sub
#echo "arguments   = "'$(ClusterID) $(ProcId)'" ${ncut} ${thick} ${file} ${thicknum} " >> bias_${file}.sub
echo "arguments   = "'$(ClusterID) $(ProcId)'" ${inoutpath} ${model} ${ntoys} ${coup} ${insigname} ${theseed} ${year} ${muin} ${mass} ${combmode} ${nominalmodel} ${cat} ${lumi} "'$(infile)'" " >> bias_$batch.sub
echo "output      = ${PWD}/${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/logs/bias_"'$(infile)'".out " >> bias_$batch.sub
echo "error       = ${PWD}/${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/logs/bias_"'$(infile)'".err " >> bias_$batch.sub
echo "log         = ${PWD}/${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/logs/bias_"'$(infile)'"_htc.log " >> bias_$batch.sub
#echo "output      = ${PWD}/${year}/${insigname}/${combmode}/${coup}/bias_"'$(infile)'".out " >> bias_$batch.sub
#echo "error       = ${PWD}/${year}/${insigname}/${combmode}/${coup}/bias_"'$(infile)'".err " >> bias_$batch.sub
#echo "log         = ${PWD}/${year}/${insigname}/${combmode}/${coup}/bias_"'$(infile)'"_htc.log " >> bias_$batch.sub

#echo 'requirements = (OpSysAndVer =?= "CentOS7") ' >> bias_${batch}.sub
echo 'max_retries = 1' >> bias_$batch.sub

rm voodoo
touch voodoo
foreach jobspercluster (`seq 1 1`)
#foreach jobspercluster (`seq 1 3`)
#foreach jobspercluster (`seq 1 20`)
set num=`expr ${batch} \* 10  + ${jobspercluster} `
echo -n "${num} " >> voodoo
end

setenv batchfilelist `cat voodoo`
echo "queue infile in (${batchfilelist}) " >> bias_$batch.sub

mv bias_$batch.sub ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/jobs/bias_$batch.sub
chmod 755 ${year}/${insigname}/${combmode}/${coup}/${cat}/mu${muin}/${model}/mass${mass}/jobs/bias_$batch.sub

echo bias_$batch.sub

end 

end

end

end

end 

end

end










