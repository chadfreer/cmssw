
#ifndef PtLutInputBranches_h
#define PtLutInputBranches_h

// GEN particles
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

// EMTF classes
#include "DataFormats/L1TMuon/interface/EMTFHit.h"
#include "DataFormats/L1TMuon/interface/EMTFTrack.h"

// Helpful tools
#include "EMTFAnalyzer/NTupleMaker/interface/HelperFunctions.h"
#include "L1Trigger/L1TMuonEndCap/interface/TrackTools.h"


// Size of branches
const unsigned int N_GEN =  2;
const unsigned int N_HIT = 24; // 24 for MuGun MC, 48 for JPsi MC
const unsigned int N_TRK =  4; //  4 for MuGun MC,  6 for JPsi MC

// Default fill values
const int   DINT = -999;
const float DFLT = -999.0;

// Structs for output tree
typedef struct {
  int nMuons;
  float pt[N_GEN], eta[N_GEN], theta[N_GEN], phi[N_GEN];
  int charge[N_GEN];
  void Initialize();
  void Fill(unsigned int i, reco::GenParticle genMuon);
} GenMuonBranch;

typedef struct {
  int nHits;
  float eta[N_HIT], theta[N_HIT], phi[N_HIT], phi_loc[N_HIT];
  int eta_int[N_HIT], theta_int[N_HIT], phi_int[N_HIT];
  int endcap[N_HIT], sector[N_HIT], sector_index[N_HIT], station[N_HIT], ring[N_HIT];
  int CSC_ID[N_HIT], chamber[N_HIT], FR[N_HIT], pattern[N_HIT];
  int roll[N_HIT], subsector[N_HIT], isRPC[N_HIT], valid[N_HIT];
  int BX[N_HIT], strip[N_HIT], wire[N_HIT];
  void Initialize();
  void Fill(unsigned int i, l1t::EMTFHit emtfHit);
} EMTFHitBranch;

typedef struct {
  int nTracks;
  float pt[N_TRK], eta[N_TRK], theta[N_TRK], phi[N_TRK], phi_loc[N_TRK];
  int pt_int[N_TRK], eta_int[N_TRK], theta_int[N_TRK], phi_int[N_TRK], BX[N_TRK];
  int endcap[N_TRK], sector[N_TRK], sector_index[N_TRK], mode[N_TRK], charge[N_TRK];

  int nHits[N_TRK], nRPC[N_TRK];
  float hit_eta[N_TRK][4], hit_theta[N_TRK][4], hit_phi[N_TRK][4], hit_phi_loc[N_TRK][4];
  int hit_eta_int[N_TRK][4], hit_theta_int[N_TRK][4], hit_phi_int[N_TRK][4];
  int hit_endcap[N_TRK][4], hit_sector[N_TRK][4], hit_sector_index[N_TRK][4], hit_station[N_TRK][4], hit_ring[N_TRK][4];
  int hit_CSC_ID[N_TRK][4], hit_chamber[N_TRK][4], hit_FR[N_TRK][4], hit_pattern[N_TRK][4];
  int hit_roll[N_TRK][4], hit_subsector[N_TRK][4], hit_isRPC[N_TRK][4], hit_valid[N_TRK][4];
  int hit_BX[N_TRK][4], hit_strip[N_TRK][4], hit_wire[N_TRK][4];

  void Initialize();
  void Fill(unsigned int i, l1t::EMTFTrack emtfTrk);
} EMTFTrackBranch;


#endif /* define PtLutInputBranches_h */
