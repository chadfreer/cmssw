#ifndef MatcherSegLCTSegMatcher_h
#define MatcherSegLCTSegMatcher_h

// Common branch info
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/Common.h"

//specific branches to grab
#include "EMTFAnalyzer/NTupleMaker/interface/HelperFunctions.h"
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/CSCSegInfo.h"
#include "DataFormats/L1TMuon/interface/EMTFHit.h"
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EMTFHitInfo.h"

////////////////////////////////
///  Matching variables      ///
////////////////////////////////

struct LCTSegMatcher {
  std::vector<TString> ints = {{"numFills"}};
  std::vector<TString> vFlt = {{"segment_time"}};
  std::vector<TString> vInt = {{"segment_nRecHits"}};
  std::map<TString, int> mInts;
  std::map<TString, std::vector<float> > mVFlt;
  std::map<TString, std::vector<int> > mVInt;

  void Initialize();
  void Reset();
  void Fill(const CSCSegInfo & cscSegs, const EMTFHitInfo & emtfHits);
};

#endif
