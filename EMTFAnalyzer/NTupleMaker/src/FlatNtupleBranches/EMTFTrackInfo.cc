
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EMTFHitInfo.h"
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EMTFTrackInfo.h"

void EMTFTrackInfo::Initialize() {
  for (auto & str : ints)  mInts .insert( std::pair<TString, int>(str, DINT) );
  for (auto & str : vFlt)  mVFlt .insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  for (auto & str : vInt)  mVInt .insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
  for (auto & str : vvInt) mVVInt.insert( std::pair<TString, std::vector<std::vector<int> > >(str, DVVINT) );
}

void EMTFTrackInfo::Reset() {
  for (auto & it : mInts)  it.second = DINT;
  for (auto & it : mVFlt)  it.second.clear();
  for (auto & it : mVInt)  it.second.clear();
  for (auto & it : mVVInt) it.second.clear();
  INSERT(mInts, "nTracks", 0);
  INSERT(mInts, "nTracksBX0", 0);
}

void EMTFTrackInfo::Fill(const l1t::EMTFTrack & emtfTrk, const EMTFHitInfo & hits) {
  // std::cout << "Filling EMTFTrackInfo" << std::endl;

  INSERT(mInts, "nTracks", ACCESS(mInts, "nTracks") + 1 );
  if (emtfTrk.BX() == 0) 
    INSERT(mInts, "nTracksBX0", ACCESS(mInts, "nTracksBX0") + 1 );

  INSERT(mVFlt, "trk_pt",            emtfTrk.Pt() );
  INSERT(mVFlt, "trk_eta",           emtfTrk.Eta() );
  INSERT(mVFlt, "trk_theta",         emtfTrk.Theta() );
  INSERT(mVFlt, "trk_phi",           emtfTrk.Phi_glob() );
  INSERT(mVFlt, "trk_phi_loc",       emtfTrk.Phi_loc() );
  INSERT(mVInt, "trk_pt_int",        emtfTrk.GMT_pt() );
  INSERT(mVInt, "trk_eta_int",       emtfTrk.GMT_eta() );
  INSERT(mVInt, "trk_theta_int",     emtfTrk.Theta_fp() );
  INSERT(mVInt, "trk_phi_int",       emtfTrk.Phi_fp() );
  INSERT(mVInt, "trk_BX",            emtfTrk.BX() );
  INSERT(mVInt, "trk_endcap",        emtfTrk.Endcap() );
  INSERT(mVInt, "trk_sector",        emtfTrk.Sector() );
  INSERT(mVInt, "trk_sector_index",  emtfTrk.Sector_idx() );
  INSERT(mVInt, "trk_mode",          emtfTrk.Mode() );
  INSERT(mVInt, "trk_mode_CSC",      emtfTrk.Mode_CSC() );
  INSERT(mVInt, "trk_mode_RPC",      emtfTrk.Mode_RPC() );
  INSERT(mVInt, "trk_mode_neighbor", emtfTrk.Mode_neighbor() );
  INSERT(mVInt, "trk_charge",        emtfTrk.Charge() );

  INSERT(mVVInt, "trk_iHit", DVINT ); 

  int _nTrkHits = 0, _nTrkRPC = 0, _nTrkNeighbor = 0;
  int _minBX =  9999, _minPh =  9999, _minTh =  9999;
  int _maxBX = -9999, _maxPh = -9999, _maxTh = -9999;

  for (const auto& trk_hit : emtfTrk.Hits()) {

    _nTrkHits += 1;
    if (trk_hit.Is_RPC() == 1)
      _nTrkRPC += 1;
    if (trk_hit.Neighbor() == 1)
      _nTrkNeighbor += 1;

    bool foundHit = false;
    bool foundTwoHits = false;
    for (int i = 0; i < ACCESS(hits.mInts, "nHits"); i++) {
      const std::map<TString, std::vector<int> > * iHit = &(hits.mVInt);

      if ( trk_hit.Is_CSC()     == ACCESS(*iHit, "hit_isCSC").at(i) &&
	   trk_hit.Is_RPC()     == ACCESS(*iHit, "hit_isRPC").at(i) &&  
	   trk_hit.BX()         == ACCESS(*iHit, "hit_BX").at(i) && 
	   trk_hit.Endcap()     == ACCESS(*iHit, "hit_endcap").at(i) &&
	   trk_hit.Sector()     == ACCESS(*iHit, "hit_sector").at(i) &&
	   trk_hit.Sector_idx() == ACCESS(*iHit, "hit_sector_index").at(i) &&
	   trk_hit.Subsector()  == ACCESS(*iHit, "hit_subsector").at(i) &&
	   trk_hit.Station()    == ACCESS(*iHit, "hit_station").at(i) &&
	   trk_hit.Ring()       == ACCESS(*iHit, "hit_ring").at(i) &&
	   trk_hit.Chamber()    == ACCESS(*iHit, "hit_chamber").at(i) &&
	   ( ( trk_hit.Is_CSC() && 
	       trk_hit.CSC_ID()  == ACCESS(*iHit, "hit_CSC_ID").at(i) &&
	       trk_hit.Pattern() == ACCESS(*iHit, "hit_pattern").at(i) &&
	       trk_hit.Quality() == ACCESS(*iHit, "hit_quality").at(i) &&
	       trk_hit.Strip()   == ACCESS(*iHit, "hit_strip").at(i) &&
	       trk_hit.Wire()    == ACCESS(*iHit, "hit_wire").at(i)   ) ||
	     ( trk_hit.Is_RPC() &&
	       trk_hit.Roll()      == ACCESS(*iHit, "hit_roll").at(i) &&
	       trk_hit.Strip_hi()  == ACCESS(*iHit, "hit_strip_hi").at(i) &&
	       trk_hit.Strip_low() == ACCESS(*iHit, "hit_strip_low").at(i) ) ) ) {

	INSERT(mVVInt, "trk_iHit", i );
	if (foundHit) foundTwoHits = true;
	foundHit = true;
	_minBX = std::min(_minBX, trk_hit.BX());
	_maxBX = std::max(_maxBX, trk_hit.BX());
	_minPh = std::min(_minPh, trk_hit.Phi_fp());
	_maxPh = std::max(_maxPh, trk_hit.Phi_fp());
	_minTh = std::min(_minTh, trk_hit.Theta_fp());
	_maxTh = std::max(_maxTh, trk_hit.Theta_fp());
      }

    } // End loop: for (int i = 0; i < ACCESS(hits.mInts, "nHits"); i++)
    if ((not foundHit) or foundTwoHits) {
      std::cout << "\n\n***  Rare EMTF track matching bug  ***" << std::endl;
      std::cout << "Found no match (or two matches) in emulator for the following emulator hit:" << std::endl;
      PrintEMTFHit(trk_hit);
      for (int i = 0; i < ACCESS(hits.mInts, "nHits"); i++) {
	const std::map<TString, std::vector<int> > * iHit = &(hits.mVInt);
	PrintHit(iHit, i);
      }
      std::cout << "\n\n" << std::endl;
      assert(foundHit);
    }
    assert(not foundTwoHits);

  } // End loop: for (const auto& trk_hit : emtfTrk.Hits()) {

  INSERT(mVInt, "trk_nHits",      _nTrkHits );
  INSERT(mVInt, "trk_nRPC",       _nTrkRPC );
  INSERT(mVInt, "trk_nNeighbor",  _nTrkNeighbor );
  INSERT(mVInt, "trk_dBX",        _maxBX - _minBX );
  INSERT(mVInt, "trk_dPhi_int",   _maxPh - _minPh );
  INSERT(mVInt, "trk_dTheta_int", _maxTh - _minTh );

  // std::cout << "Filled EMTFTrackInfo" << std::endl;
} // End function: EMTFTrackInfo::Fill(const l1t::EMTFTrack & emtfTrk, const EMTFHitInfo & hits)
