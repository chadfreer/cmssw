/*Code to add segment information to branch
 *Written by Chad Freer, March, 2018
 *
 * Uses CSCDetIds for location in detector, 
 * segments for location and direction in chamber
 * and rechits for strip and wire information
*/
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

void CSCSegInfo::Fill(const CSCSegment cscSeg) {
  //Set CSCDetId to get position of segment in detector
  CSCDetId id  = (CSCDetId)(cscSeg).cscDetId();
  INSERT(mInts, "nSegs", ACCESS(mInts, "nSegs") + 1 );
  //if (cscSeg.tbins() == 8) 
    //INSERT(mInts, "nSegsBX0", ACCESS(mInts, "nSegsBX0") + 1 );

/*//cout for testing
  std::cout     << "\n chi2" 		<< (cscSeg).chi2() 
		<< "\n time" 		<< (cscSeg).time()
                << "\n segx" 		<< (cscSeg).localPosition().x()
                << "\n segy" 		<< (cscSeg).localPosition().y()
                << "\n segDirx" 	<< (cscSeg).localDirection().x()
                << "\n segDiry" 	<< (cscSeg).localDirection().y()
                << "\n segDirz"         << (cscSeg).localDirection().z()
                << "\n endcap" 		<< id.endcap()
                << "\n ring" 		<< id.ring()
                << "\n station" 	<< id.station()
                << "\n chamber" 	<< id.chamber()
                << "\n nRecHits" 	<< (cscSeg).nRecHits() 	
			<< std::endl;
*/
  INSERT(mVFlt, "seg_chi2",          (cscSeg).chi2() );
  INSERT(mVFlt, "seg_time",          (cscSeg).time() );
  INSERT(mVFlt, "seg_segx",          (cscSeg).localPosition().x() );
  INSERT(mVFlt, "seg_segy",          (cscSeg).localPosition().y() );
  INSERT(mVFlt, "seg_segDirx",       (cscSeg).localDirection().x() );
  INSERT(mVFlt, "seg_segDiry",       (cscSeg).localDirection().y() );
  INSERT(mVFlt, "seg_segDirz",       (cscSeg).localDirection().z() );
    
  INSERT(mVInt, "seg_endcap",        id.zendcap() );
  INSERT(mVInt, "seg_ring",          id.ring() );
  INSERT(mVInt, "seg_station",       id.station() );
  INSERT(mVInt, "seg_chamber",       id.chamber() );
    
  INSERT(mVInt, "seg_triggerSector", id.triggerSector() );
  INSERT(mVInt, "seg_triggerCscId",  id.triggerCscId() );
  // INSERT(mVInt, "seg_wire_layer",    id.ilayer() );
  // INSERT(mVInt, "seg_strip",         id.channel() );

  INSERT(mVInt, "seg_nRecHits",      (cscSeg).nRecHits() );

  int wire_max=-1;
  int wire_min=1000;
  int strip_max=-1;
  int strip_min=1000;
  const std::vector<CSCRecHit2D> recHits = cscSeg.specificRecHits();
  for (int iHit = 0; iHit < cscSeg.nRecHits(); iHit++) {
     const CSCRecHit2D  recHit = recHits.at(iHit);
     if (wire_max<recHit.hitWire()) wire_max=recHit.hitWire();
     if (wire_min>recHit.hitWire()) wire_min=recHit.hitWire();
     for (int i = 0; i < 3; i++){
        if (strip_max<recHit.channels(i)) strip_max=recHit.channels(i);
        if (strip_min>recHit.channels(i)) strip_min=recHit.channels(i);
     }
  }   

  INSERT(mVInt, "seg_wire_max",        wire_max );
  INSERT(mVInt, "seg_wire_min",        wire_min );
  INSERT(mVInt, "seg_strip_max",       strip_max );
  INSERT(mVInt, "seg_strip_min",       strip_min );
      
  //std::cout << "For hit " << iHit << ", wire = " << recHit.hitWire() << ", first strip = " << recHit.channels(0) << std::endl;  

} // End function: CSCSegInfo::Fill(const l1t::CSCSeg & cscSeg)

