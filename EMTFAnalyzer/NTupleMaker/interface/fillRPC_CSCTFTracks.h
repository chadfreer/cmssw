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

void fillRPC_CSCTFTracks(DataEvtSummary_t &ev, edm::Handle<std::vector<L1TMuon::InternalTrack>> tracks, int printLevel) {

  // loop over CSCTF tracks
  int nTrk=0;
  for( auto trk = tracks->cbegin(); trk < tracks->cend(); trk++,nTrk++) {
    
    // Access the track variables
    float trPt          = trk -> pt;
    float trGblEta      = trk -> gblEta;
    float trGblPhi      = trk -> gblPhi;
    int trMode          = trk -> trkMode;
    int isRPC           = trk -> isRPC_cand;
    
    if (printLevel > 0) {
      cout << " RPC Track # " << nTrk << endl;
      cout << "===========================" << endl;
      cout << " RPC Track Pt        = " << trPt << endl ;
      cout << " RPC Track mode      = " << trMode << endl;
      cout << " RPC Track Eta       = " << trGblEta  << endl;
      cout << " RPC Track Phi       = " << trGblPhi  << endl;
      cout << " RPC Cand            = " << isRPC  << endl;
      //cout << " Track Quality   = " << trQuality  << endl;
    }


    // Fill Track Branches
    ev.trkPt_rpc   -> push_back(trPt);
    ev.trkEta_rpc  -> push_back(trGblEta);
    ev.trkPhi_rpc  -> push_back(trGblPhi);
    ev.trkMode_rpc -> push_back(trMode);
    ev.isRPC_cand  -> push_back(isRPC);

  } // end track loop

  ev.numTrks_rpc = nTrk;

} // end fill Tracks
