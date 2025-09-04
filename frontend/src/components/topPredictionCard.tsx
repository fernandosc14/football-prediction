"use client";

import { ReactNode } from "react";
import { Trophy } from "lucide-react";

import ConfidenceBar from "@/components/ui/confidenceBar";

interface TopPredictionCardProps {
  team1: string;
  team2: string;
  tip: string;
  confidence: number;
  icon?: ReactNode;
}

export default function TopPredictionCard({ team1, team2, tip, confidence, icon }: TopPredictionCardProps) {
  return (
    <section className="relative top-prediction-card max-w-3xl mx-auto overflow-hidden shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] rounded-2xl p-8 bg-gradient-to-br from-slate-800/50 to-gray-900/50 backdrop-blur-lg">
      <div
        className="absolute left-0 top-0 w-full h-1.5 rounded-t-2xl"
        style={{
          background: "linear-gradient(90deg, #3b82f6 0%, #a855f7 60%, #ec4899 100%)"
        }}
      />
      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
        <div className="flex-grow">
          <div className="flex items-center gap-3 mb-4">
            <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Top Prediction</span>
          </div>
          <div className="text-2xl md:text-3xl font-bold text-white">{team1} vs {team2}</div>
          <div className="flex items-center gap-2 mt-2 text-lg text-cyan-300">
            {icon || <Trophy className="w-5 h-5" />}
            <span>{tip}</span>
          </div>
        </div>
        <div className="w-full md:w-1/3 mt-6 md:mt-0 md:pl-8">
          <ConfidenceBar confidence={confidence} />
        </div>
      </div>
    </section>
  );
}
