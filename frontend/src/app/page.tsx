import { Trophy } from "lucide-react";
import { getPredictions } from "@/services/api";

import Header from "@/components/header";
import InfoCard from "@/components/infoCards";
import TopPredictionCard from "@/components/topPredictionCard";
import PredictionCard from "@/components/predictionCard";

export const dynamic = 'force-dynamic';

export default async function Home() {
  const prediction = await getPredictions();

  const topMatch = [
    { team1: "Team A", team2: "Team B", tip: "Over 2.5", confidence: 75, icon: <Trophy /> },
  ]

  const matches = [
    { team1: "Team A", team2: "Team B", tip: "Over 2.5", confidence: 75},
    { team1: "Team C", team2: "Team D", tip: "BTTS", confidence: 60},
    { team1: "Team C", team2: "Team D", tip: "BTTS", confidence: 80},
    { team1: "Team C", team2: "Team D", tip: "BTTS", confidence: 50},
    { team1: "Team C", team2: "Team D", tip: "BTTS", confidence: 60},
    { team1: "Team C", team2: "Team D", tip: "BTTS", confidence: 60},
  ];

  return (
    <div className="min-h-screen container mx-auto px-4 py-8 md:py-16">
      <Header />
      <main className="space-y-12 md:space-y-16">
        <InfoCard />
        <TopPredictionCard
          team1={topMatch[0].team1}
          team2={topMatch[0].team2}
          tip={topMatch[0].tip}
          confidence={topMatch[0].confidence}
          icon={topMatch[0].icon}
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {matches.map((match, idx) => (
            <PredictionCard
              key={idx}
              team1={match.team1}
              team2={match.team2}
              tip={match.tip}
              confidence={match.confidence}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
