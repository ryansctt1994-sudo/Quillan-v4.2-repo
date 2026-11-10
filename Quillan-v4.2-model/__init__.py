"""Quillan v4.2 model package.

Only the modules that exist in this repository are exported. ``model.py`` needs
``layers`` and ``train`` sub-packages that are not included, so they are not imported here.
"""
from .config import RLConfig
from .quillan_council_enhanced import CouncilExpert, CouncilMoELayer, CouncilOutput, HierarchicalConsensus

__all__ = ["RLConfig", "CouncilExpert", "CouncilMoELayer", "CouncilOutput", "HierarchicalConsensus"]
