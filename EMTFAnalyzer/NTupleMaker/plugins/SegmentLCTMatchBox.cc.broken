#include "SegmentLCTMatchBox.h"

#include <TH1F.h>
#include <TH2F.h>
#include <TFile.h>
#include <TMath.h>
#include <TString.h>

#include "DataFormats/MuonDetId/interface/CSCDetId.h"
#include "L1Trigger/L1TMuonEndCap/interface/PhiMemoryImage.h"
#include "L1Trigger/L1TMuonEndCap/interface/EmulatorClasses.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCTFPtLUT.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCSectorReceiverLUT.h"
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "L1Trigger/L1TMuon/interface/MuonTriggerPrimitive.h"



using namespace std;

const int SegmentLCTMatchBox::_alctEnvelopes[] = { 2, 1, 0, 1, 2, 2 };
const int SegmentLCTMatchBox::_clctEnvelopes[] = { 5, 2, 0, 2, 4, 5 };


SegmentLCTMatchBox::SegmentLCTMatchBox( int nHitsSegment, int nHitsALCT, int nHitsCLCT, int printLevel, bool monitorHist ):
  _printLevel    ( printLevel   ),
  _outFile       ( 0 ),
//  _delStrip      ( 0 ),
//  _delWireg      ( 0 ),
//  _closestWireg  ( 0 ),
//  _closestStrip  ( 0 ),
//  _posWithinStrip( 0 ),
//  _alctPattern   ( 0 ),
//  _clctPattern   ( 0 ),
//  _numLCTSChamber( 0 ),
  _nHitsSegment  ( nHitsSegment ), 
  _nHitsALCT     ( nHitsALCT    ),
  _nHitsCLCT     ( nHitsCLCT    ),
  _monitorHist   ( monitorHist  )
{

  if ( _monitorHist ){

    _outFile = new TFile("SegmentLCTMatchBox.root","RECREATE");

    _outFile -> cd();

    TString tempString;

    for (int i = 0; i < 5; i++){

      tempString = TString::Format("delWireg%d", i);
      _delWireg[i] = new TH1F(tempString.Data(),"",300,-149,150);

      tempString = TString::Format("delStrip%d", i);
      _delStrip[i] = new TH1F(tempString.Data(),"",321,-159.5,159.5);

      tempString = TString::Format("closestWireg%d", i);
      _closestWireg[i] = new TH1F(tempString.Data(), "", 300, -149, 150);

      tempString = TString::Format("closestStrip%d", i);
      _closestStrip[i] = new TH1F(tempString.Data(), "", 321, -159.5, 159.5);

      tempString = TString::Format("alctPattern%d", i);
      _alctPattern [i] = new TH2F(tempString.Data(),  "", 9, -4.5, 4.5, 8,-0.5,7.5);

      tempString = TString::Format("clctPattern%d", i);
      _clctPattern [i] = new TH2F(tempString.Data(),  "", 13,-6.5, 6.5, 8,-0.5,7.5);
    
      tempString = TString::Format("numLCTSChamber%d", i);
      _numLCTSChamber [i] = new TH1F(tempString.Data(), "", 10, 0, 10);

    }
    
  }

}

SegmentLCTMatchBox::~SegmentLCTMatchBox(){

  if ( _monitorHist ){

    _outFile -> cd();

    for (int i = 0; i < 5; i++){

      _delWireg       [i]  -> Write();
      _delStrip       [i]  -> Write();
      _closestWireg   [i]  -> Write();
      _closestStrip   [i]  -> Write();
      _alctPattern    [i]  -> Write();
      _clctPattern    [i]  -> Write();
      _numLCTSChamber [i]  -> Write();
      
    }

    _outFile -> Close();

    delete _outFile;

    for (int i = 0; i < 5; i++){
      delete _delWireg       [i] ;
      delete _delStrip       [i] ;
      delete _closestWireg   [i] ;
      delete _closestStrip   [i] ; 
      delete _alctPattern    [i] ;
      delete _clctPattern    [i] ;
      delete _numLCTSChamber [i] ;
    
    }

  }
}

