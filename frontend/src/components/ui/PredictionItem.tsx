export type Match = {
    match_id: string | number;
    home_team: string;
    away_team: string;
    predictions: Prediction;
}

type PredictionField = {
    class: number;
    confidence: number;
};

type Prediction = {
    winner: PredictionField;
    over_2_5: PredictionField;
    over_1_5: PredictionField;
    double_chance: PredictionField;
    btts: PredictionField;
};

export function PredictionItem({ match } : { match: Match}) {
    const { home_team, away_team, predictions } = match;
    const classToText = (key: string, value: number) => {
        if (["btts", "over_2_5", "over_1_5"].includes(key)) {
            return value === 1 ? "Yes" : "No";
        }
        if (["winner"].includes(key)) {
            return value === 0 ? home_team : value === 1 ? "Draw" : away_team;
        }
        if (["double_chance"].includes(key)) {
            return value === 0 ? "1X" : "X2";
        }
        return value;
    };
    return (
        <li className="mb-2">
            <strong>{home_team} vs {away_team}</strong>
            <ul className="ml-4 list-disc">
                {Object.entries(predictions).map(([key, value]) => {
                    const field = value as PredictionField;
                    return (
                        <li key={key}>
                            {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}: {classToText(key, field.class)}{' '}
                            <span className="text-gray-500">({(field.confidence * 100).toFixed(0)}%)</span>
                        </li>
                    );
                })}
            </ul>
        </li>
    );
}
