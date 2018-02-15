
#include "math.h"
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"

#include <algorithm> // For std::fmax, min

void match_EMTF_to_RECO()
{

  // // Use a single input NTuple file
  // TString file_name = "root://eoscms//eos/cms/store/user/abrinke1/EMTF/Emulator/trees/SingleMuon/EMTF_EFF/160912_110056/0000/EMTF_NTuple_1.root";
  // TFile *in_files = TFile::Open(file_name);
  // if (file == 0) {
  //   // If we cannot open the file, print an error message and return immediately
  //   cout << "Error: cannot open " << file_name << endl;
  //   return;
  // }
  // TTreeReader myReader("ntuple/tree", in_files); // Creates a tree reader (of type Int_t) on the branch "fEventSize"
  
  // Use multiple input NTuple files
  TString prefix = "root://eoscms//eos/cms";
  TString file_dir = "/store/user/abrinke1/EMTF/Emulator/trees/SingleMuon/EMTF_EFF/160912_110056/0000/";
  TString file_name;
  TChain in_files("ntuple/tree");
  for (Long_t i = 1; i < 88; i++) {
    file_name = prefix+file_dir+"EMTF_NTuple_"+i+".root";
    std::cout << "Adding file " << file_name << std::endl;
    in_files.Add(file_name);
  }
  TTreeReader myReader(&in_files); // Creates a tree reader (of type Int_t) on the branch "fEventSize"
  
  // Create an output file
  TString out_file_name = "plots/match_EMTF_to_RECO.root";
  TFile *out_file = new TFile(out_file_name, "recreate");

  // Configure parameters for output
  bool  require_tag =  true; // Require tag muon in barrel that would have fired SingleMu trigger
  float min_tag_pT =     25;
  float max_tag_eta =   1.0;
  float min_RECO_pT =    20; // Only consider RECO muons with pT > XX GeV
  float max_RECO_pT = 10000; // Only consider RECO muons with pT < XX GeV
  float min_RECO_eta =  1.2; // Only consider RECO muons with |eta| > min
  float max_RECO_eta =  2.4; // Only consider RECO muons with |eta| < max

  
  ///////////////////////////////////////
  // Set branches for variables in NTuple
  ///////////////////////////////////////

  // Event information
  TTreeReaderValue<Int_t> my_run(myReader, "run");
  TTreeReaderValue<Int_t> my_lumi(myReader, "lumi");
  TTreeReaderValue<Int_t> my_event(myReader, "event");

  // RECO muon
  TTreeReaderValue<Int_t> my_numRecoMuons(myReader, "numRecoMuons");
  TTreeReaderArray<Float_t> my_recoEta(myReader, "recoEta");
  TTreeReaderArray<Float_t> my_recoPhi(myReader, "recoPhi");
  TTreeReaderArray<Float_t> my_recoPt(myReader, "recoPt");
  TTreeReaderArray<Float_t> my_recoSamPt(myReader, "recoSamPt");
  TTreeReaderArray<Int_t> my_recoIsTight(myReader, "recoIsTight");
  TTreeReaderArray<Int_t> my_recoCharge(myReader, "recoCharge");
  TTreeReaderArray<Int_t> my_recoMatchedStations(myReader, "recoMatchedStations");
  TTreeReaderArray<Int_t> my_recoNumCscSegs(myReader, "recoNumCscSegs");
  TTreeReaderArray<Int_t> my_recoCscSeg_endcap(myReader, "recoCscSeg_endcap");
  TTreeReaderArray<Int_t> my_recoCscSeg_station(myReader, "recoCscSeg_station");
  TTreeReaderArray<Int_t> my_recoCscSeg_sector(myReader, "recoCscSeg_sector");
  TTreeReaderArray<Int_t> my_recoCscSeg_ring(myReader, "recoCscSeg_ring");
  TTreeReaderArray<Int_t> my_recoCscSeg_chamber(myReader, "recoCscSeg_chamber");
  TTreeReaderArray<Int_t> my_recoCscSeg_lctId(myReader, "recoCscSeg_lctId");
  TTreeReaderArray<Float_t> my_recoCscSeg_glob_eta(myReader, "recoCscSeg_glob_eta");
  TTreeReaderArray<Float_t> my_recoCscSeg_glob_phi(myReader, "recoCscSeg_glob_phi");

  // All LCTs received by EMTF
  TTreeReaderValue<Int_t> my_numLCTs(myReader, "numLCTs");
  TTreeReaderArray<Int_t> my_lctBx(myReader, "lctBx");
  TTreeReaderArray<Int_t> my_lctEndcap(myReader, "lctEndcap");
  TTreeReaderArray<Int_t> my_lctStation(myReader, "lctStation");
  TTreeReaderArray<Int_t> my_lctSector(myReader, "lctSector");
  TTreeReaderArray<Int_t> my_lctRing(myReader, "lctRing");
  TTreeReaderArray<Int_t> my_lctChamber(myReader, "lctChamber");
  TTreeReaderArray<Int_t> my_lctCscId(myReader, "lctTriggerCSCID");
  TTreeReaderArray<Int_t> my_lctStrip(myReader, "lctStrip");
  TTreeReaderArray<Int_t> my_lctWire(myReader, "lctWire");
  TTreeReaderArray<Float_t> my_lctGlobalPhi(myReader, "lctGlobalPhi");
  TTreeReaderArray<Float_t> my_lctEta(myReader, "lctEta");

  // EMTF output tracks and their hits
  TTreeReaderValue<Int_t> my_numTrks(myReader, "numTrks");
  TTreeReaderArray<Float_t> my_trkEta(myReader, "trkEta");
  TTreeReaderArray<Float_t> my_trkPt(myReader, "trkPt");
  TTreeReaderArray<Int_t> my_trkMode(myReader, "trkMode");
  TTreeReaderArray<Int_t> my_numTrkLCTs(myReader, "numTrkLCTs");
  TTreeReaderArray<Int_t> my_trkLct_bx(myReader, "trkLct_bx");
  TTreeReaderArray<Int_t> my_trkLct_endcap(myReader, "trkLct_endcap");
  TTreeReaderArray<Int_t> my_trkLct_station(myReader, "trkLct_station");
  TTreeReaderArray<Int_t> my_trkLct_sector(myReader, "trkLct_sector");
  TTreeReaderArray<Int_t> my_trkLct_ring(myReader, "trkLct_ring");
  TTreeReaderArray<Int_t> my_trkLct_chamber(myReader, "trkLct_chamber");
  TTreeReaderArray<Int_t> my_trkLct_cscId(myReader, "trkLct_cscId");
  TTreeReaderArray<Int_t> my_trkLct_strip(myReader, "trkLct_strip");
  TTreeReaderArray<Int_t> my_trkLct_wire(myReader, "trkLct_wire");
  TTreeReaderArray<Float_t> my_trkLct_globPhi(myReader, "trkLct_globPhi");
  TTreeReaderArray<Float_t> my_trkLct_eta(myReader, "trkLct_eta");

  // CSCTF output tracks
  TTreeReaderValue<Int_t> my_numLegTrks(myReader, "numLegTrks");
  TTreeReaderArray<Float_t> my_leg_trkEta(myReader, "leg_trkEta");
  TTreeReaderArray<Float_t> my_leg_trkPt(myReader, "leg_trkPt");
  TTreeReaderArray<Int_t> my_numLegTrkLCTs(myReader, "numLegTrkLCTs");
  TTreeReaderArray<Int_t> my_leg_trkLct_endcap(myReader, "leg_trkLct_endcap");
  TTreeReaderArray<Int_t> my_leg_trkLct_station(myReader, "leg_trkLct_station");

  //////////////////
  // Book histograms
  //////////////////

  float station_bins[2] = {-0.5, 5.5};
  float ring_bins[2] = {-0.5, 12.5};
  float eta_bins[2] = {-221*0.010875 - (0.010875/2), 221*0.010875 + (0.010875/2)};
  float phi_bins[2] = {-3.2, 3.2};
  float dEta_bins[2] = {-0.1, 0.1};
  float dPhi_bins[2] = {-0.1, 0.1};

  TH2D * h_reco_vs_trk_matched_LCTs = new TH2D("h_reco_vs_trk_matched_LCTs", "", 7, -1.5, 5.5, 7, -1.5, 5.5);
  TH2D * h_reco_vs_trk_dR_matched_LCTs = new TH2D("h_reco_vs_trk_dR_matched_LCTs", "", 7, -1.5, 5.5, 7, -1.5, 5.5);
  
  TH1D * h_seg_dEta = new TH1D("h_seg_dEta", "", 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_max_dEta = new TH1D("h_seg_max_dEta", "", 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_dPhi = new TH1D("h_seg_dPhi", "", 40, dPhi_bins[0], dPhi_bins[1]);
  TH2D * h_seg_dEta_vs_dPhi =  new TH2D("h_seg_dEta_vs_dPhi", "", 40, dPhi_bins[0], dPhi_bins[1], 40, dEta_bins[0], dEta_bins[1]);

  TH1D * h_seg_match_dEta = new TH1D("h_seg_match_dEta", "", 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_match_max_dEta = new TH1D("h_seg_match_max_dEta", "", 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_match_dPhi = new TH1D("h_seg_match_dPhi", "", 40, dPhi_bins[0], dPhi_bins[1]);
  TH2D * h_seg_match_dEta_vs_dPhi =  new TH2D("h_seg_match_dEta_vs_dPhi", "", 40, dPhi_bins[0], dPhi_bins[1], 40, dEta_bins[0], dEta_bins[1]);

  TH1D * h_seg_unm_dEta = new TH1D("h_seg_unm_dEta", "", 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_unm_max_dEta = new TH1D("h_seg_unm_max_dEta", "", 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_unm_dPhi = new TH1D("h_seg_unm_dPhi", "", 40, dPhi_bins[0], dPhi_bins[1]);
  TH2D * h_seg_unm_dEta_vs_dPhi =  new TH2D("h_seg_unm_dEta_vs_dPhi", "", 40, dPhi_bins[0], dPhi_bins[1], 40, dEta_bins[0], dEta_bins[1]);

  TH1D * h_seg_miss_dEta = new TH1D("h_seg_miss_dEta", "", 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_miss_max_dEta = new TH1D("h_seg_miss_max_dEta", "", 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_miss_dPhi = new TH1D("h_seg_miss_dPhi", "", 40, dPhi_bins[0], dPhi_bins[1]);
  TH2D * h_seg_miss_dEta_vs_dPhi =  new TH2D("h_seg_miss_dEta_vs_dPhi", "", 40, dPhi_bins[0], dPhi_bins[1], 40, dEta_bins[0], dEta_bins[1]);
  TH1D * h_seg_miss_eta = new TH1D("h_seg_miss_eta", "", 443, eta_bins[0], eta_bins[1]);
  TH1D * h_seg_miss_phi = new TH1D("h_seg_miss_phi", "", 64, phi_bins[0], phi_bins[1]);
  TH1D * h_seg_miss_ring = new TH1D("h_seg_miss_ring", "", 13, ring_bins[0], ring_bins[1]);
  TH1D * h_seg_miss_station = new TH1D("h_seg_miss_station", "", 6, station_bins[0], station_bins[1]);
  TH2D * h_seg_miss_dEta_vs_station =  new TH2D("h_seg_miss_dEta_vs_station", "", 6, station_bins[0], station_bins[1], 40, dEta_bins[0], dEta_bins[1]);
  TH2D * h_seg_miss_dPhi_vs_station =  new TH2D("h_seg_miss_dPhi_vs_station", "", 6, station_bins[0], station_bins[1], 40, dPhi_bins[0], dPhi_bins[1]);
  TH2D * h_seg_miss_eta_vs_station =  new TH2D("h_seg_miss_eta_vs_station", "", 6, station_bins[0], station_bins[1], 443, eta_bins[0], eta_bins[1]);
  TH2D * h_seg_miss_eta_vs_ring =  new TH2D("h_seg_miss_eta_vs_ring", "", 13, ring_bins[0], ring_bins[1], 443, eta_bins[0], eta_bins[1]);
  TH2D * h_seg_miss_phi_vs_station =  new TH2D("h_seg_miss_phi_vs_station", "", 6, station_bins[0], station_bins[1], 64, phi_bins[0], phi_bins[1]);
  TH2D * h_seg_miss_ring_vs_station =  new TH2D("h_seg_miss_ring_vs_station", "", 6, station_bins[0], station_bins[1], 13, ring_bins[0], ring_bins[1]);

  TH2D * h_reco_vs_seg_eta = new TH2D("h_reco_vs_seg_eta", "", 250, -2.5, 2.5, 250, -2.5, 2.5);
  TH2D * h_reco_vs_seg_phi = new TH2D("h_reco_vs_seg_phi", "", 320, -3.2, 3.2, 320, -3.2, 3.2);

  TH1D * h_trk_mode = new TH1D("h_trk_mode", "", 16, -0.5, 15.5);
  TH2D * h_trk_mode_vs_reco_eta = new TH2D("h_trk_mode_vs_reco_eta", "", 30, 1.0, 2.5, 16, -0.5, 15.5);
  TH2D * h_trk_vs_RECO_pT = new TH2D("h_trk_vs_RECO_pT", "", 500, 0, 500, 500, 0, 500);

  uint event_num = 0;
  uint nTag = 0;
  // Loop over all entries of the TTree or TChain.
  while (myReader.Next()) {
    event_num += 1;
    // if (event_num > 50000) break;
    if (event_num % 1000 == 0) cout << "Processing event " << event_num << endl;

    // Find out if a tag muon exists
    bool tag_exists = false;
    for (uint iReco = 0; iReco < *my_numRecoMuons; iReco++) {
      if (iReco > 7) continue; // We only store the first 8 RECO muons passing our selection
      if (my_recoPt[iReco] < min_tag_pT) continue;
      if (abs(my_recoEta[iReco]) > max_tag_eta) continue;
      if ( my_recoIsTight[iReco] != 1 ) continue;
      tag_exists = true;
      nTag += 1;
    }
    if (require_tag && not tag_exists) continue;
    
    // Loop over the RECO muons
    for (uint iReco = 0; iReco < *my_numRecoMuons; iReco++) {
      if (iReco > 7) continue; // We only store the first 8 RECO muons passing our selection
      if ( abs(my_recoEta[iReco]) < min_RECO_eta ) continue;
      if ( abs(my_recoEta[iReco]) > max_RECO_eta ) continue;
      if (my_recoPt[iReco] < min_RECO_pT) continue; // Cut out low-pT muons 
      if (my_recoPt[iReco] > max_RECO_pT) continue; // Cut out low-pT muons 
      if ( my_recoIsTight[iReco] != 1 ) continue; // Only consider muons passing tight ID

      // Translate the {1, 2} convention to {+1, -1} convention used by EMTF
      int reco_endcap = (my_recoEta[iReco] > 0) ? 1 : -1; 

      // ID of LCTs matched to RECO segments by strip/wire; up to 4 in each station
      int reco_st_id[4][4] = {{-999, -999, -999, -999}, {-999, -999, -999, -999}, 
			      {-999, -999, -999, -999}, {-999, -999, -999, -999}};
      // ID of LCTs matched to RECO track in dR; up to 4 in each station
      int reco_st_id_dR[4][4] = {{-999, -999, -999, -999}, {-999, -999, -999, -999}, 
			      {-999, -999, -999, -999}, {-999, -999, -999, -999}};
      // Number of RECO segments in each station
      int reco_num_st[4] = {0, 0, 0, 0};
      int reco_num_st_any[4] = {0, 0, 0, 0}; // Don't require LCT match
      int reco_num_st_dR[4] = {0, 0, 0, 0};

      // Loop over LCTs received by EMTF
      for (uint iLCT = 0; iLCT < *my_numLCTs; iLCT++) {
	uint iSt = my_lctStation[iLCT] - 1;
	float dPhi = acos(cos(my_lctGlobalPhi[iLCT] - my_recoPhi[iReco]));
	dPhi *= sin(my_lctGlobalPhi[iLCT] - my_recoPhi[iReco]) / abs(sin(my_lctGlobalPhi[iLCT] - my_recoPhi[iReco]));
	dPhi *= my_recoCharge[iReco];
	float dEta = my_lctEta[iLCT] - my_recoEta[iReco];
	if ( abs(dPhi) < 0.1 && abs(dEta) < 0.1 ) {
	  reco_st_id_dR[iSt][reco_num_st_dR[iSt]] = iLCT;
	  reco_num_st_dR[iSt] += 1;
	}
      }

      float max_eta = -99;
      float min_eta = 99;
      // Loop over CSC segments belonging to RECO muon
      for (uint iSeg = 0; iSeg < my_recoNumCscSegs[iReco]; iSeg++) {
	if (iSeg > 15) continue; // We only store the first 16 segments (should be plenty)
	uint iSt = my_recoCscSeg_station[iReco*16 + iSeg] - 1;
	if (iSt < 4) reco_num_st_any[iSt] += 1;
	int tmp_id = my_recoCscSeg_lctId[iReco*16 + iSeg];
	if (tmp_id == -999) continue; // Only consider segments matched to LCTs

	// Print message if LCT eta/phi position is far from CSC segment eta/phi
	// Could indicate problem in LCT-segment matching in NTupleMaker, or eta/phi assignment problem in EMTF
	if ( acos(cos(my_lctGlobalPhi[tmp_id] - my_recoCscSeg_glob_phi[iReco*16 + iSeg])) > 0.2 ||
	     abs( my_lctEta[tmp_id] - my_recoCscSeg_glob_eta[iReco*16 + iSeg] ) > 0.2 ) {
	  std::cout << "\nLCT endcap = " << my_lctEndcap[tmp_id] << ", station = " << my_lctStation[tmp_id]
		    << ", sector = " << my_lctSector[tmp_id] << ", CSC ID = " << my_lctCscId[tmp_id]
		    << ", eta = " << my_lctEta[tmp_id] << ", phi = " << my_lctGlobalPhi[tmp_id] << std::endl;
	  std::cout << "Seg endcap = " << my_recoCscSeg_endcap[iReco*16 + iSeg] << ", station = " << my_recoCscSeg_station[iReco*16 + iSeg]
		    << ", sector = " << my_recoCscSeg_sector[iReco*16 + iSeg] << ", ring = " << my_recoCscSeg_ring[iReco*16 + iSeg]
		    << ", chamber = " << my_recoCscSeg_chamber[iReco*16 + iSeg]
		    << ", eta = " << my_recoCscSeg_glob_eta[iReco*16 + iSeg] << ", phi = " << my_recoCscSeg_glob_phi[iReco*16 + iSeg] << std::endl;
	  std::cout << "\n Available LCTs:" << std::endl;
	  for (uint iLCT = 0; iLCT < *my_numLCTs; iLCT++)
	    std::cout << "LCT endcap = " << my_lctEndcap[iLCT] << ", station = " << my_lctStation[iLCT]
	  	      << ", sector = " << my_lctSector[iLCT] << ", CSC ID = " << my_lctCscId[iLCT]
	  	      << ", eta = " << my_lctEta[iLCT] << ", phi = " << my_lctGlobalPhi[iLCT] << std::endl;
	}

	// If there is not already an LCT matched to a segment in this station, fill it
	bool tmp_has_match = false;
	if (reco_num_st[iSt] != 0) { 
	  // Loop over the existing matched LCTs in this station and check for a match
	  for (uint id0 = 0; id0 < reco_num_st[iSt]; id0++) {
	    if ( my_lctBx[tmp_id] == my_lctBx[reco_st_id[iSt][id0]] &&
		 (my_lctEndcap[tmp_id] == 1) == (my_lctEndcap[reco_st_id[iSt][id0]] == 1) &&
		 my_lctStation[tmp_id] == my_lctStation[reco_st_id[iSt][id0]] &&
		 my_lctSector[tmp_id] == my_lctSector[reco_st_id[iSt][id0]] &&
		 my_lctRing[tmp_id] == my_lctRing[reco_st_id[iSt][id0]] &&
		 my_lctChamber[tmp_id] == my_lctChamber[reco_st_id[iSt][id0]] &&
		 my_lctStrip[tmp_id] == my_lctStrip[reco_st_id[iSt][id0]] &&
		 my_lctWire[tmp_id] == my_lctWire[reco_st_id[iSt][id0]] ) tmp_has_match = true;
	  }
	} // End conditional: if (reco_num_st[iSt] != 0) 
	
	// Only fill this LCT if it is not a duplicate
	if (not tmp_has_match) {
	  if (reco_num_st[iSt] > 3) {
	    cout << "Super-bizzare situation where > 4 LCTs in a single station are matched to the RECO muon" << endl;
	    continue;
	  }

	  // Compute the dPhi and dEta between the LCT and the RECO muon
	  float dPhi = acos(cos(my_lctGlobalPhi[tmp_id] - my_recoPhi[iReco]));
	  dPhi *= sin(my_lctGlobalPhi[tmp_id] - my_recoPhi[iReco]) / abs(sin(my_lctGlobalPhi[tmp_id] - my_recoPhi[iReco]));
	  dPhi *= my_recoCharge[iReco];
	  float dEta = my_lctEta[tmp_id] - my_recoEta[iReco];
	  max_eta = std::fmax( max_eta, my_lctEta[tmp_id] );
	  min_eta = std::fmin( min_eta, my_lctEta[tmp_id] );

	  // // Compute the dPhi between the CSC segment and the RECO muon
	  // float dPhi = acos(cos(my_recoCscSeg_glob_phi[iReco*16 + iSeg] - my_recoPhi[iReco]));
	  // dPhi *= sin(my_recoCscSeg_glob_phi[iReco*16 + iSeg] - my_recoPhi[iReco]) / abs(sin(my_recoCscSeg_glob_phi[iReco*16 + iSeg] - my_recoPhi[iReco]));
	  // float dEta = my_recoCscSeg_glob_eta[iReco*16 + iSeg] - my_recoEta[iReco];

	  // Record the index of LCTs matched to segments of the RECO track
	  reco_st_id[iSt][reco_num_st[iSt]] = tmp_id;
	  reco_num_st[iSt] += 1;

	  // Fill plots comparing the LCT eta/phi to the RECO muon eta/phi
	  h_reco_vs_seg_eta->Fill( my_recoEta[iReco], my_lctEta[tmp_id] );
	  h_reco_vs_seg_phi->Fill( my_recoPhi[iReco], my_lctGlobalPhi[tmp_id] );
	  h_seg_dEta->Fill( std::fmin( std::fmax(dEta, dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );
	  h_seg_dPhi->Fill( std::fmin( std::fmax(dPhi, dPhi_bins[0]+0.01), dPhi_bins[1]-0.01 ) );
	  h_seg_dEta_vs_dPhi->Fill( std::fmin( std::fmax(dPhi, dPhi_bins[0]+0.01), dPhi_bins[1]-0.01 ), 
				    std::fmin( std::fmax(dEta, dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );


	  // // Fill plots comparing the CSC segment eta/phi to the RECO muon eta/phi
	  // h_reco_vs_seg_eta->Fill( my_recoEta[iReco], my_recoCscSeg_glob_eta[iReco*16 + iSeg] );
	  // h_reco_vs_seg_phi->Fill( my_recoPhi[iReco], my_recoCscSeg_glob_phi[iReco*16 + iSeg] );
	  // h_seg_dEta->Fill( std::fmin( std::fmax(dEta, dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );
	  // h_seg_dPhi->Fill( std::fmin( std::fmax(dPhi, dPhi_bins[0]+0.01), dPhi_bins[1]-0.01 ) );
	  // h_seg_dEta_vs_dPhi->Fill( std::fmin( std::fmax(dPhi, dPhi_bins[0]+0.01), dPhi_bins[1]-0.01 ), 
	  // 			    std::fmin( std::fmax(dEta, dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );

	} // End conditional: if (not tmp_has_match)

      } // End loop: for (uint iSeg = 0; iSeg < my_recoNumCscSegs[iReco]; iSeg++)
      if (max_eta != -99 && min_eta != 99)
	h_seg_max_dEta->Fill( std::fmin( std::fmax(max_eta - min_eta, dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );
      else h_seg_max_dEta->Fill(-0.05);


      ////////////////////////////////////////////
      // Look for EMTF tracks matched to RECO muon
      ////////////////////////////////////////////
      
      int trk_st_id[4] = {-999, -999, -999, -999};       // LCT index of every LCT in the EMTF track, one for each station
      int trk_st_id_match[4] = {-999, -999, -999, -999}; // LCT index of every LCT in the EMTF track matched to the RECO muon
      int trk_st_id_unm[4] = {-999, -999, -999, -999};   // LCT index of every LCT in the EMTF track not matched the RECO muon
      
      int max_trk_num_matched = 0; // Maximum number of LCTs matched between the RECO muon and a single EMTF track
      int best_trkId = -999;       // Index of the EMTF track with the most LCTs matched to the RECO muon

      // Loop over EMTF tracks
      for (uint iTrk = 0; iTrk < *my_numTrks; iTrk++) {
	if (iTrk > 7) continue; // We don't store more than 8 tracks in these files
	
	// The ID of LCTs in the trkLct_* arrays for this track, both matched to the RECO muon and unmatched
	int tmp_st_id[4] = {-999, -999, -999, -999};
	int tmp_st_id_match[4] = {-999, -999, -999, -999};
	int tmp_st_id_unm[4] = {-999, -999, -999, -999};

	// Number of LCTs in the EMTF track which match CSC segments
	int trk_num_matched = 0;
	
	if (my_numTrkLCTs[iTrk] > 4) cout << "Why are there " << my_numTrkLCTs[iTrk] << " LCTs in EMTF track " << iTrk+1 << "?" << endl;

	// Loop over LCTs in EMTF track
	for (uint iLct = 0; iLct < my_numTrkLCTs[iTrk]; iLct++) {

	  uint iSt = my_trkLct_station[iTrk*4 + iLct] - 1;

	  if (tmp_st_id[iSt] != -999) cout << "Why does EMTF track " << iTrk+1 << " have more than one hit in station " << iSt+1 << "?" << endl;
	  tmp_st_id[iSt] = iLct;

	  // // Print out information about each LCT in the EMTF track
	  // cout << "\nStation " << iSt+1 << " EMTF LCT: BX = " << my_trkLct_bx[iTrk*4 + iLct] << ", endcap = " <<  my_trkLct_endcap[iTrk*4 + iLct] 
	  // 	    << ", sector = " << my_trkLct_sector[iTrk*4 + iLct] << ", cscId = " << my_trkLct_cscId[iTrk*4 + iLct]
	  // 	    << ", strip = " << my_trkLct_strip[iTrk*4 + iLct] << ", wire = " << my_trkLct_wire[iTrk*4 + iLct] << endl;

	  // Loop over indices of LCTs matched to the RECO muon
	  for (uint iID = 0; iID < reco_num_st[iSt]; iID++) {
	    // // Print out information about each LCT matched to the RECO muon
	    // cout << "Station " << iSt+1 << " RECO LCT " << iID+1 << ": BX = " << my_lctBx[reco_st_id[iSt][iID]] << ", endcap = " <<  my_lctEndcap[reco_st_id[iSt][iID]] 
	    //      << ", sector = " << my_lctSector[reco_st_id[iSt][iID]] << ", cscId = " << my_lctCscId[reco_st_id[iSt][iID]]
	    //      << ", strip = " << my_lctStrip[reco_st_id[iSt][iID]] << ", wire = " << my_lctWire[reco_st_id[iSt][iID]] << endl;

	    // Check if the EMTF LCT and the RECO muon LCT are identical
	    if ( my_trkLct_bx[iTrk*4 + iLct] == my_lctBx[reco_st_id[iSt][iID]] && 
		 (my_trkLct_endcap[iTrk*4 + iLct] == 1) == (my_lctEndcap[reco_st_id[iSt][iID]] == 1) &&
		 my_trkLct_sector[iTrk*4 + iLct] == my_lctSector[reco_st_id[iSt][iID]] && 
		 my_trkLct_ring[iTrk*4 + iLct] == my_lctRing[reco_st_id[iSt][iID]] && 
		 my_trkLct_chamber[iTrk*4 + iLct] == my_lctChamber[reco_st_id[iSt][iID]] && 
		 my_trkLct_strip[iTrk*4 + iLct] == my_lctStrip[reco_st_id[iSt][iID]] && 
		 my_trkLct_wire[iTrk*4 + iLct] == my_lctWire[reco_st_id[iSt][iID]] ) {

	      if (tmp_st_id_match[iSt] != -999) cout << "Why does EMTF hit in station " << iSt+1 << " have more than one matched RECO segment?" << endl;
	      tmp_st_id_match[iSt] = iLct; // Track the indices of EMTF LCTs matched to RECO muons
	      trk_num_matched += 1;
	    } // End conditional: if EMTF LCT matches RECO segment LCT
	  } // End loop: for (uint iID = 0; iID < reco_num_st[iSt]; iID++)
	  
	  // LCT in EMTF track has no matching RECO segment
	  if (tmp_st_id_match[iSt] == -999) tmp_st_id_unm[iSt] = iLct;
	} // End loop: for (uint iLct = 0; iLct < my_numTrkLCTs[iTrk]; iLct++)

	// Check if this EMTF track has the most LCTs matched to the RECO muon
	if (trk_num_matched > max_trk_num_matched) {
	  max_trk_num_matched = trk_num_matched;
	  best_trkId = iTrk;
	  for (uint iSt = 0; iSt < 4; iSt++) {
	    trk_st_id[iSt] = tmp_st_id[iSt];
	    trk_st_id_match[iSt] = tmp_st_id_match[iSt];
	    trk_st_id_unm[iSt] = tmp_st_id_unm[iSt];
	  }
	}
      } // End loop: for (uint iTrk = 0; iTrk < *my_numTrks; iTrk++)
      

      bool deviant = false;
      float max_eta_match = -99;
      float min_eta_match = 99;
      float max_eta_unm = -99;
      float min_eta_unm = 99;
      float max_eta_miss = -99;
      float min_eta_miss = 99;
      // Loop over the LCTs in each station
      for (uint iSt = 0; iSt < 4; iSt++) {

	// LCTs in EMTF track matched to RECO track
	if (trk_st_id_match[iSt] != -999) {

	  float dPhi = acos(cos(my_trkLct_globPhi[best_trkId*4 + trk_st_id_match[iSt]] - my_recoPhi[iReco]));
	  dPhi *= sin(my_trkLct_globPhi[best_trkId*4 + trk_st_id_match[iSt]] - my_recoPhi[iReco]) /
	    abs(sin(my_trkLct_globPhi[best_trkId*4 + trk_st_id_match[iSt]] - my_recoPhi[iReco]));
	  dPhi *= my_recoCharge[iReco];
	  float dEta = my_trkLct_eta[best_trkId*4 + trk_st_id_match[iSt]] - my_recoEta[iReco];
	  dEta = std::fmin( std::fmax(dEta, dEta_bins[0]+0.01), dEta_bins[1]-0.01 );
	  dPhi = std::fmin( std::fmax(dPhi, dPhi_bins[0]+0.01), dPhi_bins[1]-0.01 );
	  max_eta_match = std::fmax( max_eta_match, my_trkLct_eta[best_trkId*4 + trk_st_id_match[iSt]] );
	  min_eta_match = std::fmin( min_eta_match, my_trkLct_eta[best_trkId*4 + trk_st_id_match[iSt]] );

	  h_seg_match_dEta->Fill( dEta );
	  h_seg_match_dPhi->Fill( dPhi );
	  h_seg_match_dEta_vs_dPhi->Fill( dPhi, dEta );
	}

	// LCTs in EMTF track not matched to RECO track
	if (trk_st_id_unm[iSt] != -999) {

	  float dPhi = acos(cos(my_trkLct_globPhi[best_trkId*4 + trk_st_id_unm[iSt]] - my_recoPhi[iReco]));
	  dPhi *= sin(my_trkLct_globPhi[best_trkId*4 + trk_st_id_unm[iSt]] - my_recoPhi[iReco]) /
	    abs(sin(my_trkLct_globPhi[best_trkId*4 + trk_st_id_unm[iSt]] - my_recoPhi[iReco]));
	  dPhi *= my_recoCharge[iReco];
	  float dEta = my_trkLct_eta[best_trkId*4 + trk_st_id_unm[iSt]] - my_recoEta[iReco];
	  dEta = std::fmin( std::fmax(dEta, dEta_bins[0]+0.01), dEta_bins[1]-0.01 );
	  dPhi = std::fmin( std::fmax(dPhi, dPhi_bins[0]+0.01), dPhi_bins[1]-0.01 );
	  max_eta_unm = std::fmax( max_eta_unm, my_trkLct_eta[best_trkId*4 + trk_st_id_unm[iSt]] );
	  min_eta_unm = std::fmin( min_eta_unm, my_trkLct_eta[best_trkId*4 + trk_st_id_unm[iSt]] );

	  h_seg_unm_dEta->Fill( dEta );
	  h_seg_unm_dPhi->Fill( dPhi );
	  h_seg_unm_dEta_vs_dPhi->Fill( dPhi, dEta );

	  if ( abs(dPhi) > 1 || abs(dEta) > 1 ) deviant = true;
	}

	// LCTs in RECO track in station with no matched LCT between EMTF and RECO
	if (trk_st_id_match[iSt] == -999) {

	  // Also require that EMTF track had no LCT in this station at all
	  bool skip_event = false;
	  if (best_trkId > -1) {
	    if (iSt == 0 && (my_trkMode[best_trkId] & 8) == 8) skip_event = true;
	    if (iSt == 1 && (my_trkMode[best_trkId] & 4) == 4) skip_event = true;
	    if (iSt == 2 && (my_trkMode[best_trkId] & 2) == 2) skip_event = true;
	    if (iSt == 3 && (my_trkMode[best_trkId] & 1) == 1) skip_event = true;
	  }
	  if (skip_event) continue;

	  for (uint iID = 0; iID < reco_num_st[iSt]; iID++) {
	    float dPhi = acos(cos(my_lctGlobalPhi[reco_st_id[iSt][iID]] - my_recoPhi[iReco]));
	    dPhi *= sin(my_lctGlobalPhi[reco_st_id[iSt][iID]] - my_recoPhi[iReco]) /
	      abs(sin(my_lctGlobalPhi[reco_st_id[iSt][iID]] - my_recoPhi[iReco]));
	    dPhi *= my_recoCharge[iReco];
	    float dEta = my_lctEta[reco_st_id[iSt][iID]] - my_recoEta[iReco];
	    dEta = std::fmin( std::fmax(dEta, dEta_bins[0]+0.01), dEta_bins[1]-0.01 );
	    dPhi = std::fmin( std::fmax(dPhi, dPhi_bins[0]+0.01), dPhi_bins[1]-0.01 );
	    float station = std::fmin( std::fmax(my_lctStation[reco_st_id[iSt][iID]], station_bins[0]+0.01), station_bins[1]-0.01 );
	    float ring = my_lctRing[reco_st_id[iSt][iID]];
	    if (station > 1) ring += (station*2);
	    float eta = std::fmin( std::fmax(my_lctEta[reco_st_id[iSt][iID]], eta_bins[0]+0.01), eta_bins[1]-0.01 );
	    float phi = std::fmin( std::fmax(my_lctGlobalPhi[reco_st_id[iSt][iID]], phi_bins[0]+0.01), phi_bins[1]-0.01 );
	    max_eta_miss = std::fmax( max_eta_miss, my_lctEta[reco_st_id[iSt][iID]] );
	    min_eta_miss = std::fmin( min_eta_miss, my_lctEta[reco_st_id[iSt][iID]] );

	    h_seg_miss_dEta->Fill( dEta );
	    h_seg_miss_dPhi->Fill( dPhi );
	    h_seg_miss_dEta_vs_dPhi->Fill( dPhi, dEta );
	    h_seg_miss_eta->Fill( eta );
	    h_seg_miss_phi->Fill( phi );
	    h_seg_miss_ring->Fill( ring );
	    h_seg_miss_station->Fill( station );
	    h_seg_miss_dEta_vs_station->Fill( station, dEta );
	    h_seg_miss_dPhi_vs_station->Fill( station, dPhi );
	    h_seg_miss_eta_vs_station->Fill( station, eta );
	    h_seg_miss_eta_vs_ring->Fill( ring, eta );
	    h_seg_miss_phi_vs_station->Fill( station, phi );
	    h_seg_miss_ring_vs_station->Fill( station, ring );

	    // if (abs(dEta) < 0.03 && dPhi > -0.05 && dPhi < 0 && (reco_num_st[0] > 0) + (reco_num_st[1] > 0) + (reco_num_st[2] > 0) + (reco_num_st[3] > 0) > 2) {
	    //   cout << "\nMissing hit in run " << *my_run << ", lumi " << *my_lumi << ", event " << *my_event << endl;
	    //   cout << "RECO muon with pT " << my_recoPt[iReco] << ", eta " << my_recoEta[iReco] << ", phi " << my_recoPhi[iReco]
	    // 	   << " has " << reco_num_st[0] << "/" << reco_num_st[1] << "/" << reco_num_st[2] << "/" << reco_num_st[3]
	    // 	   << " LCTs in stations 1/2/3/4" << endl;
	    //   cout << "Missing hit in station " << station << ", ring " << ring << ", with eta " << eta << ", phi " << phi 
	    // 	   << ", strip " << my_lctStrip[reco_st_id[iSt][iID]] << ", wire " << my_lctWire[reco_st_id[iSt][iID]] << endl;
	    //   if (best_trkId > -1) cout << "Best-matched track has mode " << my_trkMode[best_trkId] << endl;
	    //   else cout << "No EMTF track matched to RECO muon" << endl;
	    // }

	  }
	} // End LCTs in RECO track in station with no matched LCT between EMTF and RECO

      } // End loop over the LCTs in each station
      if (max_eta_match != -99 && min_eta_match != 99) {
	h_seg_match_max_dEta->Fill( std::fmin( std::fmax(max_eta_match - min_eta_match, dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );
	if (max_eta_unm != -99 && min_eta_unm != 99)
	  h_seg_unm_max_dEta->Fill( std::fmin( std::fmax( std::fmax(max_eta_unm - min_eta_match, max_eta_match - min_eta_unm), dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );
	if (max_eta_miss != -99 && min_eta_miss != 99)
	  h_seg_miss_max_dEta->Fill( std::fmin( std::fmax( std::fmax(max_eta_miss - min_eta_match, max_eta_match - min_eta_miss), dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );
      }
      else {
	h_seg_match_max_dEta->Fill(-0.05);
	if (max_eta_unm != -99 && min_eta_unm != 99)
	  h_seg_unm_max_dEta->Fill( std::fmin( std::fmax(max_eta_unm - min_eta_unm, dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );
	else h_seg_unm_max_dEta->Fill(-0.05);
	if (max_eta_miss != -99 && min_eta_miss != 99)
	  h_seg_miss_max_dEta->Fill( std::fmin( std::fmax(max_eta_miss - min_eta_miss, dEta_bins[0]+0.01), dEta_bins[1]-0.01 ) );
	else h_seg_miss_max_dEta->Fill(-0.05);
      }


      if (deviant) {
	cout << "*** EMTF track with very deviant hits ***" << endl;
	cout << "RECO                           eta / phi = " << my_recoEta[iReco] << " / " << my_recoPhi[iReco] << endl;
	for (uint iSt = 0; iSt < 4; iSt++) {
	  if (trk_st_id_match[iSt] != -999)
	    cout << "Matched   hit in station " << iSt+1 << " has eta / phi = " << my_trkLct_eta[best_trkId*4 + trk_st_id_match[iSt]]
		 << " / " << my_trkLct_globPhi[best_trkId*4 + trk_st_id_match[iSt]] << endl;
	  if (trk_st_id_unm[iSt] != -999)
	    cout << "Unmatched hit in station " << iSt+1 << " has eta / phi = " << my_trkLct_eta[best_trkId*4 + trk_st_id_unm[iSt]]
		 << " / " << my_trkLct_globPhi[best_trkId*4 + trk_st_id_unm[iSt]] << endl;
	}
      }

      h_reco_vs_trk_matched_LCTs->Fill( (reco_num_st[0] > 0) + (reco_num_st[1] > 0) + (reco_num_st[2] > 0) + (reco_num_st[3] > 0), max_trk_num_matched );
      h_reco_vs_trk_dR_matched_LCTs->Fill( (reco_num_st_dR[0] > 0) + (reco_num_st_dR[1] > 0) + (reco_num_st_dR[2] > 0) + (reco_num_st_dR[3] > 0), max_trk_num_matched );

      if (best_trkId != -999) {
	h_trk_mode->Fill(my_trkMode[best_trkId]);
	h_trk_mode_vs_reco_eta->Fill( abs(my_recoEta[iReco]), my_trkMode[best_trkId]);
	h_trk_vs_RECO_pT->Fill(my_recoPt[iReco], my_trkPt[best_trkId]);
      }
      else {
	h_trk_mode->Fill( 0 );
	h_trk_mode_vs_reco_eta->Fill( abs(my_recoEta[iReco]), 0);
	h_trk_vs_RECO_pT->Fill( my_recoPt[iReco], 0 ); 
      }

    } // End loop over RECO muons     
    
  } // End loop over TTree entries (events)

  std::cout << nTag << " / " << event_num << " events have a tag muon" << std::endl;
  
  out_file->cd();
  
  h_reco_vs_trk_matched_LCTs->Write();
  h_reco_vs_trk_dR_matched_LCTs->Write();

  h_reco_vs_seg_eta->Write();
  h_reco_vs_seg_phi->Write();

  h_seg_dEta->Write();
  h_seg_max_dEta->Write();
  h_seg_dPhi->Write();
  h_seg_dEta_vs_dPhi->Write();

  h_seg_match_dEta->Write();
  h_seg_match_max_dEta->Write();
  h_seg_match_dPhi->Write();
  h_seg_match_dEta_vs_dPhi->Write();

  h_seg_unm_dEta->Write();
  h_seg_unm_max_dEta->Write();
  h_seg_unm_dPhi->Write();
  h_seg_unm_dEta_vs_dPhi->Write();

  h_seg_miss_dEta->Write();
  h_seg_miss_max_dEta->Write();
  h_seg_miss_dPhi->Write();
  h_seg_miss_dEta_vs_dPhi->Write();
  h_seg_miss_eta->Write();
  h_seg_miss_phi->Write();
  h_seg_miss_ring->Write();
  h_seg_miss_station->Write();
  h_seg_miss_dEta_vs_station->Write();
  h_seg_miss_dPhi_vs_station->Write();
  h_seg_miss_eta_vs_station->Write();
  h_seg_miss_eta_vs_ring->Write();
  h_seg_miss_phi_vs_station->Write();
  h_seg_miss_ring_vs_station->Write();

  h_trk_mode->Write();
  h_trk_vs_RECO_pT->Write();
  h_trk_mode_vs_reco_eta->Write();

  // Look up TCanvas, saveAs("name.png"), emacs shortcuts (select, copy-past, find-replace)
  
  out_file->Close();
  
  printf("Exiting match_EMTF_to_RECO()\n");
}

