#ifndef RECCALORIMETER_DUMMYCALODIGITIZER_H
#define RECCALORIMETER_DUMMYCALODIGITIZER_H

// k4FWCore
#include "k4FWCore/Transformer.h"

// EDM4hep
#include "edm4hep/CalorimeterHitCollection.h"
#include "edm4hep/SimCalorimeterHitCollection.h"

/** @class DummyCaloDigitizer
 *
 *  Dummy calorimeter digitizer that transforms SimCalorimeterHits to CalorimeterHits.
 *
 *  @author Your Name
 *  @date   2026-01
 */

class DummyCaloDigitizer : public k4FWCore::Transformer<
    edm4hep::CalorimeterHitCollection(const edm4hep::SimCalorimeterHitCollection&)> {

public:
  DummyCaloDigitizer(const std::string& name, ISvcLocator* svcLoc);
  
  /** Initialize.
   *  @return status code
   */
  StatusCode initialize() override;

  /** Execute transformation.
   *  @param[in] input SimCalorimeterHitCollection
   *  @return output CalorimeterHitCollection
   */
  edm4hep::CalorimeterHitCollection operator()(
      const edm4hep::SimCalorimeterHitCollection& input) const override;

  /** Finalize.
   *  @return status code
   */
  StatusCode finalize() override;

private:
  // dummy calribration constant
  Gaudi::Property<float> m_calibConst{this, "calibrationConstant", 1., "dummy calibration constant"};
};

#endif /* RECCALORIMETER_DUMMYCALODIGITIZER_H */
