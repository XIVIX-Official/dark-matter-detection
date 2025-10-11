import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart, Area, AreaChart, PieChart, Pie, Cell } from 'recharts';
import { Play, RotateCcw, Download, Settings, Zap, Activity, Target, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';

export default function DarkMatterDetector() {
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  
  const [params, setParams] = useState({
    detector_type: 'superfluid_helium',
    mass_kg: 1.0,
    temperature_mk: 15,
    energy_threshold_kev: 3.0,
    background_rate: 0.01,
    exposure_time_days: 365,
    background_events: 1000,
    dark_matter_events: 50
  });

  const API_BASE = 'http://localhost:5000/api';

  const runSimulation = async () => {
    setLoading(true);
    setIsRunning(true);
    try {
      const response = await fetch(`${API_BASE}/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Simulation error:', error);
      alert('Failed to run simulation. Make sure the backend is running on localhost:5000');
    } finally {
      setLoading(false);
      setIsRunning(false);
    }
  };

  const handleParamChange = (key, value) => {
    setParams(prev => ({ ...prev, [key]: isNaN(value) ? value : parseFloat(value) }));
  };

  const downloadResults = () => {
    if (!results) return;
    const element = document.createElement('a');
    element.href = URL.createObjectURL(new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' }));
    element.download = `dark-matter-sim-${new Date().getTime()}.json`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const resetSimulation = () => {
    setResults(null);
    setParams({
      detector_type: 'superfluid_helium',
      mass_kg: 1.0,
      temperature_mk: 15,
      energy_threshold_kev: 3.0,
      background_rate: 0.01,
      exposure_time_days: 365,
      background_events: 1000,
      dark_matter_events: 50
    });
  };

  // Prepare chart data
  const energyChartData = results?.energy_spectrum?.bins?.slice(0, -1).map((bin, i) => ({
    energy: parseFloat((bin + (results.energy_spectrum.bins[i + 1] || bin)) / 2).toFixed(1),
    count: results.energy_spectrum.counts[i] || 0
  })) || [];

  const temporalChartData = results?.temporal_distribution?.times?.slice(0, -1).map((time, i) => ({
    time: Math.round(time / 86400),
    events: results.temporal_distribution.counts[i] || 0
  })) || [];

  const stats = results?.statistics || {};
  const discovery = stats.dark_matter_candidates > 5 ? 'High' : stats.dark_matter_candidates > 1 ? 'Medium' : 'Low';
  const discoveryColor = discovery === 'High' ? 'text-emerald-400' : discovery === 'Medium' ? 'text-yellow-400' : 'text-red-400';

  const eventDistribution = [
    { name: 'Dark Matter', value: stats.dark_matter_candidates || 0, fill: '#06b6d4' },
    { name: 'Background', value: stats.background_events || 0, fill: '#f43f5e' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-lg">
              <Zap size={28} />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                XIVIX
              </h1>
              <p className="text-slate-400 text-sm">Dark Matter Detection Simulation</p>
            </div>
          </div>
          <div className="text-right text-slate-400 text-sm">
            <p>Status: <span className={isRunning ? 'text-yellow-400 animate-pulse' : 'text-emerald-400'}>
              {isRunning ? 'Running...' : results ? 'Complete' : 'Ready'}
            </span></p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
        {/* Control Panel */}
        <div className="lg:col-span-1">
          <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur border border-slate-700/50 rounded-xl p-6 sticky top-6">
            <div className="flex items-center gap-2 mb-6">
              <Settings size={20} className="text-cyan-400" />
              <h2 className="text-xl font-bold">Configuration</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-2">Detector Type</label>
                <select 
                  value={params.detector_type}
                  onChange={(e) => handleParamChange('detector_type', e.target.value)}
                  className="w-full bg-slate-700/50 border border-slate-600 rounded px-3 py-2 text-sm focus:outline-none focus:border-cyan-500"
                >
                  <option>superfluid_helium</option>
                  <option>liquid_xenon</option>
                  <option>germanium</option>
                  <option>scintillator</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Mass (kg)</label>
                  <input 
                    type="number" 
                    value={params.mass_kg}
                    onChange={(e) => handleParamChange('mass_kg', e.target.value)}
                    step="0.1"
                    className="w-full bg-slate-700/50 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Temp (mK)</label>
                  <input 
                    type="number" 
                    value={params.temperature_mk}
                    onChange={(e) => handleParamChange('temperature_mk', e.target.value)}
                    step="1"
                    className="w-full bg-slate-700/50 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Energy Threshold (keV)</label>
                <input 
                  type="number" 
                  value={params.energy_threshold_kev}
                  onChange={(e) => handleParamChange('energy_threshold_kev', e.target.value)}
                  step="0.1"
                  className="w-full bg-slate-700/50 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Bg Rate (1/kg/d)</label>
                  <input 
                    type="number" 
                    value={params.background_rate}
                    onChange={(e) => handleParamChange('background_rate', e.target.value)}
                    step="0.001"
                    className="w-full bg-slate-700/50 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Exposure (d)</label>
                  <input 
                    type="number" 
                    value={params.exposure_time_days}
                    onChange={(e) => handleParamChange('exposure_time_days', e.target.value)}
                    step="1"
                    className="w-full bg-slate-700/50 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Bg Events</label>
                  <input 
                    type="number" 
                    value={params.background_events}
                    onChange={(e) => handleParamChange('background_events', e.target.value)}
                    step="100"
                    className="w-full bg-slate-700/50 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">DM Events</label>
                  <input 
                    type="number" 
                    value={params.dark_matter_events}
                    onChange={(e) => handleParamChange('dark_matter_events', e.target.value)}
                    step="5"
                    className="w-full bg-slate-700/50 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              <div className="pt-4 flex gap-2">
                <button
                  onClick={runSimulation}
                  disabled={loading || isRunning}
                  className="flex-1 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 disabled:opacity-50 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-all duration-200"
                >
                  <Play size={16} />
                  {loading ? 'Running...' : 'Simulate'}
                </button>
                <button
                  onClick={resetSimulation}
                  className="bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center gap-2 transition-all duration-200"
                >
                  <RotateCcw size={16} />
                </button>
              </div>

              {results && (
                <button
                  onClick={downloadResults}
                  className="w-full bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-all duration-200"
                >
                  <Download size={16} />
                  Export Data
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Main Results */}
        <div className="lg:col-span-3 space-y-6">
          {/* Stats Cards */}
          {results && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-500/20 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-cyan-400 text-xs font-semibold">DM Candidates</span>
                  <Target size={16} className="text-cyan-400" />
                </div>
                <p className="text-2xl font-bold">{stats.dark_matter_candidates || 0}</p>
              </div>

              <div className="bg-gradient-to-br from-rose-500/10 to-pink-500/10 border border-rose-500/20 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-rose-400 text-xs font-semibold">Background</span>
                  <Activity size={16} className="text-rose-400" />
                </div>
                <p className="text-2xl font-bold">{stats.background_events || 0}</p>
              </div>

              <div className={`bg-gradient-to-br ${discovery === 'High' ? 'from-emerald-500/10 to-green-500/10 border border-emerald-500/20' : discovery === 'Medium' ? 'from-yellow-500/10 to-amber-500/10 border border-yellow-500/20' : 'from-red-500/10 to-rose-500/10 border border-red-500/20'} rounded-lg p-4`}>
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-xs font-semibold ${discoveryColor}`}>Discovery</span>
                  <AlertCircle size={16} className={discoveryColor} />
                </div>
                <p className={`text-2xl font-bold ${discoveryColor}`}>{discovery}</p>
              </div>

              <div className="bg-gradient-to-br from-purple-500/10 to-indigo-500/10 border border-purple-500/20 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-purple-400 text-xs font-semibold">Efficiency</span>
                  <TrendingUp size={16} className="text-purple-400" />
                </div>
                <p className="text-2xl font-bold">{(stats.detector_efficiency * 100).toFixed(1)}%</p>
              </div>
            </div>
          )}

          {/* Energy Spectrum */}
          {results && energyChartData.length > 0 && (
            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur border border-slate-700/50 rounded-xl p-6">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <div className="w-3 h-3 bg-cyan-400 rounded-full"></div>
                Energy Spectrum
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={energyChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(100,116,139,0.1)" />
                  <XAxis dataKey="energy" stroke="rgba(148,163,184,0.5)" />
                  <YAxis stroke="rgba(148,163,184,0.5)" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(15,23,42,0.8)', border: '1px solid rgba(100,116,139,0.3)', borderRadius: '8px' }}
                    cursor={{ fill: 'rgba(6,182,212,0.1)' }}
                  />
                  <Bar dataKey="count" fill="url(#colorGradient)" radius={[8, 8, 0, 0]} />
                  <defs>
                    <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.8}/>
                      <stop offset="100%" stopColor="#0369a1" stopOpacity={0.2}/>
                    </linearGradient>
                  </defs>
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Event Distribution Pie + Temporal */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {results && eventDistribution.some(d => d.value > 0) && (
              <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur border border-slate-700/50 rounded-xl p-6">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <div className="w-3 h-3 bg-purple-400 rounded-full"></div>
                  Event Distribution
                </h3>
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie
                      data={eventDistribution}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {eventDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'rgba(15,23,42,0.8)', border: '1px solid rgba(100,116,139,0.3)' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}

            {results && temporalChartData.length > 0 && (
              <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur border border-slate-700/50 rounded-xl p-6">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <div className="w-3 h-3 bg-blue-400 rounded-full"></div>
                  Temporal Distribution
                </h3>
                <ResponsiveContainer width="100%" height={280}>
                  <AreaChart data={temporalChartData}>
                    <defs>
                      <linearGradient id="colorEvents" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(100,116,139,0.1)" />
                    <XAxis dataKey="time" stroke="rgba(148,163,184,0.5)" />
                    <YAxis stroke="rgba(148,163,184,0.5)" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'rgba(15,23,42,0.8)', border: '1px solid rgba(100,116,139,0.3)' }}
                    />
                    <Area type="monotone" dataKey="events" stroke="#3b82f6" fillOpacity={1} fill="url(#colorEvents)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>

          {/* Detailed Statistics */}
          {results && (
            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur border border-slate-700/50 rounded-xl p-6">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <CheckCircle size={20} className="text-emerald-400" />
                Simulation Details
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <p className="text-slate-400 mb-1">Total Events</p>
                  <p className="text-xl font-bold">{stats.total_events || 0}</p>
                </div>
                <div>
                  <p className="text-slate-400 mb-1">Mean Energy</p>
                  <p className="text-xl font-bold">{stats.mean_energy?.toFixed(2) || 0} keV</p>
                </div>
                <div>
                  <p className="text-slate-400 mb-1">Max Energy</p>
                  <p className="text-xl font-bold">{stats.max_energy?.toFixed(2) || 0} keV</p>
                </div>
                <div>
                  <p className="text-slate-400 mb-1">Exposure</p>
                  <p className="text-xl font-bold">{stats.total_exposure?.toFixed(1) || 0} kg·d</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-12 text-center text-slate-500 text-sm border-t border-slate-800 pt-6">
        <p>XIVIX Dark Matter Detection Simulation v1.0 | Monte Carlo Based Physics Engine</p>
      </div>
    </div>
  );
}
