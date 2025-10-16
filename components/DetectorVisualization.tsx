
import React, { useState, useEffect } from 'react';
import { Detector, SimulationEvent } from '../types';
import { DETECTOR_PROPERTIES } from '../constants';

interface DetectorVisualizationProps {
  detector: Detector;
  latestEvent: SimulationEvent | null;
}

const ParticleHit: React.FC<{ event: SimulationEvent }> = ({ event }) => (
  <div
    className="absolute rounded-full pointer-events-none animate-ping-slow"
    style={{
      left: `${event.position.x}%`,
      top: `${event.position.y}%`,
      width: `${Math.max(10, event.energy / 5)}px`,
      height: `${Math.max(10, event.energy / 5)}px`,
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      boxShadow: '0 0 15px 5px rgba(255, 255, 255, 0.7)',
      transform: 'translate(-50%, -50%)',
    }}
  />
);

export const DetectorVisualization: React.FC<DetectorVisualizationProps> = ({ detector, latestEvent }) => {
  const [hits, setHits] = useState<SimulationEvent[]>([]);
  const detectorProps = DETECTOR_PROPERTIES[detector];

  useEffect(() => {
    if (latestEvent) {
      setHits(prev => [...prev, latestEvent]);
      const timer = setTimeout(() => {
        setHits(currentHits => currentHits.filter(h => h.id !== latestEvent.id));
      }, 1000); // Animation duration
      return () => clearTimeout(timer);
    }
  }, [latestEvent]);

  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-2xl p-6 shadow-2xl space-y-4">
       <h2 className="text-xl font-bold text-cyan-300 border-b border-slate-600 pb-2">Detector Chamber</h2>
      <div className={`relative w-full h-80 overflow-hidden rounded-lg border-2 ${detectorProps.style} ${detectorProps.color} transition-all duration-500`}>
        <div className="absolute inset-0 bg-black/30"></div>
        {hits.map(hit => (
          <ParticleHit key={hit.id} event={hit} />
        ))}
        <div className="absolute top-2 left-3 bg-black/50 px-3 py-1 rounded-md text-sm font-semibold">{detector}</div>
      </div>
    </div>
  );
};

// Add custom animation to tailwind config if we could, otherwise use inline style or a style tag.
// Here, we'll use a trick by defining it in the global scope if this were a real app setup
// For this single-file output, a simple keyframes in index.html would be better.
// Or we just rely on existing animations. Let's create a custom ping.
if (typeof window !== 'undefined') {
    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = `
        @keyframes ping-slow {
            75%, 100% {
                transform: translate(-50%, -50%) scale(2.5);
                opacity: 0;
            }
        }
        .animate-ping-slow {
            animation: ping-slow 1s cubic-bezier(0, 0, 0.2, 1) forwards;
        }
    `;
    document.head.appendChild(styleSheet);
}
