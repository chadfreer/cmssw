
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/RecoMuonInfo.h"

void RecoMuonInfo::Initialize() {
  for (auto & str : ints)  mInts .insert( std::pair<TString, int>(str, DINT) );
  for (auto & str : vFlt)  mVFlt .insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  for (auto & str : vInt)  mVInt .insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
}

void RecoMuonInfo::Reset(){
  for (auto & it : mInts)  it.second = DINT;
  for (auto & it : mVFlt)  it.second.clear();
  for (auto & it : mVInt)  it.second.clear();
  INSERT(mInts, "nRecoMuons", 0);
}

void RecoMuonInfo::Fill(const reco::Muon mu, const reco::Vertex vertex,
			PropagateToMuon muProp1st, PropagateToMuon muProp2nd,
			const float min_eta, const float max_eta) {

  // Propagate muon phi and eta coordinates to muon chambers
  float eta_St1   = -999.;
  float theta_St1 = -999.;
  float phi_St1   = -999.;
  float eta_St2   = -999.;
  float theta_St2 = -999.;
  float phi_St2   = -999.;
  
  TrajectoryStateOnSurface station1 = muProp1st.extrapolate(mu);
  if (station1.isValid()) {
    eta_St1   = station1.globalPosition().eta();
    theta_St1 = emtf::range_theta_deg( emtf::calc_theta_deg( eta_St1 ) );
    phi_St1   = station1.globalPosition().phi();
    phi_St1   = emtf::rad_to_deg( phi_St1 );
  }
  
  TrajectoryStateOnSurface station2 = muProp2nd.extrapolate(mu);
  if (station2.isValid()) {
    eta_St2   = station2.globalPosition().eta();
    theta_St2 = emtf::range_theta_deg( emtf::calc_theta_deg( eta_St2 ) );
    phi_St2   = station2.globalPosition().phi();
    phi_St2   = emtf::rad_to_deg( phi_St2 );
  }
  
  // RECO muon selection cuts
  if (abs(mu.eta()) < min_eta || abs(mu.eta()) > max_eta) return;
  if (abs(eta_St1)  < min_eta || abs(eta_St1)  > max_eta) return;
  if (not muon::isLooseMuon(mu) ) return;
  
  INSERT(mInts, "nRecoMuons", ACCESS(mVFlt, "reco_pt").size() + 1);
  
  INSERT(mVInt, "reco_ID_loose",  muon::isLooseMuon(mu) );
  INSERT(mVInt, "reco_ID_medium", muon::isMediumMuon(mu) );
  INSERT(mVInt, "reco_ID_tight",  muon::isTightMuon(mu, vertex) );
  INSERT(mVInt, "reco_charge",    mu.charge() );
  INSERT(mVFlt, "reco_pt",        mu.pt() );
  INSERT(mVFlt, "reco_eta",       mu.eta() );
  INSERT(mVFlt, "reco_eta_St1",   eta_St1 );
  INSERT(mVFlt, "reco_eta_St2",   eta_St2 );
  INSERT(mVFlt, "reco_theta",     emtf::range_theta_deg( emtf::calc_theta_deg( mu.eta() ) ) );
  INSERT(mVFlt, "reco_theta_St1", theta_St1 );
  INSERT(mVFlt, "reco_theta_St2", theta_St2 );
  INSERT(mVFlt, "reco_phi",       emtf::rad_to_deg( mu.phi() ) );
  INSERT(mVFlt, "reco_phi_St1",   phi_St1 );
  INSERT(mVFlt, "reco_phi_St2",   phi_St2 );
}
