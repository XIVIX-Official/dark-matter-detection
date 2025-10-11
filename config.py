"""
XIVIX Configuration Constants
This file contains all configuration parameters for the dark matter detection simulation
"""

# ============================================================================
# PHYSICAL CONSTANTS (SI units)
# ============================================================================
SPEED_OF_LIGHT = 3e8  # m/s
PLANCK_CONSTANT = 6.626e-34  # J·s
REDUCED_PLANCK = 1.055e-34  # J·s
ELEMENTARY_CHARGE = 1.602e-19  # C
BOLTZMANN_CONSTANT = 1.381e-23  # J/K

# ============================================================================
# DARK MATTER PARAMETERS
# ============================================================================
WIMP_MASS_GEV = 50.0  # GeV/c^2 - Typical WIMP mass
WIMP_CROSS_SECTION_CM2 = 1e-45  # cm^2 - WIMP-nucleon cross section
GALACTIC_HALO_DENSITY = 0.3  # GeV/cm^3 - Local dark matter density
EARTH_VELOCITY = 230e3  # m/s - Velocity in galactic frame
SUN_VELOCITY = 220e3  # m/s - Sun's velocity relative to galactic center
LOCAL_VELOCITY_DISPERSION = 155e3  # m/s - Velocity dispersion

# ============================================================================
# DETECTOR TYPES AND SPECIFICATIONS
# ============================================================================
DETECTOR_TYPES = {
    'superfluid_helium': {
        'threshold_kev': 3.0,
        'energy_resolution': 0.03,  # 3%
        'background_rate_per_kg_day': 0.01,
        'efficiency_plateau': 0.85,
        'temperature_mk': 15,
        'operating_description': 'Superfluid Helium-3 cryogenic detector'
    },
    'liquid_xenon': {
        'threshold_kev': 5.0,
        'energy_resolution': 0.05,  # 5%
        'background_rate_per_kg_day': 0.005,
        'efficiency_plateau': 0.90,
        'temperature_mk': 184,
        'operating_description': 'Liquid Xenon time projection chamber'
    },
    'germanium': {
        'threshold_kev': 1.0,
        'energy_resolution': 0.02,  # 2%
        'background_rate_per_kg_day': 0.02,
        'efficiency_plateau': 0.80,
        'temperature_mk': 77,
        'operating_description': 'Cryogenic germanium detector'
    },
    'scintillator': {
        'threshold_kev': 10.0,
        'energy_resolution': 0.10,  # 10%
        'background_rate_per_kg_day': 0.05,
        'efficiency_plateau': 0.70,
        'temperature_mk': 293,
        'operating_description': 'Scintillation detector'
    }
}

# ============================================================================
# ENERGY SCALES (in keV)
# ============================================================================
IONIZATION_ENERGY_KEV = 13.6e-3  # keV per electron-ion pair
SCINTILLATION_PHOTON_ENERGY_KEV = 7.0  # keV per photon
RECOIL_THRESHOLD_KEV = 3.0  # Minimum detectable nuclear recoil

# ============================================================================
# STATISTICAL PARAMETERS
# ============================================================================
DEFAULT_EXPOSURE_DAYS = 365  # days
DEFAULT_DETECTOR_MASS_KG = 1.0  # kg
DEFAULT_TEMPERATURE_MK = 15  # milliKelvin
SIGNIFICANCE_THRESHOLD = 3.0  # 3-sigma detection threshold
CONFIDENCE_LEVEL = 0.9545  # 2-sigma (95.45%)

# ============================================================================
# MONTE CARLO SIMULATION PARAMETERS
# ============================================================================
MONTE_CARLO_ITERATIONS = 10000
RANDOM_SEED = None  # Set to integer for reproducibility (e.g., 42)
VELOCITY_DISTRIBUTION = 'maxwell_boltzmann'
ANGULAR_DISTRIBUTION = 'isotropic'

# ============================================================================
# BACKGROUND MODELS
# ============================================================================
BACKGROUND_SOURCES = {
    'radioactive_decay': 0.3,  # fraction
    'cosmic_rays': 0.4,  # fraction
    'neutron_activation': 0.2,  # fraction
    'other': 0.1  # fraction
}

# ============================================================================
# API CONFIGURATION
# ============================================================================
API_HOST = '0.0.0.0'
API_PORT = 5000
API_DEBUG = True
API_CORS_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173'
]

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'xivix_simulation.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ============================================================================
# FRONTEND CONFIGURATION
# ============================================================================
FRONTEND_API_URL = 'http://localhost:5000'
FRONTEND_APP_NAME = 'XIVIX'
FRONTEND_APP_VERSION = '1.0.0'
ENABLE_EXPORT = True
ENABLE_HISTORY = True

# ============================================================================
# PHYSICS CONSTANTS - PARTICLE MASSES (GeV/c^2)
# ============================================================================
PARTICLE_MASSES = {
    'electron': 0.511e-3,
    'muon': 105.7e-3,
    'tau': 1.777,
    'proton': 0.938,
    'neutron': 0.940,
    'wimp': WIMP_MASS_GEV
}

# ============================================================================
# QUENCHING FACTORS - Scintillation efficiency
# ============================================================================
QUENCHING_FACTORS = {
    'electron_recoil': 1.0,  # Reference
    'nuclear_recoil': 0.3,  # Lindhard theory
    'alpha_particle': 0.05,
    'helium_nucleus': 0.08
}

# ============================================================================
# EFFICIENCY CURVES
# ============================================================================
EFFICIENCY_THRESHOLDS = {
    'low': 3.0,  # keV
    'mid': 10.0,  # keV
    'high': 50.0  # keV
}

# ============================================================================
# VALIDATION RANGES
# ============================================================================
PARAMETER_RANGES = {
    'mass_kg': {'min': 0.01, 'max': 10000.0},
    'temperature_mk': {'min': 5, 'max': 300},
    'energy_threshold_kev': {'min': 0.1, 'max': 100},
    'background_rate': {'min': 0.0001, 'max': 1.0},
    'exposure_time_days': {'min': 1, 'max': 3650},
    'background_events': {'min': 10, 'max': 50000},
    'dark_matter_events': {'min': 1, 'max': 1000}
}

# ============================================================================
# FILE PATHS
# ============================================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')

# Create directories if they don't exist
import os
for directory in [DATA_DIR, RESULTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# ============================================================================
# ADVANCED PHYSICS OPTIONS
# ============================================================================
USE_LINDHARD_QUENCHING = True
INCLUDE_CHANNELING = False
INCLUDE_DIRECTIONAL_INFO = False
INCLUDE_TIME_DEPENDENCE = False

# ============================================================================
# SUMMARY
# ============================================================================
"""
Configuration Summary:
- WIMP Mass: {} GeV/c^2
- Cross Section: {} cm^2
- Primary Detectors: {}
- Default Exposure: {} days
- Significance Threshold: {}σ
""".format(
    WIMP_MASS_GEV,
    WIMP_CROSS_SECTION_CM2,
    ', '.join(DETECTOR_TYPES.keys()),
    DEFAULT_EXPOSURE_DAYS,
    SIGNIFICANCE_THRESHOLD
)
