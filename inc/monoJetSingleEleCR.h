#ifndef monoJetSingleEleCR_h
#define monoJetSingleEleCR_h

#include "monoJetAnalysis.h"

class monoJetSingleEleCR : public virtual monoJetAnalysis {
public:
  static const std::string REGION;
  int lepindex;
  TLorentzVector lep;
  float lepton_pt,lepton_eta,lepton_phi,lepMET_mt;

  TH1F *h_lepMET_MT;
  TH1F *h_LeptonPt[maxHisto], *h_LeptonEta[maxHisto],*h_LeptonPhi[maxHisto];
  
  virtual void BookHistos(int i,std::string histname);
  virtual void fillHistos(int nhist,float event_weight);
  virtual void initVars();
  virtual void initTree(TTree* tree);
  inline bool isW_or_ZJet() { return monoJetAnalysis::isW_or_ZJet() || sample.type == DYJets || sample.type == DYJets_NLO; }
  virtual float getSF(int lepindex);
  bool CRSelection(std::vector<int> tight,std::vector<int> loose);
  virtual vector<int> getJetCand(vector<int> jetlist, int lepindex);
  virtual vector<int> jet_veto(int lepindex);
  virtual bool muon_veto();
  virtual bool photon_veto(int lepindex);
  virtual bool tau_veto(int lepindex);
  virtual bool bjet_veto(int lepindex);
};

#endif
