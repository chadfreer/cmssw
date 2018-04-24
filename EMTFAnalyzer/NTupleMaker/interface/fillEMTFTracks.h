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

void fillEMTFTracks(DataEvtSummary_t &ev, edm::Handle<std::vector<l1t::EMTFTrack>> tracks, int printLevel) {
  
    // loop over CSCTF tracks
  int nTrk=0;
  for( auto trk = tracks->cbegin(); trk < tracks->cend(); trk++,nTrk++) {
    
    // Access the track variables
    float trPt     = trk -> Pt();
    float trGblEta = trk -> Eta();
    float trGblPhi = trk -> Phi_glob_rad();
    int trMode     = trk -> Mode();
    int trBx       = trk -> First_BX();

    if (printLevel > 0) {
      cout << " CSC Track # " << nTrk << endl;
      cout << "===========================" << endl;
      cout << " Track Pt        = " << trPt << endl ;
      cout << " Track mode      = " << trMode << endl;
      cout << " Track Eta       = " << trGblEta  << endl;
      cout << " Track Phi       = " << trGblPhi  << endl;
    }

    // Fill Track Branches
    ev.trkPt   -> push_back(trPt);
    ev.trkEta  -> push_back(trGblEta);
    ev.trkPhi  -> push_back(trGblPhi);
    ev.trkMode -> push_back(trMode);
    ev.trkBx  -> push_back(trBx);
    ev.trkRank -> push_back( trk->Rank() );
    ev.trkStraight -> push_back( trk->Straightness() );

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
      float trlct_globPhi = lct->Phi_glob_rad();
      float trlct_geomphi = lct->Phi_geom_rad();
      float trlct_eta = lct->Eta();
      int trlct_locphi   = lct->Phi_loc_rad();
      int trlct_loctheta = lct->Theta_loc();
      int trlct_bx       = lct->BX();
      if (trlct_bx > trBx_beg) trBx_beg = trlct_bx;
      if (trlct_bx < trBx_end) trBx_end = trlct_bx;

      if (trlct_station < 1 || trlct_station > 4) std::cout << "Station = " << trlct_station << std::endl;
      
      // for consistency with LCT collection
      if (trlct_endcap<0) trlct_endcap = 2;
      
      if (printLevel > 0) {
	cout << "   === CSC LCT # "<< LctTrkId_ << endl;
	cout << "   Phi       = "  << trlct_globPhi << endl;
	cout << "   Eta       = "  << trlct_eta << endl;
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
      	

      ev.trkLct_endcap[nTrk][LctTrkId_] = trlct_endcap;
            
      // sector (end 1: 1->6, end 2: 7 -> 12)
      //if ( trlct_endcap == 1)
      ev.trkLct_sector[nTrk][LctTrkId_] = trlct_sector;
      //else
      //	trLctSector[nTrk][LctTrkId_] = 6+trlct_sector;
      
      ev.trkLct_station[nTrk][LctTrkId_] = trlct_station;
      
      ev.trkLct_ring[nTrk][LctTrkId_] = trlct_ring;
      
      ev.trkLct_chamber[nTrk][LctTrkId_] = trlct_chamber;
      
      ev.trkLct_cscId[nTrk][LctTrkId_] = trlct_cscID;
      
      ev.trkLct_wire[nTrk][LctTrkId_] = trlct_wire;
      
      ev.trkLct_strip[nTrk][LctTrkId_] = trlct_strip;
      
      ev.trkLct_globPhi[nTrk][LctTrkId_] = trlct_globPhi;
      
      ev.trkLct_geomPhi[nTrk][LctTrkId_] = trlct_geomphi;
      
      ev.trkLct_eta[nTrk][LctTrkId_] = trlct_eta;

      ev.trkLct_locPhi[nTrk][LctTrkId_] = trlct_locphi;
      
      ev.trkLct_locTheta[nTrk][LctTrkId_] = trlct_loctheta;
      
      ev.trkLct_bx[nTrk][LctTrkId_] = trlct_bx;

      ev.trkLct_qual[nTrk][LctTrkId_] = lct->Quality();

      ev.trkLct_pattern[nTrk][LctTrkId_] = lct->Pattern();
      
    } // end track LCT loop
    
    ev.trkBxBeg  -> push_back(trBx_beg);
    ev.trkBxEnd  -> push_back(trBx_end);
    ev.numTrkLCTs -> push_back(LctTrkId_);
    
  } // end track loop

  ev.numTrks = nTrk;


} // end fill Tracks
