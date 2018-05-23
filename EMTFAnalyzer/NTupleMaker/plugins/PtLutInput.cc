
// Make NTuples for input to BDT training
// Runs off of the new 2017 EMTF emultor
// Andrew Brinkerhoff - 27.06.17

#include "EMTFAnalyzer/NTupleMaker/plugins/PtLutInput.h"

// Constructor
PtLutInput::PtLutInput(const edm::ParameterSet& iConfig) {

  // Output file
  edm::Service<TFileService> fs;
  out_tree = fs->make<TTree>("tree","PtLutInputTree");

  // Config parameters
  isMC = iConfig.getParameter<bool>("isMC");

  // Input collections
  if (isMC)
    GenMuon_token = consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genMuonTag"));

  EMTFHit_token = consumes<std::vector<l1t::EMTFHit>>(iConfig.getParameter<edm::InputTag>("emtfHitTag"));
  EMTFTrack_token = consumes<std::vector<l1t::EMTFTrack>>(iConfig.getParameter<edm::InputTag>("emtfTrackTag"));

} // End PtLutInput::PtLutInput

// Destructor
PtLutInput::~PtLutInput() {}


// Called once per event
void PtLutInput::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  // Get input collections
  edm::Handle<std::vector<reco::GenParticle>> genMuons;
  if (isMC)
    iEvent.getByToken(GenMuon_token, genMuons);

  edm::Handle<std::vector<l1t::EMTFHit>> emtfHits;
  iEvent.getByToken(EMTFHit_token, emtfHits);
  edm::Handle<std::vector<l1t::EMTFTrack>> emtfTracks;
  iEvent.getByToken(EMTFTrack_token, emtfTracks);

  // Initialize branch values
  _muon.Initialize();
  _hit.Initialize();
  _track.Initialize();

  // Get indices of GEN muons in event
  std::vector<std::pair<int, float>> gen_etas;
  if ( isMC && genMuons.isValid() ) {
    int iGen = -1;
    for (reco::GenParticle genMuon: *genMuons) {
      iGen += 1;
      if (abs(genMuon.pdgId()) != 13) continue; // Must be a muon

      if ( (fabs(genMuon.eta()) > MIN_GEN_ETA) && (fabs(genMuon.eta()) < MAX_GEN_ETA) )
  	gen_etas.push_back(std::make_pair(iGen, genMuon.eta()));
    }
  }
  else if (isMC) {
    std::cout << "ERROR: could not get genMuons from event!!!" << std::endl;
    return;
  }

  // Skip event if there are no GEN muons within acceptance
  if (isMC && gen_etas.size() == 0) {
    return;
  }

  // Sort GEN muons by eta, high to low
  std::stable_sort(gen_etas.begin(), gen_etas.end(), 
  		   [](auto &left, auto &right) {
  		     return left.second > right.second; } );
  
  
  // Get indices of EMTF hits in event
  std::vector<std::tuple<int, int, int, float>> hit_sect_stat_etas;
  if ( emtfHits.isValid() ) {
    int iHit = -1;
    for (l1t::EMTFHit emtfHit: *emtfHits) {
      iHit += 1;
      float eta_flt = emtf::calc_eta_from_theta_deg( emtfHit.Theta(), emtfHit.Endcap() );
      hit_sect_stat_etas.push_back(std::make_tuple( iHit, emtfHit.Sector_idx(), emtfHit.Station(), eta_flt));
    }
    if (iHit == -1 && not isMC)
      return;
  }
  else {
    std::cout << "ERROR: could not get emtfHits from event!!!" << std::endl;
    return;
  }

  // Sort EMTF hits by sector (low to high), then eta (high to low)
  std::stable_sort(hit_sect_stat_etas.begin(), hit_sect_stat_etas.end(), 
  		   [](auto &left, auto &right) {
  		     return ( std::get<1>(left) == std::get<1>(right) ?       // If same sector
  			      ( std::get<2>(left) == std::get<2>(right) ?     // If same station
  				std::get<3>(left)  > std::get<3>(right) :     // Sort by eta (high-to-low)
  				std::get<2>(left)  < std::get<2>(right) ) :   // Else sort by sector (low-to-high)
  			      std::get<1>(left)  < std::get<1>(right) ); } ); // Else sort by sector (low-to-high)

  // Get indices of EMTF tracks in event
  std::vector<std::tuple<int, int, float>> trk_sect_etas;
  if ( emtfTracks.isValid() ) {
    int iTrk = -1;
    for (l1t::EMTFTrack emtfTrk: *emtfTracks) {
      iTrk += 1;
      trk_sect_etas.push_back(std::make_tuple(iTrk, emtfTrk.Sector_idx(), emtfTrk.Eta()));
    }
  }
  else {
    std::cout << "ERROR: could not get emtfTracks from event!!!" << std::endl;
    return;
  }

  // Sort EMTF tracks by sector (low to high), then eta (high to low)
  std::stable_sort(trk_sect_etas.begin(), trk_sect_etas.end(), 
  		   [](auto &left, auto &right) {
  		     return ( std::get<1>(left) == std::get<1>(right) ?       // If same sector
  			      std::get<2>(left)  > std::get<2>(right) :       // Sort by eta (high-to-low)
  			      std::get<1>(left)  < std::get<1>(right) ); } ); // Else sort by sector (low-to-high)

  // // For MuGun sample, don't allow more than one track per sector
  // bool ghost_track = false;
  // int last_sect = -1;
  // for (uint i = 0; i < trk_sect_etas.size(); i++ ) {
  //   if (std::get<1>(trk_sect_etas.at(i)) == last_sect)
  //     ghost_track = true;
  // }
  // if (ghost_track) {
  //   out_tree->Fill();
  //   return;
  // }

  // Fill GEN muon branches
  for (uint i = 0; i < N_GEN; i++) {
    if (i < gen_etas.size()) {
      int idx = gen_etas.at(i).first;
      int iGen = -1;
      for (reco::GenParticle genMuon: *genMuons) {
  	iGen += 1;
  	if (iGen != idx) 
  	  continue;

  	_muon.Fill(i, genMuon);

      } // End for (reco::GenParticle genMuon: *genMuons)
    } // End if (i < gen_etas.size())
  } // End for (uint i = 0; i < N_GEN; i++)

  // Fill EMTF hit branches
  for (uint i = 0; i < N_HIT; i++) {
    if (i < hit_sect_stat_etas.size()) {
      int idx = std::get<0>(hit_sect_stat_etas.at(i));
      int iHit = -1;
      for (l1t::EMTFHit emtfHit: *emtfHits) {
  	iHit += 1;
  	if (iHit != idx) 
  	  continue;

  	_hit.Fill(i, emtfHit);

      } // End for (l1t::EMTFHit emtfHit: *emtfHits)
    } // End if (i < hit_sect_stat_etas.size())
  } // End for (uint i = 0; i < N_HIT; i++)
  
  // Fill EMTF track branches
  for (uint i = 0; i < N_TRK; i++) {
    if (i < trk_sect_etas.size()) {
      int idx = std::get<0>(trk_sect_etas.at(i));
      int iTrk = -1;
      for (l1t::EMTFTrack emtfTrk: *emtfTracks) {
  	iTrk += 1;
  	if (iTrk != idx) 
  	  continue;

  	_track.Fill(i, emtfTrk);
	
      } // End for (l1t::EMTFTrack emtfTrk: *emtfTracks)
    } // End if (i < trk_sect_etas.size())
  } // End for (uint i = 0; i < N_TRK; i++)
      
  out_tree->Fill();
  return;
      
} // End PtLutInput::analyze


