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
  for (auto & str : vFlt)  mVFlt .insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  for (auto & str : vInt)  mVInt .insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
}

void LCTSegMatcher::Reset() {
  for (auto & it : mInts)  it.second = DINT;
  for (auto & it : mVFlt)  it.second.clear();
  for (auto & it : mVInt)  it.second.clear();
  INSERT(mInts, "numFills", 0);
}

void LCTSegMatcher::Fill(const CSCSegInfo & cscSeg, const EMTFHitInfo & emtfHits) {

  //simple counter
  INSERT(mInts, "numFills", ACCESS(mInts, "numFills") + 1 ); 
std::cout << "I am here!!!" << std::endl;
/*
  std::vector<int> result(n1, -1);
  std::vector<float> seg_eta_St2(n1, NOMATCH);
  std::vector<float> seg_phi_St2(n1, NOMATCH);
  std::vector<float> seg_eta_St1(n1, NOMATCH);
  std::vector<float> seg_phi_St1(n1, NOMATCH);
  std::vector<float> segEta(n1, NOMATCH);
  std::vector<float> segPhi(n1, NOMATCH);
  std::vector<float> hitEta(n2, NOMATCH);
  std::vector<float> hitPhi(n2, NOMATCH);
  std::vector<std::vector<float> > deltaRMatrix(n1, std::vector<float>(n2, NOMATCH));
  std::vector<std::vector<float> > deltaEtaMatrix(n1, std::vector<float>(n2, NOMATCH));
  std::vector<std::vector<float> > deltaPhiMatrix(n1, std::vector<float>(n2, NOMATCH));
*/  
  //prepare variables for loops over segments/LCTs
  const float NOMATCH = -999.;
  const int n1 = ACCESS(cscSeg.mInts, "nSegs");
  const int n2 = ACCESS(emtfHits.mInts, "nHits");

    std::cout << "nsegs:   " << n1 << "    nLCTs:     " << n2 << std::endl;

  for (int i = 0; i < 10; i++){   //loop over segments
    for (int j = 0; j < 10; j++) {//loop over LCTs

    std::cout << "I am still here mawfucka!!!" << std::endl;

      //define the segments vs the LCTs to allow for quick comparisons      
      //std::vector<float> * iseg = &(cscSegs.mVFlt);
      //std::vector<float> * ihit = &(emtfHits.mVFlt);

      std::cout << "so far I am unmatched:(" << std::endl;

      //Check to see if the segment and LCT are in the same endcap (EMTFHit:endcap-->+/-1,CSCDetId:zendcap-->+/-1)
      //int seg_endcap = ACCESS(*iseg, "seg_endcap").at(i);
      //int LCT_endcap = ACCESS(*ihit, "hit_endcap").at(j);
      //if (seg_endcap != LCT_endcap) continue;

      std::cout << "1" << std::endl;

      //Check to see if the segment and LCT are in the same station (EMTFHit:station-->1-4,CSCDetId:station-->1-4)
      int seg_station = ACCESS(cscSeg.mVInt, "seg_station").at(i);
      int LCT_station = ACCESS(emtfHits.mVInt, "hit_station").at(j);
      if (seg_station != LCT_station) continue;

      std::cout << "2" << std::endl;

      //Check to see if the segment and LCT are in the same Ring (EMTFHit:ring-->1-4,CSCDetId:ring-->1-4)
      int seg_ring = ACCESS(cscSeg.mVInt, "seg_ring").at(i);
      int LCT_ring = ACCESS(emtfHits.mVInt, "hit_ring").at(j);
      if (seg_ring != LCT_ring) continue;

      std::cout << "3" << std::endl;

      //Check to see if the segment and LCT are in the same Chamber (EMTFHit:chamber-->1-36,CSCDetId:chamber-->1-36)
      int seg_chamber = ACCESS(cscSeg.mVInt, "seg_chamber").at(i);
      int LCT_chamber = ACCESS(emtfHits.mVInt, "hit_chamber").at(j);
      if (seg_chamber != LCT_chamber) continue;
    
      std::cout << "so far I have matched!!" << std::endl;
      
      float s_time = ACCESS(cscSeg.mVFlt, "seg_time").at(i);
      int s_nRecHits = ACCESS(cscSeg.mVInt, "seg_nRecHits").at(i);

      INSERT(mVFlt, "segment_time", s_time);
      INSERT(mVInt, "segment_nRecHits", s_nRecHits);

    }//end j loop
  }//end i loop 


/*
  for (int i = 0; i < n1; i++){
    for (int j = 0; j < n2; j++) {
	    
      //Use reco mu extrapolated coordinates
      const std::map<TString, std::vector<float> > * iseg = &(cscSegs.mVFlt);
      const std::map<TString, std::vector<float> > * ihit = &(emtfHits.mVFlt);
      reco_eta_St2[i] = ACCESS(*imu, "reco_eta_St2").at(i);
      reco_phi_St2[i] = ACCESS(*imu, "reco_phi_St2").at(i);
      reco_eta_St1[i] = ACCESS(*imu, "reco_eta_St1").at(i);
      reco_phi_St1[i] = ACCESS(*imu, "reco_phi_St1").at(i);
      //reco_eta_St2[i] = ACCESS(recoMuons.mVFlt, "reco_eta_St2").at(i);
      //reco_phi_St2[i] = ACCESS(recoMuons.mVFlt, "reco_phi_St2").at(i);
      //reco_eta_St1[i] = ACCESS(recoMuons.mVFlt, "reco_eta_St1").at(i);
      //reco_phi_St1[i] = ACCESS(recoMuons.mVFlt, "reco_phi_St1").at(i);
      trkEta[j] = ACCESS(*itrk, "trk_eta").at(j);
      trkPhi[j] = ACCESS(*itrk, "trk_phi").at(j);
      //trkEta[j] = ACCESS(emtfTrks.mVFlt, "trk_eta").at(j);
      //trkPhi[j] = ACCESS(emtfTrks.mVFlt, "trk_phi").at(j);
	    
      //2nd station higher priority    
      if(  fabs(reco_eta_St2[i] ) < max_eta && fabs(reco_eta_St2[i]) > min_eta
        && fabs(reco_phi_St2[i]*TMath::Pi()/180.) < TMath::Pi() 
	&& fabs(reco_phi_St2[i]*TMath::Pi()/180.) > -1.0*TMath::Pi() ){
	      recoEta[i] = reco_eta_St2[i];
	      recoPhi[i] = reco_phi_St2[i]*TMath::Pi()/180.;
      }
      else{
	      recoEta[i] = reco_eta_St1[i];
	      recoPhi[i] = reco_phi_St1[i]*TMath::Pi()/180.;
      }
     
      deltaEtaMatrix[i][j] = recoEta[i]-trkEta[j];
      deltaPhiMatrix[i][j] = recoPhi[i]-trkPhi[j]*TMath::Pi()/180.;
      deltaRMatrix[i][j] = sqrt( pow(deltaEtaMatrix[i][j],2) + pow(deltaPhiMatrix[i][j],2) );
    }//end for i
  }//end for j
  
*/

/*
  // Run through the matrix n1 times to make sure we've found all matches.
  for (int k = 0; k < n1; k++) {
    int i_min = -1;
    int j_min = -1;
    float minDeltaR = -1.0*NOMATCH;
    // find the smallest deltaR b/t reco muons and trks
    for      if(  fabs(reco_eta_St2[i] ) < max_eta && fabs(reco_eta_St2[i]) > min_eta
        && fabs(reco_phi_St2[i]*TMath::Pi()/180.) < TMath::Pi()
        && fabs(reco_phi_St2[i]*TMath::Pi()/180.) > -1.0*TMath::Pi() ){
              recoEta[i] = reco_eta_St2[i];
              recoPhi[i] = reco_phi_St2[i]*TMath::Pi()/180.;
      }
      else{
              recoEta[i] = reco_eta_St1[i];
              recoPhi[i] = reco_phi_St1[i]*TMath::Pi()/180.;
      }

      deltaEtaMatrix[i][j] = recoEta[i]-trkEta[j];
      deltaPhiMatrix[i][j] = recoPhi[i]-trkPhi[j]*TMath::Pi()/180.;
      deltaRMatrix[i][j] = sqrt( pow(deltaEtaMatrix[i][j],2) + pow(deltaPhiMatrix[i][j],2) ); (int i = 0; i < n1; i++){
      for (int j = 0; j < n2; j++){
	if (deltaRMatrix[i][j] < minDeltaR) {
	  i_min = i;
	  j_min = j;
	  minDeltaR = deltaRMatrix[i][j];
	}
      }
    }
	  
    //removed matched pairs
    if (minDeltaR < -1.0*NOMATCH) {
      result[i_min] = j_min;
      deltaRMatrix[i_min] = std::vector<float>(n2, NOMATCH);
      for (int i = 0; i < n1; i++) deltaRMatrix[i][j_min] = NOMATCH;
    }
  }//end for k
  
  for (int k = 0; k < n1; k++) {
	  if(result[k]!=-1){
		  INSERT(mVFlt, "reco_match_trk_dPhi", deltaPhiMatrix[k][result[k]]);
                  INSERT(mVFlt, "reco_match_trk_dEta", deltaEtaMatrix[k][result[k]]);
	          INSERT(mVFlt, "reco_match_trk_dR", sqrt( pow(deltaEtaMatrix[k][result[k]],2) + pow(deltaPhiMatrix[k][result[k]],2) ) );       
	  }
	  else{//didn't find a match
		  INSERT(mVFlt, "reco_match_trk_dPhi", NOMATCH);
                  INSERT(mVFlt, "reco_match_trk_dEta", NOMATCH);
	          INSERT(mVFlt, "reco_match_trk_dR", NOMATCH);
	  }
	  INSERT(mVInt, "reco_match_iTrk", result[k]); 
  }
  */
}//end Fill
