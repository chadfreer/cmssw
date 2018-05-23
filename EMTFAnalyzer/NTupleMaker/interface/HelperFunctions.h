
#ifndef HelperFunctions_h
#define HelperFunctions_h

// Most helper functions already defined in EMTF emulator
#include "L1Trigger/L1TMuonEndCap/interface/TrackTools.h"

inline bool calc_FR_bit(int station, int ring, int chamber) {
  bool result = false;
  bool isOverlapping = !(station == 1 && ring == 3);
  // Not overlapping means back
  if(isOverlapping) {
    bool isEven = (chamber % 2 == 0);
    // odd chambers are bolted to the iron, which faces
    // forward in 1 & 2, backward in 3 & 4, so...
    result = (station < 3) ? isEven : !isEven;
  }
  return result;
}

// Taken from L1Trigger/L1TMuonEndCap/src/AngleCalculation.cc
inline bool isFront(int station, int ring, int chamber, int subsystem) {

  if (subsystem > 2)  // Not CSC and not RPC
    return true;

  bool result = false;
  bool isOverlapping = !(station == 1 && ring == 3);
  // not overlapping means back
  if(isOverlapping) {
    bool isEven = (chamber % 2 == 0);
    // odd chambers are bolted to the iron, which faces
    // forward in 1&2, backward in 3&4, so...
    result = (station < 3) ? isEven : !isEven;
  }
  return result;
}


#endif /* define HelperFunctions_h */
