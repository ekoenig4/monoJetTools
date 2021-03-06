from ROOT import *

def DataStyle(hs_data):
    hs_data.SetLineWidth(2)
    hs_data.SetLineColor(kWhite);
    hs_data.SetTitle("");
    # hs_data.GetXaxis().SetTitle("");
    # hs_data.GetXaxis().SetTickLength(0);
    # hs_data.GetXaxis().SetLabelOffset(999);
    # hs_data.GetYaxis().SetTitle("");
    # hs_data.GetYaxis().SetTickLength(0);
    # hs_data.GetYaxis().SetLabelOffset(999);
    hs_data.SetLineColor(kBlack);
    hs_data.SetMarkerStyle(20);
    hs_data.SetMarkerSize(1);
###################################################################
    
def MCStyle(hs_mc,color):
    # hs_mc.SetTitle("");
    # hs_mc.GetXaxis().SetTitle("");
    # hs_mc.GetXaxis().SetTickLength(0);
    # hs_mc.GetXaxis().SetLabelOffset(999);
    # hs_mc.GetYaxis().SetTitle("");
    # hs_mc.GetYaxis().SetTickLength(0);
    # hs_mc.GetYaxis().SetLabelOffset(999);
    hs_mc.SetFillColor(color);
###################################################################

def UncBandStyle(uncband,color=33):
    uncband.SetTitle("")
    # uncband.SetFillStyle(3144)
    uncband.SetFillStyle(2001)
    uncband.SetFillColor(color)
###################################################################

def fillStack(samples,hs_datamc,threshold=0.001):
    if samples.name == 'Cutflow': threshold=0
    MCLegOrder = []
    for process in reversed(samples.MCOrder):
        percent=samples[process].scaled_total/samples.total_bkg
        if percent > threshold:
            hs_datamc.Add(samples[process].histo)
            MCLegOrder.append(process)
    return list(reversed(MCLegOrder))
###################################################################

def getLegend(xmin=0.55,ymin=0.5,xmax=0.9,ymax=0.887173,scale=1):
    leg = TLegend(xmin,ymin,xmax,ymax,"")
    leg.SetFillColor(kWhite);
    leg.SetFillStyle(0);
    leg.SetTextSize(0.048*scale);
    return leg
###################################################################
def getCMSTex(x=0.15,y=0.8,scale=1,text="#bf{CMS} #it{Preliminary}"):
    texCMS = TLatex(x,y,text); 
    texCMS.SetNDC();
    texCMS.SetTextFont(42);
    texCMS.SetTextSize(0.060*scale);
    return texCMS
###################################################################
def getLumiTex(lumi_label,year,x=0.58,y=0.907173,scale=1,text="%s (13 TeV, %s)"):
    texLumi = TLatex(x,y,text % (lumi_label,year)); 
    texLumi.SetNDC();
    texLumi.SetTextFont(42);
    texLumi.SetTextSize(0.048*scale);
    return texLumi
###################################################################
def getCMSText(lumi_label,year,scale=1):
    texS = getLumiTex(lumi_label,year,scale=scale)
    texS.Draw();
    texS1 = getCMSTex(scale=scale)
    texS1.Draw();

    return texS,texS1
###################################################################

def RatioStyle(ratio,rymin=0.65,rymax=1.35,color=kBlack,xname=None,yname='Data/Bkg'):
    ratio.SetStats(0);
    ratio.SetMarkerColor(color)
    ratio.SetLineColor(color)
    ratio.SetLineWidth(1)
    ratio.SetMarkerStyle(20);
    ratio.SetMarkerSize(1.1);

    ratio.GetYaxis().CenterTitle();
    ratio.GetYaxis().SetTitle(yname)
    ratio.GetYaxis().SetLabelSize(0.12);
    ratio.GetYaxis().SetTitleSize(0.12);
    ratio.GetYaxis().SetLabelFont(42);
    ratio.GetYaxis().SetTitleFont(42);
    ratio.GetYaxis().SetTitleOffset(0.35);
    ratio.GetYaxis().SetNdivisions(208);
    ratio.GetYaxis().SetRangeUser(rymin,rymax);

    if xname is not None and xname is not 'Cutflow': ratio.GetXaxis().SetTitle(xname)
    ratio.GetXaxis().SetLabelSize(0.15);
    ratio.GetXaxis().SetTitleSize(0.15);
    ratio.GetXaxis().SetLabelFont(42);
    ratio.GetXaxis().SetTitleFont(42);
    ratio.GetXaxis().SetTitleOffset(1.1);
    ratio.GetXaxis().SetTickLength(0.05);
###################################################################

def getRatioLine(xmin,xmax):
    line = TLine(xmin, 1.,xmax, 1.);
    line.SetLineStyle(8);
    line.SetLineColor(kBlack);
    return line
###################################################################

def StackStyle(hs_stack,yscale=5,scaleWidth=False):
    hs_stack.GetYaxis().SetTitle("Events" if not scaleWidth else "Events / GeV");
    hs_stack.GetYaxis().SetTitleOffset(1.5);
    hs_stack.SetTitle("");
    ymax = hs_stack.GetMaximum()*pow(10,yscale)
    ymin = pow(10,-2)

    hs_stack.SetMaximum(ymax)
    hs_stack.SetMinimum(ymin)
###################################################################

def makeXaxis(xmin,xmax,ymin,ndiv,name=None):
    xaxis = TGaxis(xmin,ymin,xmax,ymin,xmin,xmax,ndiv);
    if name != None: xaxis.SetTitle(name);
    xaxis.SetLabelFont(42);
    xaxis.SetLabelSize(0.10);
    xaxis.SetTitleFont(42);
    xaxis.SetTitleSize(0.12);
    xaxis.SetTitleOffset(1.2);
    return xaxis
###################################################################

def XaxisCutflowStyle(xaxis,hs):
    xaxis.SetLabelOffset(-999)
    xaxis.SetTitle("");
    for i in range(1,hs.GetXaxis().GetNbins()+1):
        label = TLatex(i-0.5,xaxis.GetY1()-0.05,hs.GetXaxis().GetBinLabel(i));
	label.SetTextSize(0.065);
	label.SetTextAngle(-30.);
	label.Draw("SAME");
###################################################################

def makeYaxis(ymin,ymax,xmin,ndiv,name=None):
    if name == None: name == 'YAxis'
    yaxis = TGaxis(xmin,ymin,xmin,ymax,ymin,ymax,ndiv,"");
    yaxis.SetTitle(name);
    yaxis.SetLabelFont(42);
    yaxis.SetLabelSize(0.10);
    yaxis.SetTitleFont(42);
    yaxis.SetTitleSize(0.12);
    yaxis.SetTitleOffset(0.35);
    yaxis.SetNdivisions(4)
    yaxis.CenterTitle()
    return yaxis
###################################################################
