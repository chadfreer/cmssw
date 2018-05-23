/* Code to match EMTF LCTs to CSC reconstructed segments
 * Written by Chad Freer March 27, 2018
 *
 * Will use EMTFHit and CSCSegment collections and check matching using
 * time, endcap, station, ring, and chamber information.
 *
 * Once we have narrowed down to same chambers will use rechit strip and wire position
 * to find if they are in the same physical location and at the same time
*/
#include "EMTFAnalyzer/NTupleMaker/interface/MatcherSeg/LCTSegMatcher.h"
#include "TMath.h"
#include <iostream>
#include <vector>

void LCTSegMatcher::Initialize() {
  for (auto & str : ints)  mInts .insert( std::pair<TString, int>(str, DINT) );
  //for (auto & str : vFlt)  mVFlt .insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  //for (auto & str : vInt)  mVInt .insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
}

void LCTSegMatcher::Reset() {
  for (auto & it : mInts)  it.second = DINT;
  //for (auto & it : mVFlt)  it.second.clear();
  //for (auto & it : mVInt)  it.second.clear();
  INSERT(mInts, "numFills", 0);
  INSERT(mInts, "numMatched", 0);
  INSERT(mInts, "numSegMatched", 0);
  INSERT(mInts, "numLCTMatched", 0);
}

