import React from "react";

const StatsSkeleton: React.FC = () => (
  <div className="w-full max-w-xs mx-auto flex flex-col py-2 animate-pulse">
    <div className="h-4 w-32 bg-gray-700 rounded mb-2" />
    <div className="h-8 w-16 bg-gray-700 rounded" />
  </div>
);

export default StatsSkeleton;
