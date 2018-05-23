
#ifndef FlatNtupleBranchesEMTFTrackInfo_h
#define FlatNtupleBranchesEMTFTrackInfo_h

// Common branch info
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/Common.h"

// Helpful tools
#include "EMTFAnalyzer/NTupleMaker/interface/HelperFunctions.h"

// EMTF classes
#include "DataFormats/L1TMuon/interface/EMTFHit.h"
#include "DataFormats/L1TMuon/interface/EMTFTrack.h"

/* // Default values for maps */
/* int       DINT  = -999; */
/* float     DFLT  = -999.; */
/* std::vector<float> DVFLT; */
/* std::vector<int>   DVINT; */
/* std::vector<std::vector<int> > DVVINT; */


////////////////////////////////
///  EMTF track information  ///
////////////////////////////////
struct EMTFTrackInfo {
  std::vector<TString> ints = {{"nTracks", "nTracksBX0"}};
  std::vector<TString> vFlt = {{"trk_pt", "trk_eta", "trk_theta", "trk_phi", "trk_phi_loc"}};
  std::vector<TString> vInt = {{"trk_pt_int", "trk_eta_int", "trk_theta_int", "trk_phi_int", "trk_BX", "trk_endcap", 
				"trk_sector", "trk_sector_index", "trk_mode", "trk_mode_CSC", "trk_mode_RPC", "trk_mode_neighbor",
				"trk_charge", "trk_nHits", "trk_nRPC", "trk_nNeighbor",
                                "trk_dBX", "trk_dPhi_int", "trk_dTheta_int"}};
  std::vector<TString> vvInt = {{"trk_iHit"}};
  std::map<TString, int> mInts;
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;
  std::map<TString, std::vector<std::vector<int> > > mVVInt;

  void Initialize();
  void Reset();
  void Fill(const l1t::EMTFTrack & emtfTrk, const EMTFHitInfo & hits);
};


#endif  // #ifndef FlatNtupleBranchesEMTFTrackInfo_h
