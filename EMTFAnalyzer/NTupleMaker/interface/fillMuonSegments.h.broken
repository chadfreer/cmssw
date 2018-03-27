//=============================================================
// Fill all REco Muons in the event record for:
// Package:    NTupleMaker
// Class:      NTupleMaker
//
// Written by David Curry
// ============================================================

#include <iostream>
#include <fstream>
#include <set>
#include <cmath>
#include <vector>
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"

#include "../plugins/SegmentLCTMatchBox.h"



using namespace std;
using namespace edm;
using namespace reco;



void fillSegmentsMuons(DataEvtSummary_t &ev, 
		       edm::Handle<reco::MuonCollection> muons, 
		       edm::Handle<CSCSegmentCollection> cscSegs, 
		       edm::ESHandle<CSCGeometry> cscGeom,
		       // const edm::Handle<CSCCorrelatedLCTDigiCollection> CSCTFlcts,
		       edm::Handle<std::vector<l1t::EMTFHit>> LCTs,
		       int printLevel) {


  // class container for the segment and number of hits matching the global muon
  class Segment {
  public:
    const CSCSegment cscsegcand;
    int nMatchedHits;
  Segment(const CSCSegment &seg, int nMHits):cscsegcand(seg), nMatchedHits(nMHits){};
  };
  
  typedef std::vector<Segment*> SegmentVector;
  
  // return a vector containing the segments associated to the muon
  //SegmentVector* SegmentsInMuon(const reco::Muon* muon, const CSCSegmentCollection* segments, edm::ESHandle<CSCGeometry> cscGeom, int printLevel);

  
  // importing directly Ivan's object...
  SegmentLCTMatchBox _matchBox;
  
  _matchBox.setPrintLevel(printLevel);
  
  // Given a muon candidate, loop over the segments and
  // find the segments belonging to the muon and see
  // if they are "LCTAble" (i.e. could generate an LCT)

  int whichMuon = -1;
  for (auto muon = muons->begin(); muon != muons->end(); muon++) {

    // Same as in fillRecoMuons.h ... really shouldn't do this manually - AWB 19.07.16
    if ( !(muon::isLooseMuon((*muon))) ) continue;
    whichMuon += 1;

    if (whichMuon > (MAX_MUONS-1) ) {
      cout << "the muon has " << whichMuon << ", but the MAX allowed is "
           << MAX_MUONS << " -> Skipping the muon... " << endl;
      continue;
    }
    
    // Need a stand-alone component to match segments
    if ( !(muon->isStandAloneMuon()) ) continue;
    
    // Get the segments which match the muon candidate.  Comes from class defined below
    // SegmentVector *segVect = SegmentsInMuon( &(*muon), &(*cscSegs), cscGeom, printLevel);
    
    SegmentVector *segVect = new SegmentVector();
    int nMuonMatchedHits=0;
    int icscSegment=0;
    
    // --------- Loop over the CSC segments -------------
    for (auto segIter = cscSegs->begin(); segIter != cscSegs->end(); segIter++){
      
      bool isSegMatched = false;
      
      int nHits=segIter -> nRecHits();

      if (printLevel > 3) {
	cout << " ======================================== " << endl;
	cout << "Segment in CSC:" << icscSegment++ << endl;
	cout << "# segs hits:"    << nHits      << endl;
      }

      if (icscSegment > MAX_SEGS_STD-1) continue;
      
      const std::vector<CSCRecHit2D>& theHits = segIter -> specificRecHits();
      std::vector<CSCRecHit2D>::const_iterator hitIter;
      
      int iHit=0;
      // loop over the segments hits
      for (hitIter = theHits.begin(); hitIter!= theHits.end(); hitIter++){
	
	if (printLevel>2) std::cout << "iHit:" << iHit++ << ", ";
	
	// check if the hit will match the standalone muon component
	bool isHitMatched=false;
	
	LocalPoint seghitlocal = hitIter -> localPosition();
	
	double segHitX = seghitlocal.x();
	double segHitY = seghitlocal.y();
	
	if (printLevel > 3)
	  std::cout << "segHitX="<<segHitX <<  ", "
		    << "segHitY="<<segHitY;
	
	// The muon now returns segments (2012), while in 2010 it was returning hits...
	for(trackingRecHit_iterator segm  = muon->outerTrack()->recHitsBegin();
	    segm != muon->outerTrack()->recHitsEnd();
	    segm++){
	  
	  // some basic protection
	  if ( !((*segm)->isValid()) ) continue;
	  
	  // Hardware ID of the RecHit (in terms of wire/strips/chambers)
	  DetId detid = (*segm)->geographicalId();
	  
	  // Interested in muon systems only
	  if( detid.det() != DetId::Muon ) continue;
	  
	  //Look only at CSC Hits (CSC id is 2)
	  if (detid.subdetId() != MuonSubdetId::CSC) continue;
	  
	  CSCDetId id(detid.rawId());
	  
	  // another sanity check
	  if  (id.station() < 1) continue;
	  
	  // get the CSCSegment
	  const CSCSegment* cscSegment = dynamic_cast<const CSCSegment*>(&**segm);
	  // check the segment is not NULL
	  if (cscSegment == NULL) continue;
	  
	  // try to get the CSC recHits that contribute to this segment.
	  std::vector<CSCRecHit2D> theseRecHits = (*cscSegment).specificRecHits();
	  
	  // loop over the rechits
	  for ( std::vector<CSCRecHit2D>::const_iterator iRH = theseRecHits.begin();
		iRH != theseRecHits.end(); iRH++) {
	    
	    // get the rechit ID
	    CSCDetId idRH = (CSCDetId)(*iRH).cscDetId();
	    
	    // CSC chamber
	    const CSCChamber* cscchamber = cscGeom->chamber(idRH);
	    if (!cscchamber) continue;
	    
	    // local position
	    LocalPoint rhitlocal = iRH->localPosition();
	    
	    if (segHitX==rhitlocal.x() && segHitY==rhitlocal.y() ) {
	      isHitMatched = true;
	      isSegMatched = true;
	    }

	  } // end loop over hits of a segment
	  
	} // end loop trackingRecHit_iterator (segments of a muon)
	
	if (printLevel > 4 ){
	  if (isHitMatched) cout<< " -> Matched" << endl;
	  else              cout<< " -> NOT Matched" << endl;
	}
	
	if (isHitMatched) nMuonMatchedHits++;
	
      }
      
      if (printLevel > 4) cout<< "segment has "  << nMuonMatchedHits
			      << " hits out of " << nHits
			      << " matched"      << endl;
      
      // fill the the vector with the matching segments
      if (nMuonMatchedHits!=0 && isSegMatched) {
	Segment* segment = new Segment(*segIter, nMuonMatchedHits);
	segVect -> push_back(segment);
      }

      
    }  // end loop on the CSC segments
    
    
    if (printLevel > 3)
      cout << "The muon has " << segVect -> size()    << " csc segments"     << endl;
    
    ev.recoNumCscSegs -> push_back(segVect->size());

    // sanity check
    if (segVect -> size() == 0) {
      delete segVect;
      continue;
    }
    
    if (printLevel > 3) cout << "Looping over the CSC segments\n\n";

    int iSegment = 0;
    for (auto segmentCSC = segVect -> begin(); segmentCSC != segVect->end(); segmentCSC++, iSegment++){
      

      if (printLevel > 3) {
        printf("#############\n");
        printf("Segment  #%d\n", iSegment);
        printf("#############\n\n");
	

	if ( iSegment > (MAX_SEGS_STD-1) ) {
          cout << "the muon has " << iSegment+1 << ", but the MAX allowed is "
	       << MAX_SEGS_STD << " -> Skipping the segment... " << endl;
          continue;
        }
      }
      
      // basic info
      CSCDetId id  = (CSCDetId) (*segmentCSC)->cscsegcand.cscDetId();
      const CSCChamber* cscchamber = cscGeom->chamber(id);

      if (!cscchamber) {
        cout << "cscchamber not valid" << endl;
        continue;
      }
      
      ev.recoCscSeg_sector [whichMuon][iSegment] = CSCTriggerNumbering::triggerSectorFromLabels(id);;
      ev.recoCscSeg_endcap [whichMuon][iSegment] = id.endcap();
      ev.recoCscSeg_station[whichMuon][iSegment] = id.station();
      ev.recoCscSeg_ring   [whichMuon][iSegment] = id.ring();
      ev.recoCscSeg_chamber[whichMuon][iSegment] = id.chamber();
      ev.recoCscSeg_nHits  [whichMuon][iSegment] = (*segmentCSC)->cscsegcand.nRecHits();
      
      if (printLevel > 3) {
	std::cout << "Endcap  = " << ev.recoCscSeg_endcap [whichMuon][iSegment] << std::endl;
	std::cout << "Ring    = " << ev.recoCscSeg_station[whichMuon][iSegment] << std::endl;
	std::cout << "Station = " << ev.recoCscSeg_ring   [whichMuon][iSegment] << std::endl;
	std::cout << "Chamber = " << ev.recoCscSeg_chamber[whichMuon][iSegment] << std::endl;
	std::cout << "nRecHits= " << ev.recoCscSeg_nHits  [whichMuon][iSegment] << std::endl << std::endl;
      }

      
      // local segment position
      LocalPoint localPos = (*segmentCSC)->cscsegcand.localPosition();
      LocalVector  segDir = (*segmentCSC)->cscsegcand.localDirection();
      
      /*
      recoCscSeg_loc_x      [whichMuon][iSegment] = localPos.x();
      recoCscSeg_loc_y      [whichMuon][iSegment] = localPos.y();
      recoCscSeg_loc_eta    [whichMuon][iSegment] = localPos.eta();
      recoCscSeg_loc_phi    [whichMuon][iSegment] = localPos.phi();
      recoCscSeg_loc_dir_eta[whichMuon][iSegment] = segDir.eta();
      recoCscSeg_loc_dir_phi[whichMuon][iSegment] = segDir.phi();

      if (printLevel > 2) {
	std::cout << "localPos.x()   = " << recoCscSeg_loc_x      [whichMuon][iSegment] << " cm"<< std::endl;
	std::cout << "localPos.y()   = " << recoCscSeg_loc_y      [whichMuon][iSegment] << " cm"<< std::endl;
	std::cout << "localPos.eta() = " << recoCscSeg_loc_eta    [whichMuon][iSegment] << std::endl;
	std::cout << "localPos.phi() = " << recoCscSeg_loc_phi    [whichMuon][iSegment] << std::endl;
	std::cout << "segDir.eta()   = " << recoCscSeg_loc_dir_eta[whichMuon][iSegment] << std::endl;
	std::cout << "segDir.phi()   = " << recoCscSeg_loc_dir_phi[whichMuon][iSegment] << std::endl << std::endl;
      }
      */

      // global segment position
      GlobalPoint globalPosition   = cscchamber->toGlobal(localPos);
      GlobalVector globalDirection = cscchamber->toGlobal(segDir);

      ev.recoCscSeg_glob_x      [whichMuon][iSegment] = globalPosition.x();
      ev.recoCscSeg_glob_y      [whichMuon][iSegment] = globalPosition.y();
      ev.recoCscSeg_glob_eta    [whichMuon][iSegment] = globalPosition.eta();
      ev.recoCscSeg_glob_phi    [whichMuon][iSegment] = globalPosition.phi();
      ev.recoCscSeg_glob_dir_eta[whichMuon][iSegment] = globalDirection.eta();
      ev.recoCscSeg_glob_dir_phi[whichMuon][iSegment] = globalDirection.phi();
      
      if (printLevel > 3) {
	std::cout << "globalPosition.x()    = " << ev.recoCscSeg_glob_x      [whichMuon][iSegment] << " cm"<< std::endl;
	std::cout << "globalPosition.y()    = " << ev.recoCscSeg_glob_y      [whichMuon][iSegment] << " cm"<< std::endl;
	std::cout << "globalPosition.eta()  = " << ev.recoCscSeg_glob_eta    [whichMuon][iSegment] << std::endl;
	std::cout << "globalPosition.phi()  = " << ev.recoCscSeg_glob_phi    [whichMuon][iSegment] << std::endl;
	std::cout << "globalDirection.eta() = " << ev.recoCscSeg_glob_dir_eta[whichMuon][iSegment] << std::endl;
	std::cout << "globalDirection.phi() = " << ev.recoCscSeg_glob_dir_phi[whichMuon][iSegment] << std::endl << std::endl;
      }
      
      /*
      // Check if segment is within DR window of RECO muon for removing bugged segments
      float dphi = ev.recoCscSeg_glob_phi[whichMuon][iSegment] - trackRef->phi();
      if (dphi > 3.14256) dphi -= 3.14256;
      if (dphi < -3.14256) dphi += 3.14256;
      float deta = ev.recoCscSeg_glob_eta[whichMuon][iSegment] - trackRef->eta();
      float dr = TMath::Sqrt(deta*deta + dphi*dphi);
      if (dr > 0.2) {
	if (printLevel > 3)  std::cout << "---> Segment is out of DR window with RECO muon" << endl;   
	ev.recoCscSeg_isMatched[whichMuon][iSegment] = -999;
	continue;
      }
      */

      // is the segment triggerable?
      bool isTriggerAble = _matchBox.isLCTAble( (*segmentCSC)->cscsegcand, 0);
      
      // is the segment matched to an LCT?
      std::vector<int> matched_IDs = _matchBox.lctsMatch( (*segmentCSC)->cscsegcand, LCTs , 0 );
      // int tmp_num_matched = 0;
      // for (uint xLCT = 0; xLCT < matched_IDs.size(); xLCT++)
	// if (matched_IDs.at(xLCT) != -999) tmp_num_matched += 1;
      // cout << "Segment is matched to " << tmp_num_matched << " LCTs" << endl;

      if (printLevel > 3) cout << "isMatched? = " << ((matched_IDs.at(0) != -999) ? 1 : 0) << endl;

      ev.recoCscSeg_isLctAble[whichMuon][iSegment] = isTriggerAble;
      ev.recoCscSeg_isMatched[whichMuon][iSegment] = (matched_IDs.at(0) != -999) ? 1 : 0;
      ev.recoCscSeg_lctId[whichMuon][iSegment] = matched_IDs.at(0);

    } // end segment loop
    //delete segVect;
    
  } // end muon loop
  
} // end fill SegmentsMuon


