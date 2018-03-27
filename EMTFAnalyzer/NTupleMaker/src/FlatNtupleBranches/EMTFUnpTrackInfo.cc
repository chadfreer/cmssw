
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EMTFHitInfo.h"
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EMTFUnpTrackInfo.h"


void EMTFUnpTrackInfo::Initialize() {
  for (auto & str : ints)  mInts .insert( std::pair<TString, int>(str, DINT) );
  for (auto & str : vFlt)  mVFlt .insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  for (auto & str : vInt)  mVInt .insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
  for (auto & str : vvInt) mVVInt.insert( std::pair<TString, std::vector<std::vector<int> > >(str, DVVINT) );
}

void EMTFUnpTrackInfo::Reset() {
  for (auto & it : mInts)  it.second = DINT;
  for (auto & it : mVFlt)  it.second.clear();
  for (auto & it : mVInt)  it.second.clear();
  for (auto & it : mVVInt) it.second.clear();
  INSERT(mInts, "nUnpTracks", 0);
  INSERT(mInts, "nUnpTracksBX0", 0);
}

void EMTFUnpTrackInfo::Fill(const l1t::EMTFTrack & emtfTrk, const EMTFHitInfo & hits) {
  // std::cout << "Filling EMTFUnpTrackInfo" << std::endl;

  bool ReEmulLCTs = true; // Don't expect perfect hit-track matching if using re-emulated LCTs as input

  INSERT(mInts, "nUnpTracks", ACCESS(mInts, "nUnpTracks") + 1 );
  if (emtfTrk.BX() == 0) 
    INSERT(mInts, "nUnpTracksBX0", ACCESS(mInts, "nUnpTracksBX0") + 1 );

  INSERT(mVFlt, "unp_trk_pt",            emtfTrk.Pt() );
  INSERT(mVFlt, "unp_trk_eta",           emtfTrk.Eta() );
  INSERT(mVFlt, "unp_trk_theta",         emtf::calc_theta_deg( fabs(emtfTrk.Eta()) ) );
  INSERT(mVFlt, "unp_trk_phi",           emtfTrk.Phi_glob() );
  INSERT(mVFlt, "unp_trk_phi_loc",       emtfTrk.Phi_loc() );
  INSERT(mVInt, "unp_trk_pt_int",        emtfTrk.GMT_pt() );
  INSERT(mVInt, "unp_trk_eta_int",       emtfTrk.GMT_eta() );
  INSERT(mVInt, "unp_trk_theta_int",     emtf::calc_theta_int( emtf::calc_theta_deg( emtfTrk.Eta() ), emtfTrk.Endcap(), 7 ) );
  INSERT(mVInt, "unp_trk_phi_int",       emtfTrk.Phi_fp() );
  INSERT(mVInt, "unp_trk_BX",            emtfTrk.BX() );
  INSERT(mVInt, "unp_trk_endcap",        emtfTrk.Endcap() );
  INSERT(mVInt, "unp_trk_sector",        emtfTrk.Sector() );
  INSERT(mVInt, "unp_trk_sector_index",  emtfTrk.Sector_idx() );
  INSERT(mVInt, "unp_trk_mode",          emtfTrk.Mode() );
  INSERT(mVInt, "unp_trk_mode_CSC",      emtfTrk.Mode_CSC() );
  INSERT(mVInt, "unp_trk_mode_RPC",      emtfTrk.Mode_RPC() );
  INSERT(mVInt, "unp_trk_mode_neighbor", emtfTrk.Mode_neighbor() );
  INSERT(mVInt, "unp_trk_charge",        emtfTrk.Charge() );

  INSERT(mVVInt, "unp_trk_iHit", DVINT ); 

  int _nTrkHits = 0, _nTrkRPC = 0, _nTrkNeighbor = 0, _TrkHitMode = 0;
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
	   trk_hit.Endcap()     == ACCESS(*iHit, "hit_endcap").at(i) &&
	   trk_hit.Sector()     == ACCESS(*iHit, "hit_sector").at(i) &&
	   trk_hit.Sector_idx() == ACCESS(*iHit, "hit_sector_index").at(i) &&
	   // trk_hit.Subsector()  == ACCESS(*iHit, "hit_subsector").at(i) &&  // Unpacker uses "-1" for CSC LCTs in stations 2 - 4, emulator uses "0"
	   trk_hit.Station()    == ACCESS(*iHit, "hit_station").at(i) &&
	   trk_hit.Ring()       == ACCESS(*iHit, "hit_ring").at(i) &&
	   trk_hit.Chamber()    == ACCESS(*iHit, "hit_chamber").at(i) &&
	   ( ( trk_hit.Is_CSC() && 
	       trk_hit.BX()      == ACCESS(*iHit, "hit_BX").at(i)      &&
	       trk_hit.CSC_ID()  == ACCESS(*iHit, "hit_CSC_ID").at(i)  &&
	       // trk_hit.Pattern() == ACCESS(*iHit, "hit_pattern").at(i) &&  // Subject to corrupt unpacked values, patched by emulator - AWB 28.09.17
	       // trk_hit.Quality() == ACCESS(*iHit, "hit_quality").at(i) &&  // Subject to corrupt unpacked values, patched by emulator - AWB 28.09.17
	       ( ( trk_hit.Ring() == 4 && (trk_hit.Strip() % 128) == (ACCESS(*iHit, "hit_strip").at(i) % 128) ) ||
		 ( trk_hit.Strip() == ACCESS(*iHit, "hit_strip").at(i) ) ) ) || // Unpacker allows strip > 128 for ME1/1a ("ring 4")
	           // trk_hit.Wire()  == ACCESS(*iHit, "hit_wire").at(i)        // Match only strip, for cases with two LCTs in the same chamber  
	     ( trk_hit.Is_RPC() &&
	       abs(trk_hit.BX() - ACCESS(*iHit, "hit_BX").at(i)) < 2      &&  // Unpacked RPC hits often off by 1 BX - AWB 25.09.17
	       trk_hit.Theta_fp() == ACCESS(*iHit, "hit_theta_int").at(i) &&
	       trk_hit.Phi_fp()   == ACCESS(*iHit, "hit_phi_int").at(i)    ) ) ) {
	
	if ( trk_hit.Is_CSC() && trk_hit.Wire() == ACCESS(*iHit, "hit_wire").at(i) &&
	     ( trk_hit.Pattern() != ACCESS(*iHit, "hit_pattern").at(i) ||
	       trk_hit.Quality() != ACCESS(*iHit, "hit_quality").at(i) ) ) {
	  std::cout << "\n\n***  Bizzare EMTF unpacked CSC LCT corrupt pattern or quality  ***" << std::endl;
	  PrintEMTFHit(trk_hit);
	  PrintHit(iHit, i);
	  std::cout << "\n\n" << std::endl;
	}


	if (not foundHit) {
	  INSERT(mVVInt, "unp_trk_iHit", i );
	  _TrkHitMode += pow(2, (4 - trk_hit.Station()));
	} else if ( trk_hit.Is_CSC() && ACCESS(*iHit, "hit_wire").at(i) != ACCESS(*iHit, "hit_wire").at( mVVInt.at("unp_trk_iHit").back().back() ) ) {
	  // std::cout << "\nTwo matched CSC LCTs: unpacked track theta_int = " << ACCESS(mVInt, "unp_trk_theta_int").back()
	  // 	    << ", previous emulated hit theta_int = " << ACCESS(*iHit, "hit_theta_int").at( mVVInt.at("unp_trk_iHit").back().back() )
	  // 	    << ", new hit theta_int = " << ACCESS(*iHit, "hit_theta_int").at(i) << ". " << std::endl;
	  // PrintEMTFHit(trk_hit);
	  // PrintHit(iHit, mVVInt.at("unp_trk_iHit").back().back());
	  // PrintHit(iHit, i);
	  if ( std::abs(ACCESS(mVInt, "unp_trk_theta_int").back() - ACCESS(*iHit, "hit_theta_int").at(i)) < 
	       std::abs(ACCESS(mVInt, "unp_trk_theta_int").back() - ACCESS(*iHit, "hit_theta_int").at( mVVInt.at("unp_trk_iHit").back().back() )) ) {
	    // std::cout << "Using new one.\n" << std::endl;
	    mVVInt.at("unp_trk_iHit").back().pop_back(); // Remove the previous CSC LCT
	    INSERT(mVVInt, "unp_trk_iHit", i );          // Insert the new CSC LCT
	  } else {
	    // std::cout << "Keeping old one.\n" << std::endl;
	  }
	} else if ( trk_hit.Is_RPC() ) {
	  std::cout << "\nTwo matched RPC hits: unpacked track hit in BX " << trk_hit.BX() 
		    << ", previous emulated hit in BX " << ACCESS(*iHit, "hit_BX").at( ACCESS(mVVInt, "unp_trk_iHit").back().back() )
		    << ", new hit in BX " << ACCESS(*iHit, "hit_BX").at(i) << ". ";
	  assert( ACCESS(*iHit, "hit_BX").at( ACCESS(mVVInt, "unp_trk_iHit").back().back() ) != ACCESS(*iHit, "hit_BX").at(i) );
	  if (trk_hit.BX() == ACCESS(*iHit, "hit_BX").at(i) ) {
	    mVVInt.at("unp_trk_iHit").back().pop_back(); // Remove the previous RPC hit
	    INSERT(mVVInt, "unp_trk_iHit", i );          // Insert the new RPC hit
	    std::cout << "Using new one.\n" << std::endl;
	  } else {
	    std::cout << "Keeping old one.\n" << std::endl;
	  }
	} else if (foundHit) {
	  foundTwoHits = true;
	}
	foundHit = true;
      }

    } // End loop: for (int i = 0; i < ACCESS(hits.mInts, "nHits"); i++)
    if (foundHit) {
      _minBX = std::min(_minBX, trk_hit.BX());
      _maxBX = std::max(_maxBX, trk_hit.BX());
      _minPh = std::min(_minPh, ACCESS(hits.mVInt, "hit_phi_int").at( mVVInt.at("unp_trk_iHit").back().back() ) );
      _maxPh = std::max(_maxPh, ACCESS(hits.mVInt, "hit_phi_int").at( mVVInt.at("unp_trk_iHit").back().back() ) );
      _minTh = std::min(_minTh, ACCESS(hits.mVInt, "hit_theta_int").at( mVVInt.at("unp_trk_iHit").back().back() ) );
      _maxTh = std::max(_maxTh, ACCESS(hits.mVInt, "hit_theta_int").at( mVVInt.at("unp_trk_iHit").back().back() ) );
    }

    // if (not foundHit) {
    if ( ((not foundHit) && (not trk_hit.Is_RPC()) && (not ReEmulLCTs)) || foundTwoHits ) { // Only print out for missing CSC LCTs; missing RPCs not that rare - AWB 26.09.17
      std::cout << "\n\n***  Rare EMTF unpacked track matching bug  ***" << std::endl;
      std::cout << "Found no match (or two matches) in emulator for the following unpacked hit:" << std::endl;
      PrintEMTFHit(trk_hit);
      for (int i = 0; i < ACCESS(hits.mInts, "nHits"); i++) {
	const std::map<TString, std::vector<int> > * iHit = &(hits.mVInt);
	if (ACCESS(*iHit, "hit_isCSC").at(i)) {
	  PrintHit(iHit, i);
	}
      }
      std::cout << "\n\n" << std::endl;
      if (trk_hit.Is_CSC()) {
	assert(foundHit || ReEmulLCTs);
      }
    }
    assert(not foundTwoHits);

  } // End loop: for (const auto& trk_hit : emtfTrk.Hits()) {

  INSERT(mVInt, "unp_trk_nHits",     _nTrkHits );
  INSERT(mVInt, "unp_trk_nRPC",      _nTrkRPC );
  INSERT(mVInt, "unp_trk_nNeighbor", _nTrkNeighbor );
  INSERT(mVInt, "unp_trk_found_hits", (_TrkHitMode == emtfTrk.Mode() ) );
  INSERT(mVInt, "unp_trk_dBX",        _maxBX - _minBX );
  INSERT(mVInt, "unp_trk_dPhi_int",   _maxPh - _minPh );
  INSERT(mVInt, "unp_trk_dTheta_int", _maxTh - _minTh );

  // std::cout << "Filled EMTFUnpTrackInfo" << std::endl;
} // End function: EMTFUnpTrackInfo::Fill(const l1t::EMTFTrack & emtfTrk, const EMTFHitInfo & hits)
