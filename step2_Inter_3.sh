#!/bin/bash

python python/bTag_extractShapes_Interpolater_scan_2018_Inter_up.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b
python python/ReScaleInterpolation_2018_Inter_UD.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2018_Inter_central.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b
python python/ReScaleInterpolation_2018_Inter.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2018_Inter_down.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b
python python/ReScaleInterpolation_2018_Inter_UD.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2016_Inter_up.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b
python python/ReScaleInterpolation_2016_Inter_UD.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2016_Inter_central.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b
python python/ReScaleInterpolation_2016_Inter.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2016_Inter_down.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b
python python/ReScaleInterpolation_2016_Inter_UD.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2017_Inter_up.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b
python python/ReScaleInterpolation_2017_Inter_UD.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2017_Inter_central.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b
python python/ReScaleInterpolation_2017_Inter.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2017_Inter_down.py -m  DMgq0p25 -e signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b -c le1b
python python/extract.py -m  DMgq0p25  -i signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b
python python/ReScaleInterpolation_2017_Inter_UD.py  -m  DMgq0p25  -F signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2018_Inter_up.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b
python python/ReScaleInterpolation_2018_Inter_UD.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2018_Inter_central.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b
python python/ReScaleInterpolation_2018_Inter.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2018_Inter_down.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b
python python/ReScaleInterpolation_2018_Inter_UD.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2016_Inter_up.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b
python python/ReScaleInterpolation_2016_Inter_UD.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2016_Inter_central.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b
python python/ReScaleInterpolation_2016_Inter.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2016_Inter_down.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b
python python/ReScaleInterpolation_2016_Inter_UD.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2017_Inter_up.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b
python python/ReScaleInterpolation_2017_Inter_UD.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2017_Inter_central.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b
python python/ReScaleInterpolation_2017_Inter.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b -c le1b

python python/bTag_extractShapes_Interpolater_scan_2017_Inter_down.py -m  DMgq0p2 -e signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b -c le1b
python python/extract.py -m  DMgq0p2  -i signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b
python python/ReScaleInterpolation_2017_Inter_UD.py  -m  DMgq0p2  -F signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b -c le1b

