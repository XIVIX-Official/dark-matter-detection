"""
Main detector simulation module.
"""
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
import config
from .particle import WIMP, Nucleus, DetectionEvent, EventCollection
from .physics import (
    maxwell_boltzmann_velocity,
    calculate_recoil_energy,
    calculate_interaction_rate,
    generate_background,
    apply_detector_response
)

class Detector:
    """Base class for dark matter detectors."""
    
    def __init__(self, detector_type: str, mass_kg: float, temperature_mk: float):
        """
        Initialize detector.
        
        Args:
            detector_type: Type of detector (e.g., 'superfluid_helium')
            mass_kg: Mass of detector material (kg)
            temperature_mk: Operating temperature (mK)
        """
        if detector_type not in config.DETECTOR_CONFIGS:
            raise ValueError(f"Unknown detector type: {detector_type}")
            
        self.type = detector_type
        self.mass = mass_kg
        self.temperature = temperature_mk
        self.config = config.DETECTOR_CONFIGS[detector_type]
        
        # Initialize event collection
        self.events = EventCollection()
        
    def get_target_nucleus(self) -> Nucleus:
        """Get the target nucleus based on detector type."""
        nucleus_properties = {
            'superfluid_helium': (2, 3),    # He-3
            'liquid_xenon': (54, 131),      # Xe-131
            'germanium': (32, 73),          # Ge-73
            'scintillator': (53, 127)       # I-127 (typical for NaI)
        }
        
        Z, A = nucleus_properties[self.type]
        
        return Nucleus(
            mass=A * 0.9315,  # GeV/c²
            energy=0,
            position=np.zeros(3),
            velocity=np.zeros(3),
            atomic_number=Z,
            atomic_mass=A
        )
        
    def simulate_wimp_event(self, wimp: WIMP) -> Optional[DetectionEvent]:
        """
        Simulate a single WIMP interaction.
        
        Args:
            wimp: WIMP particle
            
        Returns:
            DetectionEvent if detected, None otherwise
        """
        # Get target nucleus
        nucleus = self.get_target_nucleus()
        
        # Calculate scattering angle
        cos_theta = np.random.uniform(-1, 1)
        theta = np.arccos(cos_theta)
        
        # Calculate recoil energy
        E_r = calculate_recoil_energy(wimp, nucleus, theta)
        
        # Apply detector response
        E_detected = apply_detector_response(
            E_r,
            self.config['resolution'],
            self.config['efficiency']
        )
        
        if E_detected is None or E_detected < self.config['threshold_kev']:
            return None
            
        # Create detection event
        event = DetectionEvent(
            event_id=len(self.events.events),
            timestamp=datetime.now(),
            energy_deposited=E_r,
            position=wimp.position,
            is_signal=True,
            detector_response=E_detected,
            metadata={
                'scattering_angle': theta,
                'wimp_mass': wimp.mass,
                'wimp_velocity': np.sqrt(np.sum(wimp.velocity**2))
            }
        )
        
        return event
        
    def simulate_background_event(self, time: datetime) -> DetectionEvent:
        """
        Simulate a background event.
        
        Args:
            time: Event timestamp
            
        Returns:
            DetectionEvent
        """
        # Generate background energy
        E_bg = generate_background(
            energy_range=(0, 100),  # keV
            rate=self.config['background_rate'],
            exposure_time=1  # Single event
        )[0]
        
        # Apply detector response
        E_detected = apply_detector_response(
            E_bg,
            self.config['resolution'],
            self.config['efficiency']
        )
        
        if E_detected is None:
            E_detected = E_bg
            
        # Random position in detector
        position = np.random.uniform(-1, 1, 3)  # m
        
        # Create detection event
        event = DetectionEvent(
            event_id=len(self.events.events),
            timestamp=time,
            energy_deposited=E_bg,
            position=position,
            is_signal=False,
            detector_response=E_detected,
            metadata={'event_type': 'background'}
        )
        
        return event
        
    def run_simulation(self, 
                      exposure_time_days: float,
                      n_wimp_events: int,
                      n_background_events: int) -> EventCollection:
        """
        Run full detector simulation.
        
        Args:
            exposure_time_days: Total exposure time (days)
            n_wimp_events: Number of WIMP events to simulate
            n_background_events: Number of background events to simulate
            
        Returns:
            EventCollection with all detected events
        """
        start_time = datetime.now()
        end_time = start_time + timedelta(days=exposure_time_days)
        
        # Simulate WIMP events
        for _ in range(n_wimp_events):
            # Create WIMP with random velocity
            wimp = WIMP(
                mass=config.WIMP_MASS_GEV,
                energy=0,
                position=np.random.uniform(-1, 1, 3),
                velocity=maxwell_boltzmann_velocity(),
                cross_section=config.WIMP_CROSS_SECTION_CM2
            )
            
            # Simulate event
            event = self.simulate_wimp_event(wimp)
            if event is not None:
                self.events.add_event(event)
                
        # Simulate background events
        for _ in range(n_background_events):
            # Random time during exposure
            event_time = start_time + timedelta(
                days=np.random.uniform(0, exposure_time_days)
            )
            
            # Simulate event
            event = self.simulate_background_event(event_time)
            self.events.add_event(event)
            
        return self.events
        
    def get_results(self) -> Dict:
        """Get simulation results summary."""
        return {
            'detector_config': {
                'type': self.type,
                'mass_kg': self.mass,
                'temperature_mk': self.temperature,
                'threshold_kev': self.config['threshold_kev'],
                'resolution': self.config['resolution'],
                'efficiency': self.config['efficiency']
            },
            'statistics': self.events.get_statistics(),
            'energy_spectrum': self.events.get_energy_spectrum(),
            'temporal_distribution': self.events.get_temporal_distribution()
        }