#ifndef FlatNtupleBranchesRecoMuonInfo_h
#define FlatNtupleBranchesRecoMuonInfo_h

// Common branch info
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/Common.h"

// Helpful tools
#include "EMTFAnalyzer/NTupleMaker/interface/HelperFunctions.h"

// RECO muons
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"

// RECO vertex
#include "DataFormats/VertexReco/interface/Vertex.h"

// Muon propator
#include "MuonAnalysis/MuonAssociators/interface/PropagateToMuon.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"


////////////////////////////////
///  RECO muon  information  ///
////////////////////////////////

struct RecoMuonInfo {
  std::vector<TString> ints = {{"nRecoMuons"}};
  std::vector<TString> vFlt = {{"reco_pt", "reco_eta", "reco_eta_St1", "reco_eta_St2", 
				"reco_theta", "reco_theta_St1", "reco_theta_St2", 
				"reco_phi", "reco_phi_St1", "reco_phi_St2"}};
  std::vector<TString> vInt = {{"reco_ID_loose", "reco_ID_medium", "reco_ID_tight", "reco_charge"}};
  std::map<TString, int> mInts;
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;

  void Initialize();
  void Reset();
  void Fill(const reco::Muon mu, const reco::Vertex vertex, 
	    PropagateToMuon muProp1st, PropagateToMuon muProp2nd,
	    const float min_eta, const float max_eta);
};

#endif
