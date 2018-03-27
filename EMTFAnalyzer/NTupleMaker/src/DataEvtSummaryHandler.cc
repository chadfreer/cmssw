#include "EMTFAnalyzer/NTupleMaker/interface/DataEvtSummaryHandler.h"

using namespace std;
 
//
DataEvtSummaryHandler::DataEvtSummaryHandler()
{

 

}

//
bool DataEvtSummaryHandler::initTree(TTree *t)
{
    if(t==0) return false;
    t_ = t;
    

    //event info
    t_->Branch("run",   &evSummary_.run,   "run/I");
    t_->Branch("lumi",  &evSummary_.lumi,  "lumi/I");
    t_->Branch("event", &evSummary_.event, "event/I");
    

    // ==================
    // Gen Muons
    // ==================
    t_->Branch("numGenMuons", &evSummary_.numGenMuons, "numGenMuons/I");
    
    t_->Branch("genEta",  &evSummary_.genEta);
    t_->Branch("genPhi",  &evSummary_.genPhi);
    t_->Branch("genId",   &evSummary_.genId);
    t_->Branch("genPt",   &evSummary_.genPt);

    
    // ==================
    // RECO Global Muons
    // ==================
    
    // ==================
    t_->Branch("numRecoMuons", &evSummary_.numRecoMuons, "numRecoMuons/I");

    t_->Branch("recoPt",   &evSummary_.recoPt);
    t_->Branch("recoEta",  &evSummary_.recoEta);
    t_->Branch("recoPhi",  &evSummary_.recoPhi);
    t_->Branch("recoCharge",   &evSummary_.recoCharge);
    t_->Branch("recoSamPt",   &evSummary_.recoSamPt);
    t_->Branch("recoIsTight",   &evSummary_.recoIsTight);
    t_->Branch("recoMatchedStations",   &evSummary_.recoMatchedStations);
    t_->Branch("recoChi2Norm",   &evSummary_.recoChi2Norm);

    // Muon CSC Segments
    t_->Branch("recoNumCscSegs", &evSummary_.recoNumCscSegs);
    t_->Branch("recoCscSeg_glob_x"      ,  evSummary_.recoCscSeg_glob_x      ,"recoCscSeg_glob_x[numRecoMuons][16]/F");
    t_->Branch("recoCscSeg_glob_y"      ,  evSummary_.recoCscSeg_glob_y      ,"recoCscSeg_glob_y[numRecoMuons][16]/F");
    t_->Branch("recoCscSeg_glob_eta"    ,  evSummary_.recoCscSeg_glob_eta    ,"recoCscSeg_glob_eta[numRecoMuons][16]/F");
    t_->Branch("recoCscSeg_glob_phi"    ,  evSummary_.recoCscSeg_glob_phi    ,"recoCscSeg_glob_phi[numRecoMuons][16]/F");
    t_->Branch("recoCscSeg_glob_dir_eta"    ,  evSummary_.recoCscSeg_glob_dir_eta    ,"recoCscSeg_glob_dir_eta[numRecoMuons][16]/F");
    t_->Branch("recoCscSeg_glob_dir_phi"    ,  evSummary_.recoCscSeg_glob_dir_phi    ,"recoCscSeg_glob_dir_phi[numRecoMuons][16]/F");
    
    t_->Branch("recoCscSeg_endcap" ,  evSummary_.recoCscSeg_endcap ,"recoCscSeg_endcap[numRecoMuons][16]/I");
    t_->Branch("recoCscSeg_station",  evSummary_.recoCscSeg_station,"recoCscSeg_station[numRecoMuons][16]/I");
    t_->Branch("recoCscSeg_ring"   ,  evSummary_.recoCscSeg_ring   ,"recoCscSeg_ring[numRecoMuons][16]/I");
    t_->Branch("recoCscSeg_chamber", evSummary_.recoCscSeg_chamber,"recoCscSeg_chamber[numRecoMuons][16]/I");
    t_->Branch("recoCscSeg_nHits"  , evSummary_.recoCscSeg_nHits  ,"recoCscSeg_nHits[numRecoMuons][16]/I");
    
    t_->Branch("recoCscSeg_isLctAble", evSummary_.recoCscSeg_isLctAble,"recoCscSeg_isLctAble[numRecoMuons][16]/I");
    t_->Branch("recoCscSeg_isMatched"   , evSummary_.recoCscSeg_isMatched,   "recoCscSeg_isMatched[numRecoMuons][16]/I");
    t_->Branch("recoCscSeg_lctId"       , evSummary_.recoCscSeg_lctId    ,   "recoCscSeg_lctId[numRecoMuons][16]/I");
    t_->Branch("recoCscSeg_sector"   , evSummary_.recoCscSeg_sector,    "recoCscSeg_sector[numRecoMuons][16]/I");
    
    // Muon RPC Clusters
    t_->Branch("recoNumRpcClusts", &evSummary_.recoNumRpcClusts);
    t_->Branch("recoRpcClust_glob_x"      ,  evSummary_.recoRpcClust_glob_x      ,"recoRpcClust_glob_x[numRecoMuons][16]/F");
    t_->Branch("recoRpcClust_glob_y"      ,  evSummary_.recoRpcClust_glob_y      ,"recoRpcClust_glob_y[numRecoMuons][16]/F");
    t_->Branch("recoRpcClust_glob_eta"    ,  evSummary_.recoRpcClust_glob_eta    ,"recoRpcClust_glob_eta[numRecoMuons][16]/F");
    t_->Branch("recoRpcClust_glob_phi"    ,  evSummary_.recoRpcClust_glob_phi    ,"recoRpcClust_glob_phi[numRecoMuons][16]/F");
    t_->Branch("recoRpcClust_glob_dir_eta"    ,  evSummary_.recoRpcClust_glob_dir_eta    ,"recoRpcClust_glob_dir_eta[numRecoMuons][16]/F");
    t_->Branch("recoRpcClust_glob_dir_phi"    ,  evSummary_.recoRpcClust_glob_dir_phi    ,"recoRpcClust_glob_dir_phi[numRecoMuons][16]/F");
    
    t_->Branch("recoRpcClust_endcap" ,  evSummary_.recoRpcClust_endcap ,"recoRpcClust_endcap[numRecoMuons][16]/I");
    t_->Branch("recoRpcClust_station",  evSummary_.recoRpcClust_station,"recoRpcClust_station[numRecoMuons][16]/I");
    t_->Branch("recoRpcClust_ring"   ,  evSummary_.recoRpcClust_ring   ,"recoRpcClust_ring[numRecoMuons][16]/I");
    t_->Branch("recoRpcClust_chamber", evSummary_.recoRpcClust_chamber,"recoRpcClust_chamber[numRecoMuons][16]/I");
    t_->Branch("recoRpcClust_nHits"  , evSummary_.recoRpcClust_nHits  ,"recoRpcClust_nHits[numRecoMuons][16]/I");
    
    t_->Branch("recoRpcClust_isLctAble", evSummary_.recoRpcClust_isLctAble,"recoRpcClust_isLctAble[numRecoMuons][16]/I");
    t_->Branch("recoRpcClust_isMatched"   , evSummary_.recoRpcClust_isMatched,   "recoRpcClust_isMatched[numRecoMuons][16]/I");
    t_->Branch("recoRpcClust_lctId"       , evSummary_.recoRpcClust_lctId    ,   "recoRpcClust_lctId[numRecoMuons][16]/I");
    t_->Branch("recoRpcClust_sector"   , evSummary_.recoRpcClust_sector,    "recoRpcClust_sector[numRecoMuons][16]/I");
    

    // ==================
    // CSC LCTS
    // ==================
    t_->Branch("numLCTs",         &evSummary_.numLCTs,    "numLCTs/I");
    t_->Branch("lctGlobalPhi",    &evSummary_.lctGlobalPhi);
    t_->Branch("lctEta",    &evSummary_.lctEta);
    t_->Branch("lctLocPhi",       &evSummary_.lctLocPhi);
    t_->Branch("lctEndcap",       &evSummary_.lctEndcap);
    t_->Branch("lctStation",      &evSummary_.lctStation);
    t_->Branch("lctSector",       &evSummary_.lctSector);
    t_->Branch("lctSubSector",    &evSummary_.lctSubSector);
    t_->Branch("lctRing",         &evSummary_.lctRing);
    t_->Branch("lctChamber",      &evSummary_.lctChamber);
    t_->Branch("lctTriggerCSCID", &evSummary_.lctTriggerCSCID);
    t_->Branch("lctBx",           &evSummary_.lctBx);
    t_->Branch("lctBc0",          &evSummary_.lctBc0);
    t_->Branch("lctWire",         &evSummary_.lctWire);
    t_->Branch("lctStrip",        &evSummary_.lctStrip);

    // ==================
    // RPC Clusters
    // ==================
    
    t_->Branch("numClusts",    &evSummary_.numClusts,    "numClusts/I");
    t_->Branch("clustEndcap",        &evSummary_.clustEndcap);
    t_->Branch("clustStation",        &evSummary_.clustStation);
    t_->Branch("clustSector",        &evSummary_.clustSector);
    t_->Branch("clustBx",        &evSummary_.clustBx);
    t_->Branch("clustSubSector",        &evSummary_.clustSubSector);
    t_->Branch("clustGlobalPhi",        &evSummary_.clustGlobalPhi);
    t_->Branch("clustEta",        &evSummary_.clustEta);
    t_->Branch("clustChamber",        &evSummary_.clustChamber);
    t_->Branch("clustWire",        &evSummary_.clustWire);
    t_->Branch("clustStrip",        &evSummary_.clustStrip);
    t_->Branch("clustRing",        &evSummary_.clustRing);
    t_->Branch("clustCscId",        &evSummary_.clustCscId);

    
    // ====================
    // Emulator EMTF Tracks and LCTs
    // ====================
    t_->Branch("numTrks", &evSummary_.numTrks,    "numTrks/I");
    t_->Branch("trkPt",  &evSummary_.trkPt);
    t_->Branch("trkEta", &evSummary_.trkEta);
    t_->Branch("trkPhi", &evSummary_.trkPhi);
    t_->Branch("trkMode",&evSummary_.trkMode);
    t_->Branch("trkBx",&evSummary_.trkBx);
    t_->Branch("trkBxBeg",&evSummary_.trkBxBeg);
    t_->Branch("trkBxEnd",&evSummary_.trkBxEnd);
    t_->Branch("trkRank",&evSummary_.trkRank);
    t_->Branch("trkStraight",&evSummary_.trkStraight);
    t_->Branch("numTrkLCTs", &evSummary_.numTrkLCTs);

    t_->Branch("trkLct_endcap",    &evSummary_.trkLct_endcap,    "trkLct_endcap[8][4]/I");
    t_->Branch("trkLct_chamber",    &evSummary_.trkLct_chamber,    "trkLct_chamber[8][4]/I");
    t_->Branch("trkLct_station",    &evSummary_.trkLct_station,    "trkLct_station[8][4]/I");
    t_->Branch("trkLct_sector",    &evSummary_.trkLct_sector,    "trkLct_sector[8][4]/I");
    t_->Branch("trkLct_ring",    &evSummary_.trkLct_ring,    "trkLct_ring[8][4]/I");
    t_->Branch("trkLct_wire",    &evSummary_.trkLct_wire,    "trkLct_wire[8][4]/I");
    t_->Branch("trkLct_strip",    &evSummary_.trkLct_strip,    "trkLct_strip[8][4]/I");
    t_->Branch("trkLct_cscId",    &evSummary_.trkLct_cscId,    "trkLct_cscId[8][4]/I");
    t_->Branch("trkLct_globPhi",    &evSummary_.trkLct_globPhi,    "trkLct_globPhi[8][4]/F");
    t_->Branch("trkLct_geomPhi",    &evSummary_.trkLct_geomPhi,    "trkLct_geomPhi[8][4]/F");
    t_->Branch("trkLct_eta",    &evSummary_.trkLct_eta,    "trkLct_eta[8][4]/F");
    t_->Branch("trkLct_locPhi",    &evSummary_.trkLct_locPhi,    "trkLct_locPhi[8][4]/I");
    t_->Branch("trkLct_locTheta",    &evSummary_.trkLct_locTheta,    "trkLct_locTheta[8][4]/I");
    t_->Branch("trkLct_bx",    &evSummary_.trkLct_bx,    "trkLct_bx[8][4]/I");
    t_->Branch("trkLct_qual",    &evSummary_.trkLct_qual,    "trkLct_qual[8][4]/I");
    t_->Branch("trkLct_pattern",    &evSummary_.trkLct_pattern,    "trkLct_pattern[8][4]/I");


    
    // ====================
    // Unpacked EMTF Tracks and LCTs
    // ====================
    t_->Branch("numUnpTrks", &evSummary_.numUnpTrks,    "numUnpTrks/I");
    t_->Branch("unp_trkPt",  &evSummary_.unp_trkPt);
    t_->Branch("unp_trkEta", &evSummary_.unp_trkEta);
    t_->Branch("unp_trkPhi", &evSummary_.unp_trkPhi);
    t_->Branch("unp_trkMode",&evSummary_.unp_trkMode);
    t_->Branch("unp_trkBx",&evSummary_.unp_trkBx);
    t_->Branch("unp_trkBxBeg",&evSummary_.unp_trkBxBeg);
    t_->Branch("unp_trkBxEnd",&evSummary_.unp_trkBxEnd);
    t_->Branch("numUnpTrkLCTs", &evSummary_.numUnpTrkLCTs);

    t_->Branch("unp_trkLct_endcap",    &evSummary_.unp_trkLct_endcap,    "unp_trkLct_endcap[8][4]/I");
    t_->Branch("unp_trkLct_chamber",    &evSummary_.unp_trkLct_chamber,    "unp_trkLct_chamber[8][4]/I");
    t_->Branch("unp_trkLct_station",    &evSummary_.unp_trkLct_station,    "unp_trkLct_station[8][4]/I");
    t_->Branch("unp_trkLct_sector",    &evSummary_.unp_trkLct_sector,    "unp_trkLct_sector[8][4]/I");
    t_->Branch("unp_trkLct_ring",    &evSummary_.unp_trkLct_ring,    "unp_trkLct_ring[8][4]/I");
    t_->Branch("unp_trkLct_wire",    &evSummary_.unp_trkLct_wire,    "unp_trkLct_wire[8][4]/I");
    t_->Branch("unp_trkLct_strip",    &evSummary_.unp_trkLct_strip,    "unp_trkLct_strip[8][4]/I");
    t_->Branch("unp_trkLct_cscId",    &evSummary_.unp_trkLct_cscId,    "unp_trkLct_cscId[8][4]/I");
    t_->Branch("unp_trkLct_bx",    &evSummary_.unp_trkLct_bx,    "unp_trkLct_bx[8][4]/I");
    t_->Branch("unp_trkLct_qual",    &evSummary_.unp_trkLct_qual,    "unp_trkLct_qual[8][4]/I");
    t_->Branch("unp_trkLct_pattern",    &evSummary_.unp_trkLct_pattern,    "unp_trkLct_pattern[8][4]/I");

    // ====================
    // Legacy Tracks
    // ====================
    t_->Branch("numLegTrks",    &evSummary_.numLegTrks,    "numLegTrks/I");
    t_->Branch("leg_trkPt",  &evSummary_.leg_trkPt);
    t_->Branch("leg_trkPtOld",  &evSummary_.leg_trkPtOld);
    t_->Branch("leg_trkPtMatt",  &evSummary_.leg_trkPtMatt);
    t_->Branch("leg_trkPtGmt",  &evSummary_.leg_trkPtGmt);
    t_->Branch("leg_trkEta", &evSummary_.leg_trkEta);
    t_->Branch("leg_trkPhi", &evSummary_.leg_trkPhi);
    t_->Branch("leg_trkMode",&evSummary_.leg_trkMode);
    t_->Branch("leg_trkModeA",&evSummary_.leg_trkModeA);
    t_->Branch("leg_trkModeB",&evSummary_.leg_trkModeB);
    t_->Branch("leg_trkQual",&evSummary_.leg_trkQual);
    t_->Branch("leg_trkQualA",&evSummary_.leg_trkQualA);
    t_->Branch("leg_trkQualB",&evSummary_.leg_trkQualB);
    t_->Branch("leg_trkBx",&evSummary_.leg_trkBx);
    t_->Branch("leg_trkBxBeg",&evSummary_.leg_trkBxBeg);
    t_->Branch("leg_trkBxEnd",&evSummary_.leg_trkBxEnd);

    t_->Branch("numLegTrkLCTs", &evSummary_.numLegTrkLCTs);
    t_->Branch("leg_trkLct_endcap",    &evSummary_.leg_trkLct_endcap,    "leg_trkLct_endcap[8][4]/I");
    t_->Branch("leg_trkLct_chamber",    &evSummary_.leg_trkLct_chamber,    "leg_trkLct_chamber[8][4]/I");
    t_->Branch("leg_trkLct_station",    &evSummary_.leg_trkLct_station,    "leg_trkLct_station[8][4]/I");
    t_->Branch("leg_trkLct_sector",    &evSummary_.leg_trkLct_sector,    "leg_trkLct_sector[8][4]/I");
    t_->Branch("leg_trkLct_ring",    &evSummary_.leg_trkLct_ring,    "leg_trkLct_ring[8][4]/I");
    t_->Branch("leg_trkLct_wire",    &evSummary_.leg_trkLct_wire,    "leg_trkLct_wire[8][4]/I");
    t_->Branch("leg_trkLct_strip",    &evSummary_.leg_trkLct_strip,    "leg_trkLct_strip[8][4]/I");
    t_->Branch("leg_trkLct_cscId",    &evSummary_.leg_trkLct_cscId,    "leg_trkLct_cscId[8][4]/I");
    t_->Branch("leg_trkLct_globPhi",    &evSummary_.leg_trkLct_globPhi,    "leg_trkLct_globPhi[8][4]/F");
    t_->Branch("leg_trkLct_eta",    &evSummary_.leg_trkLct_eta,    "leg_trkLct_eta[8][4]/F");
    t_->Branch("leg_trkLct_locPhi",    &evSummary_.leg_trkLct_locPhi,    "leg_trkLct_locPhi[8][4]/I");
    t_->Branch("leg_trkLct_bx",    &evSummary_.leg_trkLct_bx,    "leg_trkLct_bx[8][4]/I");
    
    // ================================
    // Legacy CSCTF input-to-GMT Tracks
    // ================================
    t_->Branch("numCsctfTrks",    &evSummary_.numCsctfTrks,    "numCsctfTrks/I");
    t_->Branch("csctf_trkPt",  &evSummary_.csctf_trkPt);
    t_->Branch("csctf_trkEta", &evSummary_.csctf_trkEta);
    t_->Branch("csctf_trkPhi", &evSummary_.csctf_trkPhi);
    t_->Branch("csctf_trkCharge",&evSummary_.csctf_trkCharge);
    t_->Branch("csctf_trkQual",&evSummary_.csctf_trkQual);
    t_->Branch("csctf_trkBx",&evSummary_.csctf_trkBx);

    // ====================
    // Legacy GMT Tracks
    // ====================
    
    // From any part of the detector
    t_->Branch("numGtTrks",    &evSummary_.numGtTrks,    "numGtTrks/I");
    t_->Branch("gt_trkEta",  &evSummary_.gt_trkEta);
    t_->Branch("gt_trkPhi",  &evSummary_.gt_trkPhi);
    t_->Branch("gt_trkPt",  &evSummary_.gt_trkPt);
    t_->Branch("gt_trkQual",&evSummary_.gt_trkQual);
    t_->Branch("gt_trkBx",&evSummary_.gt_trkBx);
    t_->Branch("gt_trkDetector",&evSummary_.gt_trkDetector);

    // Only from endcaps
    t_->Branch("numGmtTrks",    &evSummary_.numGmtTrks,    "numGmtTrks/I");
    t_->Branch("gmt_trkPt",  &evSummary_.gmt_trkPt);
    t_->Branch("gmt_trkEta", &evSummary_.gmt_trkEta);
    t_->Branch("gmt_trkPhi", &evSummary_.gmt_trkPhi);
    t_->Branch("gmt_trkCharge",&evSummary_.gmt_trkCharge);
    t_->Branch("gmt_trkQual",&evSummary_.gmt_trkQual);
    t_->Branch("gmt_trkBx",&evSummary_.gmt_trkBx);
    t_->Branch("gmt_trkDetector",&evSummary_.gmt_trkDetector);


    return true;
}



