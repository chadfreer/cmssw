
// Make NTuples for input to BDT training
// Runs off of the new 2017 EMTF emultor
// Andrew Brinkerhoff - 27.06.17

#include "EMTFAnalyzer/NTupleMaker/plugins/FlatNtuple.h"
#include <DataFormats/PatCandidates/interface/Muon.h>
#include "L1Trigger/L1TNtuples/interface/MuonID.h"

// Constructor
FlatNtuple::FlatNtuple(const edm::ParameterSet& iConfig):
  muProp1st_(iConfig.getParameter<edm::ParameterSet>("muProp1st")), // Propagate RECO muon coordinates to 1st muon station
  muProp2nd_(iConfig.getParameter<edm::ParameterSet>("muProp2nd"))  // Propagate RECO muon coordinates to 2nd muon station
{
  // Output file
  edm::Service<TFileService> fs;
  out_tree = fs->make<TTree>("tree","FlatNtupleTree");
  
  // Config parameters  
  isMC   = iConfig.getParameter<bool>("isMC");
  isReco = iConfig.getParameter<bool>("isReco");
  
  // Input collections
  if (isMC)   GenMuon_token    = consumes<std::vector<reco::GenParticle>> (iConfig.getParameter<edm::InputTag>("genMuonTag"));
  if (isReco) RecoMuon_token   = consumes<reco::MuonCollection>           (iConfig.getParameter<edm::InputTag>("recoMuonTag"));
  if (isReco) RecoVertex_token = consumes<reco::VertexCollection>         (iConfig.getParameter<edm::InputTag>("recoVertexTag")); 
  
  EMTFHit_token      = consumes<std::vector<l1t::EMTFHit>>   (iConfig.getParameter<edm::InputTag>("emtfHitTag"));
  EMTFTrack_token    = consumes<std::vector<l1t::EMTFTrack>> (iConfig.getParameter<edm::InputTag>("emtfTrackTag"));
  EMTFUnpTrack_token = consumes<std::vector<l1t::EMTFTrack>> (iConfig.getParameter<edm::InputTag>("emtfUnpTrackTag"));
  
} // End FlatNtuple::FlatNtuple

// Destructor
FlatNtuple::~FlatNtuple() {}


