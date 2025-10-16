
import { Detector, SimulationParameters } from './types';

export const DEFAULT_SIMULATION_PARAMETERS: SimulationParameters = {
  detector: Detector.LiquidXenon,
  wimpMass: 100,
  crossSection: 1e-45,
};

export const DETECTOR_PROPERTIES: Record<Detector, { color: string; style: string; energyMean: number; energyStdDev: number }> = {
  [Detector.SuperfluidHelium]: {
    color: 'bg-cyan-500/20',
    style: 'border-cyan-400',
    energyMean: 10,
    energyStdDev: 3
  },
  [Detector.LiquidXenon]: {
    color: 'bg-indigo-500/20',
    style: 'border-indigo-400',
    energyMean: 50,
    energyStdDev: 15
  },
  [Detector.Germanium]: {
    color: 'bg-slate-500/20',
    style: 'border-slate-400',
    energyMean: 80,
    energyStdDev: 8
  },
  [Detector.Scintillator]: {
    color: 'bg-emerald-500/20',
    style: 'border-emerald-400',
    energyMean: 120,
    energyStdDev: 25
  },
};