void DataEvtSummaryHandler::initStruct() {

  
  evSummary_.run   = 0;
  evSummary_.lumi  = 0;
  evSummary_.event = 0;


  
  // ==================
  // Gen Muons
  // ==================
  evSummary_.numGenMuons = 0;
  evSummary_.genEta = new vector<float>;
  evSummary_.genPhi = new vector<float>;
  evSummary_.genPt  = new vector<float>;
  evSummary_.genId  = new vector<int>;

  
  // ==================
  // RECO Muons
  // ==================
  evSummary_.numRecoMuons = 0;
  evSummary_.recoPt  = new vector<float>;
  evSummary_.recoEta = new vector<float>;
  evSummary_.recoPhi = new vector<float>;
  evSummary_.recoCharge  = new vector<int>;
  evSummary_.recoSamPt  = new vector<float>;
  evSummary_.recoIsTight  = new vector<int>;
  evSummary_.recoMatchedStations  = new vector<int>;
  evSummary_.recoChi2Norm  = new vector<float>;
  
  // Segments
  evSummary_.recoNumCscSegs = new std::vector<int>;
  evSummary_.recoNumRpcClusts = new std::vector<int>;

  for (int row=0; row < MAX_MUONS; row++) {

    for (int col=0; col < MAX_SEGS_STD; col++) {
      evSummary_.recoCscSeg_glob_x[row][col] = -999;
      evSummary_.recoCscSeg_glob_y[row][col] = -999;
      evSummary_.recoCscSeg_glob_eta[row][col] = -999;
      evSummary_.recoCscSeg_glob_phi[row][col] = -999;
      evSummary_.recoCscSeg_glob_dir_eta[row][col] = -999;
      evSummary_.recoCscSeg_glob_dir_phi[row][col] = -999;
      
      evSummary_.recoCscSeg_endcap[row][col] = -999;
      evSummary_.recoCscSeg_station[row][col] = -999;
      evSummary_.recoCscSeg_ring[row][col] = -999;
      evSummary_.recoCscSeg_chamber[row][col] = -999;
      evSummary_.recoCscSeg_nHits[row][col] = -999;
      evSummary_.recoCscSeg_sector[row][col] = -999;

      evSummary_.recoCscSeg_isLctAble[row][col] = -999;
      evSummary_.recoCscSeg_isMatched[row][col] = -999;
      evSummary_.recoCscSeg_lctId[row][col] = -999;
      //evSummary_.recoCscSeg_nmatched[row][col] = -999;
    }

    for (int col=0; col < MAX_SEGS_STD; col++) {
      evSummary_.recoRpcClust_glob_x[row][col] = -999;
      evSummary_.recoRpcClust_glob_y[row][col] = -999;
      evSummary_.recoRpcClust_glob_eta[row][col] = -999;
      evSummary_.recoRpcClust_glob_phi[row][col] = -999;
      evSummary_.recoRpcClust_glob_dir_eta[row][col] = -999;
      evSummary_.recoRpcClust_glob_dir_phi[row][col] = -999;
      
      evSummary_.recoRpcClust_endcap[row][col] = -999;
      evSummary_.recoRpcClust_station[row][col] = -999;
      evSummary_.recoRpcClust_ring[row][col] = -999;
      evSummary_.recoRpcClust_chamber[row][col] = -999;
      evSummary_.recoRpcClust_nHits[row][col] = -999;
      evSummary_.recoRpcClust_sector[row][col] = -999;

      evSummary_.recoRpcClust_isLctAble[row][col] = -999;
      evSummary_.recoRpcClust_isMatched[row][col] = -999;
      evSummary_.recoRpcClust_lctId[row][col] = -999;
      //evSummary_.recoRpcClust_nmatched[row][col] = -999;
    }

  }


  
  // ==================
  // CSC LCTS
  // ==================
  evSummary_.numLCTs = 0;
  evSummary_.lctGlobalPhi    = new vector<float>;
  evSummary_.lctEta    = new vector<float>;
  evSummary_.lctLocPhi       = new vector<int>;
  evSummary_.lctEndcap       = new vector<int>;
  evSummary_.lctSector       = new vector<int>;
  evSummary_.lctSubSector    = new vector<int>;
  evSummary_.lctBx           = new vector<int>;
  evSummary_.lctBc0          = new vector<int>;
  evSummary_.lctStation      = new vector<int>;
  evSummary_.lctRing         = new vector<int>;
  evSummary_.lctChamber      = new vector<int>;
  evSummary_.lctTriggerCSCID = new vector<int>;
  evSummary_.lctStrip        = new vector<int>;
  evSummary_.lctWire         = new vector<int>;
  evSummary_.lctRing         = new vector<int>;


  
  // ====================
  // EMTF Emulator Tracks and LCTs
  // ====================

  evSummary_.numTrks    = 0;

  evSummary_.trkPt   = new vector<float>;
  evSummary_.trkEta  = new vector<float>;
  evSummary_.trkPhi  = new vector<float>;
  evSummary_.trkMode = new vector<Int_t>;
  evSummary_.trkBx = new vector<Int_t>;
  evSummary_.trkBxBeg = new vector<Int_t>;
  evSummary_.trkBxEnd = new vector<Int_t>;
  evSummary_.trkRank = new vector<Int_t>;
  evSummary_.trkStraight = new vector<Int_t>;
  evSummary_.numTrkLCTs = new vector<Int_t>;

  // ====================
  // Unpacked Emulator Tracks and LCTs
  // ====================

  evSummary_.numUnpTrks    = 0;

  evSummary_.unp_trkPt   = new vector<float>;
  evSummary_.unp_trkEta  = new vector<float>;
  evSummary_.unp_trkPhi  = new vector<float>;
  evSummary_.unp_trkMode = new vector<Int_t>;
  evSummary_.unp_trkBx = new vector<Int_t>;
  evSummary_.unp_trkBxBeg = new vector<Int_t>;
  evSummary_.unp_trkBxEnd = new vector<Int_t>;
  evSummary_.numUnpTrkLCTs = new vector<Int_t>;

  // RPC Clusters
  evSummary_.numClusts = 0;
  evSummary_.clustGlobalPhi = new vector<float>;
  evSummary_.clustEta = new vector<float>;
  evSummary_.clustStation   = new vector<int>;
  evSummary_.clustSector    = new vector<int>;
  evSummary_.clustBx    = new vector<int>;
  evSummary_.clustSubSector = new vector<int>;
  evSummary_.clustEndcap    = new vector<int>;
  evSummary_.clustChamber    = new vector<int>;
  evSummary_.clustWire    = new vector<int>;
  evSummary_.clustStrip    = new vector<int>;
  evSummary_.clustRing    = new vector<int>;
  evSummary_.clustCscId    = new vector<int>;

  // Track LCTs
  for (int i=0; i < MAXTRK; i++) {
    for (int j=0; j < MAXTRKHITS; j++) {
    
      evSummary_.trkLct_endcap[i][j]  = -999;
      evSummary_.trkLct_station[i][j] = -999;
      evSummary_.trkLct_sector[i][j]  = -999;
      evSummary_.trkLct_ring[i][j]    = -999;
      evSummary_.trkLct_chamber[i][j] = -999;
      evSummary_.trkLct_wire[i][j]    = -999;
      evSummary_.trkLct_strip[i][j]   = -999;
      evSummary_.trkLct_cscId[i][j]   = -999;
      evSummary_.trkLct_globPhi[i][j]  = -999;
      evSummary_.trkLct_geomPhi[i][j]  = -999;
      evSummary_.trkLct_eta[i][j]  = -999;
      evSummary_.trkLct_locPhi[i][j]  = -999;
      evSummary_.trkLct_locTheta[i][j]  = -999;
      evSummary_.trkLct_bx[i][j]  = -999;
      evSummary_.trkLct_qual[i][j]  = -999;
      evSummary_.trkLct_pattern[i][j]  = -999;

      
      evSummary_.unp_trkLct_endcap[i][j]  = -999;
      evSummary_.unp_trkLct_station[i][j] = -999;
      evSummary_.unp_trkLct_sector[i][j]  = -999;
      evSummary_.unp_trkLct_ring[i][j]    = -999;
      evSummary_.unp_trkLct_chamber[i][j] = -999;
      evSummary_.unp_trkLct_wire[i][j]    = -999;
      evSummary_.unp_trkLct_strip[i][j]   = -999;
      evSummary_.unp_trkLct_cscId[i][j]   = -999;
      evSummary_.unp_trkLct_bx[i][j]  = -999;
      evSummary_.unp_trkLct_qual[i][j]  = -999;
      evSummary_.unp_trkLct_pattern[i][j]  = -999;

    
      
      evSummary_.leg_trkLct_endcap[i][j]  = -999;
      evSummary_.leg_trkLct_station[i][j] = -999;
      evSummary_.leg_trkLct_sector[i][j]  = -999;
      evSummary_.leg_trkLct_ring[i][j]    = -999;
      evSummary_.leg_trkLct_chamber[i][j] = -999;
      evSummary_.leg_trkLct_wire[i][j]    = -999;
      evSummary_.leg_trkLct_strip[i][j]   = -999;
      evSummary_.leg_trkLct_cscId[i][j]   = -999;
      evSummary_.leg_trkLct_globPhi[i][j]  = -999;
      evSummary_.leg_trkLct_eta[i][j]  = -999;
      evSummary_.leg_trkLct_locPhi[i][j]  = -999;
      evSummary_.leg_trkLct_bx[i][j]  = -999;
      


    }
  }
  
  
  // ====================
  // Legacy CSC Tracks
  // ====================
  evSummary_.numLegTrks = 0;

  evSummary_.leg_trkPt   = new vector<float>;
  evSummary_.leg_trkPtOld   = new vector<float>;
  evSummary_.leg_trkPtMatt   = new vector<float>;
  evSummary_.leg_trkPtGmt   = new vector<float>;
  evSummary_.leg_trkEta  = new vector<float>;
  evSummary_.leg_trkPhi  = new vector<float>;
  evSummary_.leg_trkMode = new vector<Int_t>;
  evSummary_.leg_trkModeA = new vector<Int_t>;
  evSummary_.leg_trkModeB = new vector<Int_t>;
  evSummary_.leg_trkQual = new vector<Int_t>;
  evSummary_.leg_trkQualA = new vector<Int_t>;
  evSummary_.leg_trkQualB = new vector<Int_t>;
  evSummary_.leg_trkBx = new vector<Int_t>;
  evSummary_.leg_trkBxBeg = new vector<Int_t>;
  evSummary_.leg_trkBxEnd = new vector<Int_t>;
  evSummary_.numLegTrkLCTs = new vector<Int_t>;


  
  // ====================
  // Legacy CSCTF input-to-GMT Tracks
  // ====================
  evSummary_.numCsctfTrks = 0;

  evSummary_.csctf_trkPt   = new vector<float>;
  evSummary_.csctf_trkEta  = new vector<float>;
  evSummary_.csctf_trkPhi  = new vector<float>;
  evSummary_.csctf_trkCharge = new vector<Int_t>;
  evSummary_.csctf_trkQual = new vector<Int_t>;
  evSummary_.csctf_trkBx = new vector<Int_t>;

  // ====================
  // Legacy GMT Tracks
  // ====================
  evSummary_.numGtTrks = 0;
  evSummary_.gt_trkEta   = new vector<float>;
  evSummary_.gt_trkPhi   = new vector<float>;
  evSummary_.gt_trkPt   = new vector<float>;
  evSummary_.gt_trkQual = new vector<Int_t>;
  evSummary_.gt_trkBx = new vector<Int_t>;
  evSummary_.gt_trkDetector = new vector<Int_t>;

  evSummary_.numGmtTrks = 0;
  evSummary_.gmt_trkPt   = new vector<float>;
  evSummary_.gmt_trkEta  = new vector<float>;
  evSummary_.gmt_trkPhi  = new vector<float>;
  evSummary_.gmt_trkCharge = new vector<Int_t>;
  evSummary_.gmt_trkQual = new vector<Int_t>;
  evSummary_.gmt_trkBx = new vector<Int_t>;
  evSummary_.gmt_trkDetector = new vector<Int_t>;

}


