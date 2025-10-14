import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

function SimulationForm({ onSubmit, loading }) {
  const [parameters, setParameters] = useState(null);
  const [formData, setFormData] = useState({
    detector_type: 'superfluid_helium',
    mass_kg: 1.0,
    temperature_mk: 15,
    energy_threshold_kev: 3.0,
    background_rate: 0.01,
    exposure_time_days: 365,
    background_events: 1000,
    dark_matter_events: 50
  });

  useEffect(() => {
    // Fetch available parameters
    const fetchParameters = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/parameters`);
        setParameters(response.data);
      } catch (error) {
        console.error('Error fetching parameters:', error);
      }
    };
    fetchParameters();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  if (!parameters) {
    return <div>Loading parameters...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">
          Detector Type
        </label>
        <select
          name="detector_type"
          value={formData.detector_type}
          onChange={handleChange}
          className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
        >
          {parameters.detector_types.map(type => (
            <option key={type} value={type}>
              {type.replace('_', ' ').toUpperCase()}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">
          Detector Mass (kg)
        </label>
        <input
          type="number"
          name="mass_kg"
          value={formData.mass_kg}
          onChange={handleChange}
          step="0.1"
          min="0.1"
          max="1000"
          className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">
          Temperature (mK)
        </label>
        <input
          type="number"
          name="temperature_mk"
          value={formData.temperature_mk}
          onChange={handleChange}
          step="1"
          min="5"
          max="300"
          className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">
          Exposure Time (days)
        </label>
        <input
          type="number"
          name="exposure_time_days"
          value={formData.exposure_time_days}
          onChange={handleChange}
          step="1"
          min="1"
          max="3650"
          className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">
          Background Events
        </label>
        <input
          type="number"
          name="background_events"
          value={formData.background_events}
          onChange={handleChange}
          step="100"
          min="0"
          max="10000"
          className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">
          Dark Matter Events
        </label>
        <input
          type="number"
          name="dark_matter_events"
          value={formData.dark_matter_events}
          onChange={handleChange}
          step="10"
          min="0"
          max="1000"
          className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className={`w-full py-2 px-4 rounded-md font-medium ${
          loading
            ? 'bg-blue-500 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? 'Running Simulation...' : 'Run Simulation'}
      </button>
    </form>
  );
}

export default SimulationForm;