// Called once per job before starting event loop
void PtLutInput::beginJob() {

  ////////////////////////////////////////////////
  ////   WARNING!!! CONSTRUCTION OF STRUCTS   ////
  ////////////////////////////////////////////////
  // All variables in the struct must have the same length
  // e.g. Int_t (I) and Float_t (F) have 4 bytes, Long64_t (L) and Double_t (D) have 8 bytes
  // https://twiki.cern.ch/twiki/bin/view/Main/RootNotes#Conventions_and_Types
  // https://root.cern.ch/root/html534/guides/users-guide/Trees.html#adding-a-branch-to-hold-a-list-of-variables

  out_tree->Branch("muon", &_muon, 
		   "nMuons/I:pt[2]/F:eta[2]/F:theta[2]/F:phi[2]/F:charge[2]/I");
  out_tree->Branch("hit", &_hit, 
		   "nHits/I:eta[24]/F:theta[24]/F:phi[24]/F:phi_loc[24]/F:"
		   "eta_int[24]/I:theta_int[24]/I:phi_int[24]/I:"
		   "endcap[24]/I:sector[24]/I:sector_index[24]/I:station[24]/I:"
		   "ring[24]/I:CSC_ID[24]/I:chamber[24]/I:FR[24]/I:pattern[24]/I:"
		   "roll[24]/I:subsector[24]/I:isRPC[24]/I:valid[24]/I:BX[24]/I:"
		   "strip[24]/I:wire[24]/I");
  out_tree->Branch("track", &_track,
		   "nTracks/I:pt[4]/F:eta[4]/F:theta[4]/F:phi[4]/F:phi_loc[4]/F:"
		   "pt_int[4]/I:eta_int[4]/I:theta_int[4]/I:phi_int[4]/I:BX[4]/I:"
		   "endcap[4]/I:sector[4]/I:sector_index[4]/I:mode[4]/I:charge[4]/I:"
		   "nHits[4]/I:nRPC[4]/I:"
		   "hit_eta[4][4]/F:hit_theta[4][4]/F:hit_phi[4][4]/F:hit_phi_loc[4][4]/F:"
		   "hit_eta_int[4][4]/I:hit_theta_int[4][4]/I:hit_phi_int[4][4]/I:"
		   "hit_endcap[4][4]/I:hit_sector[4][4]/I:hit_sector_index[4][4]/I:hit_station[4][4]/I:"
		   "hit_ring[4][4]/I:hit_CSC_ID[4][4]/I:hit_chamber[4][4]/I:hit_FR[4][4]/I:hit_pattern[4][4]/I:"
		   "hit_roll[4][4]/I:hit_subsector[4][4]/I:hit_isRPC[4][4]/I:hit_valid[4][4]/I:hit_BX[4][4]/I:"
		   "hit_strip[4][4]/I:hit_wire[4][4]/I");

} // End PtLutInput::beginJob

// Called once per job after ending event loop
void PtLutInput::endJob() {}
