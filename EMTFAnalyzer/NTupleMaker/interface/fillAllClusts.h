// -*- C++ -*-
//=============================================================
// Fill all RPC clusters in the event record for: 
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
#include "L1Trigger/L1TMuonEndCap/plugins/L1TMuonEndCapTrackProducer.h"
#include "L1Trigger/CSCCommonTrigger/interface/CSCPatternLUT.h"
#include "L1Trigger/CSCTrackFinder/test/src/RefTrack.h"

#include "L1Trigger/L1TMuon/interface/deprecate/SubsystemCollectorFactory.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include <TMath.h>
#include <TCanvas.h>
#include <TLorentzVector.h>

#include <TStyle.h>
#include <TLegend.h>
#include <TF1.h>
#include <TH2.h>
#include <TH1F.h>
#include <TFile.h>
#include "L1Trigger/L1TMuon/interface/GeometryTranslator.h"

//#include "L1Trigger/L1TMuon/interface/MuonTriggerPrimitive.h"
//#include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrack.h"
//#include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrackFwd.h"
//#include "L1Trigger/L1TMuonEndCap/interface/PrimitiveConverter.h"

#include "L1Trigger/L1TMuonEndCap/interface/PhiMemoryImage.h"
#include "L1Trigger/L1TMuonEndCap/interface/EmulatorClasses.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCTFPtLUT.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCSectorReceiverLUT.h"
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "L1Trigger/L1TMuon/interface/MuonTriggerPrimitive.h"
#include <L1Trigger/CSCTrackFinder/interface/CSCTFSPCoreLogic.h>
#include "L1Trigger/L1TMuonEndCap/interface/EmulatorClasses.h"


using namespace std;
using namespace edm;
using namespace reco;
using namespace csc;


