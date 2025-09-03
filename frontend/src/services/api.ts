
export async function getPredictions() {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/predictions`);
    if (!response.ok) throw new Error('Failed to fetch predictions');
    return response.json();
}

export async function getPredictionById(matchId: string | number) {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/predictions/${matchId}`);
    if (!response.ok) throw new Error('Prediction not found');
    return response.json();
}
