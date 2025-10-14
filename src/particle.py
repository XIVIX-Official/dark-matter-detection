"""
Particle and Event classes for dark matter simulation.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict
import numpy as np
from datetime import datetime

@dataclass
class Particle:
    """Base class for particles in the simulation."""
    mass: float  # GeV/c²
    energy: float  # keV
    position: np.ndarray  # [x, y, z] in meters
    velocity: np.ndarray  # [vx, vy, vz] in m/s
    
    def __post_init__(self):
        """Convert lists to numpy arrays if needed."""
        if isinstance(self.position, list):
            self.position = np.array(self.position)
        if isinstance(self.velocity, list):
            self.velocity = np.array(self.velocity)

@dataclass
class WIMP(Particle):
    """Weakly Interacting Massive Particle."""
    cross_section: float  # cm²

    def get_kinetic_energy(self) -> float:
        """Calculate kinetic energy in keV."""
        return 0.5 * self.mass * np.sum(self.velocity ** 2) * 1e-6  # Convert to keV

@dataclass
class Nucleus(Particle):
    """Target nucleus in the detector."""
    atomic_number: int
    atomic_mass: int
    form_factor: float = 1.0

@dataclass
class DetectionEvent:
    """Represents a detection event in the simulation."""
    event_id: int
    timestamp: datetime
    energy_deposited: float  # keV
    position: np.ndarray  # [x, y, z] in meters
    is_signal: bool  # True for WIMP events, False for background
    detector_response: float  # Efficiency-adjusted energy
    metadata: Dict = None

    def __post_init__(self):
        """Convert lists to numpy arrays and ensure proper types."""
        if isinstance(self.position, list):
            self.position = np.array(self.position)
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict:
        """Convert event to dictionary for API responses."""
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'energy_deposited': float(self.energy_deposited),
            'position': self.position.tolist(),
            'is_signal': self.is_signal,
            'detector_response': float(self.detector_response),
            'metadata': self.metadata
        }

class EventCollection:
    """Collection of detection events with analysis methods."""
    def __init__(self):
        self.events: List[DetectionEvent] = []
        
    def add_event(self, event: DetectionEvent):
        """Add an event to the collection."""
        self.events.append(event)
        
    def get_energy_spectrum(self, bins: int = 100) -> Dict:
        """Calculate energy spectrum of events."""
        energies = [e.detector_response for e in self.events]
        hist, bin_edges = np.histogram(energies, bins=bins)
        return {
            'bins': bin_edges.tolist(),
            'counts': hist.tolist()
        }
        
    def get_temporal_distribution(self, bins: int = 50) -> Dict:
        """Calculate temporal distribution of events."""
        times = [(e.timestamp - self.events[0].timestamp).total_seconds()
                for e in self.events]
        hist, bin_edges = np.histogram(times, bins=bins)
        return {
            'times': bin_edges.tolist(),
            'counts': hist.tolist()
        }
        
    def get_statistics(self) -> Dict:
        """Calculate basic statistics of the event collection."""
        energies = np.array([e.detector_response for e in self.events])
        signal_events = [e for e in self.events if e.is_signal]
        
        return {
            'total_events': len(self.events),
            'dark_matter_candidates': len(signal_events),
            'background_events': len(self.events) - len(signal_events),
            'mean_energy': float(np.mean(energies)),
            'max_energy': float(np.max(energies)),
            'min_energy': float(np.min(energies))
        }