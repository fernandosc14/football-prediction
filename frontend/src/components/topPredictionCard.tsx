"use client";

import { ReactNode } from "react";
import { Trophy, BarChart2, Shuffle, Users } from "lucide-react";

import ConfidenceBar from "@/components/ui/confidenceBar";

interface Tip {
  name: string;
  confidence: number;
  class?: number;
}

interface TopPredictionCardProps {
  team1: string;
  team2: string;
  tips: Tip[];
  icon?: ReactNode;
  date?: string;
}

export default function TopPredictionCard({ team1, team2, tips = [], date}: TopPredictionCardProps) {
  return (
  <section className="relative top-prediction-card max-w-2xl mx-auto overflow-hidden shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] rounded-2xl p-6 bg-gradient-to-br from-slate-800/50 to-gray-900/50 backdrop-blur-lg">
      <div
        className="absolute left-0 top-0 w-full h-1.5 rounded-t-2xl"
        style={{
          background: "linear-gradient(90deg, #3b82f6 0%, #a855f7 60%, #ec4899 100%)"
        }}
      />
      <div className="flex flex-col gap-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Top Prediction</span>
        </div>
        <div className="flex flex-col mb-2">
          <span className="text-3xl md:text-4xl font-extrabold text-white tracking-wide drop-shadow">
            {team1} <span className="text-pink-400">vs</span> {team2}
          </span>
          {date && (
            <span className="text-sm text-gray-300 mt-1">{date}</span>
          )}
        </div>
        <div className="flex flex-col gap-4 mt-4">
          {tips.map((tip, idx) => {
            let TipIcon = Trophy;
            if (tip.name.toLowerCase().includes("over 2.5") || tip.name.toLowerCase().includes("over 1.5")) {
              TipIcon = BarChart2;
            } else if (tip.name.toLowerCase().includes("double chance")) {
              TipIcon = Shuffle;
            } else if (tip.name.toLowerCase().includes("btts")) {
              TipIcon = Users;
            } else if (tip.name.toLowerCase().includes("winner")) {
              TipIcon = Trophy;
            }
            return (
              <div key={idx} className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-4 p-2 rounded border-b border-b-gray-700/80">
                <div className="flex items-center gap-2 mb-2 sm:mb-0">
                  <TipIcon className="w-5 h-5 text-cyan-300" />
                  <span className="font-semibold text-white drop-shadow text-base">{tip.name}</span>
                  {typeof tip.class !== "undefined" && (
                    <span className="ml-2 px-2 py-0.5 rounded bg-cyan-700 text-white text-sm font-bold border border-cyan-500">
                      {(() => {
                        const name = tip.name.toLowerCase();
                        if (name === "winner") {
                          if (tip.class === 0) return `${team1}`;
                          if (tip.class === 1) return "Draw";
                          if (tip.class === 2) return `${team2}`;
                        }
                        if (name === "double chance") {
                          if (tip.class === 0) return "1X";
                          if (tip.class === 1) return "X2";
                          if (tip.class === 2) return "12";
                        }
                        if (name === "over 2.5") {
                          if (tip.class === 0) return "No";
                          if (tip.class === 1) return "Yes";
                        }
                        if (name === "over 1.5") {
                          if (tip.class === 0) return "No";
                          if (tip.class === 1) return "Yes";
                        }
                        if (name === "btts") {
                          if (tip.class === 0) return "No";
                          if (tip.class === 1) return "Yes";
                        }
                        return tip.class;
                      })()}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2 w-full sm:w-auto min-w-[180px] sm:min-w-[220px] justify-end">
                  <div className="w-full sm:w-56 md:w-72">
                    <ConfidenceBar confidence={tip.confidence} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
