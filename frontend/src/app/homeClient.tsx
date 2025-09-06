"use client";
import { useEffect, useState } from "react";

import Header from "@/components/header";
import InfoCard from "@/components/infoCards";
import TopPredictionCard from "@/components/topPredictionCard";
import PredictionCard from "@/components/predictionCard";
import StatsAverage, { StatsType } from "@/components/StatsAverage";
import CardSkeleton from "@/components/CardSkeleton";
import StatsSkeleton from "@/components/StatsSkeleton";

import { getPredictions, getStats, getLastUpdate } from "@/services/api";

export default function HomeClient() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const [predictions, setPredictions] = useState<any[]>([]);
  const [stats, setStats] = useState<StatsType | null>(null);
  const [lastUpdate, setLastUpdate] = useState("");

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError("");
      try {
        const [preds, statsData, lastUpdateObj] = await Promise.all([
          getPredictions(),
          getStats(),
          getLastUpdate(),
        ]);
        console.log("Predictions:", preds);
        console.log("Stats:", statsData);
        console.log("LastUpdate:", lastUpdateObj);
        setPredictions(preds || []);
        setStats(statsData || null);
        const lastUpdateRaw = lastUpdateObj?.last_update;
        if (lastUpdateRaw) {
          const dateObj = new Date(lastUpdateRaw.replace(" ", "T"));
          setLastUpdate(
            dateObj.toLocaleDateString("pt-PT", { day: "2-digit", month: "2-digit", year: "numeric" }) +
              " " +
              dateObj.toLocaleTimeString("pt-PT", { hour: "2-digit", minute: "2-digit" })
          );
        }
        // Só mostra erro se todos os dados vierem vazios
        if ((!preds || preds.length === 0) && (!statsData || Object.keys(statsData).length === 0)) {
          setError("No data available.");
        }
      } catch (err: any) {
        setError("Failed to load data. Please try again later.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const tips = [
    { key: "winner", label: "Winner" },
    { key: "over_2_5", label: "Over 2.5" },
    { key: "over_1_5", label: "Over 1.5" },
    { key: "double_chance", label: "Double Chance" },
    { key: "btts", label: "BTTS" },
  ];

  const topMatch = predictions?.length > 0
    ? {
        team1: predictions[0].home_team,
        team2: predictions[0].away_team,
        date: predictions[0].date,
        tips: tips.map((tip) => {
          const tipData = predictions[0].predictions[tip.key];
          return {
            name: tip.label,
            confidence: Math.round(tipData.confidence * 100),
            class: tipData.class
          };
        })
      }
    : undefined;

  const matches = predictions?.length > 1
    ? predictions.slice(1).map((pred: any) => ({
        team1: pred.home_team,
        team2: pred.away_team,
        date: pred.date,
        tips: tips.map((tip) => {
          const tipData = pred.predictions[tip.key];
          return {
            name: tip.label,
            confidence: Math.round(tipData.confidence * 100),
            class: tipData.class
          };
        })
      }))
    : [];

  if (loading) {
    return (
      <div className="min-h-screen container mx-auto px-4 py-8 md:py-16">
        <Header />
        <main className="space-y-12 md:space-y-16">
          <InfoCard />
          <div className="mb-8">
            <StatsSkeleton />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(3)].map((_, idx) => (
              <CardSkeleton key={idx} />
            ))}
          </div>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center text-center px-4">
        <Header />
        <div className="mt-12">
          <span className="text-lg text-red-400 font-semibold">{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen container mx-auto px-4 py-8 md:py-16">
      <Header />
      <main className="space-y-12 md:space-y-16">
        <InfoCard />
        {stats && Object.keys(stats).length > 0 && (
          <div className="mb-8">
            <StatsAverage stats={stats} />
          </div>
        )}
        {topMatch && (
          <TopPredictionCard
            team1={topMatch.team1}
            team2={topMatch.team2}
            tips={topMatch.tips}
            date={topMatch.date}
          />
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {matches.map((match, idx) => (
            <PredictionCard
              key={idx}
              team1={match.team1}
              team2={match.team2}
              date={match.date}
              tips={match.tips}
            />
          ))}
        </div>
        <div className="w-full text-center mt-10">
          {lastUpdate && (
            <span className="text-xs text-gray-400">Last Update: {lastUpdate}</span>
          )}
        </div>
      </main>
    </div>
  );
}
