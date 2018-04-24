
#ifndef FlatNtupleBranchesEMTFUnpTrackInfo_h
#define FlatNtupleBranchesEMTFUnpTrackInfo_h

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
struct EMTFUnpTrackInfo {
  std::vector<TString> ints = {{"nUnpTracks", "nUnpTracksBX0"}};
  std::vector<TString> vFlt = {{"unp_trk_pt", "unp_trk_eta", "unp_trk_theta", "unp_trk_phi", "unp_trk_phi_loc"}};
  std::vector<TString> vInt = {{"unp_trk_pt_int", "unp_trk_eta_int", "unp_trk_theta_int", "unp_trk_phi_int", "unp_trk_BX","unp_trk_endcap", 
				"unp_trk_sector", "unp_trk_sector_index", "unp_trk_mode", "unp_trk_mode_CSC", "unp_trk_mode_RPC", "unp_trk_mode_neighbor",
				"unp_trk_charge", "unp_trk_nHits", "unp_trk_nRPC", "unp_trk_nNeighbor", "unp_trk_found_hits",
                                "unp_trk_dBX", "unp_trk_dPhi_int", "unp_trk_dTheta_int"}};
  std::vector<TString> vvInt = {{"unp_trk_iHit"}};
  std::map<TString, int> mInts;
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;
  std::map<TString, std::vector<std::vector<int> > > mVVInt;

  void Initialize();
  void Reset();
  void Fill(const l1t::EMTFTrack & emtfTrk, const EMTFHitInfo & hits);
};


#endif  // #ifndef FlatNtupleBranchesEMTFUnpTrackInfo_h
