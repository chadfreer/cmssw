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

using namespace std;
using namespace edm;
using namespace reco;


bool fillRecoMuons(DataEvtSummary_t &ev, edm::Handle<reco::MuonCollection> muons, 
		   edm::Handle<std::vector<reco::Vertex>> vertices, int printLevel) {
  
  bool tagExists = false;
  bool probeExists = false;

  int numMuons = 0;
  for (MuonCollection::const_iterator muon=muons->begin(); muon!=muons->end(); muon++) {

    // isLooseMuon == ( isPFMuon && (isGlobalMuon || isTrackerMuon) )
    // See twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
    // !!! Be sure to synch with cut in fillMuonSegments.h !!!
    if ( !(muon::isLooseMuon((*muon))) ) continue;

    if (printLevel > 4 ) {
      printf("************************************************\n");
      printf("GBL RECO MOUN # %d\n", numMuons);
      printf("************************************************\n\n");
      printf("%s\n"    , "--------------------------------");
      printf("%s: %d\n", "isGlobalMuon    ()", muon->isGlobalMuon    ());
      printf("%s: %d\n", "isTrackerMuon   ()", muon->isTrackerMuon   ());
      printf("%s: %d\n", "isStandAloneMuon()", muon->isStandAloneMuon());
      printf("%s: %d\n", "combinedMuon    ().isNonnull()", muon->combinedMuon  ().isNonnull());
      printf("%s: %d\n", "track           ().isNonnull()", muon->track         ().isNonnull());
      printf("%s: %d\n", "standAloneMuon  ().isNonnull()", muon->standAloneMuon().isNonnull());
      printf("%s\n\n"  , "--------------------------------");
      
      printf("muon->pt(): %10.5f, muon->eta(): %10.5f, muon->phi(): %10.5f\n",
	     muon->pt(), muon->eta(), muon->phi());
    }
    
    if ( abs(muon->eta()) < 1.0 && muon->pt() > 30 ) tagExists = true;
      
    /* // Only fill for known CSC eta range */
    /* if ( abs(muon->eta()) < 1.0 || abs(muon->eta()) > 2.5) continue; */

    ev.recoPt       -> push_back(muon->pt()); // If muon is particle-flow, equivalent to pfP4().Pt()
    ev.recoEta      -> push_back(muon->eta());
    ev.recoPhi      -> push_back(muon->phi());
    ev.recoCharge   -> push_back(muon->charge());
    if (muon->isStandAloneMuon())
      ev.recoSamPt    -> push_back(muon->standAloneMuon()->pt());
    else ev.recoSamPt -> push_back(-999);
    // ev.recoSamEta   -> push_back(muon->standAloneMuon()->eta() );
    // ev.recoSamPhi   -> push_back(muon->standAloneMuon()->phi() );
    ev.recoIsTight  -> push_back(muon::isTightMuon((*muon), (*vertices).at(0)));
    ev.recoMatchedStations -> push_back(muon->numberOfMatchedStations());
    if (muon->isGlobalMuon())
      ev.recoChi2Norm -> push_back(muon->globalTrack()->normalizedChi2());
    else ev.recoChi2Norm -> push_back(-999);
    
    probeExists = true;
    
    numMuons++;
    
  } // End muon loop

  ev.numRecoMuons = numMuons;
  
  return (tagExists && probeExists);

}
