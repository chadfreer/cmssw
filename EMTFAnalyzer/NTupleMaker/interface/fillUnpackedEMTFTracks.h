// -*- C++ -*-
//=============================================================
// Fill all LCTs in the event record for: 
// Package:    NTupleMaker
// Class:      NTupleMaker
//
// Written by David Curry
// ============================================================

#include <string.h>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <set>
#include <cmath>
#include <vector>


using namespace std;

void fillUnpackedEMTFTracks(DataEvtSummary_t &ev, edm::Handle<std::vector<l1t::EMTFTrack>> tracks, int printLevel) {
  
  // loop over CSCTF tracks
  int nTrk=0;
  for( auto trk = tracks->cbegin(); trk < tracks->cend(); trk++,nTrk++) {
    
    // Access the track variables
    float trPt     = trk -> Pt();
    float trGblEta = trk -> Eta();
    float trGblPhi = trk -> Phi_glob_rad();
    int trMode     = trk -> Mode();
    int trBx       = trk -> BX();

    if (printLevel > 0) {
      cout << " Unpacked EMTF Track # " << nTrk << endl;
      cout << "===========================" << endl;
      cout << " Track Pt        = " << trPt << endl ;
      cout << " Track mode      = " << trMode << endl;
      cout << " Track Eta       = " << trGblEta  << endl;
      cout << " Track Phi       = " << trGblPhi  << endl;
    }

    // Fill Track Branches
    ev.unp_trkPt   -> push_back(trPt);
    ev.unp_trkEta  -> push_back(trGblEta);
    ev.unp_trkPhi  -> push_back(trGblPhi);
    ev.unp_trkMode -> push_back(trMode);
    ev.unp_trkBx  -> push_back(trBx);

    int trBx_beg = -99;
    int trBx_end = 99;

    // Fill Track LCTs  
    int LctTrkId_ = 0;
    //for( auto lct = trk->GetCSCPrimitiveCollection().cbegin(); lct < trk->GetCSCPrimitiveCollection().cend(); lct++, LctTrkId_++) {
    
    for( auto lct = trk->PtrHits()->cbegin(); lct < trk->PtrHits()->cend(); lct++, LctTrkId_++) {
      
      int trlct_endcap = lct->Endcap();
      if (trlct_endcap == 2) trlct_endcap = -1;
      
      int trlct_sector   = lct->Sector();
      int trlct_station  = lct->Station();
      int trlct_ring     = lct->Ring();
      int trlct_wire     = lct->Wire();
      int trlct_strip    = lct->Strip();
      int trlct_chamber  = lct->Chamber();
      int trlct_cscID    = lct->CSC_ID();
      int trlct_bx       = lct->BX();
      if (trlct_bx > trBx_beg) trBx_beg = trlct_bx;
      if (trlct_bx < trBx_end) trBx_end = trlct_bx;
      
      // for consistency with LCT collection
      if (trlct_endcap<0) trlct_endcap = 2;
      
      if (printLevel > 0) {
	cout << "   === CSC LCT # "<< LctTrkId_ << endl;
	cout << "   Sector    = "  << trlct_sector  << endl;
	cout << "   Endcap    = "  << trlct_endcap  << endl;
	cout << "   Station   = "  << trlct_station  << endl;
	cout << "   Ring      = "  << trlct_ring  << endl;
	cout << "   Chamber   = "  << trlct_chamber  << endl;
	cout << "   cscID     = "  << trlct_cscID  << endl ;
	cout << "   Wire      = "  << trlct_wire  << endl;
	cout << "   Strip     = "  << trlct_strip  << endl << endl;
      }
      
      // Do not FIll array over their given size!!
      if (nTrk > MAXTRK-1) {
	if (printLevel > 1) cout << "-----> nTrks is greater than MAXTRK-1.  Skipping this Track..." << endl;
	continue;
      }
      
      if (LctTrkId_ > MAXTRKHITS-1) {
	if (printLevel > 1)cout << "-----> LctTrkId_ is greater than MAXTRKHITS-1.  Skipping this Track..." << endl;
	continue;
      }
      	

      ev.unp_trkLct_endcap[nTrk][LctTrkId_] = trlct_endcap;
            
      // sector (end 1: 1->6, end 2: 7 -> 12)
      //if ( trlct_endcap == 1)
      ev.unp_trkLct_sector[nTrk][LctTrkId_] = trlct_sector;
      //else
      //	trLctSector[nTrk][LctTrkId_] = 6+trlct_sector;
      
      ev.unp_trkLct_station[nTrk][LctTrkId_] = trlct_station;
      
      ev.unp_trkLct_ring[nTrk][LctTrkId_] = trlct_ring;
      
      ev.unp_trkLct_chamber[nTrk][LctTrkId_] = trlct_chamber;
      
      ev.unp_trkLct_cscId[nTrk][LctTrkId_] = trlct_cscID;
      
      ev.unp_trkLct_wire[nTrk][LctTrkId_] = trlct_wire;
      
      ev.unp_trkLct_strip[nTrk][LctTrkId_] = trlct_strip;
      
      ev.unp_trkLct_bx[nTrk][LctTrkId_] = trlct_bx;

      ev.unp_trkLct_qual[nTrk][LctTrkId_] = lct->Quality();

      ev.unp_trkLct_pattern[nTrk][LctTrkId_] = lct->Pattern();
      
    } // end track LCT loop
    
    ev.unp_trkBxBeg  -> push_back(trBx_beg);
    ev.unp_trkBxEnd  -> push_back(trBx_end);
    ev.numUnpTrkLCTs -> push_back(LctTrkId_);
    
  } // end track loop

  ev.numUnpTrks = nTrk;


} // end fill Tracks
