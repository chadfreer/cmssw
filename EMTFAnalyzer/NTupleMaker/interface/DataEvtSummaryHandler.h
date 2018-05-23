#ifndef dataevtsummaryhandler_h
#define dataevtsummaryhandler_h

#if !defined(__CINT__) || defined(__MAKECINT__)
 
#include <string.h>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <set>
#include <cmath>

#include "Math/LorentzVector.h"
#include "TMath.h"
#include "TVector2.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"

#endif

#define MAXTRK 8
#define MAXTRKHITS 4
#define MAX_MUONS 8
#define MAX_CSC_RECHIT 48 // 4 stations x 6 layers + (overlap between chambers: added other 24 hits to be safe)
#define MAX_LCTS_PER_TRK 4  // max # of LCTS which form a CSCTF track
#define MAX_SEGS_STD 16 // MAX number of segments which can be associated to StandAlone component of the GBL muon

struct DataEvtSummary_t {

  Int_t run,lumi,event;
    
  // ==================
  // Gen Muons
  // ================== 
  Int_t numGenMuons;

  std::vector<float>* genEta;
  std::vector<float>* genPt;
  std::vector<float>* genPhi;
  std::vector<int>*   genId;
  
  // ==================
  // RECO Global Muons
  // ==================
  int numRecoMuons;
  
  std::vector<float>* recoPt;
  std::vector<float>* recoEta;
  std::vector<float>* recoPhi;
  std::vector<int>* recoCharge;
  std::vector<float>* recoSamPt;
  std::vector<int>* recoIsTight;
  std::vector<int>* recoMatchedStations;
  std::vector<float>* recoChi2Norm;

  // Muon CSC Segments
  std::vector<int>* recoNumCscSegs;

  // Segment position information, global
  float recoCscSeg_glob_x[MAX_MUONS][MAX_SEGS_STD];
  float recoCscSeg_glob_y[MAX_MUONS][MAX_SEGS_STD];
  float recoCscSeg_glob_eta[MAX_MUONS][MAX_SEGS_STD];
  float recoCscSeg_glob_phi[MAX_MUONS][MAX_SEGS_STD];
  float recoCscSeg_glob_dir_eta[MAX_MUONS][MAX_SEGS_STD];
  float recoCscSeg_glob_dir_phi[MAX_MUONS][MAX_SEGS_STD];
  
  // General segment information
  int recoCscSeg_endcap[MAX_MUONS][MAX_SEGS_STD];
  int recoCscSeg_station[MAX_MUONS][MAX_SEGS_STD];
  int recoCscSeg_ring[MAX_MUONS][MAX_SEGS_STD];
  int recoCscSeg_chamber[MAX_MUONS][MAX_SEGS_STD];
  int recoCscSeg_nHits[MAX_MUONS][MAX_SEGS_STD];
  int recoCscSeg_sector[MAX_MUONS][MAX_SEGS_STD];
  int recoCscSeg_isLctAble[MAX_MUONS][MAX_SEGS_STD];
  int recoCscSeg_isMatched[MAX_MUONS][MAX_SEGS_STD];  // lctId is the position of the lct in the all LCT collection
  int recoCscSeg_lctId[MAX_MUONS][MAX_SEGS_STD];
  
  // Muon RPC Clusters
  std::vector<int>* recoNumRpcClusts;

  // Cluster position information, global
  float recoRpcClust_glob_x[MAX_MUONS][MAX_SEGS_STD];
  float recoRpcClust_glob_y[MAX_MUONS][MAX_SEGS_STD];
  float recoRpcClust_glob_eta[MAX_MUONS][MAX_SEGS_STD];
  float recoRpcClust_glob_phi[MAX_MUONS][MAX_SEGS_STD];
  float recoRpcClust_glob_dir_eta[MAX_MUONS][MAX_SEGS_STD];
  float recoRpcClust_glob_dir_phi[MAX_MUONS][MAX_SEGS_STD];
  
  // General cluster information
  int recoRpcClust_endcap[MAX_MUONS][MAX_SEGS_STD];
  int recoRpcClust_station[MAX_MUONS][MAX_SEGS_STD];
  int recoRpcClust_ring[MAX_MUONS][MAX_SEGS_STD];
  int recoRpcClust_chamber[MAX_MUONS][MAX_SEGS_STD];
  int recoRpcClust_nHits[MAX_MUONS][MAX_SEGS_STD];
  int recoRpcClust_sector[MAX_MUONS][MAX_SEGS_STD];
  int recoRpcClust_isLctAble[MAX_MUONS][MAX_SEGS_STD];
  int recoRpcClust_isMatched[MAX_MUONS][MAX_SEGS_STD];  // lctId is the position of the lct in the all LCT collection
  int recoRpcClust_lctId[MAX_MUONS][MAX_SEGS_STD];
  
