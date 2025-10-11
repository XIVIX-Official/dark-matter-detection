import numpy as np
from dataclasses import dataclass
from typing import List, Dict
from .particle import Particle, ParticleType, Event
from .physics import PhysicsEngine

@dataclass
class DetectorConfig:
    """Detector configuration parameters"""
    detector_type: str = "superfluid_helium"
    mass_kg: float = 1.0
    temperature_mk: float = 15.0
    energy_threshold_kev: float = 3.0
    energy_resolution: float = 0.03
    background_rate_per_kg_day: float = 0.01
    exposure_time_days: float = 365.0

class Detector:
    """Main detector simulation class"""
    
    def __init__(self, config: DetectorConfig = None):
        if config is None:
            config = DetectorConfig()
        
        self.config = config
        self.physics = PhysicsEngine()
        self.events: List[Event] = []
        self.particles: List[Particle] = []
        self.event_counter = 0
        self.simulation_stats = {}
        self.detector_response = []
    
    def generate_background_events(self, num_events: int) -> List[Particle]:
        """Generate background (non-dark matter) events"""
        background = []
        
        for _ in range(num_events):
            energy = np.random.exponential(10.0)
            energy = np.clip(energy, self.config.energy_threshold_kev, 1000)
            
            theta = np.arccos(np.random.uniform(-1, 1))
            phi = np.random.uniform(0, 2*np.pi)
            
            momentum = np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ]) * energy
            
            particle = Particle(
                particle_type=np.random.choice([ParticleType.BACKGROUND, ParticleType.COSMIC_RAY]),
                energy=energy,
                momentum=momentum,
                position=np.random.uniform(-1, 1, 3),
                timestamp=np.random.uniform(0, self.config.exposure_time_days * 86400),
                interaction_type="background"
            )
            background.append(particle)
        
        return background
    
    def generate_dark_matter_events(self, num_events: int) -> List[Particle]:
        """Generate simulated dark matter events"""
        dm_events = []
        
        for _ in range(num_events):
            v0 = 220e3
            speed = np.random.normal(v0, v0/4)
            
            recoil_energy = self.physics.nuclear_recoil_energy(
                self.physics.WIMP_MASS, 20, speed
            )
            
            if recoil_energy < self.config.energy_threshold_kev:
                continue
            
            if np.random.random() > self.physics.detector_efficiency(recoil_energy):
                continue
            
            measured_energy = recoil_energy * np.random.normal(1.0, self.config.energy_resolution)
            
            theta = np.arccos(np.random.uniform(-1, 1))
            phi = np.random.uniform(0, 2*np.pi)
            
            momentum = np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ]) * measured_energy
            
            particle = Particle(
                particle_type=ParticleType.DARK_MATTER,
                energy=measured_energy,
                momentum=momentum,
                position=np.random.uniform(-1, 1, 3),
                timestamp=np.random.uniform(0, self.config.exposure_time_days * 86400),
                interaction_type="nuclear_recoil"
            )
            dm_events.append(particle)
        
        return dm_events
    
    def process_event(self, particle: Particle) -> Event:
        """Process a single particle event into detector event"""
        self.event_counter += 1
        
        cascade = self.physics.simulate_interaction_cascade(particle.energy)
        
        expected_background = self.config.background_rate_per_kg_day * self.config.mass_kg
        significance = self.physics.statistical_significance(1, int(expected_background))
        
        background_prob = 1.0 - (particle.particle_type == ParticleType.DARK_MATTER)
        
        event = Event(
            event_id=self.event_counter,
            particles=[particle],
            total_energy=particle.energy,
            timestamp=particle.timestamp,
            detector_hit_count=cascade['secondary_ionizations'],
            significance=significance,
            background_probability=background_prob
        )
        
        self.events.append(event)
        self.particles.append(particle)
        self.detector_response.append({
            'energy': particle.energy,
            'type': particle.particle_type.name,
            'timestamp': particle.timestamp
        })
        
        return event
    
    def run_simulation(self, background_events: int = 1000, 
                     dark_matter_events: int = 10) -> Dict:
        """Run complete detector simulation"""
        bg_particles = self.generate_background_events(background_events)
        dm_particles = self.generate_dark_matter_events(dark_matter_events)
        
        all_particles = bg_particles + dm_particles
        np.random.shuffle(all_particles)
        
        for particle in all_particles:
            self.process_event(particle)
        
        dm_detections = sum(1 for e in self.events if e.particles[0].particle_type == ParticleType.DARK_MATTER)
        bg_rejections = sum(1 for e in self.events if e.particles[0].particle_type != ParticleType.DARK_MATTER)
        
        self.simulation_stats = {
            'total_events': len(self.events),
            'dark_matter_candidates': dm_detections,
            'background_events': bg_rejections,
            'mean_energy': np.mean([e.total_energy for e in self.events]) if self.events else 0,
            'max_energy': max([e.total_energy for e in self.events]) if self.events else 0,
            'min_energy': min([e.total_energy for e in self.events]) if self.events else 0,
            'total_exposure': self.config.exposure_time_days * self.config.mass_kg,
            'detector_efficiency': dm_detections / dark_matter_events if dark_matter_events > 0 else 0
        }
        
        return self.simulation_stats
    
    def get_energy_spectrum(self) -> Dict:
        """Get binned energy spectrum"""
        if not self.events:
            return {'bins': [], 'counts': []}
        
        energies = [e.total_energy for e in self.events]
        counts, bins = np.histogram(energies, bins=50, range=(0, max(energies)))
        
        return {
            'bins': bins.tolist(),
            'counts': counts.tolist(),
            'energies': energies
        }
    
    def get_temporal_distribution(self) -> Dict:
        """Get event distribution over time"""
        if not self.events:
            return {'times': [], 'counts': []}
        
        timestamps = [e.timestamp for e in self.events]
        counts, bins = np.histogram(timestamps, bins=30)
        
        return {
            'times': bins.tolist(),
            'counts': counts.tolist(),
            'total_time': self.config.exposure_time_days * 86400
        }
