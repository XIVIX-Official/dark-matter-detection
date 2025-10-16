
import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Header } from './components/Header';
import { ControlPanel } from './components/ControlPanel';
import { DetectorVisualization } from './components/DetectorVisualization';
import { ResultsChart } from './components/ResultsChart';
import { runSimulation, stopSimulation } from './services/simulationService';
import { Detector, SimulationEvent, SimulationParameters } from './types';
import { DEFAULT_SIMULATION_PARAMETERS } from './constants';
import { exportData } from './utils/export';

const App: React.FC = () => {
  const [simulationParams, setSimulationParams] = useState<SimulationParameters>(DEFAULT_SIMULATION_PARAMETERS);
  const [events, setEvents] = useState<SimulationEvent[]>([]);
  const [latestEvent, setLatestEvent] = useState<SimulationEvent | null>(null);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const simulationId = useRef<number | null>(null);

  const handleNewEvent = useCallback((event: SimulationEvent) => {
    setEvents(prevEvents => [...prevEvents.slice(-499), event]); // Keep last 500 events for performance
    setLatestEvent(event);
  }, []);

  const handleStart = useCallback(() => {
    if (isRunning) return;
    setIsRunning(true);
    setEvents([]); // Clear previous events
    simulationId.current = runSimulation(simulationParams, handleNewEvent);
  }, [isRunning, simulationParams, handleNewEvent]);

  const handleStop = useCallback(() => {
    if (!isRunning || simulationId.current === null) return;
    setIsRunning(false);
    stopSimulation(simulationId.current);
    simulationId.current = null;
  }, [isRunning]);
  
  const handleReset = useCallback(() => {
    handleStop();
    setEvents([]);
    setLatestEvent(null);
    setSimulationParams(DEFAULT_SIMULATION_PARAMETERS);
  }, [handleStop]);

  const handleExport = useCallback(() => {
    exportData(events, 'dark-matter-simulation-results.json');
  }, [events]);

  const handleParamsChange = useCallback(<K extends keyof SimulationParameters>(param: K, value: SimulationParameters[K]) => {
    setSimulationParams(prev => ({...prev, [param]: value}));
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (simulationId.current !== null) {
        stopSimulation(simulationId.current);
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 font-sans bg-[url('https://www.transparenttextures.com/patterns/stardust.png')]">
      <Header />
      <main className="container mx-auto p-4 md:p-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <ControlPanel
              isRunning={isRunning}
              params={simulationParams}
              onParamsChange={handleParamsChange}
              onStart={handleStart}
              onStop={handleStop}
              onReset={handleReset}
              onExport={handleExport}
              eventCount={events.length}
            />
          </div>
          <div className="lg:col-span-2 space-y-8">
            <DetectorVisualization 
              detector={simulationParams.detector} 
              latestEvent={latestEvent} 
            />
            <ResultsChart data={events} detector={simulationParams.detector} />
          </div>
        </div>
      </main>
      <footer className="text-center p-4 text-slate-500 text-sm">
        <p>Dark Matter Detection Simulation &copy; {new Date().getFullYear()}. For educational purposes only.</p>
      </footer>
    </div>
  );
};

export default App;
