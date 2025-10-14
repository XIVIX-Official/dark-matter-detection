import React from 'react';

function StatisticsCard({ title, value }) {
  return (
    <div className="bg-gray-800 p-4 rounded-lg">
      <h3 className="text-sm font-medium text-gray-400">{title}</h3>
      <p className="mt-2 text-3xl font-semibold">{value}</p>
    </div>
  );
}

export default StatisticsCard;