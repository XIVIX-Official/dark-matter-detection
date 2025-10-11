"""XIVIX Dark Matter Detection Package"""

__version__ = "1.0.0"
__author__ = "XIVIX Contributors"
__description__ = "Monte Carlo simulation for detecting dark matter particles"

from .particle import Particle, Event, ParticleType
from .physics import PhysicsEngine
from .detector import Detector, DetectorConfig

__all__ = [
    'Particle',
    'Event', 
    'ParticleType',
    'PhysicsEngine',
    'Detector',
    'DetectorConfig'
]