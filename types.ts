
export enum Detector {
  SuperfluidHelium = 'Superfluid Helium',
  LiquidXenon = 'Liquid Xenon',
  Germanium = 'Germanium',
  Scintillator = 'Scintillator',
}

export interface SimulationEvent {
  id: string;
  energy: number; // in keV
  timestamp: number;
  position: {
    x: number; // percentage
    y: number; // percentage
  };
}

export interface SimulationParameters {
  detector: Detector;
  wimpMass: number; // in GeV/c^2
  crossSection: number; // in cm^2
}