  // ==================
  // CSC LCTS
  // ==================  
  Int_t numLCTs;

  std::vector<int>* lctEndcap;
  std::vector<int>* lctSector;
  std::vector<int>* lctSubSector;
  std::vector<int>* lctBx;
  std::vector<int>* lctBc0;
  std::vector<int>* lctStation;
  std::vector<int>* lctRing;
  std::vector<int>* lctChamber;
  std::vector<int>* lctTriggerCSCID;
  std::vector<float>* lctGlobalPhi;
  std::vector<float>* lctEta;
  std::vector<int>* lctLocPhi;
  std::vector<int>* lctStrip;
  std::vector<int>* lctWire;
  
  // ==================
  // RPC clusters
  // ==================  
  Int_t numClusts;

  std::vector<int>* clustEndcap;
  std::vector<int>* clustSector;
  std::vector<int>* clustSubSector;
  std::vector<int>* clustBx;
  std::vector<int>* clustStation;
  std::vector<int>* clustChamber;
  std::vector<int>* clustWire;
  std::vector<int>* clustStrip;
  std::vector<int>* clustRing;
  std::vector<int>* clustCscId;
  std::vector<float>* clustGlobalPhi;
  std::vector<float>* clustEta;
  std::vector<float>* clustSize;
  
  // ====================
  // Emulator EMTF Tracks and LCTs
  // ====================
  Int_t numTrks;
  std::vector<Int_t>* numTrkLCTs;
  std::vector<float>* trkPt;
  std::vector<float>* trkEta;
  std::vector<float>* trkPhi;
  std::vector<float>* trkGeomPhi;
  std::vector<Int_t>* trkMode;
  std::vector<Int_t>* trkBx;
  std::vector<Int_t>* trkBxBeg;
  std::vector<Int_t>* trkBxEnd;
  std::vector<Int_t>* trkRank;
  std::vector<Int_t>* trkStraight;

  // Track CSC hits
  Int_t trkLct_endcap[MAXTRK][MAXTRKHITS];
  Int_t trkLct_station[MAXTRK][MAXTRKHITS];
  Int_t trkLct_sector[MAXTRK][MAXTRKHITS];
  Int_t trkLct_ring[MAXTRK][MAXTRKHITS];
  Int_t trkLct_chamber[MAXTRK][MAXTRKHITS];
  Int_t trkLct_wire[MAXTRK][MAXTRKHITS];
  Int_t trkLct_strip[MAXTRK][MAXTRKHITS];
  Int_t trkLct_cscId[MAXTRK][MAXTRKHITS];
  float trkLct_globPhi[MAXTRK][MAXTRKHITS];
  float trkLct_geomPhi[MAXTRK][MAXTRKHITS];
  float trkLct_eta[MAXTRK][MAXTRKHITS];
  Int_t trkLct_locPhi[MAXTRK][MAXTRKHITS];
  Int_t trkLct_locTheta[MAXTRK][MAXTRKHITS];
  Int_t trkLct_bx[MAXTRK][MAXTRKHITS];
  Int_t trkLct_qual[MAXTRK][MAXTRKHITS];
  Int_t trkLct_pattern[MAXTRK][MAXTRKHITS];
  
  // Track RPC hits
  Int_t trkClust_endcap[MAXTRK][MAXTRKHITS];
  Int_t trkClust_station[MAXTRK][MAXTRKHITS];
  Int_t trkClust_sector[MAXTRK][MAXTRKHITS];
  Int_t trkClust_ring[MAXTRK][MAXTRKHITS];
  Int_t trkClust_chamber[MAXTRK][MAXTRKHITS];
  Int_t trkClust_wire[MAXTRK][MAXTRKHITS];
  Int_t trkClust_strip[MAXTRK][MAXTRKHITS];
  Int_t trkClust_cscId[MAXTRK][MAXTRKHITS];
  float trkClust_globPhi[MAXTRK][MAXTRKHITS];
  float trkClust_geomPhi[MAXTRK][MAXTRKHITS];
  float trkClust_eta[MAXTRK][MAXTRKHITS];
  Int_t trkClust_locPhi[MAXTRK][MAXTRKHITS];
  Int_t trkClust_locTheta[MAXTRK][MAXTRKHITS];
  Int_t trkClust_bx[MAXTRK][MAXTRKHITS];
  Int_t trkClust_qual[MAXTRK][MAXTRKHITS];
  Int_t trkClust_pattern[MAXTRK][MAXTRKHITS];
  
