
#include "EMTFAnalyzer/NTupleMaker/interface/PtLutInputBranches.h"

void GenMuonBranch::Initialize() {
  nMuons = 0;
  for (unsigned int i = 0; i < N_GEN; i++) {
    pt[i]     = DFLT; eta[i] = DFLT;
    theta[i]  = DFLT; phi[i] = DFLT;
    charge[i] = DINT;
  }
}

void EMTFHitBranch::Initialize() {
  nHits = 0;
  for (unsigned int i = 0; i < N_HIT; i++) {
    eta[i]     = DFLT; theta[i]        = DFLT; phi[i]     = DFLT; phi_loc[i] = DFLT;
    eta_int[i] = DINT; theta_int[i]    = DINT; phi_int[i] = DINT; endcap[i]  = DINT;
    sector[i]  = DINT; sector_index[i] = DINT; station[i] = DINT; ring[i]    = DINT;
    CSC_ID[i]  = DINT; chamber[i]      = DINT; FR[i]      = DINT; pattern[i] = DINT;
    roll[i]    = DINT; subsector[i]    = DINT; isRPC[i]   = DINT; valid[i]   = DINT;
    BX[i]      = DINT; strip[i]        = DINT; wire[i]    = DINT;
  }
}

void EMTFTrackBranch::Initialize() {
  nTracks = 0;
  for (unsigned int i = 0; i < N_TRK; i++) {
    pt[i]     = DFLT; eta[i]     = DFLT; theta[i]        = DFLT; phi[i]     = DFLT; phi_loc[i] = DFLT;
    pt_int[i] = DINT; eta_int[i] = DINT; theta_int[i]    = DINT; phi_int[i] = DINT; BX[i]      = DINT;
    endcap[i] = DINT; sector[i]  = DINT; sector_index[i] = DINT; mode[i]    = DINT; charge[i]  = DINT;

    nHits[i] = 0; nRPC[i] = 0;
    for (unsigned int j = 0; j < 4; j++) {
      hit_eta[i][j]     = DFLT; hit_theta[i][j]        = DFLT; hit_phi[i][j]     = DFLT; hit_phi_loc[i][j] = DFLT;
      hit_eta_int[i][j] = DINT; hit_theta_int[i][j]    = DINT; hit_phi_int[i][j] = DINT; hit_endcap[i][j]  = DINT;
      hit_sector[i][j]  = DINT; hit_sector_index[i][j] = DINT; hit_station[i][j] = DINT; hit_ring[i][j]    = DINT;
      hit_CSC_ID[i][j]  = DINT; hit_chamber[i][j]      = DINT; hit_FR[i][j]      = DINT; hit_pattern[i][j] = DINT;
      hit_roll[i][j]    = DINT; hit_subsector[i][j]    = DINT; hit_isRPC[i][j]   = DINT; hit_valid[i][j]   = DINT;
      hit_BX[i][j]      = DINT; hit_strip[i][j]        = DINT; hit_wire[i][j]    = DINT;
    }
  }
}

void GenMuonBranch::Fill(unsigned int i, reco::GenParticle genMuon) {
  float _theta = genMuon.theta() * 180. / M_PI;
  if (_theta > 180) _theta -= 360;
  if (_theta >  90) _theta  = 180. - _theta;
  float _phi = genMuon.phi() * 180. / M_PI;
  if (_phi > 180) _phi -= 360;

  nMuons    = i+1;
  pt[i]     = genMuon.pt();
  eta[i]    = genMuon.eta();
  theta[i]  = _theta;
  phi[i]    = _phi;
  charge[i] = genMuon.charge();
}

void EMTFHitBranch::Fill(unsigned int i, l1t::EMTFHit emtfHit) {
  int   _eta_int = emtf::calc_eta_GMT( emtf::calc_eta_from_theta_deg( emtfHit.Theta(), emtfHit.Endcap() ) );
  float _eta_flt = emtf::calc_eta_from_theta_deg( emtfHit.Theta(), emtfHit.Endcap() );
  
  nHits           = i+1;
  eta[i]          = _eta_flt;
  theta[i]        = emtfHit.Theta();
  phi[i]          = emtfHit.Phi_glob();
  phi_loc[i]      = emtfHit.Phi_loc();
  eta_int[i]      = _eta_int;
  theta_int[i]    = emtfHit.Theta_fp();
  phi_int[i]      = emtfHit.Phi_fp();
  endcap[i]       = (emtfHit.Endcap() == 1 ? 1 : -1);
  sector[i]       = emtfHit.Sector();
  sector_index[i] = (emtfHit.Endcap() == 1 ? emtfHit.PC_sector() : emtfHit.PC_sector() + 6);
  station[i]      = emtfHit.Station();
  ring[i]         = emtfHit.Ring();
  CSC_ID[i]       = emtfHit.CSC_ID();
  chamber[i]      = emtfHit.Chamber();
  FR[i]           = calc_FR_bit(emtfHit.Station(), emtfHit.Ring(), emtfHit.Chamber());
  pattern[i]      = emtfHit.Pattern();
  roll[i]         = emtfHit.Roll();
  subsector[i]    = emtfHit.Subsector();
  isRPC[i]        = (emtfHit.Subsystem() == 2 ? 1 : 0);
  valid[i]        = emtfHit.Valid();
  BX[i]           = emtfHit.BX();
  strip[i]        = (emtfHit.Subsystem() == 2 ? (emtfHit.Strip_hi() + emtfHit.Strip_low()) / 2 : emtfHit.Strip());
  wire[i]         = (emtfHit.Subsystem() == 2 ? DINT : emtfHit.Wire());
}

