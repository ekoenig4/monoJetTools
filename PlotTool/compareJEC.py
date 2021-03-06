#!/usr/bin/env python
from ROOT import *
from PlotTool import *
import os
import sys

gROOT.SetBatch(1)

hdfs_store = '/hdfs/store/user/ekoenig/MonoJet/PostFiles/%s/%s/20200114_postFiles/'

def makeComparison(num,den,process):
    c = TCanvas("c", "canvas",800,800);
    gStyle.SetOptStat(0);
    gStyle.SetLegendBorderSize(0);
    #c.SetLeftMargin(0.15);
    #c.SetLogy();
    #c.cd();
    
    pad1 = TPad("pad1","pad1",0.01,0.25,0.99,0.99);
    pad1.SetBottomMargin(0.);
    pad1.Draw(); pad1.cd();
    if process != 'Data/MC': pad1.SetLogy();
    pad1.SetFillColor(0); pad1.SetFrameBorderMode(0); pad1.SetBorderMode(0);

    num.setSumOfBkg(); den.setSumOfBkg()
    num_hs = num[process].histo; den_hs = den[process].histo
    MCStyle(num_hs,kBlue); MCStyle(den_hs,kRed)
    num_hs.SetFillStyle(0); num_hs.SetLineColor(kBlue)
    den_hs.SetFillStyle(0); den_hs.SetLineColor(kRed)

    if process != 'Data/MC':
        num_hs.SetMinimum(pow(10,-2))
        num_hs.SetMaximum( max(list(num_hs))*pow(10,2.5) )
    else:
        num_hs.SetMinimum(0)
        num_hs.SetMaximum(2)

    num_hs.Draw('hist')
    den_hs.Draw('histsame')

    leg = getLegend(xmin=0.5,xmax=0.7)
    if process == 'Data/MC': process = 'DataMC'
    leg.AddEntry(num_hs,'%s %s' % (num.label,process),'l')
    leg.AddEntry(den_hs,'%s %s' % (den.label,process),'l')
    leg.Draw()

    lumi_label = '%s' % float('%.3g' % (num.lumi/1000.)) + " fb^{-1}"
    if (parser.args.normalize): lumi_label="Normalized"
    texLumi,texCMS = getCMSText(lumi_label,num.year,scale=0.8)
    texLumi.Draw();
    texCMS.Draw();

    c.cd();
    pad2 = TPad("pad2","pad2",0.01,0.01,0.99,0.25);
    pad2.Draw(); pad2.cd();
    pad2.SetFillColor(0); pad2.SetFrameBorderMode(0); pad2.SetBorderMode(0);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.35);

    ratio = GetRatio(num_hs,den_hs)
    rymin = 0.65; rymax = 1.35
    RatioStyle(ratio,rymin,rymax)
    ratio.Draw('pex0')
    ratio.GetYaxis().SetLabelSize(0)

    line = getRatioLine(num_hs.GetXaxis().GetXmin(),num_hs.GetXaxis().GetXmax())
    line.Draw("same");
    
    c.Update();

    nbins = num_hs.GetXaxis().GetNbins();
    xmin = num_hs.GetXaxis().GetXmin();
    xmax = num_hs.GetXaxis().GetXmax();
    xwmin = xmin;
    xwmax = xmax;
    
    xname = num.name if type(num.name) == str else None
    xaxis = makeXaxis(xmin,xmax,rymin,510,name=xname);
    xaxis.Draw("SAME");
    
    yaxis = makeYaxis(rymin,rymax,xmin,6,name="New/Old");
    yaxis.Draw("SAME");
    ######################################
    SaveAs(c,"%s_%s"%(process,num.varname),year=num.year,region=num.region,sub="JEC_Comparison")
    
def compareVariable(num,den,variable):
    print "Comparing",variable
    num.initiate(variable); den.initiate(variable)
    # makeComparison(num,den,'Data')

    num.setSumOfBkg(); den.setSumOfBkg()
    # makeComparison(num,den,'SumOfBkg')

    num.processes['Data/MC'] = Process('Data/MC',[],{},'datamc',year=num.year,region=num.region)
    den.processes['Data/MC'] = Process('Data/MC',[],{},'datamc',year=den.year,region=den.region)

    num['Data/MC'].histo = num['Data'].histo.Clone(); num['Data/MC'].histo.Divide(num['SumOfBkg'].histo)
    den['Data/MC'].histo = den['Data'].histo.Clone(); den['Data/MC'].histo.Divide(den['SumOfBkg'].histo)
    makeComparison(num,den,'Data/MC')
def compare():
    newjec = Region(autovar=True)
    oldjec = Region(path=hdfs_store%(newjec.year,newjec.region),autovar=True)

    jec_variables = ['ChNemPtFrac','j1pT','pfMET','recoil']
    newjec.label = 'New JEC'
    oldjec.label = 'Old JEC'
    for variable in jec_variables:
        compareVariable(newjec,oldjec,variable)
if __name__ == '__main__': compare()
