"""
Tests for physics module.
"""
import pytest
import numpy as np
from src.physics import (
    maxwell_boltzmann_velocity,
    calculate_nuclear_form_factor,
    calculate_recoil_energy,
    calculate_cross_section,
    generate_background,
    apply_detector_response
)
from src.particle import WIMP, Nucleus

def test_maxwell_boltzmann_velocity():
    """Test Maxwell-Boltzmann velocity distribution."""
    v = maxwell_boltzmann_velocity()
    assert isinstance(v, np.ndarray)
    assert len(v) == 3
    assert np.all(np.isfinite(v))
    
    # Test velocity magnitude is reasonable
    v_mag = np.sqrt(np.sum(v**2))
    assert 0 < v_mag < 544e3  # Below escape velocity

def test_nuclear_form_factor():
    """Test nuclear form factor calculation."""
    q = 1.0  # fm^-1
    A = 131  # Xenon
    F = calculate_nuclear_form_factor(q, A)
    assert isinstance(F, float)
    assert 0 <= F <= 1  # Form factor should be between 0 and 1

def test_recoil_energy():
    """Test recoil energy calculation."""
    wimp = WIMP(
        mass=50.0,
        energy=0.0,
        position=np.zeros(3),
        velocity=np.array([220e3, 0, 0]),
        cross_section=1e-45
    )
    
    nucleus = Nucleus(
        mass=131.0,
        energy=0.0,
        position=np.zeros(3),
        velocity=np.zeros(3),
        atomic_number=54,
        atomic_mass=131
    )
    
    E_r = calculate_recoil_energy(wimp, nucleus, np.pi/2)
    assert isinstance(E_r, float)
    assert E_r >= 0  # Recoil energy should be positive

def test_cross_section():
    """Test cross section calculation."""
    E_r = 10.0  # keV
    A = 131    # Xenon
    sigma_0 = 1e-45  # cm²
    
    sigma = calculate_cross_section(E_r, A, sigma_0)
    assert isinstance(sigma, float)
    assert sigma > 0  # Cross section should be positive

def test_background_generation():
    """Test background event generation."""
    energy_range = (0, 100)  # keV
    rate = 0.01  # events/kg/day
    exposure_time = 365  # days
    
    energies = generate_background(energy_range, rate, exposure_time)
    assert isinstance(energies, np.ndarray)
    assert np.all(energies >= energy_range[0])
    assert np.all(energies <= energy_range[1])

def test_detector_response():
    """Test detector response function."""
    energy = 10.0  # keV
    resolution = 0.1  # 10% resolution
    efficiency = 0.9  # 90% efficiency
    
    # Test with detection
    np.random.seed(42)  # For reproducibility
    E_detected = apply_detector_response(energy, resolution, efficiency)
    assert isinstance(E_detected, (float, type(None)))
    
    if E_detected is not None:
        assert E_detected >= 0  # Measured energy should be non-negative
        
    # Test with no detection (force efficiency = 0)
    E_not_detected = apply_detector_response(energy, resolution, 0.0)
    assert E_not_detected is None