//
void DataEvtSummaryHandler::resetStruct() {


  // ==================
  // Gen Muons
  // ==================
  vector<float>().swap(*evSummary_.genEta);
  vector<float>().swap(*evSummary_.genPhi);
  vector<float>().swap(*evSummary_.genPt);
  vector<int>().swap(*evSummary_.genId);


  // ==================
  // RECO Muons
  // ==================
  vector<float>().swap(*evSummary_.recoPt);
  vector<float>().swap(*evSummary_.recoEta);
  vector<float>().swap(*evSummary_.recoPhi);
  vector<int>().swap(*evSummary_.recoCharge);
  vector<float>().swap(*evSummary_.recoSamPt);
  vector<int>().swap(*evSummary_.recoIsTight);
  vector<int>().swap(*evSummary_.recoMatchedStations);
  vector<float>().swap(*evSummary_.recoChi2Norm);
  vector<int>().swap(*evSummary_.recoNumCscSegs);
  vector<int>().swap(*evSummary_.recoNumRpcClusts);
  

  // ==================
  // CSC LCTS
  // ==================
  vector<float>().swap(*evSummary_.lctGlobalPhi);
  vector<float>().swap(*evSummary_.lctEta);
  vector<int>().swap(*evSummary_.lctLocPhi);
  vector<int>().swap(*evSummary_.lctEndcap);
  vector<int>().swap(*evSummary_.lctSector);
  vector<int>().swap(*evSummary_.lctSubSector);
  vector<int>().swap(*evSummary_.lctBx);
  vector<int>().swap(*evSummary_.lctBc0);
  vector<int>().swap(*evSummary_.lctStation);
  vector<int>().swap(*evSummary_.lctRing);
  vector<int>().swap(*evSummary_.lctChamber);
  vector<int>().swap(*evSummary_.lctTriggerCSCID);
  vector<int>().swap(*evSummary_.lctStrip);
  vector<int>().swap(*evSummary_.lctWire);
  
  
  // ====================
  // CSC Tracks and LCTs
  // ====================
  vector<float>().swap(*evSummary_.trkPt);
  vector<float>().swap(*evSummary_.trkEta);
  vector<float>().swap(*evSummary_.trkPhi);
  vector<Int_t>().swap(*evSummary_.trkMode);
  vector<Int_t>().swap(*evSummary_.trkBx);
  vector<Int_t>().swap(*evSummary_.trkBxBeg);
  vector<Int_t>().swap(*evSummary_.trkBxEnd);
  vector<Int_t>().swap(*evSummary_.trkRank);
  vector<Int_t>().swap(*evSummary_.trkStraight);
  vector<Int_t>().swap(*evSummary_.numTrkLCTs);

  // RPC CLusters
  vector<float>().swap(*evSummary_.clustGlobalPhi);
  vector<float>().swap(*evSummary_.clustEta);
  vector<int>().swap(*evSummary_.clustStation);
  vector<int>().swap(*evSummary_.clustSector);
  vector<int>().swap(*evSummary_.clustBx);
  vector<int>().swap(*evSummary_.clustSubSector);
  vector<int>().swap(*evSummary_.clustEndcap);
  vector<int>().swap(*evSummary_.clustChamber);
  vector<int>().swap(*evSummary_.clustWire);
  vector<int>().swap(*evSummary_.clustStrip);
  vector<int>().swap(*evSummary_.clustRing);
  vector<int>().swap(*evSummary_.clustCscId);
  
  // ====================
  // Legacy CSC Tracks
  // ====================
  
  vector<Int_t>().swap(*evSummary_.numLegTrkLCTs);
  vector<float>().swap(*evSummary_.leg_trkPt);
  vector<float>().swap(*evSummary_.leg_trkPtOld);
  vector<float>().swap(*evSummary_.leg_trkPtMatt);
  vector<float>().swap(*evSummary_.leg_trkPtGmt);
  vector<float>().swap(*evSummary_.leg_trkEta);
  vector<float>().swap(*evSummary_.leg_trkPhi);
  vector<Int_t>().swap(*evSummary_.leg_trkMode);
  vector<Int_t>().swap(*evSummary_.leg_trkModeA);
  vector<Int_t>().swap(*evSummary_.leg_trkModeB);
  vector<Int_t>().swap(*evSummary_.leg_trkQual);
  vector<Int_t>().swap(*evSummary_.leg_trkQualA);
  vector<Int_t>().swap(*evSummary_.leg_trkQualB);
  vector<Int_t>().swap(*evSummary_.leg_trkBx);
  vector<Int_t>().swap(*evSummary_.leg_trkBxBeg);
  vector<Int_t>().swap(*evSummary_.leg_trkBxEnd);

  // ====================
  // Legacy CSCTF input-to-GMT Tracks
  // ====================
  
  vector<float>().swap(*evSummary_.csctf_trkPt);
  vector<float>().swap(*evSummary_.csctf_trkEta);
  vector<float>().swap(*evSummary_.csctf_trkPhi);
  vector<Int_t>().swap(*evSummary_.csctf_trkCharge);
  vector<Int_t>().swap(*evSummary_.csctf_trkQual);
  vector<Int_t>().swap(*evSummary_.csctf_trkBx);

  // ====================
  // Legacy GMT Tracks
  // ====================
  
  vector<float>().swap(*evSummary_.gt_trkEta);
  vector<float>().swap(*evSummary_.gt_trkPhi);
  vector<float>().swap(*evSummary_.gt_trkPt);
  vector<Int_t>().swap(*evSummary_.gt_trkQual);
  vector<Int_t>().swap(*evSummary_.gt_trkBx);
  vector<Int_t>().swap(*evSummary_.gt_trkDetector);

  vector<float>().swap(*evSummary_.gmt_trkPt);
  vector<float>().swap(*evSummary_.gmt_trkEta);
  vector<float>().swap(*evSummary_.gmt_trkPhi);
  vector<Int_t>().swap(*evSummary_.gmt_trkCharge);
  vector<Int_t>().swap(*evSummary_.gmt_trkQual);
  vector<Int_t>().swap(*evSummary_.gmt_trkBx);
  vector<Int_t>().swap(*evSummary_.gmt_trkDetector);

}

//
void DataEvtSummaryHandler::fillTree()
{
    if(t_) t_->Fill();
}

//
DataEvtSummaryHandler::~DataEvtSummaryHandler()
{
}
