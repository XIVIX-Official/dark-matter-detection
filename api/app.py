"""
XIVIX Dark Matter Detection API
Flask REST API for detector simulation
Run: python app.py
Access: http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.detector import Detector, DetectorConfig

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Global simulation state
simulation_state = {
    'active': False,
    'progress': 0,
    'current_sim': None,
    'history': []
}


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/simulate', methods=['POST'])
def start_simulation():
    """Start a new simulation with parameters"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Create detector configuration
        config = DetectorConfig(
            detector_type=str(data.get('detector_type', 'superfluid_helium')),
            mass_kg=float(data.get('mass_kg', 1.0)),
            temperature_mk=float(data.get('temperature_mk', 15.0)),
            energy_threshold_kev=float(data.get('energy_threshold_kev', 3.0)),
            background_rate_per_kg_day=float(data.get('background_rate', 0.01)),
            exposure_time_days=float(data.get('exposure_time_days', 365.0))
        )
        
        # Get simulation parameters
        background_events = int(data.get('background_events', 1000))
        dark_matter_events = int(data.get('dark_matter_events', 50))
        
        # Validate parameter ranges
        if background_events < 10 or background_events > 50000:
            return jsonify({'error': 'background_events must be between 10 and 50000'}), 400
        
        if dark_matter_events < 1 or dark_matter_events > 1000:
            return jsonify({'error': 'dark_matter_events must be between 1 and 1000'}), 400
        
        if config.mass_kg < 0.01 or config.mass_kg > 10000:
            return jsonify({'error': 'mass_kg must be between 0.01 and 10000'}), 400
        
        # Create detector and run simulation
        detector = Detector(config)
        results = detector.run_simulation(background_events, dark_matter_events)
        
        # Get additional data products
        spectrum = detector.get_energy_spectrum()
        temporal = detector.get_temporal_distribution()
        
        # Compile response
        response = {
            'simulation_id': len(simulation_state['history']) + 1,
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'statistics': {
                'total_events': results['total_events'],
                'dark_matter_candidates': results['dark_matter_candidates'],
                'background_events': results['background_events'],
                'mean_energy': round(results['mean_energy'], 2),
                'max_energy': round(results['max_energy'], 2),
                'min_energy': round(results['min_energy'], 2),
                'total_exposure': round(results['total_exposure'], 2),
                'detector_efficiency': round(results['detector_efficiency'], 4)
            },
            'energy_spectrum': {
                'bins': spectrum['bins'],
                'counts': spectrum['counts']
            },
            'temporal_distribution': {
                'times': temporal['times'],
                'counts': temporal['counts']
            },
            'detector_config': {
                'detector_type': config.detector_type,
                'mass_kg': config.mass_kg,
                'temperature_mk': config.temperature_mk,
                'threshold_kev': config.energy_threshold_kev,
                'background_rate': config.background_rate_per_kg_day,
                'exposure_time_days': config.exposure_time_days
            }
        }
        
        # Store in state
        simulation_state['current_sim'] = response
        simulation_state['history'].append(response)
        
        return jsonify(response), 200
    
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter value: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Simulation error: {str(e)}'}), 500


