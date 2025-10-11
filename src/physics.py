import numpy as np
from scipy.special import erf

class PhysicsEngine:
    """Handles all physics calculations for dark matter interactions"""
    
    C = 3e8
    HBAR = 1.055e-34
    WIMP_MASS = 50.0
    WIMP_CROSS_SECTION = 1e-45
    EARTH_VELOCITY = 230e3
    
    def __init__(self):
        self.interaction_count = 0
        self.total_energy_deposited = 0.0
    
    def calculate_interaction_probability(self, wimp_velocity: float) -> float:
        v0 = 220e3
        maxwell_factor = np.exp(-(wimp_velocity / v0)**2)
        prob = self.WIMP_CROSS_SECTION * maxwell_factor / 1e-44
        return min(prob, 1.0)
    
    def nuclear_recoil_energy(self, wimp_mass: float, nucleus_mass: float, 
                             wimp_velocity: float) -> float:
        mu = (wimp_mass * nucleus_mass) / (wimp_mass + nucleus_mass)
        max_energy = 2 * mu * wimp_velocity**2 / self.C**2
        recoil = np.random.uniform(0, max_energy)
        return recoil * 1000
    
    def quenching_factor(self, recoil_energy: float, particle_type) -> float:
        if particle_type.name == 'DARK_MATTER':
            epsilon = recoil_energy / 10.0
            return epsilon / (1 + 3*epsilon)
        return 1.0
    
    def scattering_angle(self) -> float:
        cos_theta = np.random.uniform(-1, 1)
        theta = np.arccos(cos_theta)
        return theta
    
    def ionization_tracks(self, energy_deposited: float) -> int:
        electron_energy = 13.6 / 1000
        tracks = int(energy_deposited / electron_energy)
        return tracks
    
    def electron_recoil_equivalent(self, nuclear_recoil: float, 
                                  quench: float) -> float:
        ere = nuclear_recoil * quench
        return ere
    
    def statistical_significance(self, signal_events: int, 
                                background_events: int) -> float:
        if background_events == 0:
            return float('inf') if signal_events > 0 else 0
        significance = signal_events / np.sqrt(signal_events + background_events)
        return significance
    
    def background_rejection_efficiency(self, signal_events: int, 
                                       rejected_background: int,
                                       total_background: int) -> float:
        if total_background == 0:
            return 0.0
        return rejected_background / total_background
    
    def detector_efficiency(self, energy: float) -> float:
        threshold = 3.0
        if energy < threshold:
            return 0.0
        elif energy < 10.0:
            return 0.4 * (energy - threshold) / (10 - threshold)
        else:
            return min(0.8, 0.8 * (energy / 50.0))
    
    def background_rate(self, energy: float, detector_mass_kg: float) -> float:
        base_rate = 1.0
        return (base_rate * 10.0 / energy) * (detector_mass_kg / 1.0)
    
    def simulate_interaction_cascade(self, initial_energy: float) -> dict:
        cascade = {
            'primary_recoil': initial_energy,
            'secondary_ionizations': self.ionization_tracks(initial_energy),
            'photon_production': int(initial_energy / 50),
            'heat_generated': initial_energy * 0.001
        }
        return cascade
