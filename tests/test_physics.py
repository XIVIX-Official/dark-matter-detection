import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.physics import PhysicsEngine
from src.particle import ParticleType


class TestPhysicsEngine:
    """Test Physics Engine calculations"""
    
    def test_engine_initialization(self):
        """Test physics engine creation"""
        engine = PhysicsEngine()
        assert engine.interaction_count == 0
        assert engine.total_energy_deposited == 0.0
        assert engine.WIMP_MASS == 50.0
        
    def test_interaction_probability(self):
        """Test WIMP interaction probability calculation"""
        engine = PhysicsEngine()
        
        # Test at various velocities
        prob_low = engine.calculate_interaction_probability(100e3)
        prob_high = engine.calculate_interaction_probability(300e3)
        
        assert 0 <= prob_low <= 1.0
        assert 0 <= prob_high <= 1.0
        # Higher velocity should give lower probability
        assert prob_low >= prob_high
        
    def test_nuclear_recoil_energy(self):
        """Test nuclear recoil energy calculation"""
        engine = PhysicsEngine()
        
        recoil = engine.nuclear_recoil_energy(
            wimp_mass=50.0,
            nucleus_mass=20.0,
            wimp_velocity=200e3
        )
        
        assert recoil >= 0
        assert isinstance(recoil, float)
        
    def test_quenching_factor_dark_matter(self):
        """Test quenching factor for dark matter"""
        engine = PhysicsEngine()
        
        quench = engine.quenching_factor(50.0, ParticleType.DARK_MATTER)
        assert 0 <= quench <= 1.0
        
    def test_quenching_factor_background(self):
        """Test quenching factor for background"""
        engine = PhysicsEngine()
        
        quench = engine.quenching_factor(50.0, ParticleType.BACKGROUND)
        assert quench == 1.0
        
    def test_scattering_angle(self):
        """Test random scattering angle generation"""
        engine = PhysicsEngine()
        
        # Generate multiple angles
        for _ in range(100):
            angle = engine.scattering_angle()
            assert 0 <= angle <= np.pi
            
    def test_ionization_tracks(self):
        """Test ionization track estimation"""
        engine = PhysicsEngine()
        
        tracks_low = engine.ionization_tracks(energy_deposited=10.0)
        tracks_high = engine.ionization_tracks(energy_deposited=100.0)
        
        assert tracks_low > 0
        assert tracks_high > tracks_low
        assert isinstance(tracks_low, int)
        
    def test_electron_recoil_equivalent(self):
        """Test electron recoil equivalent calculation"""
        engine = PhysicsEngine()
        
        ere = engine.electron_recoil_equivalent(100.0, 0.5)
        assert ere == pytest.approx(50.0)
        
    def test_detector_efficiency_below_threshold(self):
        """Test detector efficiency below threshold"""
        engine = PhysicsEngine()
        
        eff = engine.detector_efficiency(1.0)
        assert eff == 0.0
        
    def test_detector_efficiency_above_threshold(self):
        """Test detector efficiency above threshold"""
        engine = PhysicsEngine()
        
        eff_mid = engine.detector_efficiency(5.0)
        eff_high = engine.detector_efficiency(100.0)
        
        assert 0 < eff_mid < 1.0
        assert eff_high > eff_mid
        
    def test_background_rate(self):
        """Test background rate calculation"""
        engine = PhysicsEngine()
        
        rate = engine.background_rate(energy=10.0, detector_mass_kg=1.0)
        assert rate > 0
        
        # More massive detector should have higher rate
        rate_heavy = engine.background_rate(energy=10.0, detector_mass_kg=10.0)
        assert rate_heavy > rate
        
    def test_statistical_significance(self):
        """Test significance calculation"""
        engine = PhysicsEngine()
        
        sig1 = engine.statistical_significance(signal_events=100, background_events=10)
        sig2 = engine.statistical_significance(signal_events=10, background_events=100)
        sig3 = engine.statistical_significance(signal_events=0, background_events=100)
        
        assert sig1 > sig2
        assert sig3 == 0
        assert sig1 > 0
        
    def test_statistical_significance_zero_background(self):
        """Test significance with zero background"""
        engine = PhysicsEngine()
        
        sig = engine.statistical_significance(signal_events=10, background_events=0)
        assert sig == float('inf')
        
    def test_interaction_cascade(self):
        """Test interaction cascade simulation"""
        engine = PhysicsEngine()
        
        cascade = engine.simulate_interaction_cascade(initial_energy=50.0)
        
        assert 'primary_recoil' in cascade
        assert 'secondary_ionizations' in cascade
        assert 'photon_production' in cascade
        assert 'heat_generated' in cascade
        
        assert cascade['primary_recoil'] == 50.0
        assert cascade['secondary_ionizations'] > 0
        assert cascade['heat_generated'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])