import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.particle import Particle, ParticleType, Event


class TestParticle:
    """Test Particle class"""
    
    def test_particle_creation(self):
        """Test basic particle creation"""
        particle = Particle(
            particle_type=ParticleType.DARK_MATTER,
            energy=50.0,
            momentum=np.array([1.0, 2.0, 3.0]),
            position=np.array([0.0, 0.0, 0.0]),
            timestamp=0.0,
            interaction_type="nuclear_recoil"
        )
        assert particle.energy == 50.0
        assert particle.mass == 50.0
        assert particle.particle_type == ParticleType.DARK_MATTER
        
    def test_particle_mass_assignment(self):
        """Test mass assignment by particle type"""
        dm_particle = Particle(
            particle_type=ParticleType.DARK_MATTER,
            energy=50.0,
            momentum=np.array([1.0, 0.0, 0.0]),
            position=np.array([0.0, 0.0, 0.0]),
            timestamp=0.0,
            interaction_type="nuclear_recoil"
        )
        
        bg_particle = Particle(
            particle_type=ParticleType.BACKGROUND,
            energy=10.0,
            momentum=np.array([1.0, 0.0, 0.0]),
            position=np.array([0.0, 0.0, 0.0]),
            timestamp=0.0,
            interaction_type="background"
        )
        
        assert dm_particle.mass == 50.0
        assert bg_particle.mass == 0.511
        
    def test_kinetic_energy_calculation(self):
        """Test kinetic energy calculation"""
        particle = Particle(
            particle_type=ParticleType.DARK_MATTER,
            energy=100.0,
            momentum=np.array([10.0, 0.0, 0.0]),
            position=np.array([0.0, 0.0, 0.0]),
            timestamp=0.0,
            interaction_type="nuclear_recoil"
        )
        ke = particle.get_kinetic_energy()
        assert ke >= 0
        assert isinstance(ke, float)
        
    def test_ionization_loss(self):
        """Test energy loss due to ionization"""
        particle = Particle(
            particle_type=ParticleType.DARK_MATTER,
            energy=50.0,
            momentum=np.array([1.0, 2.0, 3.0]),
            position=np.array([0.0, 0.0, 0.0]),
            timestamp=0.0,
            interaction_type="nuclear_recoil"
        )
        loss = particle.ionization_loss(distance=1.0)
        assert 0 <= loss <= 50.0
        assert loss == pytest.approx(0.05, rel=0.1)
        
    def test_ionization_loss_low_energy(self):
        """Test that low energy particles have no ionization loss"""
        particle = Particle(
            particle_type=ParticleType.NEUTRINO,
            energy=0.01,
            momentum=np.array([0.0, 0.0, 0.0]),
            position=np.array([0.0, 0.0, 0.0]),
            timestamp=0.0,
            interaction_type="background"
        )
        loss = particle.ionization_loss(distance=10.0)
        assert loss == 0


class TestEvent:
    """Test Event class"""
    
    def test_event_creation(self):
        """Test event creation"""
        particle = Particle(
            particle_type=ParticleType.DARK_MATTER,
            energy=50.0,
            momentum=np.array([1.0, 0.0, 0.0]),
            position=np.array([0.0, 0.0, 0.0]),
            timestamp=100.0,
            interaction_type="nuclear_recoil"
        )
        
        event = Event(
            event_id=1,
            particles=[particle],
            total_energy=50.0,
            timestamp=100.0,
            detector_hit_count=100,
            significance=3.5,
            background_probability=0.1
        )
        
        assert event.event_id == 1
        assert event.total_energy == 50.0
        assert event.significance == 3.5
        assert len(event.particles) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])