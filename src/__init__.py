"""
Package initialization for dark matter detection simulation.
"""
from .particle import Particle, WIMP, Nucleus, DetectionEvent, EventCollection
from .physics import (
    maxwell_boltzmann_velocity,
    calculate_nuclear_form_factor,
    calculate_recoil_energy,
    calculate_cross_section,
    calculate_interaction_rate,
    generate_background,
    apply_detector_response
)
from .detector import Detector

__version__ = '0.1.0'
__author__ = 'XIVIX Team'

__all__ = [
    'Particle',
    'WIMP',
    'Nucleus',
    'DetectionEvent',
    'EventCollection',
    'Detector',
    'maxwell_boltzmann_velocity',
    'calculate_nuclear_form_factor',
    'calculate_recoil_energy',
    'calculate_cross_section',
    'calculate_interaction_rate',
    'generate_background',
    'apply_detector_response'
]