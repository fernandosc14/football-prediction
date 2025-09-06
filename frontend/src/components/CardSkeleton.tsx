import React from "react";

const CardSkeleton: React.FC = () => (
  <div className="prediction-card p-4 sm:p-6 rounded-2xl flex flex-col justify-between h-full bg-slate-800/30 border border-white/10 animate-pulse">
    <div>
      <div className="flex flex-col gap-2 sm:flex-row sm:justify-between sm:items-start">
        <div>
          <div className="h-6 w-32 bg-gray-700 rounded mb-2" />
          <div className="h-4 w-20 bg-gray-700 rounded" />
        </div>
      </div>
      <div className="flex flex-col gap-3 sm:gap-4 mt-3 sm:mt-4">
        {[...Array(3)].map((_, idx) => (
          <div key={idx} className="flex flex-row items-center justify-between gap-4 p-2 rounded border-b border-b-gray-700/80 bg-slate-900/30">
            <div className="h-4 w-24 bg-gray-700 rounded" />
            <div className="h-4 w-12 bg-gray-700 rounded-full" />
          </div>
        ))}
      </div>
    </div>
  </div>
);

export default CardSkeleton;
