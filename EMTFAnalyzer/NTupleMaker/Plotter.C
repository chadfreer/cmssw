/*Macro for plotting EMTF NTuples
 Written by Chad Freer 
 April 24, 2018
 Input tree froom EMTF NTupilizer 
 (including CSC reconstructed Segment matching to LCT)
 */

/*Variables
 ===========================================================================================|
 Evt        |Hits               |Tracks             |reco               |seg                |
 -----------+-------------------+-------------------+-------------------+-------------------|
 evt_BX     |nHits              |nTracks            |nRecoMuons         |nSegs              |
 evt_LS     |nHitsBX0           |nTracksBX0         |reco_eta           |seg_chi2           |
 evt_run    |nHitsCSC           |trk_eta            |reco_eta_St1       |seg_segDirx        |
 evt_event  |nHitsCSCBX0        |trk_phi            |reco_eta_St2       |seg_segDiry        |
 evt_orbit  |nHitsRPC           |trk_phi_loc        |reco_phi           |seg_segDirz        |
            |nHitsRPCBX0        |trk_pt             |reco_phi_St1       |seg_segx           |
            |hit_eta            |trk_theta          |reco_phi_St2       |seg_segy           |
            |hit_phi            |trk_BX             |reco_pt            |seg_time           |
            |hit_phi_loc        |trk_charge         |reco_theta         |seg_chamber        |
            |hit_theta          |trk_dBX            |reco_theta_St1     |seg_endcap         |
            |hit_BX             |trk_dPhi_int       |reco_theta_St2     |seg_match_iLCT     |
            |hit_CSC_ID         |trk_dTheta_int     |reco_ID_loose      |seg_nRecHits       |
            |hit_FR             |trk_endcap         |reco_ID_medium     |seg_ring           |
            |hit_alct_quality   |trk_eta_int        |reco_ID_tight      |seg_station        |
            |hit_chamber        |trk_mode           |reco_charge        |seg_strip_max      |
            |hit_clct_quality   |trk_mode_CSC       |reco_match_trk_dEta|seg_strip_min      |
            |hit_endcap         |trk_mode_RPC       |reco_match_trk_dPhi|seg_triggerCscId   |
            |hit_eta_int        |trk_mode_neighbor  |reco_match_trk_dR  |seg_triggerSector  |
            |hit_isCSC          |trk_nHits          |reco_match_iTrk    |seg_wire_max       |
            |hit_isRPC          |trk_nNeighbor      |                   |seg_wire_min       |
            |hit_match_iSeg     |trk_nRPC           |                   |numFills           |
            |hit_neighbor       |trk_phi_int        |                   |numLCTMatched      |
            |hit_pattern        |trk_pt_int         |                   |numMatched         |
            |hit_phi_int        |trk_sector         |                   |numSegMatched      |
            |hit_quality        |trk_sector_index   |                   |                   |
            |hit_ring           |trk_theta_int      |                   |                   |
            |hit_roll           |                   |                   |                   |
            |hit_sector         |Branch             |                   |                   |
            |hit_sector_index   |trk_iHit           |                   |                   |
            |hit_station        |                   |                   |                   |
            |hit_strip          |                   |                   |                   |
            |hit_strip_hi       |                   |                   |                   |
            |hit_strip_low      |                   |                   |                   |
            |hit_subsector      |                   |                   |                   |
            |hit_theta_int      |                   |                   |                   |
            |hit_valid          |                   |                   |                   |
            |hit_wire           |                   |                   |                   |
=============================================================================================*/

#include "TFile.h"
#include "TSystem.h"
#include "TChain.h"
#include "TTree.h"
#include "TBranch.h"
#include "TStyle.h"
#include "TMath.h"

#include "ReadNtuple.h"

const int MAX_FILES = 10;   // Max number of files to process
const int MAX_EVT   = 2000000;   // Max number of events to process
const int PRT_EVT   =  100;   // Print every N events
const bool verbose  = false; // Print information about the event and RECO and L1T muons

//for making plots
static TString xaxis="Segment #chi^{2}";
static TString yaxis="Entries";

TFile *fout = new TFile("MacroPlotter.root","RECREATE");
TH1F *h11 = new TH1F ("h11",xaxis,50,0,50);
TH1F *h12 = new TH1F ("h12",xaxis,50,0,50);
TH1F *h21 = new TH1F ("h21",xaxis,50,0,50);
TH1F *h22 = new TH1F ("h22",xaxis,50,0,50);
TH1F *h31 = new TH1F ("h31",xaxis,50,0,50);
TH1F *h32 = new TH1F ("h32",xaxis,50,0,50);
TH1F *h41 = new TH1F ("h41",xaxis,50,0,50);
TH1F *h42 = new TH1F ("h42",xaxis,50,0,50);

double bendx = 0.0;