@app.route('/api/results', methods=['GET'])
def get_results():
    """Get latest simulation results"""
    if simulation_state['current_sim']:
        return jsonify(simulation_state['current_sim']), 200
    return jsonify({'error': 'No simulation results available. Run a simulation first.'}), 404


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get all simulation history"""
    return jsonify({
        'total_simulations': len(simulation_state['history']),
        'history': simulation_state['history']
    }), 200


@app.route('/api/parameters', methods=['GET'])
def get_parameters():
    """Get available simulation parameters and their ranges"""
    parameters = {
        'detector_types': [
            'superfluid_helium',
            'liquid_xenon',
            'germanium',
            'scintillator'
        ],
        'mass_range': {
            'min': 0.01,
            'max': 10000.0,
            'default': 1.0,
            'unit': 'kg'
        },
        'temperature_range': {
            'min': 5,
            'max': 300,
            'default': 15,
            'unit': 'mK'
        },
        'energy_threshold_range': {
            'min': 0.1,
            'max': 100,
            'default': 3.0,
            'unit': 'keV'
        },
        'background_rate_range': {
            'min': 0.0001,
            'max': 1.0,
            'default': 0.01,
            'unit': 'events/kg/day'
        },
        'exposure_time_range': {
            'min': 1,
            'max': 3650,
            'default': 365,
            'unit': 'days'
        },
        'background_events_range': {
            'min': 10,
            'max': 50000,
            'default': 1000
        },
        'dark_matter_events_range': {
            'min': 1,
            'max': 1000,
            'default': 50
        }
    }
    return jsonify(parameters), 200


@app.route('/api/statistics', methods=['POST'])
def calculate_statistics():
    """Calculate advanced statistics from current simulation"""
    try:
        data = request.get_json()
        
        if not simulation_state['current_sim']:
            return jsonify({'error': 'No active simulation. Run a simulation first.'}), 404
        
        stats = simulation_state['current_sim']['statistics']
        config = simulation_state['current_sim']['detector_config']
        
        # Calculate derived statistics
        total = stats['total_events']
        dm = stats['dark_matter_candidates']
        bg = stats['background_events']
        
        s2n = (dm / max(bg, 1)) if bg > 0 else float('inf')
        discovery = 'High' if dm > 5 else 'Medium' if dm > 1 else 'Low'
        bg_rejection_pct = (bg / max(total, 1)) * 100 if total > 0 else 0
        
        analysis = {
            'signal_to_noise': round(s2n, 4),
            'discovery_potential': discovery,
            'background_rejection_percentage': round(bg_rejection_pct, 2),
            'signal_efficiency': round((dm / max(stats.get('total_exposure', 1), 1)), 4),
            'energy_range': {
                'min_kev': round(stats['min_energy'], 2),
                'max_kev': round(stats['max_energy'], 2),
                'mean_kev': round(stats['mean_energy'], 2)
            },
            'detector_info': {
                'type': config['detector_type'],
                'mass_kg': config['mass_kg'],
                'total_exposure_kg_days': round(config['exposure_time_days'] * config['mass_kg'], 2)
            },
            'recommendations': [
                'Consider longer exposure for better sensitivity' if dm < 3 else '',
                'Excellent signal detection achieved' if dm > 10 else '',
                'Background rejection is optimal' if bg_rejection_pct > 90 else ''
            ]
        }
        
        # Remove empty recommendations
        analysis['recommendations'] = [r for r in analysis['recommendations'] if r]
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({'error': f'Statistics calculation error: {str(e)}'}), 500


@app.route('/api/export', methods=['GET'])
def export_data():
    """Export current simulation data as JSON"""
    if not simulation_state['current_sim']:
        return jsonify({'error': 'No simulation data to export'}), 404
    
    return jsonify(simulation_state['current_sim']), 200


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear simulation history"""
    simulation_state['history'] = []
    simulation_state['current_sim'] = None
    return jsonify({'status': 'History cleared'}), 200


@app.route('/api/version', methods=['GET'])
def get_version():
    """Get API version information"""
    return jsonify({
        'api_version': '1.0.0',
        'app_name': 'XIVIX Dark Matter Detector',
        'description': 'Monte Carlo simulation for dark matter particle detection'
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 404,
        'message': 'The requested URL was not found on the server'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 500,
        'message': 'An unexpected error occurred'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad request',
        'status': 400,
        'message': 'The request could not be understood by the server'
    }), 400


if __name__ == '__main__':
    print("=" * 60)
    print("XIVIX Dark Matter Detection API")
    print("=" * 60)
    print(f"Starting server on http://localhost:5000")
    print("Available endpoints:")
    print("  POST   /api/simulate       - Run new simulation")
    print("  GET    /api/results        - Get latest results")
    print("  GET    /api/history        - Get all simulations")
    print("  GET    /api/parameters     - Get parameter options")
    print("  POST   /api/statistics     - Calculate statistics")
    print("  GET    /api/export         - Export current data")
    print("  POST   /api/clear          - Clear history")
    print("  GET    /api/health         - Health check")
    print("  GET    /api/version        - API version")
    print("=" * 60)
    print("\nPress Ctrl+C to stop server\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )

    