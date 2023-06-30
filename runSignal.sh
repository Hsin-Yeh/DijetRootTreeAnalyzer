#!/usr/bin/env sh

#!/usr/bin/env sh


#################### Constants ##########EEEEEEEEEE
# Cats
export yearlist=("2016" "2017" "2018")
export catlist=("EBEB" "EBEE")
# method
export syslist=("energyScaleStatUp" "energyScaleSystUp" "energyScaleGainUp" "energySigmaUp" "energyScaleStatDown" "energyScaleSystDown" "energyScaleGainDown" "energySigmaDown" "SFUp" "SFDown" "PuUp" "PuDown" "EEPFUp" "EEPFDown")

export couplist_grav=("kMpl001" "kMpl01" "kMpl02")
export method_grav="full"
export signal_grav="grav"
export signal_LongName_grav="RSGravitonToGammaGamma"
export InterpolateShapePath_grav="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method_grav}"

export couplist_hh=("0p014" "1p4" "5p6")
export method_hh="genFiducial"
export signal_hh="heavyhiggs"
export signal_LongName_hh="GluGluSpin0ToGammaGamma_W"
export InterpolateShapePath_hh="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method_hh}"

export massInterval=1

export trees="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees"
export output="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output"
cmsenv

########## Prepare trees ##########

# cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis
# for coup in {"kMpl001","kMpl01","kMpl02"}; do
#    for year in {"2016","2017","2018"}; do
#        prepareTrees.exe grav BB ${year} ${coup} "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input"
#    done
# done
# for coup in {"0p014","1p4","5p6"}; do
#    for year in {"2016","2017","2018"}; do
#        prepareTrees.exe heavyhiggs BB ${year} ${coup} "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input"
#    done
# done
# mv input/RS*.root input/trees
# mv input/Glu*.root input/trees

########## Add Samples ##########

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/
mkdir -p output/plots
mkdir -p output/${method_grav}
mkdir -p output/${method_hh}

#RS
for year in "${yearlist[@]}"; do
    echo ${year}
    for cat in "${catlist[@]}"; do
        echo ${cat}
        ## Grav ##
        for coup in "${couplist_grav[@]}"; do
            echo ${coup}
            files_RS=`ls ${trees}/RSGravitonToGammaGamma_${coup}*${year}*.root`
            python python/AddSignalShapes.py -e ${method_grav} -t nom -d output/${method_grav} -c ${cat} ${files_RS};
            for syst in "${syslist[@]}" ; do
                echo ${syst};
                python python/AddSignalShapes.py -e ${method_grav} -t systematics -s ${syst} -d output/${method_grav} -c ${cat} ${files_RS};
            done
        done
        ## Heavyhiggs ##
        for coup in "${couplist_hh[@]}"; do
            echo ${coup}
            files_GluGlu=`ls ${trees}/GluGluSpin0ToGammaGamma_W_${coup}*${year}*.root`
            python python/AddSignalShapes.py -e ${method_hh} -t nom -d output/${method_hh} -c ${cat} ${files_GluGlu};
            for syst in "${syslist[@]}" ; do
                echo ${syst};
                python python/AddSignalShapes.py -e ${method_hh} -t systematics -s ${syst} -d output/${method_hh} -c ${cat} ${files_GluGlu};
            done
        done

    done
done

# year=2017
# coup="kMpl02"
# files_RS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/RSGravitonToGammaGamma_${coup}*${year}*.root`; python python/AddSignalShapes.py -e ${method} -t nom -d output/${method} -c EBEB ${files_RS}; python python/AddSignalShapes.py -e ${method} -t nom -d output/${method} -c EBEE ${files_RS};
# for year in { 2017 }; do echo $year; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; files_RS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/RSGravitonToGammaGamma_${coup}*${year}*.root`; for syst in {"energyScaleStatUp","energyScaleSystUp","energyScaleGainUp","energySigmaUp","energyScaleStatDown","energyScaleSystDown","energyScaleGainDown","energySigmaDown","SFScaleUp","SFScaleDown","PUScaleUp","PUScaleDown"}; do echo ${syst}; python python/AddSignalShapes.py -e ${method} -t systematics -s ${syst} -d output/${method} -c EBEB ${files_RS}; python python/AddSignalShapes.py -e ${method} -t systematics -s ${syst} -d output/${method} -c EBEE ${files_RS}; done; done; done;


