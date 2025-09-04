import { ReactNode } from "react";

import ConfidenceBar from "@/components/ui/confidenceBar";

interface PredictionCardProps {
  team1: string;
  team2: string;
  tip: string;
  confidence: number;
}

export default function PredictionCard({ team1, team2, tip, confidence }: PredictionCardProps) {
  return (
    <div className="prediction-card p-6 rounded-2xl flex flex-col justify-between h-full bg-slate-800/50 border border-white/10">
      <div>
        <div className="flex justify-between items-start">
          <h3 className="text-xl font-bold text-white">{team1} vs {team2}</h3>
        </div>
        <p className="text-cyan-400 mt-2">{tip}</p>
      </div>
      <ConfidenceBar confidence={confidence} />
    </div>
  );
}