void fillAllClusts(DataEvtSummary_t &ev, edm::Handle<std::vector<l1t::EMTFHit>> clust_collection, int printLevel) {

  int clustId = 0; // count number of clusters in event
  for( auto clust = clust_collection->cbegin(); clust < clust_collection->cend(); clust++) {
    
    if (printLevel>0) cout << "\nRPC cluster " << clustId << endl;
    
    int clust_station       = clust->Station();
    int clust_endcap        = clust->Endcap();
    int clust_chamber       = clust->Chamber();
    int clust_bx            = clust->BX();
    int clust_ring          = clust->Ring();
    int clust_sector        = clust->Sector();
    int clust_subSector     = clust->Subsector();
    int clust_strip         = clust->Strip_hi();
    int clust_pattern       = clust->Pattern();
    int clust_bend          = clust->Bend();
    int clust_quality       = clust->Quality();
    int clust_keywire       = clust->Wire();
    float clust_phi         = clust->Phi_glob_rad();
    float clust_eta         = clust->Eta();

    if ( printLevel > 0 ) {
      //cout << "\nRPC cluster " << clustId
      cout << "\n======\n";
      cout <<"clustEndcap       = " << clust_endcap << endl;
      cout <<"clustSector       = " << clust_sector<< endl;
      cout <<"clustSubSector    = " << clust_subSector << endl;
      cout <<"clustStation      = " << clust_station << endl;
      cout <<"clustRing         = " << clust_ring << endl;
      cout <<"clustChamber      = " << clust_chamber << endl;
      cout <<"clustBx           = " << clust_bx << endl;
      cout <<"clustKeyWire      = " << clust_keywire << endl;
      cout <<"clustStrip        = " << clust_strip << endl;
      cout <<"clustBend         = " << clust_bend << endl;
      cout <<"clustQuality      = " << clust_quality << endl;
      cout <<"clust_pattern     = " << clust_pattern << endl;
      //cout <<"clust fpga        = " << fpga << endl;
      cout <<"phi global      = " << clust_phi << endl;
      cout <<"eta global      = " << clust_eta << endl;
    }
    
    ev.clustEndcap -> push_back(clust_endcap);
    ev.clustSector -> push_back(clust_sector);
    ev.clustSubSector -> push_back(clust_subSector);
    ev.clustStation -> push_back(clust_station);
    ev.clustRing -> push_back(clust_ring);
    ev.clustChamber -> push_back(clust_chamber);
    ev.clustBx -> push_back(clust_bx);
    ev.clustWire -> push_back(clust_keywire);
    ev.clustStrip -> push_back(clust_strip);
    ev.clustGlobalPhi -> push_back(clust_phi);
    ev.clustEta -> push_back(clust_eta);


    /*
    int EndCapLUT = 1;
    if(lct_endcap==2) EndCapLUT= 0; 
    
    //    Check if DetId is within range
    if( lct_sector < 1   || lct_sector > 12 ||
	lct_station < 1  || lct_station >  4 ||
	lct_cscID < 1    || lct_cscID >  9 ||
	EndCapLUT > 2    || EndCapLUT < 0 ||
	fpga > 5         || fpga < 0 )
      {
	if (printLevel > 1) cout << "  LCT ERROR: CSC digi are out of range! " << endl;;
	continue;
      }
    
    lclphidat lclPhi;
    try {
      lclPhi = srLUTs_[fpga][EndCapLUT] -> localPhi(lct_strip, lct_pattern, lct_quality, lct_bend);
    } 
    catch(cms::Exception &) {
      bzero(&lclPhi,sizeof(lclPhi));
    }
    
    gblphidat gblPhi;
    try {
      gblPhi = srLUTs_[fpga][EndCapLUT] -> globalPhiME(lclPhi.phi_local, lct_keywire, lct_cscID);
    } 
    catch(cms::Exception &) {
      bzero(&gblPhi,sizeof(gblPhi));
    }

    gbletadat gblEta;
    try {
      gblEta = srLUTs_[fpga][EndCapLUT] -> globalEtaME(lclPhi.phi_bend_local, lclPhi.phi_local, lct_keywire, lct_cscID);
    } 
    catch(cms::Exception &) {
      bzero(&gblEta,sizeof(gblEta));
    }
    

    // A new way to find global
    //const CSCChamber* cscchamber = cscGeom->chamber(id);


    if (printLevel>1) {
      cout <<"phi packed      = " << gblPhi.global_phi << endl;
      cout <<"eta packed      = " << gblEta.global_eta << endl;
      //cout <<"phi global      = " << ev.lctGlobalPhi[lctId] << endl;
      //cout <<"eta global      = " << ev.lctEta[lctId] << endl;
    }
    
    // Fill the branch vectors
    //ev.lctGlobalPhi -> push_back(lct_globPhi);
    //ev.lctEta -> push_back(lct_eta);
    //ev.lctLocPhi -> push_back(gblPhi.global_phi);
    //ev.lctLocEta -> push_back(gblEta.global_eta);
    
    */


    
    clustId++;

  } // end LCT loop
  
  ev.numClusts = clustId;
  
} // end fillAllClusts



/*
  for(CSCCorrelatedLCTDigiCollection::DigiRangeIterator csc=LCTs.product()->begin(); csc!=LCTs.product()->end(); csc++) {
  CSCCorrelatedLCTDigiCollection::Range range1 = LCTs.product()->get((*csc).first);
  for(CSCCorrelatedLCTDigiCollection::const_iterator Lct = range1.first; Lct != range1.second; Lct++, lctId++) {
  
  int lct_endcap    = (*csc).first.endcap()-1;
  int lct_station   = (*csc).first.station()-1;
  int lct_sector    = (*csc).first.triggerSector()-1;
  int lct_subSector = CSCTriggerNumbering::triggerSubSectorFromLabels((*csc).first);
  int lct_ring      = (*csc).first.ring();
  int lct_cscId     = (*csc).first.triggerCscId()-1;
  int lct_chamber   = (*csc).first.chamber()-1;
*/
