
#include "EMTFAnalyzer/NTupleMaker/interface/FlatNtupleBranches/EventInfo.h"

void EventInfo::Initialize() {
  for (auto & str : ints)  mInts .insert( std::pair<TString, int>(str, DINT) );
  for (auto & str : longs) mLongs.insert( std::pair<TString, long long>(str, DLONG) );
}

void EventInfo::Reset() {
  for (auto & it : mInts)  it.second = DINT;
  for (auto & it : mLongs) it.second = DLONG;
}

void EventInfo::Fill(const edm::Event & iEvent) {
  INSERT(mInts,  "evt_run",   iEvent.id().run() );
  INSERT(mInts,  "evt_LS",    iEvent.id().luminosityBlock() );
  INSERT(mLongs, "evt_event", iEvent.id().event() );
  INSERT(mLongs, "evt_orbit", iEvent.orbitNumber() );
  INSERT(mInts,  "evt_BX",    iEvent.bunchCrossing() );
} // End function: EventInfo::Fill(const edm::Event & iEvent)
