"""
Tests for detector module.
"""
import pytest
import numpy as np
from src.detector import Detector
import config

def test_detector_initialization():
    """Test detector initialization."""
    detector = Detector(
        detector_type='superfluid_helium',
        mass_kg=1.0,
        temperature_mk=15
    )
    assert detector.type == 'superfluid_helium'
    assert detector.mass == 1.0
    assert detector.temperature == 15
    assert detector.config == config.DETECTOR_CONFIGS['superfluid_helium']

def test_invalid_detector_type():
    """Test initialization with invalid detector type."""
    with pytest.raises(ValueError):
        Detector('invalid_type', 1.0, 15)

def test_target_nucleus():
    """Test target nucleus creation."""
    detector = Detector('liquid_xenon', 1.0, 15)
    nucleus = detector.get_target_nucleus()
    assert nucleus.atomic_number == 54  # Xenon
    assert nucleus.atomic_mass == 131

def test_wimp_event_simulation():
    """Test WIMP event simulation."""
    detector = Detector('germanium', 1.0, 15)
    
    # Create test WIMP
    from src.particle import WIMP
    wimp = WIMP(
        mass=config.WIMP_MASS_GEV,
        energy=0,
        position=np.zeros(3),
        velocity=np.array([220e3, 0, 0]),
        cross_section=config.WIMP_CROSS_SECTION_CM2
    )
    
    # Simulate event
    event = detector.simulate_wimp_event(wimp)
    
    # Event might be None if not detected
    if event is not None:
        assert event.is_signal
        assert event.energy_deposited > 0
        assert event.detector_response >= detector.config['threshold_kev']

def test_background_event_simulation():
    """Test background event simulation."""
    detector = Detector('scintillator', 1.0, 15)
    from datetime import datetime
    
    event = detector.simulate_background_event(datetime.now())
    assert not event.is_signal
    assert event.energy_deposited > 0
    assert isinstance(event.position, np.ndarray)
    assert len(event.position) == 3

def test_full_simulation():
    """Test full detector simulation."""
    detector = Detector('superfluid_helium', 1.0, 15)
    
    events = detector.run_simulation(
        exposure_time_days=1,
        n_wimp_events=10,
        n_background_events=100
    )
    
    # Check results format
    results = detector.get_results()
    assert 'detector_config' in results
    assert 'statistics' in results
    assert 'energy_spectrum' in results
    assert 'temporal_distribution' in results
    
    # Check statistics
    stats = results['statistics']
    assert stats['total_events'] > 0
    assert stats['background_events'] <= 100  # Some might not be detected
    assert stats['dark_matter_candidates'] <= 10  # Some might not be detected

def test_detector_statistics():
    """Test detector statistics calculation."""
    detector = Detector('liquid_xenon', 1.0, 15)
    
    # Run a short simulation
    detector.run_simulation(1, 5, 50)
    
    # Get results
    results = detector.get_results()
    stats = results['statistics']
    
    # Check statistics types and ranges
    assert isinstance(stats['total_events'], int)
    assert isinstance(stats['mean_energy'], float)
    assert stats['min_energy'] <= stats['mean_energy'] <= stats['max_energy']
    assert stats['background_events'] + stats['dark_matter_candidates'] == stats['total_events']