  // ====================
  // Unpacked EMTF Tracks and LCTs
  // ====================
  Int_t numUnpTrks;
  std::vector<Int_t>* numUnpTrkLCTs;
  std::vector<float>* unp_trkPt;
  std::vector<float>* unp_trkEta;
  std::vector<float>* unp_trkPhi;
  std::vector<float>* unp_trkGeomPhi;
  std::vector<Int_t>* unp_trkMode;
  std::vector<Int_t>* unp_trkBx;
  std::vector<Int_t>* unp_trkBxBeg;
  std::vector<Int_t>* unp_trkBxEnd;

  // Track LCTs
  Int_t unp_trkLct_endcap[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_station[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_sector[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_ring[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_chamber[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_wire[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_strip[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_cscId[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_bx[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_qual[MAXTRK][MAXTRKHITS];
  Int_t unp_trkLct_pattern[MAXTRK][MAXTRKHITS];
  
  // ====================
  // Legacy CSC Tracks
  // ====================
  Int_t numLegTrks;

  std::vector<Int_t>* numLegTrkLCTs;
  std::vector<float>* leg_trkPt;
  std::vector<float>* leg_trkPtOld;
  std::vector<float>* leg_trkPtMatt;
  std::vector<float>* leg_trkPtGmt;
  std::vector<float>* leg_trkEta;
  std::vector<float>* leg_trkPhi;
  std::vector<Int_t>* leg_trkMode;
  std::vector<Int_t>* leg_trkModeA;
  std::vector<Int_t>* leg_trkModeB;
  std::vector<Int_t>* leg_trkQual;
  std::vector<Int_t>* leg_trkQualA;
  std::vector<Int_t>* leg_trkQualB;
  std::vector<Int_t>* leg_trkBx;
  std::vector<Int_t>* leg_trkBxBeg;
  std::vector<Int_t>* leg_trkBxEnd;

  // Track LCTs
  Int_t leg_trkLct_endcap[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_station[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_sector[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_ring[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_chamber[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_wire[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_strip[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_cscId[MAXTRK][MAXTRKHITS];
  float leg_trkLct_globPhi[MAXTRK][MAXTRKHITS];
  float leg_trkLct_eta[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_locPhi[MAXTRK][MAXTRKHITS];
  Int_t leg_trkLct_bx[MAXTRK][MAXTRKHITS];
  
  // ====================
  // Legacy CSCTF input-to-GMT Tracks
  // ====================
  Int_t numCsctfTrks;

  std::vector<float>* csctf_trkPt;
  std::vector<float>* csctf_trkEta;
  std::vector<float>* csctf_trkPhi;
  std::vector<Int_t>* csctf_trkQual;
  std::vector<Int_t>* csctf_trkCharge;
  std::vector<Int_t>* csctf_trkBx;

  // ====================
  // Legacy GMT Tracks
  // ====================

  // From any part of the detector
  Int_t numGtTrks;

  std::vector<float>* gt_trkEta;
  std::vector<float>* gt_trkPhi;
  std::vector<float>* gt_trkPt;
  std::vector<Int_t>* gt_trkQual;
  std::vector<Int_t>* gt_trkBx;
  std::vector<Int_t>* gt_trkDetector;

  // Only from endcaps
  Int_t numGmtTrks;

  std::vector<float>* gmt_trkPt;
  std::vector<float>* gmt_trkEta;
  std::vector<float>* gmt_trkPhi;
  std::vector<Int_t>* gmt_trkQual;
  std::vector<Int_t>* gmt_trkCharge;
  std::vector<Int_t>* gmt_trkBx;
  std::vector<Int_t>* gmt_trkDetector;

};

class DataEvtSummaryHandler {
public:
    //
  DataEvtSummaryHandler();
  ~DataEvtSummaryHandler();

    //current event
    DataEvtSummary_t evSummary_;
    
    
    DataEvtSummary_t &getEvent() {
        return evSummary_;
    }

    //write mode
    bool initTree(TTree *t);
    void fillTree();

    //read mode
    int getEntries() {
        return (t_ ? t_->GetEntriesFast() : 0);
    }
    void getEntry(int ientry) {
        resetStruct();
        if(t_) t_->GetEntry(ientry);
    }

    void initStruct();
    void resetStruct();
    


private:
    //the tree
    TTree *t_;
};

#endif
