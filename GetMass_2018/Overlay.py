import ROOT as rt
from rootTools import tdrstyle as setTDRStyle
rt.gROOT.SetBatch()
setTDRStyle.setTDRStyle()
from ROOT import *

WP  ={
'L':0.0494,
'M':0.2770,
'T':0.7264
}

fin = TFile('Data_Rate.root')

c1 = TCanvas()

h1 = fin.Get('DeepJetle1b_TagRate_%d'%int(WP['L']*10000))
h1.SetLineColor(1)
h1.SetMarkerSize(0.5)
h2 = fin.Get('DeepJetle1b_TagRate_%d'%int(WP['M']*10000))
h2.SetLineColor(2)
h2.SetMarkerSize(0.5)
h3 = fin.Get('DeepJetle1b_TagRate_%d'%int(WP['T']*10000))
h3.SetLineColor(3)
h3.SetMarkerSize(0.5)

leg = TLegend(0.70, 0.70, 0.96, 0.89)

h1.Draw()
h1.GetYaxis().SetRangeUser(0,1.2)
h2.Draw('same')
h3.Draw('same')
leg.AddEntry(h1,'Loose WP','L')
leg.AddEntry(h2,'Medium WP','L')
leg.AddEntry(h3,'Tight WP','L')

leg.Draw('same')

c1.Print('temp.pdf')
