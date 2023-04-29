#!/bin/tcsh

#setenv combmode "samefunfit" 
setenv combmode "diffunfit"

setenv nominalmodel "dijet"

setenv models "dijet expow1 invpow1 invpowlin1"

setenv insignames "grav heavyhiggs"

setenv cats "EBEB EBEE"

# Years
setenv years "2016 2017 2018"

# setenv musinjected `seq 1 1`
#setenv musinjected "5 10 15"
#setenv musinjected `seq 1 3`
#setenv musinjected `seq 1 1`
setenv musinjected "0.1 1 2"
setenv ntoys 1000
setenv theseed 397

#This is for the number of jobs per clusterid
set jobsperclusterchoice=10

setenv PWD `pwd`

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

# This is for the output files
setenv inoutpath "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/output/${year}/combine_bias/${insigname}/${combmode}"

# Coupling now
foreach coup ($couplings)
echo "------------------------"
echo "Coupling ${coup}"

setenv masses "800 900 1000 1100 1200 1500 1800 2100 2400 2700 3000 3500 4000 4500 5000 5500 6000 6500 7000"
if ($coup == "kMpl001" || $coup == "0p014" || $coup == "1p4" || $coup == "5p6") then
setenv masses "800 900 1000 1100 1200 1500 1800 2100 2400 2700 3000 3500 4000 4500 5000"
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

#Create local structure for the bias.sub files, they will be moved here
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

end
