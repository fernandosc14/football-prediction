function getApiUrl(): string {
    const url = process.env.NEXT_PUBLIC_API_URL;
    if (!url) {
        throw new Error("NEXT_PUBLIC_API_URL is not defined. Please set it in your environment variables.");
    }
    return url;
}

async function fetchWithTimeout(
    url: string,
    options: RequestInit = {},
    timeout = 8000
) {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);

    const headers = {
        ...(options.headers || {})
    };

    try {
        const response = await fetch(url, { ...options, headers, signal: controller.signal });

        let data;
        try {
            data = await response.json();
        } catch {
            throw new Error(`Failed to parse JSON from ${url}`);
        }

        if (!response.ok) {
            throw new Error(
                `Fetch error: ${response.status} ${response.statusText} - ${JSON.stringify(data)}`
            );
        }

        return data;
    } catch (err: any) {
        if (err.name === "AbortError") {
            throw new Error(`Request to ${url} timed out after ${timeout}ms`);
        }
        throw err;
    } finally {
        clearTimeout(id);
    }
}

export async function getPredictions() {
  return fetchWithTimeout("/api/predictions");
}

export async function getStats() {
  return fetchWithTimeout("/api/stats");
}

export async function getLastUpdate() {
  return fetchWithTimeout("/api/last-update");
}
