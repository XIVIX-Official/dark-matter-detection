"""
Tests for particle module.
"""
import pytest
import numpy as np
from datetime import datetime
from src.particle import Particle, WIMP, Nucleus, DetectionEvent, EventCollection

def test_particle_initialization():
    """Test particle base class initialization."""
    particle = Particle(
        mass=50.0,
        energy=10.0,
        position=[0, 0, 0],
        velocity=[100, 200, 300]
    )
    assert isinstance(particle.position, np.ndarray)
    assert isinstance(particle.velocity, np.ndarray)
    assert particle.mass == 50.0
    assert particle.energy == 10.0

def test_wimp_creation():
    """Test WIMP particle creation and methods."""
    wimp = WIMP(
        mass=50.0,
        energy=10.0,
        position=[0, 0, 0],
        velocity=[100, 200, 300],
        cross_section=1e-45
    )
    assert wimp.cross_section == 1e-45
    assert isinstance(wimp.get_kinetic_energy(), float)

def test_nucleus_creation():
    """Test nucleus creation."""
    nucleus = Nucleus(
        mass=131.0,
        energy=0.0,
        position=[0, 0, 0],
        velocity=[0, 0, 0],
        atomic_number=54,
        atomic_mass=131
    )
    assert nucleus.atomic_number == 54
    assert nucleus.atomic_mass == 131
    assert nucleus.form_factor == 1.0

def test_detection_event():
    """Test detection event creation and methods."""
    event = DetectionEvent(
        event_id=1,
        timestamp=datetime.now(),
        energy_deposited=5.0,
        position=np.array([0.1, 0.2, 0.3]),
        is_signal=True,
        detector_response=4.8,
        metadata={'test': 'data'}
    )
    event_dict = event.to_dict()
    assert event_dict['event_id'] == 1
    assert event_dict['energy_deposited'] == 5.0
    assert len(event_dict['position']) == 3
    assert event_dict['is_signal'] is True

def test_event_collection():
    """Test event collection methods."""
    collection = EventCollection()
    
    # Add some test events
    for i in range(10):
        event = DetectionEvent(
            event_id=i,
            timestamp=datetime.now(),
            energy_deposited=float(i),
            position=np.array([0, 0, 0]),
            is_signal=i % 2 == 0,
            detector_response=float(i),
            metadata={}
        )
        collection.add_event(event)
    
    # Test statistics
    stats = collection.get_statistics()
    assert stats['total_events'] == 10
    assert stats['dark_matter_candidates'] == 5
    assert stats['background_events'] == 5
    
    # Test energy spectrum
    spectrum = collection.get_energy_spectrum(bins=5)
    assert len(spectrum['bins']) == 6  # n+1 bin edges for n bins
    assert len(spectrum['counts']) == 5
    
    # Test temporal distribution
    temporal = collection.get_temporal_distribution(bins=5)
    assert len(temporal['times']) == 6
    assert len(temporal['counts']) == 5