int SegmentLCTMatchBox::me11aNormalize ( int halfStrip ){

  int retVal = (halfStrip-1)%32+1;
  
  return retVal;
  
}

int SegmentLCTMatchBox::halfStrip( const CSCRecHit2D &hit ){

  int retVal;

  //if (hit.channels().size() == 3)
  if (hit.nStrips() == 3)

    //retVal =  2.0* (hit.channels()[1] + hit.positionWithinStrip() - 0.5 );
    retVal =  2.0* (hit.channels(1) + hit.positionWithinStrip() - 0.5 );
  
  else

    //retVal =  2.0 * (hit.channels()[0] - hit.positionWithinStrip() - 0.5 );
    retVal =  2.0 * (hit.channels(0) - hit.positionWithinStrip() - 0.5 );

  bool evenLayer =  hit.cscDetId().layer() % 2 == 0;

  if ( evenLayer )
    retVal -= 1;

  if ( (hit.cscDetId().station() == 1) && (hit.cscDetId().layer() != 3) && evenLayer )
    retVal += 1;

  return retVal;
  
}

int SegmentLCTMatchBox::wireGroup ( const CSCRecHit2D &hit ){

  //return ( hit.wgroups()[0] -1 );
  //return ( hit.nWireGroups() -1 );
  return ( hit.hitWire() -1 );
}

