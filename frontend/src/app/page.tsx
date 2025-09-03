import { PredictionItem, Match } from "@/components/ui/PredictionItem";
import { getPredictions } from "@/services/api";

export default async function Home() {
  const prediction = await getPredictions();

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">
        Football Predictions
      </h1>
      <ul>
        {prediction.map((match: Match) => (
          <PredictionItem key={match.match_id} match={match} />
        ))}
      </ul>
    </main>
  );
}
