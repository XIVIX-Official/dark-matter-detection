
import React from 'react';

const AtomIcon: React.FC<{className?: string}> = ({ className }) => (
  <svg className={className} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="1" />
    <path d="M20.2 20.2c2.04-2.03.02-5.91-4.04-9.96" />
    <path d="M3.8 3.8c-2.04 2.03-.02 5.91 4.04 9.96" />
    <path d="M20.2 3.8c-2.03 2.04-5.91.02-9.96-4.04" />
    <path d="M3.8 20.2c2.03-2.04 5.91-.02 9.96 4.04" />
  </svg>
);

export const Header: React.FC = () => {
  return (
    <header className="bg-slate-900/50 backdrop-blur-sm border-b border-slate-700/50 p-4 sticky top-0 z-50">
      <div className="container mx-auto flex items-center justify-center space-x-4">
        <AtomIcon className="w-10 h-10 text-cyan-400" />
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-100">
            Dark Matter Detection Simulation
          </h1>
          <p className="text-sm md:text-md text-slate-400">A Monte Carlo WIMP Interaction Model</p>
        </div>
      </div>
    </header>
  );
};