// Called once per event
void FlatNtuple::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  // std::cout << "\nCalling analyze" << std::endl;
  edm::Handle<std::vector<reco::GenParticle>> genMuons;
  if (isMC)   iEvent.getByToken(GenMuon_token, genMuons);
  edm::Handle<reco::MuonCollection> recoMuons;
  if (isReco) iEvent.getByToken(RecoMuon_token, recoMuons);
  edm::Handle<reco::VertexCollection> recoVertices;
  if (isReco) iEvent.getByToken(RecoVertex_token, recoVertices);
  
  edm::Handle<std::vector<l1t::EMTFHit>> emtfHits;
  iEvent.getByToken(EMTFHit_token, emtfHits);
  edm::Handle<std::vector<l1t::EMTFTrack>> emtfTracks;
  iEvent.getByToken(EMTFTrack_token, emtfTracks);
  edm::Handle<std::vector<l1t::EMTFTrack>> emtfUnpTracks;
  iEvent.getByToken(EMTFUnpTrack_token, emtfUnpTracks);
  
  // Reset branch values
  eventInfo.Reset();
  genMuonInfo.Reset();
  emtfHitInfo.Reset();
  emtfTrackInfo.Reset();
  emtfUnpTrackInfo.Reset();
  recoMuonInfo.Reset();
  recoTrkMatcher.Reset();
  
  // std::cout << "About to fill event info" << std::endl;	
  // Fill event info
  eventInfo.Fill(iEvent);
  

  // std::cout << "About to fill RECO muon info" << std::endl;	
  // Fill RECO muon info
  if ( isReco && recoMuons.isValid() && recoVertices.isValid() ) {
    // Set up muon propagator for this event
    muProp1st_.init(iSetup);
    muProp2nd_.init(iSetup);
    // Loop over RECO muons
    for ( reco::MuonCollection::const_iterator mu = recoMuons->begin(); mu != recoMuons->end(); ++mu ) {
      recoMuonInfo.Fill( *mu, (*recoVertices)[0], muProp1st_, muProp2nd_, MIN_RECO_ETA, MAX_RECO_ETA );
    }
  }
  else if (isReco) {
    std::cout << "ERROR: could not get recoMuons or recoVertices from event!!!" << std::endl;
    return;
  }
  
  
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
  
  
  // std::cout << "About to get indices" << std::endl;
  
  // Get indices of EMTF hits in event
  std::vector<std::tuple<int, int, int, float>> hit_sect_stat_etas;
  if ( emtfHits.isValid() ) {
    int iHit = -1;
    for (l1t::EMTFHit emtfHit: *emtfHits) {
      iHit += 1;
      float _hit_eta = emtf::calc_eta_from_theta_deg( emtfHit.Theta(), emtfHit.Endcap() );
      hit_sect_stat_etas.push_back(std::make_tuple( iHit, emtfHit.Sector_idx(), emtfHit.Station(), _hit_eta));
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
  
  std::vector<std::tuple<int, int, float>> unp_trk_sect_etas;
  if (not isMC) {
    // Get indices of unpacked EMTF tracks in event
    if ( emtfUnpTracks.isValid() ) {
      int iTrk = -1;
      for (l1t::EMTFTrack emtfTrk: *emtfUnpTracks) {
	iTrk += 1;
	unp_trk_sect_etas.push_back(std::make_tuple(iTrk, emtfTrk.Sector_idx(), emtfTrk.Eta()));
      }
    }
    else {
      std::cout << "ERROR: could not get emtfUnpTracks from event!!!" << std::endl;
      return;
    }
  }

  // Sort EMTF tracks by sector (low to high), then eta (high to low)
  std::stable_sort(trk_sect_etas.begin(), trk_sect_etas.end(), 
  		   [](auto &left, auto &right) {
  		     return ( std::get<1>(left) == std::get<1>(right) ?       // If same sector
  			      std::get<2>(left)  > std::get<2>(right) :       // Sort by eta (high-to-low)
  			      std::get<1>(left)  < std::get<1>(right) ); } ); // Else sort by sector (low-to-high)
  
  if (not isMC) {
    // Sort unpacked EMTF tracks by sector (low to high), then eta (high to low)
    std::stable_sort(unp_trk_sect_etas.begin(), unp_trk_sect_etas.end(), 
		     [](auto &left, auto &right) {
		       return ( std::get<1>(left) == std::get<1>(right) ?       // If same sector
				std::get<2>(left)  > std::get<2>(right) :       // Sort by eta (high-to-low)
				std::get<1>(left)  < std::get<1>(right) ); } ); // Else sort by sector (low-to-high)
  }


  if (isMC) {
    // Fill GEN muon branches
    uint nGEN = gen_etas.size();
    for (uint i = 0; i < nGEN; i++) {
      int idx = gen_etas.at(i).first;
      int iGen = -1;
      for (reco::GenParticle genMuon: *genMuons) {
	iGen += 1;
	if (iGen == idx) {
	  genMuonInfo.Fill(genMuon);
	}
      } // End for (reco::GenParticle genMuon: *genMuons)
    } // End for (uint i = 0; i < nGEN; i++)
  }

  // std::cout << "About to fill EMTF hit branches" << std::endl;

  // Fill EMTF hit branches
  uint nHIT = hit_sect_stat_etas.size();
  for (uint i = 0; i < nHIT; i++) {
    int idx = std::get<0>(hit_sect_stat_etas.at(i));
    int iHit = -1;
    for (l1t::EMTFHit emtfHit: *emtfHits) {
      iHit += 1;
      if (iHit == idx) {
	emtfHitInfo.Fill(emtfHit);
      }      
    } // End for (l1t::EMTFHit emtfHit: *emtfHits)
  } // End for (uint i = 0; i < nHIT; i++)

  // std::cout << "About to fill EMTF track branches" << std::endl;

  bool passesSingleMu16 = false;
  // Fill EMTF track branches
  uint nTRK = trk_sect_etas.size();
  for (uint i = 0; i < nTRK; i++) {
    int idx = std::get<0>(trk_sect_etas.at(i));
    int iTrk = -1;
    for (l1t::EMTFTrack emtfTrk: *emtfTracks) {
      iTrk += 1;
      if (iTrk == idx) {
	emtfTrackInfo.Fill(emtfTrk, emtfHitInfo);
	if ( (emtfTrk.Mode() == 7 || emtfTrk.Mode() == 11 || emtfTrk.Mode() > 12) &&
	     emtfTrk.Pt() >= 16 ) passesSingleMu16 = true;
      }
    } // End for (l1t::EMTFTrack emtfTrk: *emtfTracks)
  } // End for (uint i = 0; i < nTRK; i++)

  recoTrkMatcher.Fill(recoMuonInfo, emtfTrackInfo, MIN_RECO_ETA, MAX_RECO_ETA);

  // std::cout << "About to fill unpacked EMTF track branches" << std::endl;

  if (not isMC) {
  // Fill Unpacked EMTF track branches
    uint nUnpTRK = unp_trk_sect_etas.size();
    for (uint i = 0; i < nUnpTRK; i++) {
      int idx = std::get<0>(unp_trk_sect_etas.at(i));
      int iTrk = -1;
      for (l1t::EMTFTrack emtfTrk: *emtfUnpTracks) {
	iTrk += 1;
	if (iTrk == idx) {
	  emtfUnpTrackInfo.Fill(emtfTrk, emtfHitInfo);
	  if ( (emtfTrk.Mode() == 7 || emtfTrk.Mode() == 11 || emtfTrk.Mode() > 12) &&
	       emtfTrk.Pt() >= 16 ) passesSingleMu16 = true;
	}
      } // End for (l1t::EMTFTrack emtfTrk: *emtfUnpTracks)
    } // End for (uint i = 0; i < nTRK; i++)
  }
  
  // std::cout << "About to fill output tree" << std::endl;
  if (passesSingleMu16 || true) { // No filter for now
    out_tree->Fill();
  }
  // std::cout << "All done with this event!\n" << std::endl;
  return;
      
} // End FlatNtuple::analyze

//void FlatNtuple::init(const edm::EventSetup &eventSetup)
//{
  //muPropagator1st_.init(eventSetup);
  //muPropagator2nd_.init(eventSetup);
//}

// Called once per job before starting event loop
void FlatNtuple::beginJob() {
  
  eventInfo.Initialize();
  genMuonInfo.Initialize();
  emtfHitInfo.Initialize();
  emtfTrackInfo.Initialize();
  emtfUnpTrackInfo.Initialize();
  recoMuonInfo.Initialize();
  recoTrkMatcher.Initialize();
	
  ////////////////////////////////////////////////
  ////   WARNING!!! CONSTRUCTION OF STRUCTS   ////
  ////////////////////////////////////////////////
  // All variables in the struct must have the same length
  // e.g. Int_t (I) and Float_t (F) have 4 bytes, Long64_t (L) and Double_t (D) have 8 bytes
  // https://twiki.cern.ch/twiki/bin/view/Main/RootNotes#Conventions_and_Types
  // https://root.cern.ch/root/html534/guides/users-guide/Trees.html#adding-a-branch-to-hold-a-list-of-variables

  if (not isMC) {
    for (auto & it : eventInfo.mInts)  out_tree->Branch(it.first, (int*)       &it.second);
    for (auto & it : eventInfo.mLongs) out_tree->Branch(it.first, (long long*) &it.second);
  }

  if (isMC) {
    for (auto & it : genMuonInfo.mInts) out_tree->Branch(it.first, (int*) &it.second);
    for (auto & it : genMuonInfo.mVFlt) out_tree->Branch(it.first, (std::vector<float>*) &it.second);
    for (auto & it : genMuonInfo.mVInt) out_tree->Branch(it.first, (std::vector<int>*)   &it.second);
  }

  for (auto & it : emtfHitInfo.mInts) out_tree->Branch(it.first, (int*) &it.second);
  for (auto & it : emtfHitInfo.mVFlt) out_tree->Branch(it.first, (std::vector<float>*) &it.second);
  for (auto & it : emtfHitInfo.mVInt) out_tree->Branch(it.first, (std::vector<int>*)   &it.second);

  for (auto & it : emtfTrackInfo.mInts)  out_tree->Branch(it.first, (int*) &it.second);
  for (auto & it : emtfTrackInfo.mVFlt)  out_tree->Branch(it.first, (std::vector<float>*) &it.second);
  for (auto & it : emtfTrackInfo.mVInt)  out_tree->Branch(it.first, (std::vector<int>*)   &it.second);
  for (auto & it : emtfTrackInfo.mVVInt) out_tree->Branch(it.first, (std::vector<std::vector<int> >*) &it.second);
  
  for (auto & it : recoMuonInfo.mInts)  out_tree->Branch(it.first, (int*) &it.second);
  for (auto & it : recoMuonInfo.mVFlt)  out_tree->Branch(it.first, (std::vector<float>*) &it.second);
  for (auto & it : recoMuonInfo.mVInt)  out_tree->Branch(it.first, (std::vector<int>*)   &it.second);

  for (auto & it : recoTrkMatcher.mVFlt)  out_tree->Branch(it.first, (std::vector<float>*) &it.second);
  for (auto & it : recoTrkMatcher.mVInt)  out_tree->Branch(it.first, (std::vector<int>*)   &it.second);
	
  if (not isMC) {
    for (auto & it : emtfUnpTrackInfo.mInts)  out_tree->Branch(it.first, (int*) &it.second);
    for (auto & it : emtfUnpTrackInfo.mVFlt)  out_tree->Branch(it.first, (std::vector<float>*) &it.second);
    for (auto & it : emtfUnpTrackInfo.mVInt)  out_tree->Branch(it.first, (std::vector<int>*)   &it.second);
    for (auto & it : emtfUnpTrackInfo.mVVInt) out_tree->Branch(it.first, (std::vector<std::vector<int> >*) &it.second);
  }

} // End FlatNtuple::beginJob

// Called once per job after ending event loop
void FlatNtuple::endJob() {}

