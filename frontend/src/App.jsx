import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell
} from 'recharts';
import SimulationForm from './components/SimulationForm';
import StatisticsCard from './components/StatisticsCard';
import { COLORS } from './styles/theme';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [simulationResults, setSimulationResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runSimulation = async (params) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`${API_BASE_URL}/simulate`, params);
      setSimulationResults(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const formatEnergyData = (spectrum) => {
    if (!spectrum) return [];
    const { bins, counts } = spectrum;
    return bins.slice(0, -1).map((bin, i) => ({
      energy: `${bin.toFixed(1)}-${bins[i + 1].toFixed(1)}`,
      counts: counts[i]
    }));
  };

  const formatPieData = (stats) => {
    if (!stats) return [];
    return [
      { name: 'Dark Matter', value: stats.dark_matter_candidates },
      { name: 'Background', value: stats.background_events }
    ];
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="py-6 px-4 border-b border-gray-800">
        <h1 className="text-3xl font-bold text-center">
          XIVIX: Dark Matter Detection Simulation
        </h1>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Simulation Form */}
          <div className="bg-gray-800 rounded-lg p-6">
            <SimulationForm onSubmit={runSimulation} loading={loading} />
            {error && (
              <div className="mt-4 p-4 bg-red-900 text-white rounded">
                {error}
              </div>
            )}
          </div>

          {/* Results Section */}
          {simulationResults && (
            <div className="space-y-8">
              {/* Statistics Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <StatisticsCard
                  title="Total Events"
                  value={simulationResults.statistics.total_events}
                />
                <StatisticsCard
                  title="Dark Matter Candidates"
                  value={simulationResults.statistics.dark_matter_candidates}
                />
                <StatisticsCard
                  title="Mean Energy"
                  value={`${simulationResults.statistics.mean_energy.toFixed(2)} keV`}
                />
                <StatisticsCard
                  title="Detection Efficiency"
                  value={`${(simulationResults.detector_config.efficiency * 100).toFixed(1)}%`}
                />
              </div>

              {/* Energy Spectrum */}
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-4">Energy Spectrum</h3>
                <LineChart
                  width={500}
                  height={300}
                  data={formatEnergyData(simulationResults.energy_spectrum)}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                  <XAxis dataKey="energy" stroke="#888" />
                  <YAxis stroke="#888" />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="counts"
                    stroke="#8884d8"
                    activeDot={{ r: 8 }}
                  />
                </LineChart>
              </div>

              {/* Event Distribution */}
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-4">Event Distribution</h3>
                <PieChart width={400} height={400}>
                  <Pie
                    data={formatPieData(simulationResults.statistics)}
                    cx={200}
                    cy={200}
                    labelLine={false}
                    outerRadius={150}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {formatPieData(simulationResults.statistics).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;