
import { SimulationEvent, SimulationParameters, Detector } from '../types';
import { DETECTOR_PROPERTIES } from '../constants';

// A simple pseudo-random number generator for more deterministic "randomness" if needed.
const simplePRNG = (seed: number) => {
  let s = seed;
  return () => {
    s = Math.sin(s) * 10000;
    return s - Math.floor(s);
  };
};

const random = simplePRNG(Date.now());

// Box-Muller transform to get a normally distributed random number from a uniform one.
const randomNormal = (mean: number, stdDev: number): number => {
  let u = 0, v = 0;
  while (u === 0) u = random(); // Converting [0,1) to (0,1)
  while (v === 0) v = random();
  const num = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
  return num * stdDev + mean;
};

const generateEvent = (params: SimulationParameters): SimulationEvent => {
  const detectorProps = DETECTOR_PROPERTIES[params.detector];
  
  // A very simplified model for event energy
  const baseEnergy = randomNormal(detectorProps.energyMean, detectorProps.energyStdDev);
  const wimpFactor = 1 + (params.wimpMass / 500); // Heavier WIMPs deposit slightly more energy
  const energy = Math.max(0.1, baseEnergy * wimpFactor);
  
  return {
    id: `evt-${Date.now()}-${random()}`,
    energy,
    timestamp: Date.now(),
    position: {
      x: random() * 100,
      y: random() * 100,
    },
  };
};

export const runSimulation = (
  params: SimulationParameters,
  onNewEvent: (event: SimulationEvent) => void
): number => {
  // Rate depends on cross-section (higher means more events)
  // This is an artistic interpretation, not a physical formula
  const interval = 1000 / (params.crossSection * 1e46);
  const simulationId = window.setInterval(() => {
    const event = generateEvent(params);
    onNewEvent(event);
  }, Math.max(50, interval)); // at least 50ms interval

  return simulationId;
};

export const stopSimulation = (simulationId: number) => {
  window.clearInterval(simulationId);
};
