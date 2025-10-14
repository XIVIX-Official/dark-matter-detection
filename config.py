"""
Configuration constants for the XIVIX dark matter detection simulation.
"""

# Physical Constants
WIMP_MASS_GEV = 50.0  # GeV/c²
WIMP_CROSS_SECTION_CM2 = 1e-45  # cm²
EARTH_VELOCITY = 230e3  # m/s
IONIZATION_ENERGY = 13.6e-3  # eV per e⁻-ion pair

# Detector Settings
DEFAULT_DETECTOR_MASS_KG = 1.0
DEFAULT_TEMPERATURE_MK = 15
DEFAULT_ENERGY_THRESHOLD_KEV = 3.0
DEFAULT_EXPOSURE_TIME_DAYS = 365

# Detector Types Configuration
DETECTOR_CONFIGS = {
    'superfluid_helium': {
        'threshold_kev': 3.0,
        'resolution': 0.03,
        'background_rate': 0.01,
        'efficiency': 0.85
    },
    'liquid_xenon': {
        'threshold_kev': 5.0,
        'resolution': 0.05,
        'background_rate': 0.005,
        'efficiency': 0.90
    },
    'germanium': {
        'threshold_kev': 1.0,
        'resolution': 0.02,
        'background_rate': 0.02,
        'efficiency': 0.80
    },
    'scintillator': {
        'threshold_kev': 10.0,
        'resolution': 0.10,
        'background_rate': 0.05,
        'efficiency': 0.70
    }
}

# Simulation Parameters
MONTE_CARLO_ITERATIONS = 10000
SIGNIFICANCE_THRESHOLD = 3.0
MAX_EVENTS = 100000
MIN_EVENTS = 10

# Statistical Analysis
CONFIDENCE_LEVEL = 0.95
ENERGY_BINS = 100
TIME_BINS = 50

# API Configuration
API_HOST = '0.0.0.0'
API_PORT = 5000
CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']

# File Export Settings
EXPORT_FORMATS = ['json', 'csv']
MAX_EXPORT_SIZE = 1000000  # 1MB