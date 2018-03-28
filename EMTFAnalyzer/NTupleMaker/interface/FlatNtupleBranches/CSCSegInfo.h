
#ifndef FlatNtupleBranchesCSCSegInfo_h
#define FlatNtupleBranchesCSCSegInfo_h

// Common branch info
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/Common.h"

// Helpful tools
#include "EMTFAnalyzer/NTupleMaker/interface/HelperFunctions.h"

// CSC segment classes
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"

////////////////////////////////
///  EMTF track information  ///
////////////////////////////////
struct CSCSegInfo {
  std::vector<TString> ints = {{"nSegs"}};
  std::vector<TString> vFlt = {{"seg_chi2", "seg_time", "seg_segx", "seg_segy", "seg_segDirx", "seg_segDiry", "seg_segDirz"}};
  std::vector<TString> vInt = {{"seg_endcap", "seg_ring", "seg_station", "seg_chamber", "seg_triggerSector", "seg_triggerCscId", "seg_nRecHits", "seg_wire_max", "seg_wire_min", "seg_strip_max", "seg_strip_min"}};
  std::map<TString, int> mInts;
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;

  void Initialize();
  void Reset();
  void Fill(const CSCSegment cscSeg);
};


#endif  // #ifndef FlatNtupleBranchesCSCSegInfo_h