void Plotter(){

   TFile *f = new TFile("EMTF_ZMu_NTuple_306091_simLCT_test.root");
   TChain *in_chain= new TChain("FlatNtupleData/tree");
   in_chain->Add("EMTF_ZMu_NTuple_306091_simLCT_test.root" );
   InitializeMaps();
   SetBranchAddresses(in_chain);

   //prepare event loop
   std::cout << "\n******* About to loop over the events *******" << std::endl;
   int nEvents = in_chain->GetEntries();
   for (int iEvt = 0; iEvt < nEvents; iEvt++) {
     if (iEvt > MAX_EVT) break;
     if ( (iEvt % PRT_EVT) == 0 ) {
        std::cout << "\n*************************************" << std::endl;
        std::cout << "Looking at event " << iEvt << " out of " << nEvents << std::endl;
        std::cout << "*************************************" << std::endl;    
     }//end conditional
     in_chain->GetEntry(iEvt);

     //Loop over reco tracks
     for (int iRecoTrk = 0; iRecoTrk < I("nRecoMuons"); iRecoTrk++){
        if (F("reco_pt",iRecoTrk) < 22) continue;
        if (I("reco_match_iTrk", iRecoTrk) < 0 ) continue;						//Take only matched reco muons
        int track_index = I("reco_match_iTrk", iRecoTrk);
        std::cout << track_index << std::endl;
        if (I("trk_BX", track_index)!=0) continue;							//Take only tracks with BX0 

        //loop over unpacked tracks that are matched with high pT reco muons         
        for (int iTrkHits = 0; iTrkHits < I("trk_nHits", track_index); iTrkHits++){
           //if (I("trk_found_hits", track_index) != 1) continue;  					// For a very small fraction of unpacked tracks, can't find all hits (mostly BX != 0) 
           int iHit = I("trk_iHit", track_index, iTrkHits);  						// Access the index of each hit in the track
           if (I("hit_isCSC", iHit) != 1) continue;							// get rid of RPC hits
           if (I("hit_match_iSeg", iHit) < 0) continue;
           int iSeg = I("hit_match_iSeg", iHit);

           //=========================================================================================
           //begin fills for each station and ring (skipping ME1/3)
           if (I("seg_nRecHits",iSeg) < 5 ) continue;
           //bendx = TMath::ATan2( F("seg_segDiry",iSeg), abs(F("seg_segDirz",iSeg)) );
           bendx = F("seg_chi2", iSeg);
           if (I("hit_station", iHit)==1){
	      if (I("hit_ring", iHit)==1 || I("hit_ring", iHit)==4){
                 //h11->Fill(I("seg_nRecHits",iSeg),1); 
                 h11->Fill(bendx,1);
              }else if (I("hit_ring", iHit)==2){
                 //h12->Fill(I("seg_nRecHits",iSeg),1);
                 h12->Fill(bendx,1);
              }
           }//end station 1 fills
           else if (I("hit_station", iHit)==2){
              if (I("hit_ring", iHit)==1){
                 //h21->Fill(I("seg_nRecHits",iSeg),1);
                 h21->Fill(bendx,1);
              }else if (I("hit_ring", iHit)==2){
                 //h22->Fill(I("seg_nRecHits",iSeg),1);
                 h22->Fill(bendx,1);
              }
           }//end station 2 fills
           else if (I("hit_station", iHit)==3){
              if (I("hit_ring", iHit)==1){
                 //h31->Fill(I("seg_nRecHits",iSeg),1);
                 h31->Fill(bendx,1);
              }else if (I("hit_ring", iHit)==2){
                 //h32->Fill(I("seg_nRecHits",iSeg),1);
                 h32->Fill(bendx,1);
              }
           }//end station 3 fills
           else if (I("hit_station", iHit)==4){
              if (I("hit_ring", iHit)==1){
                 //h41->Fill(I("seg_nRecHits",iSeg),1);
                 h41->Fill(bendx,1);
              }else if (I("hit_ring", iHit)==2){
                 //h42->Fill(I("seg_nRecHits",iSeg),1);
                 h42->Fill(bendx,1);
              }
           }//end station 4 fills
           //=========================================================================================

        }//end unpacked track loop

     }//end reco muon loop

   }//end event loop

   //Might as well label things
   h11->GetXaxis()->SetTitle(xaxis);
   h11->GetYaxis()->SetTitle(yaxis);

   h12->GetXaxis()->SetTitle(xaxis);
   h12->GetYaxis()->SetTitle(yaxis);

   h21->GetXaxis()->SetTitle(xaxis);
   h21->GetYaxis()->SetTitle(yaxis);

   h22->GetXaxis()->SetTitle(xaxis);
   h22->GetYaxis()->SetTitle(yaxis);

   h31->GetXaxis()->SetTitle(xaxis);
   h31->GetYaxis()->SetTitle(yaxis);

   h32->GetXaxis()->SetTitle(xaxis);
   h32->GetYaxis()->SetTitle(yaxis);

   h41->GetXaxis()->SetTitle(xaxis);
   h41->GetYaxis()->SetTitle(yaxis);

   h42->GetXaxis()->SetTitle(xaxis);
   h42->GetYaxis()->SetTitle(yaxis);

   //Cleaning up after ourselves
   std::cout << "\n******* Finished looping over the events *******" << std::endl;
   delete in_chain;
   std::cout << "\nDone with Read_FlatNtuple(). Exiting.\n" << std::endl;
   fout->Write();

}//end void













