import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.detector import Detector, DetectorConfig
from src.particle import ParticleType


class TestDetectorConfig:
    """Test DetectorConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = DetectorConfig()
        
        assert config.detector_type == "superfluid_helium"
        assert config.mass_kg == 1.0
        assert config.temperature_mk == 15.0
        assert config.energy_threshold_kev == 3.0
        
    def test_custom_config(self):
        """Test custom configuration"""
        config = DetectorConfig(
            detector_type="liquid_xenon",
            mass_kg=5.0,
            temperature_mk=180.0,
            energy_threshold_kev=5.0
        )
        
        assert config.detector_type == "liquid_xenon"
        assert config.mass_kg == 5.0
        assert config.temperature_mk == 180.0


class TestDetector:
    """Test Detector simulation"""
    
    def test_detector_initialization(self):
        """Test detector creation with default config"""
        detector = Detector()
        
        assert detector.config is not None
        assert len(detector.events) == 0
        assert detector.event_counter == 0
        
    def test_detector_custom_initialization(self):
        """Test detector creation with custom config"""
        config = DetectorConfig(mass_kg=2.0)
        detector = Detector(config)
        
        assert detector.config.mass_kg == 2.0
        
    def test_background_event_generation(self):
        """Test background event generation"""
        detector = Detector()
        bg_particles = detector.generate_background_events(num_events=100)
        
        assert len(bg_particles) == 100
        
        for particle in bg_particles:
            assert particle.particle_type in [ParticleType.BACKGROUND, ParticleType.COSMIC_RAY]
            assert particle.energy >= detector.config.energy_threshold_kev
            
    def test_dark_matter_event_generation(self):
        """Test dark matter event generation"""
        detector = Detector()
        dm_particles = detector.generate_dark_matter_events(num_events=50)
        
        # Some may be filtered by efficiency
        assert 0 <= len(dm_particles) <= 50
        
        for particle in dm_particles:
            assert particle.particle_type == ParticleType.DARK_MATTER
            assert particle.energy >= detector.config.energy_threshold_kev
            
    def test_event_processing(self):
        """Test single event processing"""
        from src.particle import Particle
        
        detector = Detector()
        particle = Particle(
            particle_type=ParticleType.DARK_MATTER,
            energy=50.0,
            momentum=np.array([5.0, 5.0, 5.0]),
            position=np.array([0.0, 0.0, 0.0]),
            timestamp=0.0,
            interaction_type="nuclear_recoil"
        )
        
        event = detector.process_event(particle)
        
        assert event.event_id == 1
        assert event.total_energy == 50.0
        assert len(detector.events) == 1
        assert detector.event_counter == 1
        
    def test_full_simulation_short(self):
        """Test complete simulation with few events"""
        config = DetectorConfig(mass_kg=0.5, exposure_time_days=10)
        detector = Detector(config)
        
        stats = detector.run_simulation(
            background_events=50,
            dark_matter_events=5
        )
        
        assert 'total_events' in stats
        assert 'dark_matter_candidates' in stats
        assert 'background_events' in stats
        assert stats['total_events'] > 0
        assert 0 <= stats['detector_efficiency'] <= 1
        
    def test_full_simulation_standard(self):
        """Test complete simulation with standard parameters"""
        config = DetectorConfig()
        detector = Detector(config)
        
        stats = detector.run_simulation(
            background_events=200,
            dark_matter_events=20
        )
        
        assert stats['total_events'] > 0
        assert stats['dark_matter_candidates'] + stats['background_events'] == stats['total_events']
        
    def test_energy_spectrum(self):
        """Test energy spectrum calculation"""
        detector = Detector()
        detector.run_simulation(background_events=50, dark_matter_events=5)
        
        spectrum = detector.get_energy_spectrum()
        
        assert 'bins' in spectrum
        assert 'counts' in spectrum
        assert len(spectrum['bins']) > 0
        assert len(spectrum['counts']) > 0
        assert len(spectrum['bins']) == len(spectrum['counts']) + 1
        
    def test_temporal_distribution(self):
        """Test temporal distribution calculation"""
        detector = Detector()
        detector.run_simulation(background_events=50, dark_matter_events=5)
        
        temporal = detector.get_temporal_distribution()
        
        assert 'times' in temporal
        assert 'counts' in temporal
        assert len(temporal['times']) > 0
        assert len(temporal['counts']) > 0
        
    def test_empty_spectrum(self):
        """Test spectrum with no events"""
        detector = Detector()
        spectrum = detector.get_energy_spectrum()
        
        assert spectrum['bins'] == []
        assert spectrum['counts'] == []
        
    def test_empty_temporal(self):
        """Test temporal with no events"""
        detector = Detector()
        temporal = detector.get_temporal_distribution()
        
        assert temporal['times'] == []
        assert temporal['counts'] == []


class TestIntegration:
    """Integration tests"""
    
    def test_full_pipeline(self):
        """Test complete pipeline from config to analysis"""
        config = DetectorConfig(
            detector_type="superfluid_helium",
            mass_kg=1.0,
            energy_threshold_kev=3.0,
            exposure_time_days=100
        )
        
        detector = Detector(config)
        stats = detector.run_simulation(
            background_events=300,
            dark_matter_events=30
        )
        
        # Verify statistics
        assert stats['total_events'] > 0
        assert stats['dark_matter_candidates'] >= 0
        assert stats['background_events'] >= 0
        assert 0 <= stats['detector_efficiency'] <= 1
        
        # Verify data products
        spectrum = detector.get_energy_spectrum()
        assert len(spectrum['counts']) > 0
        
        temporal = detector.get_temporal_distribution()
        assert len(temporal['counts']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
    