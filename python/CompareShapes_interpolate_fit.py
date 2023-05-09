#!/usr/bin/env python
# python python/CompareShapes_interpolate_fit.py --cat EBEB --coup kMpl001 --mass 650 --year 2017 --outdir ./ --ws ../../output/2017/FinalParametricShape/workspaces --method full

from optparse import OptionParser
import ROOT
from ROOT import gROOT, gStyle, TH1D, TH1F
import rootTools
from framework import Config
from array import *
import os
import sys
import CMS_lumi, tdrstyle

######## global variables and style settings ########
gROOT.SetBatch(True);
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
'''
gStyle.SetTitleFont(42, "XYZ")
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelFont(42, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetCanvasBorderMode(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetCanvasColor(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadBottomMargin(0.15)
ROOT.TGaxis.SetMaxDigits(3)
gROOT.ForceStyle()
gROOT.Reset()
#tdrstyle.setTDRStyle()
#gROOT.SetStyle('tdrStyle')
#gROOT.ForceStyle()
'''
#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.cmsTextSize = 0.57
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = "(13 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
CMS_lumi.lumiTextSize = 0.6

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600;
W_ref = 850;
W = W_ref
H  = H_ref

iPeriod = 0


# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.08*W_ref
R = 0.04*W_ref

def color(i):
    if i == 0: return 633
    elif i == 1: return 800
    elif i == 2: return 209
    elif i == 3: return 862
    elif i == 4: return 2
    elif i == 5: return 4
    elif i == 6: return 5
    elif i == 7: return 6

    else: return 0