void LCTSegMatcher::Fill(CSCSegInfo & cscSeg, EMTFHitInfo & emtfHits) {

  //prepare variables for loops over segments/LCTs
  const int n1 = ACCESS(cscSeg.mInts, "nSegs");
  const int n2 = ACCESS(emtfHits.mInts, "nHits");
  
  std::cout << "nsegs:   " << n1 << "    nLCTs:     " << n2 << std::endl;

  for (int i = 0; i < n1; i++){   //loop over segments
    INSERT(cscSeg.mVInt, "seg_match_iLCT", DINT); // Pushes back default integer value
  }

  for (int j = 0; j < n2; j++) {//loop over LCTs
          INSERT(emtfHits.mVInt, "hit_match_iSeg", DINT); // Pushes back default integer value
  }


  for (int i = 0; i < n1; i++){   //loop over segments
    for (int j = 0; j < n2; j++) {//loop over LCTs

      if (ACCESS(emtfHits.mVInt, "hit_isCSC").at(j) != 1) continue;//prevent RPC

      //Check to see if the segment and LCT are in the same endcap (EMTFHit:endcap-->+/-1,CSCDetId:zendcap-->+/-1)
      int seg_endcap = ACCESS(cscSeg.mVInt, "seg_endcap").at(i);
      int LCT_endcap = ACCESS(emtfHits.mVInt, "hit_endcap").at(j);
      if (seg_endcap != LCT_endcap) continue;

      //Check to see if the segment and LCT are in the same station (EMTFHit:station-->1-4,CSCDetId:station-->1-4)
      int seg_station = ACCESS(cscSeg.mVInt, "seg_station").at(i);
      int LCT_station = ACCESS(emtfHits.mVInt, "hit_station").at(j);
      if (seg_station != LCT_station) continue;

      //Check to see if the segment and LCT are in the same Ring (EMTFHit:ring-->1-4,CSCDetId:ring-->1-4)
      int seg_ring = ACCESS(cscSeg.mVInt, "seg_ring").at(i);
      int LCT_ring = ACCESS(emtfHits.mVInt, "hit_ring").at(j);
      if (seg_ring != LCT_ring) continue;

      //Check to see if the segment and LCT are in the same Chamber (EMTFHit:chamber-->1-36,CSCDetId:chamber-->1-36)
      int seg_chamber = ACCESS(cscSeg.mVInt, "seg_chamber").at(i);
      int LCT_chamber = ACCESS(emtfHits.mVInt, "hit_chamber").at(j);
      if (seg_chamber != LCT_chamber) continue;
 
      //grab segment strip and wire information 
      int Segment_strip_min = ACCESS(cscSeg.mVInt, "seg_strip_min").at(i) * 2;//convert to units of halfstrips
      int Segment_strip_max = ACCESS(cscSeg.mVInt, "seg_strip_max").at(i) * 2;//convert to units of halfstrips
      int Segment_wire_min = ACCESS(cscSeg.mVInt, "seg_wire_min").at(i);
      int Segment_wire_max = ACCESS(cscSeg.mVInt, "seg_wire_max").at(i);
      if ((Segment_strip_max-Segment_strip_min) > 24)continue;//stop weird trip issue (why does this happen?!)

      //Now find the LCT strip and wire information for potential matches
      int LCT_strip = ACCESS(emtfHits.mVInt, "hit_strip").at(j) + 2;//shift one full strip     
      int LCT_wire = ACCESS(emtfHits.mVInt, "hit_wire").at(j) + 1; //Shifted because LCT starts counting at 0

      //Nice for printouts.(comment out if desired)
      int nRecHits = ACCESS(cscSeg.mVInt, "seg_nRecHits").at(i);
      std::cout << "\nnumber of Rechits:" << nRecHits   << std::endl;
      std::cout << "Segment strip:" << Segment_strip_min << "-" << Segment_strip_max << "     LCT strip:" << LCT_strip  << std::endl;
      std::cout << "Segment wire:" << Segment_wire_min << "-" << Segment_wire_max << "        LCT wire:" << LCT_wire  << "\n" << std::endl;


      //simple counter
      INSERT(mInts, "numFills", ACCESS(mInts, "numFills") + 1 ); 
      //Now start the meat of matching code. Check to see if it is within 2 of strips and wires
      if (LCT_strip > Segment_strip_min-2 && LCT_strip < Segment_strip_max + 2){
         if (LCT_wire > Segment_wire_min-2 && LCT_wire < Segment_wire_max + 2){
           
            INSERT(mInts, "numMatched", ACCESS(mInts, "numMatched") + 1 );
            std::cout << "We have a full match, segment index " << i << " to LCT index " << j << "!" << std::endl;

            //check for double matching (Need to check for neighbor LCTs)
            if (ACCESS(cscSeg.mVInt, "seg_match_iLCT").at(i) >= 0) {
              INSERT(mInts, "numLCTMatched", ACCESS(mInts, "numLCTMatched") + 1 );
              std::cout << "But segment already had a match with index " << ACCESS(cscSeg.mVInt, "seg_match_iLCT").at(i) << "!!!" << std::endl;
              int l = ACCESS(cscSeg.mVInt, "seg_match_iLCT").at(i); //old index
              //Match both LCTs to the segment index but the segment index only to the non-neighbor index
              if (ACCESS(emtfHits.mVInt, "hit_neighbor").at(l) == 1) {//The old match is a neighbor hit
                  INSERT(cscSeg.mVInt, "seg_match_iLCT", i, j); //sets the index to new LCT index
                  INSERT(emtfHits.mVInt, "hit_match_iSeg", j, i);
              }
              if (ACCESS(emtfHits.mVInt, "hit_neighbor").at(j) == 1) {//the new match is a neighbor hit
                  INSERT(emtfHits.mVInt, "hit_match_iSeg", j, i);//only set LCT to match segment and not segment to match LCT              
              }

            //check for double matching
            } else if (ACCESS(emtfHits.mVInt, "hit_match_iSeg").at(j) >= 0) {
              INSERT(mInts, "numSegMatched", ACCESS(mInts, "numSegMatched") + 1 );
      	      std::cout << "But LCT already had a match with index " << ACCESS(emtfHits.mVInt, "hit_match_iSeg").at(j) << "!!!" << std::endl;
              int k = ACCESS(emtfHits.mVInt, "hit_match_iSeg").at(j);              
              
              //check which segment has the most rechits and keep that one
              if (ACCESS(cscSeg.mVInt, "seg_nRecHits").at(i)>(ACCESS(cscSeg.mVInt, "seg_nRecHits").at(k))){
                 INSERT(cscSeg.mVInt, "seg_match_iLCT", k, DINT); // Removes old match with less rechits
                 INSERT(cscSeg.mVInt, "seg_match_iLCT", i, j); // Sets i^th  value in vector to j
                 INSERT(emtfHits.mVInt, "hit_match_iSeg", j, i); // Sets j^th value in vector to i

              }
            } else {//if no double mathing then we save the indices
                INSERT(cscSeg.mVInt, "seg_match_iLCT", i, j); // Sets i^th  value in vector to j
                INSERT(emtfHits.mVInt, "hit_match_iSeg", j, i); // Sets j^th value in vector to i
            }//end double matching checks

         }//end wire conditional

      }//end strip conditional

    }//end j loop
    
  }//end i loop 

}//end Fill
