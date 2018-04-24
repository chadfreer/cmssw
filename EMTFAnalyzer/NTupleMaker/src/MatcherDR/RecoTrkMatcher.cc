#include "EMTFAnalyzer/NTupleMaker/interface/MatcherDR/RecoTrkMatcher.h"
#include "TMath.h"
#include <iostream>
#include <vector>

void RecoTrkMatcher::Initialize() {
  for (auto & str : vFlt)  mVFlt .insert( std::pair<TString, std::vector<float> >(str, DVFLT) );
  for (auto & str : vInt)  mVInt .insert( std::pair<TString, std::vector<int> >  (str, DVINT) );
}

void RecoTrkMatcher::Reset() {
  for (auto & it : mVFlt)  it.second.clear();
  for (auto & it : mVInt)  it.second.clear();
}

void RecoTrkMatcher::Fill(const RecoMuonInfo & recoMuons, const EMTFTrackInfo & emtfTrks, const float min_eta, const float max_eta) {
  
  const float NOMATCH = -999.;
	
  //INSERT(mVFlt, "reco_match_trk_dR", DFLT);
  //INSERT(mVFlt, "reco_match_trk_dPhi", DFLT);
  //INSERT(mVFlt, "reco_match_trk_dEta", DFLT);
  //INSERT(mVInt, "reco_match_iTrk", DINT ); 
  
  const int n1 = ACCESS(recoMuons.mInts, "nRecoMuons");
  const int n2 = ACCESS(emtfTrks.mInts, "nTracks");
  
  std::vector<int> result(n1, -1);
  std::vector<float> reco_eta_St2(n1, NOMATCH);
  std::vector<float> reco_phi_St2(n1, NOMATCH);
  std::vector<float> reco_eta_St1(n1, NOMATCH);
  std::vector<float> reco_phi_St1(n1, NOMATCH);
  std::vector<float> recoEta(n1, NOMATCH);
  std::vector<float> recoPhi(n1, NOMATCH);
  std::vector<float> trkEta(n2, NOMATCH);
  std::vector<float> trkPhi(n2, NOMATCH);
  std::vector<std::vector<float> > deltaRMatrix(n1, std::vector<float>(n2, NOMATCH));
  std::vector<std::vector<float> > deltaEtaMatrix(n1, std::vector<float>(n2, NOMATCH));
  std::vector<std::vector<float> > deltaPhiMatrix(n1, std::vector<float>(n2, NOMATCH));
  
  for (int i = 0; i < n1; i++){
    for (int j = 0; j < n2; j++) {
	    
      //Use reco mu extrapolated coordinates
      const std::map<TString, std::vector<float> > * imu = &(recoMuons.mVFlt);
      const std::map<TString, std::vector<float> > * itrk = &(emtfTrks.mVFlt);
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
  
  // Run through the matrix n1 times to make sure we've found all matches.
  for (int k = 0; k < n1; k++) {
    int i_min = -1;
    int j_min = -1;
    float minDeltaR = -1.0*NOMATCH;
    // find the smallest deltaR b/t reco muons and trks
    for (int i = 0; i < n1; i++){
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
  
}//end Fill
