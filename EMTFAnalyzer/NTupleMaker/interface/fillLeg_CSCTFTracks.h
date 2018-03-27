// -*- C++ -*-
//=============================================================
// Fill all Legavy tracks in the event record for: 
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

const Double_t ptscale[31] =  { 0,
				1.5,   2.0,   2.5,   3.0,   3.5,   4.0,
				4.5,   5.0,   6.0,   7.0,   8.0,  10.0,  12.0,  14.0,
				16.0,  18.0,  20.0,  25.0,  30.0,  35.0,  40.0,  45.0,
				50.0,  60.0,  70.0,  80.0,  90.0, 100.0, 120.0, 140.0 };

void fillLeg_CSCTFTracks(DataEvtSummary_t &ev, edm::Handle<vector<pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi> > > > legacyTracks, 
			 int printLevel,
			 CSCSectorReceiverLUT* srLUTs_[5][2],
			 const L1MuTriggerScales  *ts,
			 const L1MuTriggerPtScale *tpts) {
  


  // Standard Pt LUTs
  edm::ParameterSet ptLUTset;
  ptLUTset.addParameter<bool>("ReadPtLUT", false);
  ptLUTset.addParameter<bool>("isBinary",  false);
  CSCTFPtLUT ptLUTs(ptLUTset, ts, tpts);

  int nTrks = 0;
 
  for(std::vector<std::pair<csc::L1Track,MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi>>>::const_iterator lt = legacyTracks->begin();lt != legacyTracks->end();lt++){

    if (nTrks > MAXTRK-1) break;
    
    float eta = 0.9 + 0.05*(lt->first.eta_packed()) + 0.025;
    unsigned sector = lt->first.sector();
    float phi = (0.05217*lt->first.localPhi()) + (sector-1)*1.1 + 0.0218;//*(3.14159265359/180)
    if(phi > 3.14159)
      phi -= 6.28318;
    
    // for legacy definition
    //int mode = lt->first.cscMode();
    
    //unsigned pti = 0, quality = 0;
    
    //lt->first.decodeRank(lt->first.rank(),pti,quality);//
    //float pt = ptscale[pti+1];
    
    /*
    // PtAddress gives an handle on other parameters
    ptadd thePtAddress(trk->first.ptLUTAddress());

    //Pt needs some more workaround since it is not in the unpacked data
    ptdat thePtData  = ptLUTs_->Pt(thePtAddress);

    // front or rear bit?
    if (thePtAddress.track_fr) {
      int pt_bit = thePtData.front_rank&0x1f;
      //csctf_.trQuality.push_back((thePtData.front_rank>>5)&0x3);
      //csctf_.trChargeValid.push_back(thePtData.charge_valid_front);
    } else {
      int pt_bit = thePtData.rear_rank&0x1f;
      //csctf_.trQuality.push_back((thePtData.rear_rank>>5)&0x3);
      //csctf_.trChargeValid.push_back(thePtData.charge_valid_rear);
    }

    // convert the Pt in human readable values (GeV/c)
    float pt = tpts->getPtScale()->getLowEdge(pt_bit);
    */

    // Anopther way to get Pt.
    int track_pt = lt->first.pt_packed();
    float pt  = tpts->getPtScale()->getLowEdge(track_pt);
    
    // For EMTF mode definition
    int mode = 0;
    if(lt->first.me1ID())
      mode |= 8;
    if(lt->first.me2ID())
      mode |= 4;
    if(lt->first.me3ID())
      mode |= 2;
    if(lt->first.me4ID())
      mode |= 1;

    if (printLevel > 0) {
      cout << "\n Legacy Track # " << nTrks << endl;
      cout << "============" << endl;
      cout << " Track Pt   : " << pt << endl;
      //cout << " Track Pt2  : " << trPt << endl;
      cout << " Track Eta  : " << eta << endl;
      cout << " Track Phi  : " << phi << endl;
      cout << " Track Mode : " << mode << endl;
    }
        
    ev.leg_trkPt   -> push_back(pt);
    ev.leg_trkEta  -> push_back(eta);
    ev.leg_trkPhi  -> push_back(phi);
    ev.leg_trkMode -> push_back(mode);
    

    // For each trk, get the list of its LCTs
    CSCCorrelatedLCTDigiCollection LCTs = lt -> second;
    
    /*
    int LctTrkId_ = 0;
    for(CSCCorrelatedLCTDigiCollection::DigiRangeIterator lctOfTrks = lctsOfTracks.begin(); lctOfTrks  != lctsOfTracks.end()  ; lctOfTrks++) {
      int lctTrkId = 0;
      CSCCorrelatedLCTDigiCollection::Range lctRange = lctsOfTracks.get((*lctOfTrks).first);
      for(CSCCorrelatedLCTDigiCollection::const_iterator lctTrk = lctRange.first; lctTrk  != lctRange.second; lctTrk++, lctTrkId++) {
    */   

    
    std::vector<L1TMuon::TriggerPrimitive> LCT_collection;

    auto chamber = LCTs.begin();
    auto chend  = LCTs.end();
    for( ; chamber != chend; ++chamber ) {
      auto digi = (*chamber).second.first;
      auto dend = (*chamber).second.second;
      for( ; digi != dend; ++digi ) {
	LCT_collection.push_back(TriggerPrimitive((*chamber).first,*digi));
      }
    }

    int LctTrkId_ = 0; // count number of lcts in event
    
    auto Lct = LCT_collection.cbegin();
    auto Lctend = LCT_collection.cend();
    for( ; Lct != Lctend; Lct++) {

      if (LctTrkId_ > MAXTRKHITS-1) break;

      if(Lct->subsystem() != 1) continue;

      if (printLevel>1) cout << "\n==== Legacy LCT CSC " << LctTrkId_ << endl;

      CSCDetId id                = Lct->detId<CSCDetId>();
      auto lct_station           = id.station();
      auto lct_endcap            = id.endcap();
      auto lct_chamber           = id.chamber();
      uint16_t lct_bx            = Lct->getCSCData().bx;
      int lct_ring               = id.ring();
      int lct_sector             = CSCTriggerNumbering::triggerSectorFromLabels(id);
      int lct_subSector          = CSCTriggerNumbering::triggerSubSectorFromLabels(id);
      uint16_t lct_bx0           = Lct->getCSCData().bx0;
      uint16_t lct_cscID         = Lct->getCSCData().cscID;
      uint16_t lct_strip         = Lct->getCSCData().strip;
      uint16_t lct_pattern       = Lct->getCSCData().pattern;
      uint16_t lct_bend          = Lct->getCSCData().bend;
      uint16_t lct_quality       = Lct->getCSCData().quality;
      uint16_t lct_keywire       = Lct->getCSCData().keywire;
      int fpga    = ( lct_subSector ? lct_subSector-1 : lct_station);

      
      if ( printLevel > 0 ) {
	//cout << "\nLCT CSC " << lctId
	cout << "\n======\n";
	cout <<"lctEndcap       = " << lct_endcap << endl;
	cout <<"lctSector       = " << lct_sector<< endl;
	cout <<"lctSubSector    = " << lct_subSector << endl;
	cout <<"lctStation      = " << lct_station << endl;
	cout <<"lctRing         = " << lct_ring << endl;
	cout <<"lctChamber      = " << lct_chamber << endl;
	cout <<"lctTriggerCSCID = " << lct_cscID << endl;
	cout <<"lctBx           = " << lct_bx << endl;
	cout <<"lctBx0          = " << lct_bx0 << endl;
	cout <<"lctKeyWire      = " << lct_keywire << endl;
	cout <<"lctStrip        = " << lct_strip << endl;
	cout <<"lctBend         = " << lct_bend << endl;
	cout <<"lctQuality      = " << lct_quality << endl;
	cout <<"lct_pattern     = " << lct_pattern << endl;
	cout <<"lct fpga        = " << fpga << endl;
      }

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
	  continue;}
      
      // Do not FIll array over their given size!!
      if (nTrks > MAXTRK-1) {
        if (printLevel > 1) cout << "-----> nTrks is greater than MAXTRK-1.  Skipping this Track..." << endl;
        continue;
      }

      if (LctTrkId_ > MAXTRKHITS-1) {
        if (printLevel > 1)cout << "-----> LctTrkId_ is greater than MAXTRKHITS-1.  Skipping this Track..." << endl;
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

      // in global form
      float lct_eta = ts->getRegionalEtaScale(2)->getCenter(gblEta.global_eta);

      if (lct_endcap == 1) lct_eta = abs(lct_eta);

      //float lct_globPhi = fmod( gblPhi.global_phi +14.0*M_PI/180+(lct_sector-1)*60.0*M_PI/180, 2.*M_PI );
      float lct_globPhi = fmod(gblPhi.global_phi + ((lct_sector-1)*TMath::Pi()/3) + //sector 1 starts at 15 degrees
			      (TMath::Pi()/12) , 2*TMath::Pi());

      if (lct_globPhi > M_PI) lct_globPhi -= 2.*M_PI;

      if (printLevel>1) {
	cout <<"phi packed      = " << gblPhi.global_phi << endl;
	cout <<"eta packed      = " << gblEta.global_eta << endl;
	cout <<"phi global      = " << lct_globPhi << endl;
	cout <<"eta global      = " << lct_eta << endl;
      }
      
      ev.leg_trkLct_endcap[nTrks][LctTrkId_] = lct_endcap;

      // sector (end 1: 1->6, end 2: 7 -> 12)
      //if ( lct_endcap == 1)
      ev.leg_trkLct_sector[nTrks][LctTrkId_] = lct_sector;
      //else
      //        lctSector[nTrk][LctTrkId_] = 6+lct_sector;

      ev.leg_trkLct_station[nTrks][LctTrkId_] = lct_station;

      ev.leg_trkLct_ring[nTrks][LctTrkId_] = lct_ring;

      ev.leg_trkLct_chamber[nTrks][LctTrkId_] = lct_chamber;

      ev.leg_trkLct_cscId[nTrks][LctTrkId_] = lct_cscID;

      ev.leg_trkLct_wire[nTrks][LctTrkId_] = lct_keywire;

      ev.leg_trkLct_strip[nTrks][LctTrkId_] = lct_strip;

      ev.leg_trkLct_globPhi[nTrks][LctTrkId_] = lct_globPhi;

      ev.leg_trkLct_eta[nTrks][LctTrkId_] = lct_eta;

      ev.leg_trkLct_locPhi[nTrks][LctTrkId_] = gblPhi.global_phi;

      LctTrkId_++;

    } // end track LCT loop
    
    ev.numLegTrkLCTs -> push_back(LctTrkId_);
    
    nTrks++;
    
  }
  
  ev.numLegTrks = nTrks;
  

} // end fill Tracks
