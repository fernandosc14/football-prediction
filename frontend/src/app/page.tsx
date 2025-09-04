import Header from "@/components/header";
import { PredictionItem, Match } from "@/components/ui/predictionItem";
import { getPredictions } from "@/services/api";

export const dynamic = 'force-dynamic';

export default async function Home() {
  const prediction = await getPredictions();

  return (
    <div className="min-h-screen flex flex-col bg-primary text-contrast">
      <Header />
      <main className="flex-1 p-8 max-w-3xl mx-auto w-full">
        <h1 className="text-2xl font-bold mb-4">Football Predictions</h1>
        <ul>
          {prediction.map((match: Match) => (
            <PredictionItem key={match.match_id} match={match} />
          ))}
        </ul>
      </main>
      {/* <Footer />  // TODO */}
    </div>
  );
}