# export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/"
# cd $mainpath
# #With the createJson option the insigname argument is dull and the code will run through all signals.
# #2016 (Both RS and heavy higgs)
# signalNorm.exe 2016 createJson "${mainpath}/output/2016/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2016/signalNorm" "grav" ${method}
# #2017 (Both RS and heavy higgs)
# signalNorm.exe 2017 createJson "${mainpath}/output/2017/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2017/signalNorm" "grav" ${method}
# #2018 (Both RS and heavy higgs)
# signalNorm.exe 2018 createJson "${mainpath}/output/2018/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2018/signalNorm" "grav" ${method}
# #2016 (Both RS and heavy higgs)
# rm SignalNorm_${method}.txt
# rm SignalNorm_Splines_${method}.txt
# #2016 RS
# signalNorm.exe 2016 readJson "${mainpath}/output/2016/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2016/signalNorm" "grav" "${method}"
# #2017 RS
# signalNorm.exe 2017 readJson "${mainpath}/output/2017/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2017/signalNorm" "grav" "${method}"
# #2018 RS
# signalNorm.exe 2018 readJson "${mainpath}/output/2018/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2018/signalNorm" "grav" "${method}"
# #2016 Heavy Higgs
# signalNorm.exe 2016 readJson "${mainpath}/output/2016/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2016/signalNorm" "heavyhiggs" "${method}"
# #2017 Heavy Higgs
# signalNorm.exe 2017 readJson "${mainpath}/output/2017/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2017/signalNorm" "heavyhiggs" "${method}"
# #2018 Heavy Higgs
# signalNorm.exe 2018 readJson "${mainpath}/output/2018/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2018/signalNorm" "heavyhiggs" "${method}"

# cp SignalNorm.txt SignalNorm_${method}.txt
# cp SignalNorm_Splines.txt SignalNorm_Splines_${method}.txt
# dateDir=$(date +"%Y%m%d_%H%M%S")
# for year in {"2016","2017","2018"};
# do
#     cpwww output/${year}/signalNorm ~/www/diphoton-analysis/${year}/signalNorm/${method}/${dateDir}
# done


############################################################
# Extract shapes
############################################################

mkdir ${InterpolateShapePath_grav}
cd ${InterpolateShapePath_grav}
rm -rf inputs InputShapes.root
mkdir inputs
filesToExtract_grav=`ls ${output}/${method} |grep .root | grep RSG `
for file in ${filesToExtract_grav}; do
    echo ${file};
    cp ${output}/${method_grav}/${file} .;
    filename=`echo ${file} | cut -d'.' -f 1`;
    rm -rf inputs/${filename}.py;
    ../extractShapes.py -i ${file} > inputs/${filename}.py;
done;

mkdir ${InterpolateShapePath_hh}
cd ${InterpolateShapePath_hh}
rm -rf inputs InputShapes.root
mkdir inputs
filesToExtract_hh=`ls ${output}/${method} |grep .root | grep GluGlu `
for file in ${filesToExtract_hh}; do
    echo ${file};
    cp ${output}/${method_hh}/${file} .;
    filename=`echo ${file} | cut -d'.' -f 1`;
    rm -rf inputs/${filename}.py;
    ../extractShapes.py -i ${file} > inputs/${filename}.py;
done;

# ############################################################
# # Get Resonance shapes
# ############################################################

cd ${InterpolateShapePath_grav}
filesToExtract_grav=`ls ${output}/${method} |grep .root | grep RSG `
rm ResonanceShapes*.root
for file in ${filesToExtract_grav}; do
    echo ${file}
    coup=`echo ${file} | cut -d'_' -f 3`
    echo $coup
    filename=`echo ${file} | cut -d'.' -f 1`
    ../getResonanceShapes.py -i inputs/${filename}.py -c ${coup} -f gg --massrange 600 7000 1 -o ResonanceShapes_${filename}.root;
done;

cd ${InterpolateShapePath_grav}
filesToExtract_hh=`ls ${output}/${method} |grep .root | grep GluGlu `
rm ResonanceShapes*.root
for file in ${filesToExtract_hh}; do
    echo ${file};
    coup=`echo ${file} | cut -d'_' -f 4`;
    echo $coup;
    filename=`echo ${file} | cut -d'.' -f 1`;
    ../getResonanceShapes.py -i inputs/${filename}.py -c ${coup} -f gg --massrange 600 5000 1 -o ResonanceShapes_${filename}.root;
done;


# ############################################################
# # Compare shapes - Closure Test - single plot comparison
# ############################################################

# cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/
# cmsenv
# mkdir output/plots

# for year in {2016,2017,2018}; do echo $year; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; files_RS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/RSGravitonToGammaGamma_${coup}*${year}*.root`; python python/CompareShapes.py -e ${method} -d output -c EBEB -w ${coup} ${files_RS}; python python/CompareShapes.py -e ${method} -d output -c EBEE -w ${coup} ${files_RS}; done; done;

# # ############################################################
# # # Compare shapes - Closure Test - multi plot comparison
# # ############################################################

# cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/
# cmsenv

# for year in {2016,2017,2018}; do echo $year; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; files_Selection_RS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/RSGravitonToGammaGamma_${coup}*${year}*.root`; python python/CompareShapes.py -e ${method} -d output -c EBEB -m -w ${coup} ${files_Selection_RS}; python python/CompareShapes.py -e ${method} -d output -c EBEE -m -w ${coup} ${files_Selection_RS}; done; done;

# dateDir=$(date +"%Y%m%d_%H%M%S")
# cpwww output/plots ~/www/diphoton-analysis/SignalShapeInterpolation/${method}/${dateDir}
