
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/GenMuonInfo.h"

void GenMuonInfo::Initialize() {
  for (auto & str : ints)  mInts.insert( std::pair<TString, int>(str, DINT) );
  for (auto & str : vFlt)  mVFlt.insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  for (auto & str : vInt)  mVInt.insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
}

void GenMuonInfo::Reset() {
  for (auto & it : mInts) it.second = DINT;
  for (auto & it : mVFlt) it.second.clear();
  for (auto & it : mVInt) it.second.clear();
  INSERT(mInts, "nMuons", 0);
}

void GenMuonInfo::Fill(const reco::GenParticle & genMuon) {
  // std::cout << "Filling GenMuonInfo" << std::endl;
  float _theta = genMuon.theta() * 180. / M_PI;
  if (_theta > 180) _theta -= 360;
  if (_theta >  90) _theta  = 180. - _theta;
  float _phi = genMuon.phi() * 180. / M_PI;
  if (_phi > 180) _phi -= 360;

  INSERT(mInts, "nMuons", ACCESS(mVFlt, "mu_pt").size() + 1);

  INSERT(mVFlt, "mu_pt",     genMuon.pt() );
  INSERT(mVFlt, "mu_eta",    genMuon.eta() );
  INSERT(mVFlt, "mu_theta",  _theta );
  INSERT(mVFlt, "mu_phi",    _phi );
  INSERT(mVInt, "mu_charge", genMuon.charge() );
  // std::cout << "Filled GenMuonInfo" << std::endl;
} // End function: GenMuonInfo::Fill(const reco::GenParticle & genMuon)
