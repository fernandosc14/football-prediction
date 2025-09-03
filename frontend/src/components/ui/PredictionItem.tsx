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

const predictionFields: Array<{ key: keyof Prediction; label: string }> = [
    { key: "winner", label: "Winner" },
    { key: "over_2_5", label: "Over 2.5 Goals" },
    { key: "over_1_5", label: "Over 1.5 Goals" },
    { key: "double_chance", label: "Double Chance" },
    { key: "btts", label: "Both Teams to Score" },
] as const;

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
                {predictionFields.map(({key, label}) => {
                    const field = predictions[key];
                    return (
                        <li key={key}>
                            {label}: {classToText(key, field.class)}{" "}
                            <span className="text-gray-500">({(field.confidence * 100).toFixed(0)}%)</span>
                        </li>
                    );
                })}
            </ul>
        </li>
    );
}