// bool SegmentLCTMatchBox::isMatched ( const CSCSegment &segment, const edm::Handle<CSCCorrelatedLCTDigiCollection> CSCTFlcts, int *match_report ){
// bool SegmentLCTMatchBox::isMatched ( const CSCSegment &segment, CSCCorrelatedLCTDigiCollection CSCTFlcts, int *match_report ){
std::vector<int> SegmentLCTMatchBox::lctsMatch ( const CSCSegment &segment, const edm::Handle<std::vector<l1t::EMTFHit>> LCTs, int *match_report ){

  int lct_arr[] = {-999, -999, -999, -999, -999, -999, -999, -999};

  if (_printLevel > 2)
    std::cout << "\n*** SegmentLCTMatchBox::isMatched *** " << std::endl;
  
  if (match_report)
    (*match_report) = 0;

  int LCT_key_strip = -999;
  int LCT_key_wireg = -999;

  const int noMatchVal = 9999;

  int keyStripEstim = noMatchVal;
  int keyWiregEstim = noMatchVal;

  CSCDetId *tempDetId = 0;
  const CSCDetId &origId = segment.cscDetId();

  // index for histogram filling ... 0 for ME11a, station() for the rest..

  int histoFillIndex;
  
  if (segment.cscDetId().ring() == 4)
    histoFillIndex = 0;
  else
    histoFillIndex = segment.cscDetId().station();
    
  // if we're in ME11a, we have to worry about triple-ganging of strips.

  bool me11aStation = false;

  if (segment.cscDetId().ring() == 4){
    
    me11aStation = true;
    
    tempDetId = new CSCDetId ( origId.endcap(), origId.station(), 1,origId.chamber());

  } else {

    tempDetId = new CSCDetId ( origId );

  }

  double stripSum = 0, wiregSum = 0, numHits = 0;

  // first, find the estimator for the key strip and wire group from recHits

  const std::vector<CSCRecHit2D>& theHits = segment.specificRecHits();
  std::vector<CSCRecHit2D>::const_iterator hitIter;

  bool hadKeyInfo = false;
  
  for (hitIter = theHits.begin(); hitIter!= theHits.end(); hitIter++){

    if ( hitIter -> cscDetId() . layer() == 3){

      hadKeyInfo = true;

      keyStripEstim = halfStrip ( *hitIter );
      keyWiregEstim = wireGroup ( *hitIter );

    }
    
    stripSum += halfStrip ( *hitIter );
    wiregSum += wireGroup ( *hitIter );
    numHits  += 1.0;
  }

  if (!hadKeyInfo){ // no key info .. have to improvise with averages..
    
    if (_printLevel > 2)
      std::cout << "MATCHING: NO KEY INFO!!!" << std::endl;

    keyStripEstim = stripSum / numHits;
    keyWiregEstim = wiregSum / numHits;

  }

  if (me11aStation){
    if (_printLevel > 2)
      std::cout << "ME1/1a: apply extra care!!!" << std::endl;
    keyStripEstim = me11aNormalize (keyStripEstim);
  }


  if (_printLevel > 2) {
    
    std::cout << " segment CSCDetId " << segment.cscDetId() << std::endl;
    std::cout << "Key Strip Estimation is "      << keyStripEstim << std::endl;
    std::cout << "Key Wire Group Estimation is " << keyWiregEstim << std::endl;
  }

  int numLCTsChamber = 0;

  int deltaWireg = 999, deltaStrip = 999;

  int lctId = -1;    
  for (uint iLCT = 0; iLCT < LCTs->size(); iLCT++) {

    l1t::EMTFHit _LCT =  LCTs->at(iLCT);
    if (_LCT.Neighbor() != 0) continue;
    lctId += 1;

    if (_printLevel > 2) {
      cout << "lctId = " << lctId
	/* cout */ <<", lctEndcap       = " << _LCT.Endcap() /* << endl; */
	/* cout */ <<", lctSector       = " << _LCT.Sector() /* << endl; */
	/* cout */ <<", lctSubSector    = " << _LCT.Subsector()
	/* cout */ <<", lctStation      = " << _LCT.Station() /* << endl; */
	/* cout */ <<", lctRing         = " << _LCT.Ring() /* << endl; */
	/* cout */ <<", lctChamber      = " << _LCT.Chamber() << endl;
    }

    // Require segment and LCT to be from the same chamber
    if ( (tempDetId->endcap() == 1) != (_LCT.Endcap() == 1) || tempDetId->station() != _LCT.Station() ||
	 tempDetId->triggerSector() != _LCT.Sector() || tempDetId->chamber() != _LCT.Chamber() ) continue;
    if ( tempDetId->ring() != _LCT.Ring() && abs(tempDetId->ring() - _LCT.Ring()) != 3 ) continue;
    
    /*
    CSCDetId id                = Lct->detId<CSCDetId>();
    auto lct_station           = id.station();
    auto lct_endcap            = id.endcap();
    auto lct_chamber           = id.chamber();
    uint16_t lct_bx            = Lct->getCSCData().bx;
    int lct_ring               = id.ring();
    int lct_sector             = CSCTriggerNumbering::triggerSectorFromLabels(id);
    int lct_subsector          = CSCTriggerNumbering::triggerSubSectorFromLabels(id);
    uint16_t lct_bx0           = Lct->getCSCData().bx0;
    uint16_t lct_cscID         = Lct->getCSCData().cscID;
    uint16_t lct_strip         = Lct->getCSCData().strip;
    uint16_t lct_pattern       = Lct->getCSCData().pattern;
    uint16_t lct_bend          = Lct->getCSCData().bend;
    uint16_t lct_quality       = Lct->getCSCData().quality;
    uint16_t lct_keywire       = Lct->getCSCData().keywire;
    */
    
    // // Not sure what these lines did. - AWB 01.07.16
    // if (match_report)
    //   (*match_report) |= MATCH_CHAMBER;
    
    LCT_key_wireg = _LCT.Wire();
    LCT_key_strip = _LCT.Strip();
      
    numLCTsChamber++;
      
    if (me11aStation)
      LCT_key_strip = me11aNormalize( LCT_key_strip );
      
    if (_printLevel > 2) {
      cout << "LCT_key_wireg = " << LCT_key_wireg  << endl;
      cout << "LCT_key_strip = " << LCT_key_strip  << endl;
    }
      
    deltaWireg = keyWiregEstim - LCT_key_wireg;
    deltaStrip = keyStripEstim - LCT_key_strip;
      
    if (me11aStation){ // the ganging of ME11a causes wraparound effects at the boundaries for delta strip 
        
      if (deltaStrip > 16) deltaStrip -= 32;
      if (deltaStrip < -16) deltaStrip += 32;
        
    }
            
    if (_monitorHist){
        
      _delStrip [histoFillIndex] -> Fill ( deltaStrip );
      _delWireg [histoFillIndex] -> Fill ( deltaWireg );
        
      /*  if ((lctRange.second - lctRange.first) == 1) {
        _closestStrip [histoFillIndex] -> Fill ( deltaStrip );
        _closestWireg [histoFillIndex] -> Fill ( deltaWireg );
	}*/
        
    } 

    // Fill the array of LCT ID values.  What motivates the choice of window?
    // if ( abs(deltaWireg) <= 5 && abs(deltaStrip) <= 10 ) { // This seems too wide - AWB 02.07.16
    if ( abs(deltaWireg) + abs(deltaStrip) <= 5 ) {
      // cout << "Found matching LCT at dWire = " << deltaWireg << ", dStrip = " << deltaStrip
      // << ": bx = " << _LCT.BX() << ", endcap = " <<  _LCT.Endcap() << ", sector = " << _LCT.Sector() 
      // << ", sub = " << _LCT.Subsector() << ", station = " << _LCT.Station() << ", ring = " << _LCT.Ring() 
      // << ", chamber = " <<  _LCT.Chamber() << ", CSC ID = " << _LCT.CSC_ID() << ", strip = " << _LCT.Strip() << ", wire = " << _LCT.Wire() << endl;
      for (uint i = 0; i < 8; i++) {
	if (lct_arr[i] == -999) {
	  lct_arr[i] = lctId;
	  break; }
      }
  }

    if (_printLevel > 3) {
      cout << "deltaWireg = " << deltaWireg << endl;
      cout << "deltaStrip = " << deltaStrip << endl;
    }
  }

  // // Not sure what these lines did. - AWB 01.07.16
  // if (lctWiregMatch && match_report)
  //   (*match_report) |= MATCH_WIREG;
  // if (lctStripMatch && match_report)
  //   (*match_report) |= MATCH_STRIP;
    
  //_numLCTSChamber [histoFillIndex] -> Fill ( numLCTsChamber );
	
  if (_printLevel > 2) {

    if (lct_arr[0] == -999) cout << "FAIL: no match for segment with CSC ID " << segment.cscDetId() 
				 << " in " << numLCTsChamber << " LCTs" << endl;
    else cout << "SUCCESS: segment with CSC ID " << segment.cscDetId() << " has matched LCTs with ID "
	      << lct_arr[0] << ", " << lct_arr[1] << ", " << lct_arr[2] << ", " << lct_arr[3] << " ..." << endl;

  }
  
  delete tempDetId;
  
  std::vector<int> lct_vec(lct_arr, lct_arr+8);
  return lct_vec;
  
}

