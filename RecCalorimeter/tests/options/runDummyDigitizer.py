from Gaudi.Configuration import *

# Data service
from k4FWCore import IOSvc
from Configurables import EventDataSvc
io_svc = IOSvc("IOSvc")
io_svc.Input = "input.root"
io_svc.Output = "output.root"
io_svc.OutputLevel = DEBUG

# from Configurables import k4DataSvc
# dataservice = k4DataSvc("EventDataSvc", input="input.root")

# from Configurables import PodioInput
# podioinput = PodioInput("PodioInput",
#     collections = [
#         "SCEPCal_MainCcounts",
#         "SCEPCal_MainScounts",
#     ],
#     OutputLevel = DEBUG
# )

# from Configurables import PodioOutput
# podiooutput = PodioOutput("PodioOutput", filename = "output.root", OutputLevel = DEBUG)
# podiooutput.outputCommands = ["keep *"]

# Detector geometry
from Configurables import GeoSvc
import os
geoservice = GeoSvc("GeoSvc")
path_to_detector = os.environ.get("K4GEO", "")
# detectors_to_use = [
#     'FCCee/IDEA/compact/IDEA_o1_v03/IDEA_o1_v03.xml'
# ]
geoservice.detectors = [
    "/u/user/sako/kfc-dream/k4geo/FCCee/IDEA/compact/IDEA_o2_v01/IDEA_o2_v01_noBucatini.xml" # os.path.join(path_to_detector, _det) for _det in detectors_to_use
]
geoservice.OutputLevel = INFO

# DummyCaloDigitizer: transforms SimCalorimeterHits to CalorimeterHits
from Configurables import DummyCaloDigitizer
dummyDigitizer_cheren = DummyCaloDigitizer("cherenDummyDigitizer",
    InputCollection=["SCEPCal_MainCcounts"],
    OutputCollection=["SCEPCal_digi_cheren"],
    calibrationConstant=1./97.75, # 3910/ 40 GeV
    OutputLevel=INFO
)

dummyDigitizer_scint = DummyCaloDigitizer("scintDummyDigitizer",
    InputCollection=["SCEPCal_MainScounts"],
    OutputCollection=["SCEPCal_digi_scint"],
    calibrationConstant=1./1965., # 78600/ 40 GeV
    OutputLevel=INFO
)

# Const noise tool for topoclustering
from Configurables import ConstNoiseTool
constNoiseTool = ConstNoiseTool("ConstNoiseTool",
    detectors = ["ECAL_Barrel", "ECAL_Endcap"],
    systemEncoding = "system:5",
    detectorsNoiseRMS = [0.01,0.01],
    detectorsNoiseOffset = [0.,0.],
    OutputLevel = INFO
)

# CaloTopoClusterFCCee: create topological clusters from calorimeter hits
from Configurables import CaloTopoClusterFCCee
topoCluster = CaloTopoClusterFCCee("TopoCluster",
    cells = ["SCEPCal_digi_cheren", "SCEPCal_digi_scint"],
    clusters = "TopoClusterAll",
    clusterCells = "TopoClusterAllCells",
    useNeighborMap = False,
    readoutName = "SCEPCal_Main",
    neigboursTool = None,
    noiseTool = constNoiseTool,
    systemEncoding = "system:5",
    seedSigma = 4,
    neighbourSigma = 2,
    lastNeighbourSigma = 0,
    # minClusterEnergy = 0.1,
    calorimeterIDs = [4,5],
    createClusterCellCollection = True,
    OutputLevel = INFO
)

# RNG for sipm emulation (TODO harmonize RNG with other modules)
from Configurables import HepRndm__Engine_CLHEP__RanluxEngine_ as RndmEngine
rndmEngine = RndmEngine('RndmGenSvc.Engine',
  SetSingleton = True,
  Seeds = [ 1234567 ] # default seed is 1234567
)

from Configurables import RndmGenSvc
rndmGenSvc = RndmGenSvc("RndmGenSvc",
  Engine = rndmEngine.name()
)

# Output
# io_svc.outputCommands = [
#   "keep *",
# ]

# Profiling
from Configurables import AuditorSvc, ChronoAuditor, UniqueIDGenSvc
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]

# Application manager
from k4FWCore import ApplicationMgr
application_mgr = ApplicationMgr(
    TopAlg = [
        # podioinput,
        dummyDigitizer_cheren,
        dummyDigitizer_scint,
        topoCluster,
        # podiooutput
    ],
    EvtSel = 'NONE',
    EvtMax = -1,
    ExtSvc = [
        EventDataSvc("EventDataSvc"),
        geoservice,
        audsvc,
        UniqueIDGenSvc("uidSvc"),
        rndmEngine,
        rndmGenSvc,
    ],
    StopOnSignal = True,
)

for algo in application_mgr.TopAlg:
    algo.AuditExecute = True
    algo.OutputLevel = DEBUG
