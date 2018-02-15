
#ifndef FlatNtupleBranchesEMTFHitInfo_h
#define FlatNtupleBranchesEMTFHitInfo_h

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


//////////////////////////////
///  EMTF hit information  ///
//////////////////////////////
struct EMTFHitInfo {
  std::vector<TString> ints = {{"nHits", "nHitsCSC", "nHitsRPC", "nHitsBX0", "nHitsCSCBX0", "nHitsRPCBX0"}};
  std::vector<TString> vFlt = {{"hit_eta", "hit_theta", "hit_phi", "hit_phi_loc"}};
  std::vector<TString> vInt = {{"hit_eta_int", "hit_theta_int", "hit_phi_int", "hit_endcap", "hit_sector", "hit_sector_index", "hit_station", 
				"hit_ring", "hit_CSC_ID", "hit_chamber", "hit_FR", "hit_pattern", "hit_quality", "hit_alct_quality", "hit_clct_quality", "hit_roll", "hit_subsector", 
				"hit_isCSC", "hit_isRPC", "hit_valid", "hit_BX", "hit_strip", "hit_strip_hi", "hit_strip_low", "hit_wire", "hit_neighbor"}};
  std::map<TString, int> mInts;
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;

  void Initialize();
  void Reset();
  void Fill(const l1t::EMTFHit & emtfHit);
};


/////////////////////////////////
///  Print out for debugging  ///
/////////////////////////////////

inline void PrintEMTFHit( const l1t::EMTFHit & hit ) {
  if (hit.Is_CSC()) {
    std::cout << "CSC LCT in BX " << hit.BX() << ", endcap " << hit.Endcap() << ", sector " << hit.Sector()
              << " (" << hit.Sector_idx() << "), subsector " << hit.Subsector() << ", station " << hit.Station()
              << ", ring " << hit.Ring() << ", CSC ID " << hit.CSC_ID() << ", chamber " << hit.Chamber()
              << ", pattern " << hit.Pattern() << ", quality " << hit.Quality()
              << ", strip " << hit.Strip() << ", wire " << hit.Wire() << std::endl;
  } 
  else if (hit.Is_RPC()) {
    std::cout << "RPC hit in BX " << hit.BX() << ", endcap " << hit.Endcap() << ", sector " << hit.Sector()
	      << " (" << hit.Sector_idx() << "), subsector " << hit.Subsector() << ", station " << hit.Station()
	      << ", ring " << hit.Ring() << ", chamber " << hit.Chamber()
	      << ", theta " << hit.Theta_fp() << ", phi " << hit.Phi_fp() << std::endl;
  }
  else std::cout << "EMTF hit is neither CSC nor RPC?!?" << std::endl;
}

inline void PrintHit( const std::map<TString, std::vector<int> > * iHit , const int i) {

  if (ACCESS(*iHit, "hit_isCSC").at(i)) {
    std::cout << "* Found in BX " << ACCESS(*iHit, "hit_BX").at(i) << ", endcap " << ACCESS(*iHit, "hit_endcap").at(i)
              << ", sector " << ACCESS(*iHit, "hit_sector").at(i) << " (" << ACCESS(*iHit, "hit_sector_index").at(i)
              << "), subsector " << ACCESS(*iHit, "hit_subsector").at(i) << ", station " << ACCESS(*iHit, "hit_station").at(i)
              << ", ring " << ACCESS(*iHit, "hit_ring").at(i) << ", CSC ID " << ACCESS(*iHit, "hit_CSC_ID").at(i)
              << ", chamber " << ACCESS(*iHit, "hit_chamber").at(i) << ", pattern " << ACCESS(*iHit, "hit_pattern").at(i)
              << ", quality " << ACCESS(*iHit, "hit_quality").at(i) << ", strip " << ACCESS(*iHit, "hit_strip").at(i)
              << ", wire " << ACCESS(*iHit, "hit_wire").at(i) << std::endl;
  }
  else if (ACCESS(*iHit, "hit_isRPC").at(i)) {
    std::cout << "* Found in BX " << ACCESS(*iHit, "hit_BX").at(i) << ", endcap " << ACCESS(*iHit, "hit_endcap").at(i)
	      << ", sector " << ACCESS(*iHit, "hit_sector").at(i) << " (" << ACCESS(*iHit, "hit_sector_index").at(i)
	      << "), subsector " << ACCESS(*iHit, "hit_subsector").at(i) << ", station " << ACCESS(*iHit, "hit_station").at(i)
	      << ", ring " << ACCESS(*iHit, "hit_ring").at(i) << ", chamber " << ACCESS(*iHit, "hit_chamber").at(i)
	      << ", theta " << ACCESS(*iHit, "hit_theta_int").at(i) << ", phi " << ACCESS(*iHit, "hit_phi_int").at(i) << std::endl;
  }
  else std::cout << "iHit with index " << i << " is neither CSC nor RPC?!?" << std::endl;
}

#endif  // #ifndef FlatNtupleBranchesEMTFHitInfo_h