bool SegmentLCTMatchBox::isLCTAble ( const CSCSegment &segment, int *match_report ){

  if (_printLevel > 3)
    std::cout << "\n*** SegmentLCTMatchBox::isLCTAble *** " << std::endl;

  if (match_report)
    (*match_report) = 0;

  if (segment . nRecHits() < 4 ) {
    if (_printLevel > 2)
      std::cout << "n Rec Hits < 4: return false" << std::endl;
    return false;
  }


  bool hadKeyInfo = false;

  int thisStation = segment.cscDetId().station();  

  int keyStrip = 999, keyWireg = 999;

  const std::vector<CSCRecHit2D>& theHits = segment . specificRecHits();
	    
  std::vector<CSCRecHit2D>::const_iterator hitIter;

  double sumStrip = 0, sumWireg = 0, nHits = 0;

  for (hitIter = theHits.begin(); hitIter!= theHits.end(); hitIter++){

    if (hitIter -> cscDetId(). layer() == 3){

      hadKeyInfo = true;
    
      keyStrip = halfStrip (*hitIter);
      keyWireg = wireGroup (*hitIter);

      if (match_report)
	(*match_report) |= MATCH_HASKEY;

    } 

    sumStrip += halfStrip( *hitIter );
    sumWireg += wireGroup( *hitIter );
    nHits+= 1.0;

    if (_printLevel > 3){
      std::cout << "layer: " << hitIter -> cscDetId(). layer() << " " 
        //<< " number of strips participating: " << hitIter -> channels().size() << std::endl;
                << " number of strips participating: " << hitIter -> nStrips() << std::endl;
      //if ( hitIter -> channels().size()==1 )
      if ( hitIter -> nStrips()==1 )
	//std::cout << hitIter -> channels()[0] << " " << hitIter -> positionWithinStrip() 
        std::cout << hitIter -> channels(0) << " " << hitIter -> positionWithinStrip() 
		  << halfStrip(*hitIter) << std::endl;
    }
    
  }	    

  if (!hadKeyInfo){ // no hit in key layer... improvize with the averages

    keyStrip = TMath::FloorNint( sumStrip / nHits + 0.5 );
    keyWireg = TMath::FloorNint( sumWireg / nHits + 0.5 );

    if (_printLevel > 3) {
      std::cout << "no hit in key layer... improvize with the averages\n";
      std::cout << " sumStrip: " << sumStrip 
                << " sumWireg: " << sumWireg 
                << " nHits: "    << nHits << std::endl;
    }
    
  }

  int hitsFidAlct = 0;
  int hitsFidClct = 0;

  if (_printLevel > 3 )
    std::cout << "\nkey wg, strip: " << keyWireg <<  ", " << keyStrip << std::endl;


  for (hitIter = theHits.begin(); hitIter!= theHits.end(); hitIter++){

    int thisLayer = hitIter -> cscDetId() . layer();

    int delWgroup = wireGroup( *hitIter ) - keyWireg;
    int delStrip  = halfStrip( *hitIter ) - keyStrip;
    
    if (_printLevel > 3 ){ // debug why this match didn't work
      
      std::cout << "layer: " << thisLayer << ", wg,st: " << wireGroup( *hitIter ) << ", " << halfStrip ( *hitIter )
		<< ", deltas: " << delWgroup << ", " << delStrip ;
      
    }
    
    int histoFillIndex;
    
    if (segment.cscDetId().ring() == 4)
      histoFillIndex = 0;
    else
      histoFillIndex = segment.cscDetId().station();
    
    if (_monitorHist){
      
      _alctPattern [histoFillIndex] -> Fill ( delWgroup, thisLayer );
      _clctPattern [histoFillIndex] -> Fill ( delStrip,  thisLayer );

    }

    if (thisLayer <=3)
      delWgroup = -delWgroup;
    
    if (thisStation == 3)
      delWgroup = -delWgroup;
    
    if (thisStation == 4)
      delWgroup = -delWgroup;
    
    if ( delWgroup >=0 )
      if ( delWgroup <= (_alctEnvelopes[ thisLayer - 1 ]) ) hitsFidAlct++;
    
    if ( abs(delStrip)  <= (_clctEnvelopes[ thisLayer - 1 ]) ) hitsFidClct++;
    
    if (_printLevel > 2 )
      std::cout << " hitsFid alct: " << hitsFidAlct << " clct: " << hitsFidClct << std::endl;

  }

  if (!hadKeyInfo && (_printLevel > 2)) std::cout << "NO KEY INFO!" << std::endl;


  if ( hitsFidAlct < 3 ) {
    if (_printLevel > 2) std::cout << "hitsFidAlct < 3: return false\n";
    return false;
  }
  if ( hitsFidClct < 3) {
    if (_printLevel > 2) std::cout << "hitsFidClct < 3: return false\n";
    return false;
  }
  
  if (!hadKeyInfo && (_printLevel > 2) ) std::cout << "NO KEY INFO AND FIDUCIAL! " << segment.cscDetId() << std::endl;

  if (_printLevel > 2) std::cout << "return TRUE\n";
  return true;

}



