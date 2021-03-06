#include "IOPool/Streamer/interface/MsgTools.h"
#include "IOPool/Streamer/interface/StreamerInputFile.h"
#include "IOPool/Streamer/src/StreamerFileReader.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include "FWCore/Catalog/interface/InputFileCatalog.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Sources/interface/EventSkipperByID.h"

namespace edm {

  StreamerFileReader::StreamerFileReader(ParameterSet const& pset, InputSourceDescription const& desc) :
      StreamerInputSource(pset, desc),
      streamerNames_(pset.getUntrackedParameter<std::vector<std::string> >("fileNames")),
      streamReader_(),
      eventSkipperByID_(EventSkipperByID::create(pset).release()),
      initialNumberOfEventsToSkip_(pset.getUntrackedParameter<unsigned int>("skipEvents")) {
    InputFileCatalog catalog(pset.getUntrackedParameter<std::vector<std::string> >("fileNames"), pset.getUntrackedParameter<std::string>("overrideCatalog"));
    streamerNames_ = catalog.fileNames();
    reset_();

  }

  StreamerFileReader::~StreamerFileReader() {
  }

  void
  StreamerFileReader::reset_() {
    if (streamerNames_.size() > 1) {
      streamReader_ = std::unique_ptr<StreamerInputFile>(new StreamerInputFile(streamerNames_, eventSkipperByID_));
    } else if (streamerNames_.size() == 1) {
      streamReader_ = std::unique_ptr<StreamerInputFile>(new StreamerInputFile(streamerNames_.at(0), eventSkipperByID_));
    } else {
      throw Exception(errors::FileReadError, "StreamerFileReader::StreamerFileReader")
         << "No fileNames were specified\n";
    }
    InitMsgView const* header = getHeader();
    deserializeAndMergeWithRegistry(*header, false);
    if(initialNumberOfEventsToSkip_) {
      skip(initialNumberOfEventsToSkip_);
    }
  }


  bool StreamerFileReader::checkNextEvent() {
    EventMsgView const* eview = getNextEvent();

    if (newHeader()) {
      // FDEBUG(6) << "A new file has been opened and we must compare Headers here !!" << std::endl;
      // A new file has been opened and we must compare Heraders here !!
      //Get header/init from reader
      InitMsgView const* header = getHeader();
      deserializeAndMergeWithRegistry(*header, true);
    }
    if (eview == nullptr) {
      return  false;
    }
    deserializeEvent(*eview);
    return true;
  }

  void
  StreamerFileReader::skip(int toSkip) {
    for(int i = 0; i != toSkip; ++i) {
      EventMsgView const* evMsg = getNextEvent();
      if(evMsg == nullptr)  {
        return;
      }
      // If the event would have been skipped anyway, don't count it as a skipped event.
      if(eventSkipperByID_ && eventSkipperByID_->skipIt(evMsg->run(), evMsg->lumi(), evMsg->event())) {
        --i;
      }
    }
  }

  void
  StreamerFileReader::genuineCloseFile() {
    if(streamReader_.get() != nullptr) streamReader_->closeStreamerFile();
  }

  bool
  StreamerFileReader::newHeader() {
    return streamReader_->newHeader();
  }

  InitMsgView const*
  StreamerFileReader::getHeader() {

    InitMsgView const* header = streamReader_->startMessage();

    if(header->code() != Header::INIT) { //INIT Msg
      throw Exception(errors::FileReadError, "StreamerFileReader::readHeader")
        << "received wrong message type: expected INIT, got "
        << header->code() << "\n";
    }
    return header;
  }

  EventMsgView const*
  StreamerFileReader::getNextEvent() {
    if (!streamReader_->next()) {
      return nullptr;
    }
    return streamReader_->currentRecord();
  }

  void
  StreamerFileReader::fillDescriptions(ConfigurationDescriptions& descriptions) {
    ParameterSetDescription desc;
    desc.setComment("Reads events from streamer files.");
    desc.addUntracked<std::vector<std::string> >("fileNames")
        ->setComment("Names of files to be processed.");
    desc.addUntracked<unsigned int>("skipEvents", 0U)
        ->setComment("Skip the first 'skipEvents' events that otherwise would have been processed.");
    desc.addUntracked<std::string>("overrideCatalog", std::string());
    //This next parameter is read in the base class, but its default value depends on the derived class, so it is set here.
    desc.addUntracked<bool>("inputFileTransitionsEachEvent", false);
    StreamerInputSource::fillDescription(desc);
    EventSkipperByID::fillDescription(desc);
    descriptions.add("source", desc);
  }
} //end-of-namespace

