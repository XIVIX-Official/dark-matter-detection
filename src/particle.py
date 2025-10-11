import numpy as np
from dataclasses import dataclass
from enum import Enum

class ParticleType(Enum):
    DARK_MATTER = 1
    BACKGROUND = 2
    NEUTRINO = 3
    COSMIC_RAY = 4

@dataclass
class Particle:
    """Represents a particle in the detector"""
    particle_type: ParticleType
    energy: float
    momentum: np.ndarray
    position: np.ndarray
    timestamp: float
    interaction_type: str
    
    def __post_init__(self):
        self.momentum = np.array(self.momentum)
        self.position = np.array(self.position)
        self.mass = self._get_mass()
        self.velocity = self._calculate_velocity()
    
    def _get_mass(self) -> float:
        mass_map = {
            ParticleType.DARK_MATTER: 50.0,
            ParticleType.NEUTRINO: 0.0,
            ParticleType.COSMIC_RAY: 0.938,
            ParticleType.BACKGROUND: 0.511
        }
        return mass_map.get(self.particle_type, 0.0)
    
    def _calculate_velocity(self) -> np.ndarray:
        if np.linalg.norm(self.momentum) == 0:
            return np.zeros(3)
        p_mag = np.linalg.norm(self.momentum)
        e_total = np.sqrt(p_mag**2 + self.mass**2)
        return 3e8 * self.momentum / e_total
    
    def get_kinetic_energy(self) -> float:
        p_mag = np.linalg.norm(self.momentum)
        e_total = np.sqrt(p_mag**2 + self.mass**2)
        return e_total - self.mass
    
    def ionization_loss(self, distance: float) -> float:
        if self.energy < 0.1:
            return 0
        return self.energy * distance * 0.001

@dataclass
class Event:
    """Represents a detection event"""
    event_id: int
    particles: list
    total_energy: float
    timestamp: float
    detector_hit_count: int
    significance: float
    background_probability: float