
import React from 'react';
import { Detector, SimulationParameters } from '../types';

interface ControlPanelProps {
  isRunning: boolean;
  params: SimulationParameters;
  onParamsChange: <K extends keyof SimulationParameters>(param: K, value: SimulationParameters[K]) => void;
  onStart: () => void;
  onStop: () => void;
  onReset: () => void;
  onExport: () => void;
  eventCount: number;
}

const PlayIcon: React.FC<{className?: string}> = ({ className }) => (
  <svg className={className} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z" /></svg>
);
const StopIcon: React.FC<{className?: string}> = ({ className }) => (
  <svg className={className} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h12v12H6z" /></svg>
);
const ResetIcon: React.FC<{className?: string}> = ({ className }) => (
  <svg className={className} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2.5 2v6h6M21.5 22v-6h-6"/><path d="M22 11.5A10 10 0 0 0 3.2 7.2M2 12.5a10 10 0 0 0 18.8 4.2"/></svg>
);
const ExportIcon: React.FC<{className?: string}> = ({ className }) => (
  <svg className={className} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
);


export const ControlPanel: React.FC<ControlPanelProps> = ({ isRunning, params, onParamsChange, onStart, onStop, onReset, onExport, eventCount }) => {
  
  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-2xl p-6 shadow-2xl space-y-6 h-full">
      <h2 className="text-xl font-bold text-cyan-300 border-b border-slate-600 pb-2">Simulation Controls</h2>
      
      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-4">
        <button onClick={onStart} disabled={isRunning} className="flex items-center justify-center gap-2 bg-green-600 hover:bg-green-500 disabled:bg-green-800 disabled:cursor-not-allowed text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 shadow-lg shadow-green-900/50">
          <PlayIcon className="w-5 h-5"/> Start
        </button>
        <button onClick={onStop} disabled={!isRunning} className="flex items-center justify-center gap-2 bg-red-600 hover:bg-red-500 disabled:bg-red-800 disabled:cursor-not-allowed text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 shadow-lg shadow-red-900/50">
          <StopIcon className="w-5 h-5"/> Stop
        </button>
        <button onClick={onReset} disabled={isRunning} className="flex items-center justify-center gap-2 bg-slate-600 hover:bg-slate-500 disabled:bg-slate-800 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 col-span-1">
          <ResetIcon className="w-5 h-5"/> Reset
        </button>
         <button onClick={onExport} disabled={isRunning || eventCount === 0} className="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 col-span-1">
          <ExportIcon className="w-5 h-5"/> Export
        </button>
      </div>

       <div className="text-center bg-slate-900/50 p-3 rounded-lg border border-slate-700">
          <p className="text-slate-400">Events Detected</p>
          <p className="text-2xl font-mono font-bold text-cyan-300">{eventCount}</p>
        </div>

      {/* Parameters */}
      <div className="space-y-4 pt-4 border-t border-slate-700">
        <h3 className="text-lg font-semibold text-slate-300">Parameters</h3>
        
        <div>
          <label htmlFor="detector" className="block text-sm font-medium text-slate-400">Detector Type</label>
          <select 
            id="detector" 
            value={params.detector}
            onChange={(e) => onParamsChange('detector', e.target.value as Detector)}
            disabled={isRunning}
            className="mt-1 block w-full bg-slate-700 border border-slate-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 sm:text-sm text-white disabled:opacity-50"
          >
            {Object.values(Detector).map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>

        <div>
          <label htmlFor="wimpMass" className="block text-sm font-medium text-slate-400">WIMP Mass (GeV/c²)</label>
          <div className="flex items-center gap-4">
             <input 
              type="range" 
              id="wimpMass" 
              min="10" 
              max="1000" 
              step="10"
              value={params.wimpMass}
              onChange={(e) => onParamsChange('wimpMass', Number(e.target.value))}
              disabled={isRunning}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer disabled:opacity-50"
            />
            <span className="font-mono text-cyan-400 w-16 text-center">{params.wimpMass}</span>
          </div>
        </div>
        
        <div>
          <label htmlFor="crossSection" className="block text-sm font-medium text-slate-400">Cross-Section (cm²)</label>
          <div className="flex items-center gap-4">
            <input 
              type="range" 
              id="crossSection"
              min="1e-47"
              max="1e-43"
              step="1e-48"
              value={params.crossSection}
              onChange={(e) => onParamsChange('crossSection', Number(e.target.value))}
              disabled={isRunning}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer disabled:opacity-50"
            />
             <span className="font-mono text-cyan-400 w-20 text-center">{params.crossSection.toExponential(0)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
