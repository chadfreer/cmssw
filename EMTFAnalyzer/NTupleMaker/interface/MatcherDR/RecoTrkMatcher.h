#ifndef MatcherDRRecoTrkMatcher_h
#define MatcherDRRecoTrkMatcher_h

// Common branch info
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/Common.h"

// Input
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/RecoMuonInfo.h"
#include "DataFormats/L1TMuon/interface/EMTFHit.h"
#include "DataFormats/L1TMuon/interface/EMTFTrack.h"
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EMTFHitInfo.h"
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EMTFTrackInfo.h"

////////////////////////////////
///  Matching variables      ///
////////////////////////////////

struct RecoTrkMatcher {
  std::vector<TString> vFlt = {{"reco_match_trk_dR", "reco_match_trk_dPhi", "reco_match_trk_dEta"}};
  std::vector<TString> vInt = {{"reco_match_iTrk"}};
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;
  
  void Initialize();
  void Reset();
  void Fill(const RecoMuonInfo & recoMuons, const EMTFTrackInfo & emtfTrks, const float min_eta, const float max_eta);
};

#endif
