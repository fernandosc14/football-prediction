interface Tip {
  name: string;
  confidence: number;
  class?: number;
}

interface PredictionCardProps {
  team1: string;
  team2: string;
  tips: Tip[];
  date?: string;
}

export default function PredictionCard({ team1, team2, tips, date }: PredictionCardProps) {
  function getTipResult(tip: Tip): string {
    const name = tip.name.toLowerCase();
    const classValue = tip.class;
    if (typeof classValue === "undefined") return "-";
    if (name === "winner") {
      if (classValue === 0) return `Home win (${team1})`;
      if (classValue === 1) return "Draw";
      if (classValue === 2) return `Away win (${team2})`;
    }
    if (name === "double chance") {
      if (classValue === 0) return "1X (Home or Draw)";
      if (classValue === 1) return "X2 (Away or Draw)";
      if (classValue === 2) return "12 (Home or Away)";
    }
    if (name === "over 2.5") {
      if (classValue === 0) return "Under 2.5: No";
      if (classValue === 1) return "Over 2.5: Yes";
    }
    if (name === "over 1.5") {
      if (classValue === 0) return "Under 1.5: No";
      if (classValue === 1) return "Over 1.5: Yes";
    }
    if (name === "btts") {
      if (classValue === 0) return "Both Teams to Score: No";
      if (classValue === 1) return "Both Teams to Score: Yes";
    }
    return String(classValue);
  }
  function getConfidenceColor(conf: number) {
    if (conf >= 80) return "text-green-400";
    if (conf >= 60) return "text-yellow-400";
    if (conf >= 40) return "text-orange-400";
    return "text-red-400";
  }

  return (
    <div className="prediction-card p-4 sm:p-6 rounded-2xl flex flex-col justify-between h-full bg-slate-800/50 border border-white/10">
      <div>
        <div className="flex flex-col gap-2 sm:flex-row sm:justify-between sm:items-start">
          <div>
            <h3 className="text-lg sm:text-xl md:text-2xl font-bold text-white mb-1">
              {team1} <span className="text-pink-400">vs</span> {team2}
            </h3>
            {date && (
              <div className="text-xs sm:text-sm text-gray-300 mt-1">{date}</div>
            )}
          </div>
        </div>
        <div className="flex flex-col gap-3 sm:gap-4 mt-3 sm:mt-4">
          {tips.map((tip, idx) => (
            <div key={idx} className="flex flex-row items-center justify-between gap-4 p-2 rounded border-b border-b-gray-700/80 bg-slate-900/30">
              <div className="flex items-center gap-2 mb-2 sm:mb-0">
                <span className="font-semibold text-white drop-shadow text-sm sm:text-base">{getTipResult(tip)}</span>
              </div>
              <div className="flex items-center gap-2 w-full sm:w-auto min-w-[120px] sm:min-w-[180px] justify-end">
                <span
                  className={`text-sm sm:text-base font-semibold px-3 py-1 rounded-full flex items-center justify-center
                    ${tip.confidence >= 80 ? "bg-green-500/20 text-green-400 border-green-400" : ""}
                    ${tip.confidence >= 60 && tip.confidence < 80 ? "bg-yellow-400/20 text-yellow-300 border-yellow-300" : ""}
                    ${tip.confidence >= 40 && tip.confidence < 60 ? "bg-orange-400/20 text-orange-300 border-orange-300" : ""}
                    ${tip.confidence < 40 ? "bg-gray-500/20 text-gray-300 border-gray-300" : ""}
                    border border-solid`}
                >
                  {tip.confidence}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
