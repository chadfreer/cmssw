
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/CSCSegInfo.h"

void CSCSegInfo::Initialize() {
  for (auto & str : ints)  mInts .insert( std::pair<TString, int>(str, DINT) );
  for (auto & str : vFlt)  mVFlt .insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  for (auto & str : vInt)  mVInt .insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
}

void CSCSegInfo::Reset() {
  for (auto & it : mInts)  it.second = DINT;
  for (auto & it : mVFlt)  it.second.clear();
  for (auto & it : mVInt)  it.second.clear();
  INSERT(mInts, "nSegs", 0);
 // INSERT(mInts, "nSegsBX0", 0);
}

//void CSCSegInfo::Fill(const edm::Handle<CSCSegmentCollection> & cscSeg, std::vector<CSCRecHit2D> theCSCRecHits) {
//void CSCSegInfo::Fill(const edm::Handle<CSCSegmentCollection> & cscSeg) {
void CSCSegInfo::Fill(const CSCSegment cscSeg) {
//std::vector<CSCRecHit2D> theCSCRecHits
  // std::cout << "Filling CSCSegInfo" << std::endl;
  CSCDetId id  = (CSCDetId)(*cscSeg).cscDetId();


  INSERT(mInts, "nSegs", ACCESS(mInts, "nSegs") + 1 );
  //if (cscSeg.tbins() == 8) 
    //INSERT(mInts, "nSegsBX0", ACCESS(mInts, "nSegsBX0") + 1 );
/*
  INSERT(mVFlt, "seg_chi2",          CSCSegment().chi2() );
  INSERT(mVFlt, "seg_time",          CSCSegment().time() );
  INSERT(mVFlt, "seg_segx",          CSCSegment().localPosition().x() );
  INSERT(mVFlt, "seg_segy",          CSCSegment().localPosition().y() );
  INSERT(mVFlt, "seg_segDirx",       CSCSegment().localDirection().x() );
  INSERT(mVFlt, "seg_segDiry",       CSCSegment().localDirection().y() );
  //INSERT(mVFlt, "seg_segDirz",       CSCSegment().localDirection().z() );

  INSERT(mVInt, "seg_endcap",        CSCDetId().endcap() );
  INSERT(mVInt, "seg_ring",	     CSCDetId().ring() );
  INSERT(mVInt, "seg_station",       CSCDetId().station() );
  INSERT(mVInt, "seg_chamber",       CSCDetId().chamber() );
  INSERT(mVInt, "seg_nRecHits",      CSCSegment().nRecHits() );
  // std::cout << "Filled CSCSegInfo" << std::endl;
*/


  INSERT(mVFlt, "seg_chi2",          (*cscSeg).chi2() );
  INSERT(mVFlt, "seg_time",          (*cscSeg).time() );
  INSERT(mVFlt, "seg_segx",          (*cscSeg).localPosition().x() );
  INSERT(mVFlt, "seg_segy",          (*cscSeg).localPosition().y() );
  INSERT(mVFlt, "seg_segDirx",       (*cscSeg).localDirection().x() );
  INSERT(mVFlt, "seg_segDiry",       (*cscSeg).localDirection().y() );

  INSERT(mVInt, "seg_endcap",        id.endcap() );
  INSERT(mVInt, "seg_ring",          id.ring() );
  INSERT(mVInt, "seg_station",       id.station() );
  INSERT(mVInt, "seg_chamber",       id.chamber() );
  INSERT(mVInt, "seg_nRecHits",      (*cscSeg).nRecHits() );


} // End function: CSCSegInfo::Fill(const l1t::CSCSeg & cscSeg)

