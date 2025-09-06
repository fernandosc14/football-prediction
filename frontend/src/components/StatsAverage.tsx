import React from "react";

export type StatsType = {
  winner: { percent: number };
  over_2_5: { percent: number };
  over_1_5: { percent: number };
  double_chance: { percent: number };
  btts: { percent: number };
  best_type?: string;
};

interface Props {
  stats: StatsType;
}

function getAveragePercent(stats: StatsType): number {
  const percents = [
    stats.winner?.percent,
    stats.over_2_5?.percent,
    stats.over_1_5?.percent,
    stats.double_chance?.percent,
    stats.btts?.percent,
  ].filter((v): v is number => Number.isFinite(v));

  if (percents.length === 0) return 0;
  const sum = percents.reduce((acc, val) => acc + val, 0);
  return Math.round(sum / percents.length);
}

const StatsAverage: React.FC<Props> = ({ stats }) => {
  const average = getAveragePercent(stats);
  return (
    <div className="w-full max-w-xs mx-auto flex flex-col items-center py-4 bg-slate-800/50 border border-white/10 rounded-2xl">
      <span className="text-base text-white mb-2">Total accuracy percentage</span>
      <span className="text-4xl font-bold text-green-400">{average}%</span>
    </div>
  );
};

export default StatsAverage;
