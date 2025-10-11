# XIVIX: Dark Matter Detection Simulation

A sophisticated Monte Carlo simulation for detecting dark matter particles based on particle physics interactions. Features a modern web-based UI, robust physics engine, and REST API backend.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![React](https://img.shields.io/badge/React-18+-61dafb)
![License](https://img.shields.io/badge/License-MIT-purple)

## 🌌 Features

- **Advanced Physics Engine**: Simulates WIMP (Weakly Interacting Massive Particle) interactions
- **Monte Carlo Simulation**: Realistic statistical modeling of detector events
- **Real-time Analysis**: Live visualization of simulation results
- **Multiple Detector Types**: Superfluid Helium, Liquid Xenon, Germanium, Scintillator
- **Beautiful Dashboard**: Modern glassmorphic UI with dark theme
- **REST API**: Full-featured backend for programmatic access
- **Data Export**: Download results in JSON format

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)
- pip and npm package managers

### Installation

1. **Clone and setup backend**
```bash
git clone https://github.com/yourusername/dark-matter-detection.git
cd dark-matter-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Run backend server**
```bash
cd api
python app.py
```
Server runs on `http://localhost:5000`

3. **Run frontend**
```bash
# In a new terminal
npm install
npm run dev
```
Frontend runs on `http://localhost:5173` or `http://localhost:3000`

## 📖 Usage

### Web Interface

1. Open browser to frontend URL
2. Configure simulation parameters:
   - **Detector Type**: Choose detector technology
   - **Detector Mass**: Mass of detector material (0.1-1000 kg)
   - **Temperature**: Operating temperature (5-300 mK)
   - **Energy Threshold**: Minimum detectable energy (0.1-100 keV)
   - **Background Rate**: Expected background event rate
   - **Exposure Time**: Simulation duration (1-3650 days)
   - **Event Counts**: Number of background and dark matter events
3. Click "Simulate" to run simulation
4. View results in real-time visualization
5. Download results as JSON

### API Endpoints

**Start Simulation**
```bash
POST /api/simulate
Content-Type: application/json

{
  "detector_type": "superfluid_helium",
  "mass_kg": 1.0,
  "temperature_mk": 15,
  "energy_threshold_kev": 3.0,
  "background_rate": 0.01,
  "exposure_time_days": 365,
  "background_events": 1000,
  "dark_matter_events": 50
}
```

**Get Results**
```bash
GET /api/results
```

**Get Simulation History**
```bash
GET /api/history
```

**Get Configuration Parameters**
```bash
GET /api/parameters
```

**Calculate Statistics**
```bash
POST /api/statistics
Content-Type: application/json

{
  "signal_threshold": 3.0
}
```

**Export Data**
```bash
GET /api/export
```

## 📁 Project Structure

```
dark-matter-detection/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── config.py               # Configuration constants
├── src/
│   ├── __init__.py         # Package initialization
│   ├── particle.py         # Particle and Event classes
│   ├── physics.py          # Physics calculations engine
│   ├── detector.py         # Main detector simulation
│   └── monte_carlo.py      # Monte Carlo simulation logic (optional)
├── api/
│   ├── app.py              # Flask application
│   └── routes.py           # API endpoint routes
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # React main component
│   │   ├── components/     # Reusable components
│   │   └── styles/         # Tailwind CSS
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
└── tests/
    ├── test_particle.py
    ├── test_physics.py
    └── test_detector.py
```

## 🔬 Physics Model

### Dark Matter Interactions

XIVIX simulates Weakly Interacting Massive Particles (WIMPs) based on:

- **WIMP Mass**: ~50 GeV/c² (configurable)
- **Cross Section**: ~1×10⁻⁴⁵ cm² (spin-independent)
- **Velocity Distribution**: Maxwell-Boltzmann in galactic frame
- **Nuclear Recoil**: Kinematics from elastic scattering

### Detection Mechanisms

1. **Nuclear Recoil**: WIMP collides with nucleus, causing recoil
2. **Ionization**: Recoil creates electron-ion pairs
3. **Scintillation**: Excitation produces photons
4. **Phonons**: Heat generation in cryogenic detectors

### Statistical Analysis

- Energy-dependent efficiency curves
- Background rejection algorithms
- Significance calculation (σ levels)
- Discovery potential assessment

## 🎨 Visualization Dashboard

The React-based dashboard includes:

- **Energy Spectrum**: Histogram of detected energies
- **Event Distribution**: Pie chart of signal vs background
- **Temporal Analysis**: Events over simulation time
- **Statistical Cards**: Key metrics at a glance
- **Real-time Updates**: Live progress tracking
- **Export Functionality**: Download raw data

## 📊 Simulation Parameters

### Detector Configurations

| Type | Threshold | Resolution | Background Rate | Efficiency |
|------|-----------|------------|-----------------|-----------|
| Superfluid He-3 | 3 keV | 3% | 0.01/kg/d | 85% |
| Liquid Xenon | 5 keV | 5% | 0.005/kg/d | 90% |
| Germanium | 1 keV | 2% | 0.02/kg/d | 80% |
| Scintillator | 10 keV | 10% | 0.05/kg/d | 70% |

### Physical Constants

```python
WIMP_MASS = 50.0  # GeV/c²
WIMP_CROSS_SECTION = 1e-45  # cm²
EARTH_VELOCITY = 230e3  # m/s
IONIZATION_ENERGY = 13.6 meV  # per e⁻-ion pair
```

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_detector.py -v
```

## 📚 Physics References

- WIMP scattering: Goodman & Witten (1985)
- Nuclear recoil: Lindhard theory
- Quenching factors: Experimentally measured values
- Background models: Published limits from XENON, LUX, SuperCDMS

## 🔧 Configuration

Edit `config.py` to customize:

```python
# WIMP Parameters
WIMP_MASS_GEV = 50.0
WIMP_CROSS_SECTION_CM2 = 1e-45

# Detector Settings
DEFAULT_DETECTOR_MASS_KG = 1.0
DEFAULT_TEMPERATURE_MK = 15

# Simulation
MONTE_CARLO_ITERATIONS = 10000
SIGNIFICANCE_THRESHOLD = 3.0
```

## 🌐 API Response Examples

### Successful Simulation Response

```json
{
  "simulation_id": 1,
  "status": "completed",
  "timestamp": "2025-10-11T12:34:56.789Z",
  "statistics": {
    "total_events": 1050,
    "dark_matter_candidates": 47,
    "background_events": 1003,
    "mean_energy": 25.3,
    "max_energy": 892.5,
    "min_energy": 3.1,
    "total_exposure": 365.0,
    "detector_efficiency": 0.94
  },
  "energy_spectrum": {
    "bins": [3.0, 20.5, 38.0, ...],
    "counts": [145, 128, 89, ...]
  },
  "temporal_distribution": {
    "times": [0, 86400, 172800, ...],
    "counts": [3, 4, 2, ...]
  },
  "detector_config": {
    "mass_kg": 1.0,
    "temperature_mk": 15,
    "threshold_kev": 3.0,
    "exposure_time_days": 365
  }
}
```

## 🚀 Performance

- Single simulation: ~100-500ms
- Background event generation: O(n)
- Statistical analysis: O(n log n)
- Visualization rendering: <50ms on modern browsers

## ⚙️ Troubleshooting

**Frontend won't connect to backend**
- Ensure Flask server running on localhost:5000
- Check CORS is enabled in `app.py`
- Clear browser cache and reload

**Simulation returns errors**
- Verify parameter ranges in config
- Check Python version ≥ 3.8
- Ensure numpy/scipy installed: `pip install --upgrade numpy scipy`

**Charts not displaying**
- Verify data returned from API
- Check browser console for errors
- Ensure Recharts installed: `npm install recharts`

## 📝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/NewFeature`
3. Commit changes: `git commit -m 'Add NewFeature'`
4. Push to branch: `git push origin feature/NewFeature`
5. Submit Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## ✔️ Acknowledgments

- Physics models based on peer-reviewed literature
- UI inspired by modern data visualization dashboards
- Detector specifications from XENON, LUX, and SuperCDMS collaborations

## 📞 Support

For issues, questions, or suggestions:
- Open an GitHub Issue
- Submit Pull Request with improvements
- Contact: info@codexustechnologies.com

## 🛠️ Future Enhancements

- [ ] 3D particle trajectory visualization
- [ ] Multi-detector comparison
- [ ] Machine learning background rejection
- [ ] Real dark matter detector data integration
- [ ] Advanced statistical analysis tools
- [ ] GPU-accelerated simulations
- [ ] Docker containerization
- [ ] Mobile responsive improvements

---

**Powered by XIVIX**

*Advancing dark matter detection through simulation and visualization*