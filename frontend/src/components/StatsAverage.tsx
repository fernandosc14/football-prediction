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

const statLabels = [
  { key: "winner", label: "Winner" },
  { key: "over_2_5", label: "Over 2.5" },
  { key: "over_1_5", label: "Over 1.5" },
  { key: "double_chance", label: "Double Chance" },
  { key: "btts", label: "BTTS" },
] as const;

const StatsAverage: React.FC<Props> = ({ stats }) => {
  const validPercents = statLabels
    .map(({ key }) => {
      const stat = stats[key];
      return stat && typeof stat === "object" && "percent" in stat ? stat.percent : undefined;
    })
    .filter((v): v is number => typeof v === "number" && Number.isFinite(v));
  const average = validPercents.length > 0 ? (validPercents.reduce((a, b) => a + b, 0) / validPercents.length) : 0;

  return (
    <div>
      <div className="flex justify-center mb-6">
        <div
          className="min-w-[300px] max-w-xs flex flex-col items-center py-5 px-4 bg-green-900/80 border-2 border-green-400 rounded-2xl shadow-lg"
          aria-label="Overall average accuracy"
        >
          <span className="text-base text-white mb-2 font-semibold">Overall Average</span>
          <span className="text-4xl font-extrabold text-green-200 transition-colors duration-300">
            {average.toFixed(1)}%
          </span>
        </div>
      </div>

      <div className="flex flex-wrap gap-3 justify-center">
        {statLabels.map(({ key, label }) => {
          const stat = stats[key];
          return (
            <div
              key={key}
              className="min-w-[120px] flex-1 max-w-xs flex flex-col items-center py-4 px-2 bg-slate-800/50 border border-white/10 rounded-2xl shadow-sm"
              aria-label={label + ' accuracy'}
            >
              <span className="text-base text-white mb-2">{label}</span>
              <span className="text-3xl font-bold text-green-400 transition-colors duration-300">
                {stat && typeof stat === "object" && "percent" in stat
                  ? stat.percent.toFixed(1)
                  : "0.0"}%
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StatsAverage;
