"""
Physics calculations engine for dark matter interactions.
"""
import numpy as np
from typing import Tuple, Optional
from numba import jit
from .particle import WIMP, Nucleus

# Physical constants
SPEED_OF_LIGHT = 299792458  # m/s
BOLTZMANN_CONSTANT = 8.617333262e-5  # eV/K
NUCLEON_MASS = 0.9315  # GeV/c²

@jit(nopython=True)
def maxwell_boltzmann_velocity(v_0: float = 220e3, v_esc: float = 544e3) -> np.ndarray:
    """
    Generate velocity vector from Maxwell-Boltzmann distribution.
    
    Args:
        v_0: Most probable velocity (m/s)
        v_esc: Galactic escape velocity (m/s)
        
    Returns:
        3D velocity vector (m/s)
    """
    while True:
        # Generate random velocity components
        v = np.random.normal(0, v_0, 3)
        v_mag = np.sqrt(np.sum(v**2))
        
        # Check if velocity is below escape velocity
        if v_mag < v_esc:
            return v

@jit(nopython=True)
def calculate_nuclear_form_factor(q: float, A: int) -> float:
    """
    Calculate nuclear form factor using Helm approximation.
    
    Args:
        q: Momentum transfer (fm^-1)
        A: Atomic mass number
        
    Returns:
        Form factor value
    """
    # Nuclear radius parameters
    R1 = 1.2 * A**(1/3)  # fm
    s = 0.9  # fm (surface thickness)
    R = np.sqrt(R1**2 - 5*s**2)  # fm
    
    # Helm form factor
    qR = q * R
    qs = q * s
    j1 = np.sin(qR) / (qR**2) - np.cos(qR) / qR  # Spherical Bessel function
    return 3 * j1 * np.exp(-0.5 * (qs)**2)

def calculate_recoil_energy(wimp: WIMP, nucleus: Nucleus, angle: float) -> float:
    """
    Calculate nuclear recoil energy from WIMP-nucleus collision.
    
    Args:
        wimp: WIMP particle
        nucleus: Target nucleus
        angle: Scattering angle (radians)
        
    Returns:
        Recoil energy (keV)
    """
    # Reduced mass
    mu = (wimp.mass * nucleus.mass) / (wimp.mass + nucleus.mass)
    
    # WIMP velocity magnitude
    v = np.sqrt(np.sum(wimp.velocity**2))
    
    # Calculate recoil energy
    E_r = (2 * mu**2 * v**2 * (1 - np.cos(angle))) / nucleus.mass
    
    return E_r  # keV

@jit(nopython=True)
def calculate_cross_section(E_r: float, A: int, sigma_0: float) -> float:
    """
    Calculate differential cross section.
    
    Args:
        E_r: Recoil energy (keV)
        A: Atomic mass number
        sigma_0: Zero-momentum WIMP-nucleon cross section (cm²)
        
    Returns:
        Differential cross section (cm²/keV)
    """
    # Convert recoil energy to momentum transfer
    q = np.sqrt(2 * E_r * A * NUCLEON_MASS)  # GeV/c
    
    # Calculate form factor
    F = calculate_nuclear_form_factor(q * 5.068, A)  # Convert q to fm^-1
    
    # A² scaling for coherent scattering
    sigma = sigma_0 * A**2 * F**2
    
    return sigma

def calculate_interaction_rate(wimp: WIMP, nucleus: Nucleus, detector_mass: float) -> float:
    """
    Calculate expected WIMP-nucleus interaction rate.
    
    Args:
        wimp: WIMP particle
        nucleus: Target nucleus
        detector_mass: Mass of detector material (kg)
        
    Returns:
        Interaction rate (events/day)
    """
    # Local dark matter density
    rho_dm = 0.3  # GeV/cm³
    
    # Number of target nuclei
    N_T = (detector_mass * 1000) / (nucleus.mass * 1.66e-27)  # Convert kg to g
    
    # Average velocity
    v_avg = np.sqrt(np.sum(wimp.velocity**2))
    
    # Calculate total interaction rate
    rate = (rho_dm * N_T * wimp.cross_section * v_avg) / wimp.mass
    
    return rate * 86400  # Convert to events/day

def generate_background(energy_range: Tuple[float, float], 
                       rate: float, 
                       exposure_time: float) -> np.ndarray:
    """
    Generate background events with exponential energy spectrum.
    
    Args:
        energy_range: (min_energy, max_energy) in keV
        rate: Background rate (events/kg/day)
        exposure_time: Exposure time (days)
        
    Returns:
        Array of background energies (keV)
    """
    n_events = np.random.poisson(rate * exposure_time)
    
    # Generate exponential distribution
    scale = (energy_range[1] - energy_range[0]) / 3  # Characteristic energy
    energies = np.random.exponential(scale, n_events)
    
    # Apply energy range limits
    mask = (energies >= energy_range[0]) & (energies <= energy_range[1])
    return energies[mask]

def apply_detector_response(energy: float, 
                          resolution: float, 
                          efficiency: float) -> Optional[float]:
    """
    Apply detector energy resolution and detection efficiency.
    
    Args:
        energy: True recoil energy (keV)
        resolution: Energy resolution (σ/E)
        efficiency: Detection efficiency (0-1)
        
    Returns:
        Measured energy or None if event is not detected
    """
    # Apply efficiency
    if np.random.random() > efficiency:
        return None
        
    # Apply energy resolution (Gaussian smearing)
    sigma = energy * resolution
    measured_energy = np.random.normal(energy, sigma)
    
    return max(0, measured_energy)  # Ensure non-negative energy