# Instructions for LCT-Segment matching code:

## To Grab code:
```
cmsrel CMSSW_10_0_0
cd CMSSW_10_0_0/src
cmsenv
git cms-init
git remote add chadfreer git@github.com:chadfreer/cmssw.git
git cms-merge-topic -u chadfreer:LCT-Matched-Plotter
scram b
```
## To run NTuple code (edit RunTrackFinder_data_NTuple.py to change input datasets/runs):
```
cd EMTFAnalyzer/NTupleMaker
voms-proxy-init --voms cms
cmsRun test/RunTrackFinder_data_NTuple.py
```
## To run plotting Macro (edit Plotter.C to edit input file and plots)
```
root -l Plotter.C
```
## What is included in the NTuple

Event Info&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/FlatNtupleBranches/EventInfo.cc  
EMTF Hit&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/FlatNtupleBranches/EMTFHitInfo.cc  
EMTF Track&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/FlatNtupleBranches/EMTFTrackInfo.cc  
Unpacked Tracks&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/FlatNtupleBranches/EMTFUnpTrackInfo.cc  
CSC Segments&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/FlatNtupleBranches/CSCSegInfo.cc  
Gen Muons&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/FlatNtupleBranches/GenMuonInfo.cc  
Reco Muons&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/FlatNtupleBranches/RecoMuonInfo.cc  

## Matching codes

LCT-Segments&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/MatcherSeg/LCTSegMatcher.cc  
EMTF Tracks-Reco Muons&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/MatcherDR/RecoTrkMatcher.cc  

Classes for all codes can be found in corresponding h files in interface directory
