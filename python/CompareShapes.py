from optparse import OptionParser
import ROOT as rt
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
rt.TGaxis.SetMaxDigits(3)
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

H_ref = 800; 
W_ref = 800; 
W = W_ref
H  = H_ref

iPeriod = 0


# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

def project(tree, h, var, cut):
    print 'projecting var: %s, cut: %s from tree: %s into hist: %s'%(var, cut, tree.GetName(), h.GetName())
    tree.Project(h.GetName(),var,cut)

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('-c','--cat',dest="cat",default="EBEB",type="string",
                  help="category")
    parser.add_option('-w','--coup',dest="coup",default="kMpl001",type="string",
                  help="coupling")
    parser.add_option('-d','--outdir',dest="outDir",default="./",type="string",
                  help="Output directory to store output histograms")
    parser.add_option('-m','--multi', action="store_true",
                  dest="multi", default=False,
                  help="Make a single comparison plot or multi")

    (options,args) = parser.parse_args()

    histos = []
    histosRes = []
    year = ''

    M_bins = {
        "kMpl001" : [1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000],
        "kMpl01" : [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 8000],
        "kMpl02" : [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 8000],
        "0p014": [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
        "1p4": [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
        "5p6": [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    }

    binBoundaries = {}
    #EBEB
    binBoundaries["kMpl001"] = [500, 506, 513, 519, 526, 533, 540, 547, 554, 561, 568, 575, 583, 590, 598, 605, 613, 621, 629, 637, 645, 653, 662, 670, 679, 687, 696, 705, 714, 723, 732, 741, 751, 760, 770, 779, 789, 799, 809, 820, 830, 840, 851, 862, 872, 883, 894, 906, 917, 929, 940, 952, 964, 976, 988, 1001, 1013, 1026, 1038, 1051, 1064, 1078, 1091, 1105, 1119, 1132, 1147, 1161, 1175, 1190, 1205, 1219, 1235, 1250, 1265, 1281, 1297, 1313, 1329, 1346, 1362, 1379, 1396, 1413, 1431, 1449, 1466, 1485, 1503, 1521, 1540, 1559, 1578, 1598, 1617, 1637, 1657, 1678, 1698, 1719, 1740, 1762, 1783, 1805, 1827, 1850, 1873, 1895, 1919, 1942, 1966, 1990, 2014, 2039, 2064, 2089, 2115, 2141, 2167, 2193, 2220, 2247, 2275, 2303, 2331, 2359, 2388, 2417, 2447, 2477, 2507, 2537, 2568, 2600, 2631, 2663, 2696, 2729, 2762, 2795, 2830, 2864, 2899, 2934, 2970, 3006, 3042, 3079, 3117, 3155, 3193, 3232, 3271, 3311, 3351, 3392, 3433, 3475, 3517, 3560, 3603, 3647, 3691, 3736, 3781, 3827, 3873, 3920, 3968, 4016, 4065, 4114, 4164, 4214, 4265, 4317, 4369, 4422, 4476, 4530, 4585, 4640, 4696, 4753, 4811, 4869, 4928, 4987, 5048, 5109, 5171, 5233, 5296, 5360, 5425, 5491, 5557, 5624, 5692, 5761, 5831, 5901, 5973, 6045, 6118, 6192, 6267, 6342, 6419, 6496, 6575, 6654, 6734, 6816, 6898, 6981, 7066, 7151, 7237, 7325, 7413, 7502, 7593, 7684, 7777, 7871, 7966, 8062, 8159, 8258, 8357, 8458, 8560, 8663, 8768, 8873, 8980, 9089, 9198, 9309, 9421, 9535, 9650, 9766, 9884, 10003, 10123, 10245, 10369, 10494, 10620, 10748, 10877, 11008, 11141, 11275, 11411, 11548, 11687, 11828, 11971, 12115, 12261, 12408, 12558, 12709, 12862, 13017, 13173, 13332, 13492, 13655, 13819, 13985, 14000]
    binBoundaries["kMpl01"] = [500, 509, 518, 528, 538, 548, 558, 568, 579, 589, 600, 611, 622, 634, 645, 657, 669, 681, 694, 707, 719, 732, 746, 759, 773, 787, 801, 816, 830, 845, 860, 876, 892, 908, 924, 940, 957, 974, 992, 1009, 1027, 1046, 1064, 1083, 1102, 1122, 1142, 1162, 1183, 1204, 1225, 1247, 1269, 1291, 1314, 1337, 1361, 1385, 1409, 1434, 1459, 1485, 1511, 1537, 1564, 1592, 1619, 1648, 1677, 1706, 1736, 1766, 1797, 1828, 1860, 1893, 1926, 1959, 1993, 2028, 2064, 2099, 2136, 2173, 2211, 2249, 2288, 2328, 2368, 2410, 2451, 2494, 2537, 2581, 2626, 2671, 2718, 2765, 2812, 2861, 2910, 2961, 3012, 3064, 3117, 3171, 3225, 3281, 3338, 3395, 3454, 3513, 3574, 3636, 3698, 3762, 3827, 3893, 3960, 4028, 4097, 4167, 4239, 4312, 4386, 4462, 4538, 4616, 4696, 4776, 4858, 4942, 5027, 5113, 5201, 5290, 5381, 5473, 5567, 5662, 5759, 5858, 5958, 6061, 6164, 6270, 6377, 6487, 6598, 6711, 6826, 6943, 7061, 7182, 7305, 7430, 7557, 7687, 7818, 7952, 8088, 8226, 8367, 8510, 8656, 8804, 8954, 9107, 9263, 9421, 9582, 9746, 9912, 10082, 10254, 10429, 10607, 10788, 10972, 11160, 11350, 11544, 11741, 11942, 12146, 12353, 12564, 12778, 12996, 13218, 13443, 13673, 13906, 14000]
    binBoundaries["kMpl02"] = [500, 523, 547, 572, 598, 625, 653, 683, 713, 745, 778, 812, 848, 885, 924, 964, 1005, 1049, 1094, 1141, 1190, 1241, 1293, 1348, 1405, 1465, 1527, 1591, 1658, 1727, 1800, 1875, 1953, 2034, 2119, 2207, 2298, 2393, 2492, 2595, 2702, 2813, 2929, 3050, 3175, 3305, 3440, 3581, 3728, 3880, 4038, 4203, 4374, 4553, 4738, 4931, 5131, 5339, 5556, 5782, 6016, 6260, 6514, 6777, 7052, 7337, 7634, 7942, 8263, 8597, 8944, 9305, 9680, 10070, 10477, 10899, 11338, 11795, 12270, 12764, 13277, 13812, 14000]
    
    binBoundaries["0p014"] = binBoundaries["kMpl001"]
    binBoundaries["1p4"] = binBoundaries["kMpl01"] 
    binBoundaries["5p6"] = binBoundaries["kMpl02"]

    hist_dict = {}

    if options.cat == 'EBEB': cat = 0
    elif options.cat == 'EBEE': cat = 1

    for f in args:
        hist_mass_list_rsg = rt.TH1D()
        year = f.split('.root')[0].split('_')[-1]
        if year != "2016":
            mass = int(f.split('_M_')[1].split('_TuneCP2')[0])
            title =  f.split('_M_')[0].split('/')[-1]        
        else:
            mass = int(f.split('_M-')[1].split('_TuneCP2')[0])
            title =  f.split('_M-')[0].split('/')[-1]        
        print(title,year,mass)
        #Will plot only in specific points
        if mass not in M_bins[options.coup] : continue
        tfileIn = rt.TFile.Open(f)
        tfileIn.cd()
        
        #h_mgg_1GeVbin = rt.TH1D('h_mgg_1GeVbin','h_mgg_1GeVbin',14000,0,14000)
        #h_mgg_5GeVbin = rt.TH1D('h_mgg_5GeVbin','h_mgg_5GeVbin',2800,0,14000)
        h_mgg_varbins = rt.TH1D('h_mgg_varbins','h_mgg_varbins',len(binBoundaries[options.coup])-1, array('d',binBoundaries[options.coup]) )
        thetree=tfileIn.Get("HighMassDiphoton")

        project(thetree,h_mgg_varbins, "mgg", 'eventClass==%d'%(cat) )
        
        #h = tfileIn.Get('h_mjj_ratio_%s'%options.type)
        h_mgg_varbins.SetName('h_%s_M%i_%s'%(title,mass,year))
        h_mgg_varbins.SetTitle('h_%s_M%i_%s'%(title,mass,year))
        h_mgg_varbins.SetDirectory(0)
        histos.append(h_mgg_varbins)

        #Now to the interpolated shape
        tfileRes = rt.TFile("/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/DijetShapeInterpolator/ResonanceShapes_InputShapes_%s_%s_%s.root" %(title,options.cat,year) , "read")
        tfileRes.cd()

        #tfileRes.Print()
        
        #hist_mass_list_rsg.append( tfileRes.Get("h_gg_%s"%mass) )
        #hist_mass_list_rsg = tfileRes.FindObject("h_gg_%i"%mass)
        hist_mass_list_rsg =  tfileRes.Get("h_gg_%i"%mass)
        histosRes.append(hist_mass_list_rsg)

        hist_mass_list_rsg.Print()

        count = 0;
        canvas = rt.TCanvas("c_%s_%i_%s_%s" %(title,mass,options.cat,year),"c_%s_%i_%s_%s" %(title,mass,options.cat,year),50,50,W,H)
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

        leg = rt.TLegend(0.6,0.45,0.9,0.6)
        leg.SetBorderSize(0)
        leg.SetLineColor(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineWidth(0)
        leg.SetTextFont(42)
        #leg.SetTextAlign(23) 
        
        #Pave text
        pave_fit = rt.TPaveText(0.56,0.65,0.95,0.85,"NDC")

        plabel = " "
        if options.coup == "kMpl001" or options.coup == "0p014":
            plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-4}"
        elif options.coup == "kMpl01" or options.coup == "1p4":
            plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-2}"
        elif options.coup == "kMpl02" or options.coup == "5p6":
            plabel = "#frac{#Gamma}{m} = 5.6 #times 10^{-2}"

        thespin = 10000;
        if "RSG" in title: thespin=2
        elif "GluGlu" in title: thespin=0

        pave_fit.AddText(plabel)
        pave_fit.AddText("%s J=%i" %(options.cat,thespin) )
        pave_fit.SetFillColor(0)
        pave_fit.SetLineColor(0)
        pave_fit.SetFillStyle(0)
        pave_fit.SetBorderSize(0)
        pave_fit.SetTextFont(42)
        pave_fit.SetTextSize(0.0355)
        pave_fit.SetTextAlign(23)

        pave_gof = rt.TPaveText(0.16,0.65,0.55,0.85,"NDC")


        if not options.multi: 
            h_mgg_varbins.SetLineColor(1);
            h_mgg_varbins.GetXaxis().SetRangeUser(h_mgg_varbins.GetMean()-5*h_mgg_varbins.GetRMS(),h_mgg_varbins.GetMean()+5*h_mgg_varbins.GetRMS());
            h_mgg_varbins.GetXaxis().SetTitle("DiPhoton mass [GeV]");
            h_mgg_varbins.GetYaxis().SetTitle("Normalized yield/bin width");
            h_mgg_varbins.DrawNormalized();

            hist_mass_list_rsg.GetXaxis().SetRangeUser(h_mgg_varbins.GetMean()-5*h_mgg_varbins.GetRMS(),h_mgg_varbins.GetMean()+5*h_mgg_varbins.GetRMS());
            hist_mass_list_rsg.SetLineColor(2);
            hist_mass_list_rsg.Draw("hist sames");

            res = array('d')
            pvalKStest = h_mgg_varbins.KolmogorovTest( hist_mass_list_rsg , "WW")
            print ("KolmogorovTest",pvalKStest)
            pvalchi2test = h_mgg_varbins.Chi2Test( hist_mass_list_rsg , "WW")
            #print(res)
            print ("Chi2Test",pvalchi2test)
            pave_gof.AddText("KS %f" %(pvalKStest) )
            pave_gof.AddText("#chi^{2} %f" %(pvalchi2test) )
            #pave_gof.AddText("#chi^{2} %f" %(pvalchi2test) )

            leg.AddEntry(h_mgg_varbins,"Input Shape","l");
            leg.AddEntry(hist_mass_list_rsg,"Interpolated Shape","l");
            leg.Draw();

            pave_fit.Draw();
            pave_gof.Draw();

            canvas.SaveAs("%s/plots/Closure_%s_%i_%s_%s.png" %(options.outDir,title,mass,options.cat,year) );


    '''
    #UNFINISHED WORK DOWN BELOW
    if options.multi:

        canvas = rt.TCanvas("c_%s_%i_%s_%s" %(title,mass,options.cat,year),"c_%s_%i_%s_%s" %(title,mass,options.cat,year),50,50,W,H)
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

        leg = rt.TLegend(0.6,0.45,0.9,0.6)
        leg.SetBorderSize(0)
        leg.SetLineColor(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineWidth(0)
        leg.SetTextFont(42)
        #leg.SetTextAlign(23) 
        
        #Pave text
        pave_fit = rt.TPaveText(0.56,0.65,0.95,0.85,"NDC")

        plabel = " "
        if options.coup == "kMpl001" or options.coup == "0p014":
            plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-4}"
        elif options.coup == "kMpl01" or options.coup == "1p4":
            plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-2}"
        elif options.coup == "kMpl02" or options.coup == "5p6":
            plabel = "#frac{#Gamma}{m} = 5.6 #times 10^{-2}"

        thespin = 10000;
        if "RSG" in title: thespin=2
        elif "GluGlu" in title: thespin=0

        pave_fit.AddText(plabel)
        pave_fit.AddText("%s J=%i" %(options.cat,thespin) )
        pave_fit.SetFillColor(0)
        pave_fit.SetLineColor(0)
        pave_fit.SetFillStyle(0)
        pave_fit.SetBorderSize(0)
        pave_fit.SetTextFont(42)
        pave_fit.SetTextSize(0.0355)
        pave_fit.SetTextAlign(23) 

        for i in range(len(histos)):
            histos[i].SetLineColor(1);
            histos[i].GetXaxis().SetRangeUser(0.,9000.);
            histos[i].GetXaxis().SetTitle("DiPhoton mass [GeV]");
            histos[i].GetYaxis().SetTitle("Normalized yield/5 GeV");
            histos[i].DrawNormalized();


            hist_mass_list_rsg.SetLineColor(2);
            hist_mass_list_rsg.Draw("hist sames");
        
            leg.AddEntry(histos[i],"M = %i GeV " % (),"l");
            leg.AddEntry(hist_mass_list_rsg,"Interpolated Shape","l");
            leg.Draw();

            pave_fit.Draw();

            canvas.SaveAs("%s/plots/Closure_%s_%i_%s_%s.png" %(options.outDir,title,mass,options.cat,year) );
    '''
                
                
                
        
        