def project(tree, h, var, cut):
    print 'projecting var: %s, cut: %s from tree: %s into hist: %s'%(var, cut, tree.GetName(), h.GetName())
    tree.Project(h.GetName(),var,cut)

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('--cat',    dest="cat",    default="EBEB",    type="string", help="category")
    parser.add_option('--coup',   dest="coup",   default="kMpl001", type="string", help="coupling")
    parser.add_option('--mass',   dest="mass",   default="750",     type="int",    help="category")
    parser.add_option('--year',   dest="year",   default="2016",    type="int",    help="year")
    parser.add_option('--outdir', dest="outDir", default="./",      type="string", help="Output directory to store output histograms")
    parser.add_option('--ws',     dest="ws",     default="./",      type="string", help="input directory of parametric fit results")
    parser.add_option("--method", dest="method", default="full",    type="string", help="Choose between full range or truncate with the fwhm mass range")
    parser.add_option('--multi',  dest="multi",  default=False,     action="store_true", help="Make a single comparison plot or multi")
    (options,args) = parser.parse_args()

    histos = []
    histosRes = []
    histInterpolate = []
    year = ''

    M_bins = {
        "kMpl001" : [1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000],
        "kMpl01" : [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 8000],
        "kMpl02" : [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 8000],
        # "0p014": [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
        # "1p4": [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
        # "5p6": [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
        "0p014": [750, 1000],
        "1p4": [750, 1000],
        "5p6": [750, 1000]
    }

    binBoundaries = {}
    #EBEB
    binBoundaries["kMpl001"]= [500, 506, 513, 519, 526, 533, 540, 547, 554, 561, 568, 575, 583, 590, 598, 605, 613, 621, 629, 637, 645, 653, 662, 670, 679, 687, 696, 705, 714, 723, 732, 741, 751, 760, 770, 779, 789, 799, 809, 820, 830, 840, 851, 862, 872, 883, 894, 906, 917, 929, 940, 952, 964, 976, 988, 1001, 1013, 1026, 1038, 1051, 1064, 1078, 1091, 1105, 1119, 1132, 1147, 1161, 1175, 1190, 1205, 1219, 1235, 1250, 1265, 1281, 1297, 1313, 1329, 1346, 1362, 1379, 1396, 1413, 1431, 1449, 1466, 1485, 1503, 1521, 1540, 1559, 1578, 1598, 1617, 1637, 1657, 1678, 1698, 1719, 1740, 1762, 1783, 1805, 1827, 1850, 1873, 1895, 1919, 1942, 1966, 1990, 2014, 2039, 2064, 2089, 2115, 2141, 2167, 2193, 2220, 2247, 2275, 2303, 2331, 2359, 2388, 2417, 2447, 2477, 2507, 2537, 2568, 2600, 2631, 2663, 2696, 2729, 2762, 2795, 2830, 2864, 2899, 2934, 2970, 3006, 3042, 3079, 3117, 3155, 3193, 3232, 3271, 3311, 3351, 3392, 3433, 3475, 3517, 3560, 3603, 3647, 3691, 3736, 3781, 3827, 3873, 3920, 3968, 4016, 4065, 4114, 4164, 4214, 4265, 4317, 4369, 4422, 4476, 4530, 4585, 4640, 4696, 4753, 4811, 4869, 4928, 4987, 5048, 5109, 5171, 5233, 5296, 5360, 5425, 5491, 5557, 5624, 5692, 5761, 5831, 5901, 5973, 6045, 6118, 6192, 6267, 6342, 6419, 6496, 6575, 6654, 6734, 6816, 6898, 6981, 7066, 7151, 7237, 7325, 7413, 7502, 7593, 7684, 7777, 7871, 7966, 8062, 8159, 8258, 8357, 8458, 8560, 8663, 8768, 8873, 8980, 9089, 9198, 9309, 9421, 9535, 9650, 9766, 9884, 10003, 10123, 10245, 10369, 10494, 10620, 10748, 10877, 11008, 11141, 11275, 11411, 11548, 11687, 11828, 11971, 12115, 12261, 12408, 12558, 12709, 12862, 13017, 13173, 13332, 13492, 13655, 13819, 13985, 14000]
    binBoundaries["kMpl01"] = [500, 509, 518, 528, 538, 548, 558, 568, 579, 589, 600, 611, 622, 634, 645, 657, 669, 681, 694, 707, 719, 732, 746, 759, 773, 787, 801, 816, 830, 845, 860, 876, 892, 908, 924, 940, 957, 974, 992, 1009, 1027, 1046, 1064, 1083, 1102, 1122, 1142, 1162, 1183, 1204, 1225, 1247, 1269, 1291, 1314, 1337, 1361, 1385, 1409, 1434, 1459, 1485, 1511, 1537, 1564, 1592, 1619, 1648, 1677, 1706, 1736, 1766, 1797, 1828, 1860, 1893, 1926, 1959, 1993, 2028, 2064, 2099, 2136, 2173, 2211, 2249, 2288, 2328, 2368, 2410, 2451, 2494, 2537, 2581, 2626, 2671, 2718, 2765, 2812, 2861, 2910, 2961, 3012, 3064, 3117, 3171, 3225, 3281, 3338, 3395, 3454, 3513, 3574, 3636, 3698, 3762, 3827, 3893, 3960, 4028, 4097, 4167, 4239, 4312, 4386, 4462, 4538, 4616, 4696, 4776, 4858, 4942, 5027, 5113, 5201, 5290, 5381, 5473, 5567, 5662, 5759, 5858, 5958, 6061, 6164, 6270, 6377, 6487, 6598, 6711, 6826, 6943, 7061, 7182, 7305, 7430, 7557, 7687, 7818, 7952, 8088, 8226, 8367, 8510, 8656, 8804, 8954, 9107, 9263, 9421, 9582, 9746, 9912, 10082, 10254, 10429, 10607, 10788, 10972, 11160, 11350, 11544, 11741, 11942, 12146, 12353, 12564, 12778, 12996, 13218, 13443, 13673, 13906, 14000]
    binBoundaries["kMpl02"] = [500, 523, 547, 572, 598, 625, 653, 683, 713, 745, 778, 812, 848, 885, 924, 964, 1005, 1049, 1094, 1141, 1190, 1241, 1293, 1348, 1405, 1465, 1527, 1591, 1658, 1727, 1800, 1875, 1953, 2034, 2119, 2207, 2298, 2393, 2492, 2595, 2702, 2813, 2929, 3050, 3175, 3305, 3440, 3581, 3728, 3880, 4038, 4203, 4374, 4553, 4738, 4931, 5131, 5339, 5556, 5782, 6016, 6260, 6514, 6777, 7052, 7337, 7634, 7942, 8263, 8597, 8944, 9305, 9680, 10070, 10477, 10899, 11338, 11795, 12270, 12764, 13277, 13812, 14000]

    binBoundaries["0p014"] = binBoundaries["kMpl001"]
    binBoundaries["1p4"] = binBoundaries["kMpl01"]
    binBoundaries["5p6"] = binBoundaries["kMpl02"]
    # binBoundaries["0p014"] = [500, 506, 512, 518, 524, 530, 536, 542, 548, 554, 561, 568, 575, 582, 589, 596, 603, 610, 617, 624, 631, 638, 646, 654, 662, 670, 678, 686, 694, 702, 710, 718, 726, 735, 744, 753, 762, 771, 780, 789, 798, 807, 817, 827, 837, 847, 857, 867, 877, 887, 898, 909, 920, 931, 942, 953, 964, 975, 987, 999, 1011, 1023, 1035, 1047, 1059, 1072, 1085, 1098, 1111, 1124, 1137, 1151, 1165, 1179, 1193, 1207, 1221, 1236, 1251, 1266, 1281, 1296, 1311, 1327, 1343, 1359, 1375, 1391, 1408, 1425, 1442, 1459, 1476, 1494, 1512, 1530, 1548, 1566, 1585, 1604, 1623, 1642, 1662, 1682, 1702, 1722, 1743, 1764, 1785, 1806, 1828, 1850, 1872, 1894, 1917, 1940, 1963, 1986, 2010, 2034, 2058, 2083, 2108, 2133, 2158, 2184, 2210, 2236, 2263, 2290, 2317, 2345, 2373, 2401, 2430, 2459, 2488, 2518, 2548, 2578, 2609, 2640, 2672, 2704, 2736, 2769, 2802, 2835, 2869, 2903, 2938, 2973, 3009, 3045, 3081, 3118, 3155, 3193, 3231, 3270, 3309, 3349, 3389, 3430, 3471, 3513, 3555, 3598, 3641, 3685, 3729, 3774, 3819, 3865, 3911, 3958, 4005, 4053, 4101, 4150, 4200, 4250, 4301, 4352, 4404, 4457, 4510, 4564, 4619, 4674, 4730, 4787, 4844, 4902, 4961, 5020, 5080, 5141, 5203, 5265, 5328, 5392, 5457, 5522, 5588, 5655, 5723, 5792, 5861, 5931, 6002, 6074, 6147, 6221, 6296, 6371, 6447, 6524, 6602, 6681, 6761, 6842, 6924, 7007, 7091, 7176, 7262, 7349, 7437, 7526, 7616, 7707, 7799, 7892, 7987, 8083, 8180, 8278, 8377, 8477, 8579, 8682, 8786, 8891, 8998, 9106, 9215, 9325, 9437, 9550, 9664, 9780, 9897, 10016, 10136, 10257, 10380, 10504, 10630, 10757, 10886, 11016, 11148, 11282, 11417, 11554, 11693, 11833, 11975, 12119, 12264, 12411, 12560, 12711, 12863, 13017, 13173, 13331, 13491, 13653, 13817, 13983, 14000]
    # binBoundaries["1p4"] = [500, 508, 517, 526, 535, 544, 553, 562, 571, 580, 590, 600, 610, 620, 630, 640, 650, 661, 672, 683, 694, 705, 716, 728, 740, 752, 764, 776, 788, 801, 814, 827, 840, 853, 866, 880, 894, 908, 922, 936, 951, 966, 981, 996, 1011, 1027, 1043, 1059, 1075, 1092, 1109, 1126, 1143, 1160, 1178, 1196, 1214, 1232, 1251, 1270, 1289, 1309, 1329, 1349, 1369, 1390, 1411, 1432, 1454, 1476, 1498, 1520, 1543, 1566, 1589, 1613, 1637, 1661, 1686, 1711, 1736, 1762, 1788, 1815, 1842, 1869, 1897, 1925, 1953, 1982, 2011, 2041, 2071, 2101, 2132, 2163, 2195, 2227, 2260, 2293, 2327, 2361, 2396, 2431, 2467, 2503, 2540, 2577, 2615, 2653, 2692, 2731, 2771, 2811, 2852, 2893, 2935, 2978, 3021, 3065, 3109, 3154, 3200, 3246, 3293, 3341, 3389, 3438, 3488, 3538, 3589, 3641, 3693, 3746, 3800, 3855, 3910, 3966, 4023, 4081, 4140, 4199, 4259, 4320, 4382, 4445, 4509, 4574, 4640, 4706, 4773, 4841, 4910, 4980, 5051, 5123, 5196, 5270, 5345, 5421, 5498, 5576, 5656, 5737, 5819, 5902, 5986, 6071, 6157, 6245, 6334, 6424, 6515, 6608, 6702, 6797, 6894, 6992, 7091, 7192, 7294, 7398, 7503, 7610, 7718, 7828, 7939, 8052, 8166, 8282, 8399, 8518, 8639, 8761, 8885, 9011, 9139, 9268, 9399, 9532, 9667, 9804, 9943, 10084, 10227, 10372, 10519, 10668, 10819, 10972, 11127, 11284, 11443, 11605, 11769, 11935, 12104, 12275, 12448, 12624, 12802, 12983, 13166, 13352, 13540, 13731, 13925, 14000]
    # binBoundaries["5p6"] = [500, 517, 534, 552, 570, 589, 608, 628, 649, 670, 692, 714, 737, 761, 785, 810, 836, 863, 890, 918, 947, 977, 1008, 1040, 1073, 1107, 1141, 1176, 1212, 1250, 1289, 1329, 1370, 1412, 1455, 1500, 1546, 1593, 1642, 1692, 1743, 1796, 1850, 1906, 1964, 2023, 2084, 2147, 2212, 2279, 2347, 2417, 2489, 2564, 2641, 2720, 2801, 2885, 2971, 3060, 3151, 3245, 3341, 3440, 3542, 3647, 3755, 3866, 3981, 4099, 4220, 4345, 4473, 4605, 4741, 4881, 5025, 5173, 5325, 5482, 5643, 5809, 5980, 6156, 6337, 6523, 6715, 6912, 7115, 7324, 7539, 7760, 7987, 8221, 8462, 8710, 8965, 9227, 9497, 9775, 10061, 10355, 10658, 10969, 11289, 11619, 11958, 12307, 12666, 13036, 13416, 13807, 14000]



    hist_dict = {}

    if options.cat == 'EBEB': cat = 0
    elif options.cat == 'EBEE': cat = 1

    if not options.multi:

        filename = options.ws + "/SignalParametricShapes_ws_" + options.coup + ".root"
        fparamshape = ROOT.TFile(filename);
        wsparamshape = fparamshape.Get("ws_inputs");
        # RooRealVar x{"x", "x", 1.0, binEdges[0], binEdges.back()};
        mgg = wsparamshape.var("mgg")
        MH  = wsparamshape.var("MH")
        MH.setVal(options.mass);
        varbin = ROOT.RooBinning(len(binBoundaries[options.coup])-1, array('d', binBoundaries[options.coup]))
        # p = mgg.frame()
        p = mgg.frame(0,1000,125)
        shape = wsparamshape.pdf("SignalShape_%s_EBEB"%(options.coup));
        shape.plotOn(p,ROOT.RooFit.DrawOption("B"),ROOT.RooFit.LineColor(4))
        # hist_mass_list_rsg = ROOT.TH1D()

        # #Now to the interpolated shape
        tfileRes = ROOT.TFile("/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/%s/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_finebinned.root" %(options.method,options.coup,options.cat,options.year) , "read")
        tfileRes.cd()

        # #tfileRes.Print()

        # hist_mass_list_rsg.append( tfileRes.Get("h_gg_%s"%mass) )
        # hist_mass_list_rsg = tfileRes.FindObject("h_gg_%i"%mass)
        hist_mass_list_rsg =  tfileRes.Get("h_gg_%i"%(options.mass))
        # p.addTH1(hist_mass_list_rsg,"HISTsame")
        # h = ROOT.RooDataHist("h","h",ROOT.RooArgList(mgg),ROOT.RooFit.Import(hist_mass_list_rsg)) ;
        # h.plotOn(p,ROOT.RooFit.DrawOption("B"),ROOT.RooFit.XErrorSize(0))
        # histosRes.append(hist_mass_list_rsg)

        # hist_mass_list_rsg.Print()

        canvas = ROOT.TCanvas()
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetLeftMargin(0.05+ L/W )
        canvas.SetRightMargin( R/W )
        canvas.SetTopMargin( T/H )
        canvas.SetBottomMargin( B/H )
        canvas.SetTickx()
        canvas.SetTicky()
        canvas.cd()



        # leg = ROOT.TLegend(0.65,0.45,0.95,0.6)
        # leg.SetBorderSize(0)
        # leg.SetLineColor(0)
        # leg.SetFillColor(0)
        # leg.SetFillStyle(0)
        # leg.SetLineWidth(0)
        # leg.SetTextFont(42)
        # #leg.SetTextAlign(23)

        # #Pave text
        # pave_fit = ROOT.TPaveText(0.56,0.65,0.95,0.85,"NDC")

        # plabel = " "
        # if options.coup == "kMpl001" or options.coup == "0p014":
        #     plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-4}"
        # elif options.coup == "kMpl01" or options.coup == "1p4":
        #     plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-2}"
        # elif options.coup == "kMpl02" or options.coup == "5p6":
        #     plabel = "#frac{#Gamma}{m} = 5.6 #times 10^{-2}"

        # thespin = 10000;
        # if "RSG" in title: thespin=2
        # elif "GluGlu" in title: thespin=0

        # pave_fit.AddText("%s, M=%i" %(year,mass) )
        # pave_fit.AddText("%s, J=%i" %(options.cat,thespin) )
        # pave_fit.AddText(plabel)
        # pave_fit.SetFillColor(0)
        # pave_fit.SetLineColor(0)
        # pave_fit.SetFillStyle(0)
        # pave_fit.SetBorderSize(0)
        # pave_fit.SetTextFont(42)
        # pave_fit.SetTextSize(0.0355)
        # pave_fit.SetTextAlign(23)

        # pave_gof = ROOT.TPaveText(0.65,0.85,0.95,1.0,"NDC")

        p.SetLineColor(1)
        p.GetXaxis().SetRangeUser(500, 800)
        p.GetXaxis().SetTitle("DiPhoton mass [GeV]")
        p.GetYaxis().SetTitle("Normalized yield/bin width")
        # p.Scale(1/h_mgg_fit.GetSumOfWeights())
        p.Draw("HIST")
        # hist_mass_list_rsg.GetXaxis().SetRangeUser(massMin, massMax)
        # hist_mass_list_rsg.SetLineColor(2)
        # hist_mass_list_rsg.Draw("hist same")

        # rp = ROOT.TRatioPlot(hist_mass_list_rsg,h_mgg_varbins)
        # rp.SetRightMargin(0.05)
        # rp.SetLeftMargin(0.13)
        # rp.SetH1DrawOpt("HIST")
        # rp.SetH2DrawOpt("HIST same")
        # rp.SetGraphDrawOpt("P")
        # rp.Draw()
        # rp.GetLowerRefGraph().SetMinimum(0.7);
        # rp.GetLowerRefGraph().SetMaximum(1.3);
        # rp.GetLowerRefGraph().SetLineColor(0)
        # rp.GetLowerRefGraph().SetMarkerColor(1)
        # rp.GetLowerRefGraph().SetMarkerStyle(20)
        # rp.GetLowerRefYaxis().SetTitle("Interp / Orig")
        # canvas.Update()



        # res = array('d')
        # pvalKStest = h_mgg_varbins.KolmogorovTest( hist_mass_list_rsg , "WW")
        # print ("KolmogorovTest",pvalKStest)
        # pvalchi2test = h_mgg_varbins.Chi2Test( hist_mass_list_rsg , "WW")
        # #print(res)
        # print ("Chi2Test",pvalchi2test)
        # pave_gof.AddText("KS %f" %(pvalKStest) )
        # pave_gof.AddText("#chi^{2} %f" %(pvalchi2test) )
        # #pave_gof.AddText("#chi^{2} %f" %(pvalchi2test) )

        # leg.AddEntry(h_mgg_varbins,"Input Shape","l");
        # leg.AddEntry(hist_mass_list_rsg,"Interpolated Shape","l");
        # leg.Draw();

        # pave_fit.Draw();
        # pave_gof.Draw();

        canvas.SaveAs("%s/test.png" %(options.outDir) );


    #UNFINISHED WORK DOWN BELOW
    if options.multi:

        for f in args:
            hist_mass_list_rsg = ROOT.TH1D()
            year = f.split('.root')[0].split('_')[-1]
            mass = int(f.split('_M_')[1].split('_TuneCP2')[0])
            title =  f.split('_M_')[0].split('/')[-1]
            print(title,year,mass)
            if mass not in M_bins[options.coup] : continue
            if M_bins[options.coup].index(mass) == len(M_bins[options.coup])-1 : continue

            mass1 = mass
            tfileMin = ROOT.TFile.Open(f)
            tfileMin.cd()
            h_min = ROOT.TH1D('h_min','h_min',len(binBoundaries[options.coup])-1, array('d',binBoundaries[options.coup]) )
            thetreeMin=tfileMin.Get("HighMassDiphoton")
            massMin=0.8*mass1;
            massMax=1.2*mass1;
            h_mgg1 = ROOT.TH1D('h_mgg1','h_mgg1',1000,massMin,massMax)
            project(thetreeMin,h_mgg1,"mgg","1")
            bin1 = h_mgg1.FindFirstBinAbove(h_mgg1.GetMaximum()/2)
            bin2 = h_mgg1.FindLastBinAbove(h_mgg1.GetMaximum()/2)
            mean = h_mgg1.GetBinCenter(h_mgg1.GetMaximumBin())
            fwhm = h_mgg1.GetBinCenter(bin2) - h_mgg1.GetBinCenter(bin1);
            massMin=mean-2*fwhm
            massMax=mean+2*fwhm

            if options.method=="truncate":
                project(thetreeMin,h_min, "mgg", 'eventClass==%d && mgg>%f && mgg<%f'%(cat,massMin,massMax) )
            elif options.method=="full" or options.method=="genFiducial":
                project(thetreeMin,h_min, "mgg", 'eventClass==%d'%(cat) )

            mass2 = M_bins[options.coup][M_bins[options.coup].index(mass)+1]
            tfileMax = ROOT.TFile.Open(f.replace(str(mass), str(mass2)))
            tfileMax.cd()
            h_max = ROOT.TH1D('h_max','h_max',len(binBoundaries[options.coup])-1, array('d',binBoundaries[options.coup]) )
            thetreeMax=tfileMax.Get("HighMassDiphoton")

            massMin=0.8*mass2;
            massMax=1.2*mass2;
            h_mgg2 = ROOT.TH1D('h_mgg2','h_mgg2',1000,massMin,massMax)
            project(thetreeMax,h_mgg2,"mgg","1")
            bin1 = h_mgg2.FindFirstBinAbove(h_mgg2.GetMaximum()/2)
            bin2 = h_mgg2.FindLastBinAbove(h_mgg2.GetMaximum()/2)
            mean = h_mgg2.GetBinCenter(h_mgg2.GetMaximumBin())
            fwhm = h_mgg2.GetBinCenter(bin2) - h_mgg2.GetBinCenter(bin1);
            massMin=mean-2*fwhm
            massMax=mean+2*fwhm

            if options.method=="truncate":
                project(thetreeMax,h_max, "mgg", 'eventClass==%d && mgg>%f && mgg<%f'%(cat,massMin,massMax) )
            else:
                project(thetreeMax,h_max, "mgg", 'eventClass==%d'%(cat) )

            h_min.SetName('h_min_%s_M%i_%s'%(title,mass1,year))
            h_min.SetTitle('h_min_%s_M%i_%s'%(title,mass1,year))
            h_min.SetDirectory(0)
            h_max.SetName('h_max_%s_M%i_%s'%(title,mass2,year))
            h_max.SetTitle('h_max_%s_M%i_%s'%(title,mass2,year))
            h_max.SetDirectory(0)

            canvas = ROOT.TCanvas("c_%s_%i_%i_%s_%s" %(title,mass1,mass2,options.cat,year),"c_%s_%i_%i_%s_%s" %(title,mass1,mass2,options.cat,year),50,50,W,H)
            canvas.SetFillColor(0)
            canvas.SetBorderMode(0)
            canvas.SetFrameFillStyle(0)
            canvas.SetFrameBorderMode(0)
            canvas.SetLeftMargin(0.05+ L/W )
            canvas.SetRightMargin( R/W )
            canvas.SetTopMargin( T/H )
            canvas.SetBottomMargin( B/H )
            canvas.SetTickx()
            canvas.SetTicky()
            canvas.cd()

            leg = ROOT.TLegend(0.2,0.7,0.9,0.9)
            leg.SetBorderSize(0)
            leg.SetLineColor(0)
            leg.SetFillColor(17)
            # leg.SetFillStyle(0)
            leg.SetLineWidth(0)
            leg.SetTextFont(42)
            #leg.SetTextAlign(23)
            leg.SetNColumns(2);

            #Pave text
            pave_fit = ROOT.TPaveText(0.55,0.8,0.95,0.95,"NDC")

            plabel = " "
            if options.coup == "kMpl001" or options.coup == "0p014":
                plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-4}"
            elif options.coup == "kMpl01" or options.coup == "1p4":
                plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-2}"
            elif options.coup == "kMpl02" or options.coup == "5p6":
                plabel = "#frac{#Gamma}{m} = 5.6 #times 10^{-2}"

            thespin = 10000;
            legtitle=""
            if "RSG" in title:
                thespin=2
                legtitle="RSGraviton"
            elif "GluGlu" in title:
                thespin=0
                legtitle="HeavyHiggs"

            pave_fit.AddText("RS Graviton  {}".format(plabel))
            pave_fit.SetFillColor(0)
            pave_fit.SetLineColor(0)
            pave_fit.SetFillStyle(0)
            pave_fit.SetBorderSize(0)
            pave_fit.SetTextFont(42)
            pave_fit.SetTextSize(0.038)
            pave_fit.SetTextAlign(23)

            h_min.SetLineColor(1);
            h_min.SetLineStyle(9);
            h_min.GetXaxis().SetRangeUser(mass1*0.5,mass2*1.04);
            h_min.GetXaxis().SetTitle("DiPhoton mass [GeV]");
            h_min.GetYaxis().SetTitle("Normalized yield");
            h_min.Scale(1/h_min.GetSumOfWeights());
            h_min.Draw("hist");
            h_min.GetYaxis().SetRangeUser(0,0.5);
            leg.AddEntry(h_min,"M_{Min Input} = %i GeV" % mass1,"l")

            h_max.SetLineColor(1);
            h_max.SetLineStyle(2);
            h_max.DrawNormalized("hist same");
            leg.AddEntry(h_max,"M_{Max Input} = %i GeV" % mass2,"l")


            #Now to the interpolated shape
            tfileRes = ROOT.TFile("/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/%s/ResonanceShapes_InputShapes_%s_%s_%s.root" %(method,title,options.cat,year) , "read")
            tfileRes.cd()

            i=0
            for mass in range(mass1-250, mass2, 100):
                hist =  tfileRes.Get("h_gg_%i"%mass)
                hist.SetLineColor(color(i));
                hist.SetFillColor(color(i));
                hist.DrawNormalized("hist sames");
                i = i+1

                leg.AddEntry(hist,"M_{Interpolate} = %i GeV " % mass,"f");

            leg.SetHeader("{} {}".format(legtitle, plabel))
            leg.Draw();
            # pave_fit.Draw();

            canvas.SaveAs("%s/plots/Multi_%s_%i_%i_%s_%s_after.png" %(options.outDir,title,mass1,mass2,options.cat,year) );
            canvas.SaveAs("%s/plots/Multi_%s_%i_%i_%s_%s_after.pdf" %(options.outDir,title,mass1,mass2,options.cat,year) );
