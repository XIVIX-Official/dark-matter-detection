"""
API routes for the dark matter detection simulation.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import numpy as np
import config
from src.detector import Detector
from src.particle import EventCollection

api = Blueprint('api', __name__)

# Store simulation history
simulation_history = []

@api.route('/simulate', methods=['POST'])
def simulate():
    """Start a new simulation with given parameters."""
    try:
        data = request.get_json()
        
        # Create detector
        detector = Detector(
            detector_type=data.get('detector_type', 'superfluid_helium'),
            mass_kg=float(data.get('mass_kg', config.DEFAULT_DETECTOR_MASS_KG)),
            temperature_mk=float(data.get('temperature_mk', config.DEFAULT_TEMPERATURE_MK))
        )
        
        # Run simulation
        events = detector.run_simulation(
            exposure_time_days=float(data.get('exposure_time_days', config.DEFAULT_EXPOSURE_TIME_DAYS)),
            n_wimp_events=int(data.get('dark_matter_events', 50)),
            n_background_events=int(data.get('background_events', 1000))
        )
        
        # Get results
        results = detector.get_results()
        
        # Add to history
        simulation_id = len(simulation_history) + 1
        simulation_history.append({
            'simulation_id': simulation_id,
            'timestamp': datetime.now().isoformat(),
            'parameters': data,
            'results': results
        })
        
        # Return results
        return jsonify({
            'simulation_id': simulation_id,
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            **results
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@api.route('/results', methods=['GET'])
def get_results():
    """Get results of latest simulation."""
    if not simulation_history:
        return jsonify({
            'status': 'error',
            'message': 'No simulations have been run yet'
        }), 404
        
    return jsonify(simulation_history[-1])

@api.route('/history', methods=['GET'])
def get_history():
    """Get simulation history."""
    return jsonify(simulation_history)

@api.route('/parameters', methods=['GET'])
def get_parameters():
    """Get available configuration parameters."""
    return jsonify({
        'detector_types': list(config.DETECTOR_CONFIGS.keys()),
        'default_parameters': {
            'mass_kg': config.DEFAULT_DETECTOR_MASS_KG,
            'temperature_mk': config.DEFAULT_TEMPERATURE_MK,
            'energy_threshold_kev': config.DEFAULT_ENERGY_THRESHOLD_KEV,
            'exposure_time_days': config.DEFAULT_EXPOSURE_TIME_DAYS
        },
        'detector_configs': config.DETECTOR_CONFIGS,
        'wimp_parameters': {
            'mass_gev': config.WIMP_MASS_GEV,
            'cross_section_cm2': config.WIMP_CROSS_SECTION_CM2
        }
    })

@api.route('/statistics', methods=['POST'])
def calculate_statistics():
    """Calculate additional statistics from simulation results."""
    try:
        data = request.get_json()
        signal_threshold = float(data.get('signal_threshold', config.SIGNIFICANCE_THRESHOLD))
        
        if not simulation_history:
            return jsonify({
                'status': 'error',
                'message': 'No simulations have been run yet'
            }), 404
            
        latest_results = simulation_history[-1]['results']
        stats = latest_results['statistics']
        
        # Calculate additional statistics
        total_events = stats['total_events']
        signal_events = stats['dark_matter_candidates']
        background_events = stats['background_events']
        
        # Significance calculation
        expected_background = background_events
        observed_signal = signal_events
        
        if expected_background > 0:
            significance = (observed_signal - expected_background) / np.sqrt(expected_background)
        else:
            significance = 0
            
        return jsonify({
            'total_events': total_events,
            'signal_events': signal_events,
            'background_events': background_events,
            'signal_to_background_ratio': signal_events / background_events if background_events > 0 else float('inf'),
            'significance_sigma': float(significance),
            'discovery_threshold_met': significance >= signal_threshold
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@api.route('/export', methods=['GET'])
def export_data():
    """Export simulation data in requested format."""
    if not simulation_history:
        return jsonify({
            'status': 'error',
            'message': 'No simulations have been run yet'
        }), 404
        
    format = request.args.get('format', 'json')
    if format not in config.EXPORT_FORMATS:
        return jsonify({
            'status': 'error',
            'message': f'Unsupported format. Use one of: {", ".join(config.EXPORT_FORMATS)}'
        }), 400
        
    # Get latest simulation data
    data = simulation_history[-1]
    
    if format == 'json':
        return jsonify(data)
    elif format == 'csv':
        # TODO: Implement CSV export
        return jsonify({
            'status': 'error',
            'message': 'CSV export not implemented yet'
        }), 501