void EMTFTrackBranch::Fill(unsigned int i, l1t::EMTFTrack emtfTrk) {

  nTracks         = i+1;
  pt[i]           = emtfTrk.Pt();
  eta[i]          = emtfTrk.Eta();
  theta[i]        = emtfTrk.Theta();
  phi[i]          = emtfTrk.Phi_glob();
  phi_loc[i]      = emtfTrk.Phi_loc();
  eta_int[i]      = emtfTrk.GMT_eta();
  theta_int[i]    = emtfTrk.Theta_fp();
  phi_int[i]      = emtfTrk.Phi_fp();
  BX[i]           = emtfTrk.BX();
  endcap[i]       = (emtfTrk.Endcap() == 1 ? 1 : -1);
  sector[i]       = emtfTrk.Sector();
  sector_index[i] = emtfTrk.Sector_idx();
  mode[i]         = emtfTrk.Mode();
  charge[i]       = (emtfTrk.GMT_charge() == 1 ? -1 : 1);

  int _nHits = 0;
  int _nRPC  = 0;
  for (const auto& trk_hit : emtfTrk.Hits()) {
    _nHits += 1;
    unsigned int j = trk_hit.Station() - 1;
    assert(j < 4);

    int   _eta_int_hit = emtf::calc_eta_GMT( emtf::calc_eta_from_theta_deg( trk_hit.Theta(), trk_hit.Endcap() ) );
    float _eta_flt_hit = emtf::calc_eta_from_theta_deg( trk_hit.Theta(), trk_hit.Endcap() );
  
    hit_eta[i][j]          = _eta_flt_hit;
    hit_theta[i][j]        = trk_hit.Theta();
    hit_phi[i][j]          = trk_hit.Phi_glob();
    hit_phi_loc[i][j]      = trk_hit.Phi_loc();
    hit_eta_int[i][j]      = _eta_int_hit;
    hit_theta_int[i][j]    = trk_hit.Theta_fp();
    hit_phi_int[i][j]      = trk_hit.Phi_fp();
    hit_endcap[i][j]       = (trk_hit.Endcap() == 1 ? 1 : -1);
    hit_sector[i][j]       = trk_hit.Sector();
    hit_sector_index[i][j] = (trk_hit.Endcap() == 1 ? trk_hit.PC_sector() : trk_hit.PC_sector() + 6);
    hit_station[i][j]      = trk_hit.Station();
    hit_ring[i][j]         = trk_hit.Ring();
    hit_CSC_ID[i][j]       = trk_hit.CSC_ID();
    hit_chamber[i][j]      = trk_hit.Chamber();
    hit_FR[i][j]           = calc_FR_bit(trk_hit.Station(), trk_hit.Ring(), trk_hit.Chamber());
    hit_pattern[i][j]      = trk_hit.Pattern();
    hit_roll[i][j]         = trk_hit.Roll();
    hit_subsector[i][j]    = trk_hit.Subsector();
    hit_isRPC[i][j]        = (trk_hit.Subsystem() == 2 ? 1 : 0);
    hit_valid[i][j]        = trk_hit.Valid();
    hit_BX[i][j]           = trk_hit.BX();
    hit_strip[i][j]        = (trk_hit.Subsystem() == 2 ? (trk_hit.Strip_hi() + trk_hit.Strip_low()) / 2 : trk_hit.Strip());
    hit_wire[i][j]         = (trk_hit.Subsystem() == 2 ? DINT : trk_hit.Wire());
    if (trk_hit.Subsystem() == 2) _nRPC += 1;
  }
  nHits[i] = _nHits;
  nRPC[i]  = _nRPC;
}
