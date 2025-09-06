import { getPredictions, getStats, getLastUpdate } from "@/services/api";

import Header from "@/components/header";
import InfoCard from "@/components/infoCards";
import TopPredictionCard from "@/components/topPredictionCard";
import PredictionCard from "@/components/predictionCard";
import StatsAverage, { StatsType } from "@/components/statsAverage";


export default async function Home() {

  const predictions = await getPredictions();
  const stats: StatsType = await getStats();
  const lastUpdateObj = await getLastUpdate();
  const lastUpdateRaw = lastUpdateObj?.last_update;
  let lastUpdate = "";
  if (lastUpdateRaw) {
    const dateObj = new Date(lastUpdateRaw.replace(" ", "T"));
    lastUpdate = dateObj.toLocaleDateString("pt-PT", { day: "2-digit", month: "2-digit", year: "numeric" }) +
      " " +
      dateObj.toLocaleTimeString("pt-PT", { hour: "2-digit", minute: "2-digit" });
  }

  type PredictionApi = {
    match_id: number;
    date: string;
    time: string;
    league: string;
    home_team: string;
    away_team: string;
    odds: Record<string, number>;
    predictions: {
      winner: { class: number; confidence: number };
      over_2_5: { class: number; confidence: number };
      over_1_5: { class: number; confidence: number };
      double_chance: { class: number; confidence: number };
      btts: { class: number; confidence: number };
    };
    finished: boolean;
  };

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

  const matches: Array<{
    team1: string;
    team2: string;
    date: string;
    tips: Array<{ name: string; confidence: number; class?: number }>;
  }> = predictions?.length > 1
    ? predictions.slice(1).map((pred: PredictionApi) => ({
        team1: pred.home_team,
        team2: pred.away_team,
        date: pred.date,
        tips: tips.map((tip) => {
          const tipData = pred.predictions[tip.key as keyof typeof pred.predictions];
          return {
            name: tip.label,
            confidence: Math.round(tipData.confidence * 100),
            class: tipData.class
          };
        })
      }))
    : [];

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
              <span className="text-xs text-gray-400">Last update: {lastUpdate}</span>
            )}
          </div>
      </main>
    </div>
  );
}
