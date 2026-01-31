import sys, os

ROOT = os.path.dirname(__file__)
sys.path.insert(0, ROOT)

from demo.app import main
from demo.backend.pytorch import DET_ARCHS, RECO_ARCHS

main(DET_ARCHS, RECO_ARCHS)
