
#ifndef FlatNtupleBranchesGenMuonInfo_h
#define FlatNtupleBranchesGenMuonInfo_h

// Common branch info
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/Common.h"

// GEN particles
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

/* // Default values for maps */
/* int       DINT  = -999; */
/* float     DFLT  = -999.; */
/* std::vector<float> DVFLT; */
/* std::vector<int>   DVINT; */


//////////////////////////////
///  GEN muon information  ///
//////////////////////////////
struct GenMuonInfo {
  std::vector<TString> ints = {{"nMuons"}};
  std::vector<TString> vFlt = {{"mu_pt", "mu_eta", "mu_theta", "mu_phi"}};
  std::vector<TString> vInt = {{"mu_charge"}};
  std::map<TString, int> mInts;
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;

  void Initialize();
  void Reset();
  void Fill(const reco::GenParticle & genMuon);
};


#endif  // #ifndef FlatNtupleBranchesGenMuonInfo_h
