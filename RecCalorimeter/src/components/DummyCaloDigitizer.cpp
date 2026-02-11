#include "DummyCaloDigitizer.h"

// EDM4hep
#include "edm4hep/CalorimeterHit.h"

DECLARE_COMPONENT(DummyCaloDigitizer)

DummyCaloDigitizer::DummyCaloDigitizer(const std::string& name, ISvcLocator* svcLoc)
    : Transformer(name, svcLoc,
                  {KeyValues("InputCollection", {"SimCalorimeterHitCollection"})},
                  {KeyValues("OutputCollection", {"CalorimeterHitCollection"})}) {}

StatusCode DummyCaloDigitizer::initialize() {
  info() << "DummyCaloDigitizer initialized with calibration constant: " << m_calibConst.value() << endmsg;
  return StatusCode::SUCCESS;
}

edm4hep::CalorimeterHitCollection DummyCaloDigitizer::operator()(
    const edm4hep::SimCalorimeterHitCollection& input) const {
  
  // Create output collection
  edm4hep::CalorimeterHitCollection output;
  
  // Loop over input SimCalorimeterHits
  for (const auto& simHit : input) {
    // Create a new CalorimeterHit
    auto caloHit = output.create();
    
    // Copy cellID
    caloHit.setCellID(simHit.getCellID());
    
    // Copy position
    caloHit.setPosition(simHit.getPosition());
    
    // Copy energy (multiplied by calibration constant)
    caloHit.setEnergy(simHit.getEnergy() * m_calibConst.value());
  }
  
  debug() << "Processed " << input.size() << " SimCalorimeterHits -> " 
          << output.size() << " CalorimeterHits" << endmsg;
  
  return output;
}

StatusCode DummyCaloDigitizer::finalize() {
  return StatusCode::SUCCESS;
}
