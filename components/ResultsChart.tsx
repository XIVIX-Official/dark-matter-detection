
import React, { useMemo } from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { SimulationEvent, Detector } from '../types';
import { DETECTOR_PROPERTIES } from '../constants';

interface ResultsChartProps {
  data: SimulationEvent[];
  detector: Detector;
}

const CustomTooltip: React.FC<any> = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-800/80 backdrop-blur-sm border border-slate-600 p-3 rounded-md shadow-lg">
        <p className="label text-slate-300">{`Energy: ${label} keV`}</p>
        <p className="intro text-cyan-400">{`Events: ${payload[0].value}`}</p>
      </div>
    );
  }
  return null;
};


export const ResultsChart: React.FC<ResultsChartProps> = ({ data, detector }) => {
  const chartData = useMemo(() => {
    if (data.length === 0) return [];

    const binSize = 5; // keV
    const maxEnergy = Math.max(...data.map(e => e.energy), 50);
    const bins = Math.ceil(maxEnergy / binSize);
    
    const histogram = Array.from({ length: bins }, (_, i) => ({
      energy: i * binSize,
      count: 0,
    }));

    data.forEach(event => {
      const binIndex = Math.floor(event.energy / binSize);
      if (binIndex >= 0 && binIndex < bins) {
        histogram[binIndex].count++;
      }
    });

    return histogram;
  }, [data]);

  const detectorColor = DETECTOR_PROPERTIES[detector].style.replace('border-', '');

  return (
     <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-2xl p-6 shadow-2xl h-96">
      <h2 className="text-xl font-bold text-cyan-300 mb-4">Energy Spectrum</h2>
      {data.length > 0 ? (
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 5, right: 20, left: -10, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 116, 139, 0.3)" />
            <XAxis 
              dataKey="energy" 
              stroke="#94a3b8" 
              tick={{ fontSize: 12 }} 
              label={{ value: 'Energy (keV)', position: 'insideBottom', offset: -10, fill: '#94a3b8' }}
            />
            <YAxis 
              stroke="#94a3b8" 
              tick={{ fontSize: 12 }} 
              label={{ value: 'Event Count', angle: -90, position: 'insideLeft', fill: '#94a3b8' }}
              allowDecimals={false}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(100, 116, 139, 0.2)' }} />
            <Legend wrapperStyle={{paddingTop: '20px'}} />
            <Bar dataKey="count" name="Events" fill={`#${detectorColor.replace('400', '500')}`} fillOpacity={0.8} />
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <div className="flex items-center justify-center h-full text-slate-500">
          <p>Start the simulation to see results.</p>
        </div>
      )}
    </div>
  );
};
