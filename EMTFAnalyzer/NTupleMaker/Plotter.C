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

static TString axis="Number of Segments per event";
const int MAX_FILES = 10;   // Max number of files to process
const int MAX_EVT   = 2000000;   // Max number of events to process
const int PRT_EVT   =  100;   // Print every N events
const bool verbose  = false; // Print information about the event and RECO and L1T muons

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

        //loop over unpacked tracks that are matched with high pT reco muons         
        for (int iUnpTrkHits = 0; iUnpTrkHits < I("unp_trk_nHits", track_index); iUnpTrkHits++){
           if (I("unp_trk_found_hits", track_index) != 1) continue;  					// For a very small fraction of unpacked tracks, can't find all hits (mostly BX != 0) 
           int iHit = I("unp_trk_iHit", track_index, iUnpTrkHits);  					// Access the index of each hit in the track
           if (I("hit_isCSC", iHit) != 1) continue;							// get rid of RPC hits
           std::cout << I("hit_station", iHit) << std::endl;
        }//end unpacked track loop

     }//end reco muon loop

   }//end event loop

}//end void













