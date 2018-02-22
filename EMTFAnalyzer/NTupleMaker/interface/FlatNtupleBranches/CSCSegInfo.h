
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
  //std::vector<TString> vFlt = {{"seg_eta"}};
  //std::vector<TString> vFlt = {{"seg_chi2", "seg_time", "seg_segx", "seg_segy", "seg_segDirx", "seg_segDiry", "seg_Dirz"}};
  std::vector<TString> vFlt = {{"seg_chi2", "seg_time", "seg_segx", "seg_segy", "seg_segDirx", "seg_segDiry"}};
  std::vector<TString> vInt = {{"seg_endcap", "seg_ring", "seg_station", "seg_chamber", "seg_nRecHits"}};
  std::map<TString, int> mInts;
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;

  void Initialize();
  void Reset();
  //void Fill(const edm::Handle<CSCSegmentCollection> & cscSeg, std::vector<CSCRecHit2D> theCSCRecHits);
  //void Fill(const edm::OwnVector<CSCSegment> & cscSeg);
  //void Fill(const CSCSegment cscSeg);
  //void Fill(const edm::Handle<CSCSegmentCollection> & cscSeg);
  void Fill(const CSCSegment cscSeg);
};


#endif  // #ifndef FlatNtupleBranchesCSCSegInfo_h
