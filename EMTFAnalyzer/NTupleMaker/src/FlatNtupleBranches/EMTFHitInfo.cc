
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EMTFHitInfo.h"

void EMTFHitInfo::Initialize() {
  for (auto & str : ints)  mInts.insert( std::pair<TString, int>(str, DINT) );
  for (auto & str : vFlt)  mVFlt.insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  for (auto & str : vInt)  mVInt.insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
}

void EMTFHitInfo::Reset() {
  for (auto & it : mInts) it.second = DINT;
  for (auto & it : mVFlt) it.second.clear();
  for (auto & it : mVInt) it.second.clear();
  INSERT(mInts, "nHits", 0);
  INSERT(mInts, "nHitsCSC", 0);
  INSERT(mInts, "nHitsRPC", 0);
  INSERT(mInts, "nHitsBX0", 0);
  INSERT(mInts, "nHitsCSCBX0", 0);
  INSERT(mInts, "nHitsRPCBX0", 0);
}

void EMTFHitInfo::Fill(const l1t::EMTFHit & emtfHit) {
  // std::cout << "Filling EMTFHitInfo" << std::endl;

  INSERT(mInts, "nHits", ACCESS(mInts, "nHits") + 1 );
  if (emtfHit.Is_CSC() == 1) 
    INSERT(mInts, "nHitsCSC", ACCESS(mInts, "nHitsCSC") + 1 );
  if (emtfHit.Is_RPC() == 1) 
    INSERT(mInts, "nHitsRPC", ACCESS(mInts, "nHitsRPC") + 1 );
  if (emtfHit.BX() == 0) {
    INSERT(mInts, "nHitsBX0", ACCESS(mInts, "nHitsBX0") + 1 );
    if (emtfHit.Is_CSC() == 1) 
      INSERT(mInts, "nHitsCSCBX0", ACCESS(mInts, "nHitsCSCBX0") + 1 );
    if (emtfHit.Is_RPC() == 1) 
      INSERT(mInts, "nHitsRPCBX0", ACCESS(mInts, "nHitsRPCBX0") + 1 );
  }

  INSERT(mVFlt, "hit_eta",          emtf::calc_eta_from_theta_deg( emtfHit.Theta(), emtfHit.Endcap() ) );
  INSERT(mVFlt, "hit_theta",        emtfHit.Theta() );
  INSERT(mVFlt, "hit_phi",          emtfHit.Phi_glob() );
  INSERT(mVFlt, "hit_phi_loc",      emtfHit.Phi_loc() );
  INSERT(mVInt, "hit_eta_int",      emtf::calc_eta_GMT( emtf::calc_eta_from_theta_deg( emtfHit.Theta(), emtfHit.Endcap() ) ) );
  INSERT(mVInt, "hit_theta_int",    emtfHit.Theta_fp() );
  INSERT(mVInt, "hit_phi_int",      emtfHit.Phi_fp() );
  INSERT(mVInt, "hit_endcap",       emtfHit.Endcap() );
  INSERT(mVInt, "hit_sector",       emtfHit.Sector() );
  INSERT(mVInt, "hit_sector_index", emtfHit.Sector_idx() );
  INSERT(mVInt, "hit_station",      emtfHit.Station() );
  INSERT(mVInt, "hit_ring",         emtfHit.Ring() );
  INSERT(mVInt, "hit_CSC_ID",       ( emtfHit.Is_RPC() ? DINT : emtfHit.CSC_ID()) );
  INSERT(mVInt, "hit_chamber",      emtfHit.Chamber() );
  assert( calc_FR_bit(emtfHit.Station(), emtfHit.Ring(), emtfHit.Chamber()) == isFront(emtfHit.Station(), emtfHit.Ring(), emtfHit.Chamber(), emtfHit.Subsystem()) );
  // INSERT(mVInt, "hit_FR",           calc_FR_bit(emtfHit.Station(), emtfHit.Ring(), emtfHit.Chamber()) );
  INSERT(mVInt, "hit_FR",           isFront( emtfHit.Station(), emtfHit.Ring(), emtfHit.Chamber(), emtfHit.Subsystem() ) );
  INSERT(mVInt, "hit_pattern",      ( emtfHit.Is_RPC() ? DINT : emtfHit.Pattern()) );
  INSERT(mVInt, "hit_quality",      ( emtfHit.Is_RPC() ? DINT : emtfHit.Quality()) );
  INSERT(mVInt, "hit_alct_quality", ( emtfHit.Is_RPC() ? DINT : emtfHit.ALCT_quality()) );
  INSERT(mVInt, "hit_clct_quality", ( emtfHit.Is_RPC() ? DINT : emtfHit.CLCT_quality()) );
  INSERT(mVInt, "hit_roll",         (!emtfHit.Is_RPC() ? DINT : emtfHit.Roll()) );
  INSERT(mVInt, "hit_subsector",    emtfHit.Subsector() );
  INSERT(mVInt, "hit_isCSC",        emtfHit.Is_CSC() );
  INSERT(mVInt, "hit_isRPC",        emtfHit.Is_RPC() );
  INSERT(mVInt, "hit_valid",        emtfHit.Valid() );
  INSERT(mVInt, "hit_BX",           emtfHit.BX() );
  INSERT(mVInt, "hit_strip",        ( emtfHit.Is_RPC() ? DINT : emtfHit.Strip()) );
  INSERT(mVInt, "hit_strip_hi",     (!emtfHit.Is_RPC() ? DINT : emtfHit.Strip_hi()) );
  INSERT(mVInt, "hit_strip_low",    (!emtfHit.Is_RPC() ? DINT : emtfHit.Strip_low()) );
  INSERT(mVInt, "hit_wire",         ( emtfHit.Is_RPC() ? DINT : emtfHit.Wire()) );
  INSERT(mVInt, "hit_neighbor",     emtfHit.Neighbor() );
  // std::cout << "Filled EMTFHitInfo" << std::endl;
} // End function: EMTFHitInfo::Fill(const l1t::EMTFHit & emtfHit)
