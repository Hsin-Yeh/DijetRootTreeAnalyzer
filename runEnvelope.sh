#!/usr/bin/env sh

mass=1000
coup="kMpl01"
cat="EBEB"
year=2016
cardDir="./datacards/multi/full/${year}/DiPhotons_${coup}_${cat}_${year}/"
cardName=${cardDir}/diphoton_combine_${mass}_DiPhotons_${coup}_${cat}_${year}.txt
echo ${cardName}

combine -M MultiDimFit -d ${cardName} --algo grid --setParameterRanges r=-1,3 --cminDefaultMinimizerStrategy 0 --saveNLL -n Envelope -m ${mass} --setParameters myIndex=-1 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --X-rtd MINIMIZER_freezeDisassociatedParams
combine -M MultiDimFit -d ${cardName} --algo grid --setParameterRanges r=-1,3 --cminDefaultMinimizerStrategy 0 --saveNLL --freezeParameters pdf_index_${cat}_${year} --setParameters pdf_index_${cat}_${year}=0 -n fixed_pdf_0 -m ${mass} --X-rtd REMOVE_CONSTANT_ZERO_POINT=1
combine -M MultiDimFit -d ${cardName} --algo grid --setParameterRanges r=-1,3 --cminDefaultMinimizerStrategy 0 --saveNLL --freezeParameters pdf_index_${cat}_${year} --setParameters pdf_index_${cat}_${year}=1 -n fixed_pdf_1 -m ${mass} --X-rtd REMOVE_CONSTANT_ZERO_POINT=1
combine -M MultiDimFit -d ${cardName} --algo grid --setParameterRanges r=-1,3 --cminDefaultMinimizerStrategy 0 --saveNLL --freezeParameters pdf_index_${cat}_${year} --setParameters pdf_index_${cat}_${year}=2 -n fixed_pdf_2 -m ${mass} --X-rtd REMOVE_CONSTANT_ZERO_POINT=1

python plotNLL.py higgs*fix*.root higgs*Envelope*.root --mass ${mass} --coup ${coup} --cat ${cat} --year ${year}
