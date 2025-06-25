import type { AIInsightRequest, AIInsightResponse } from "../models/insights";

const BASE_URL = "http://localhost:8000/api";

export class InsightsApiClient {
    private async fetchData<T>(url: string): Promise<T> {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching AI insights:", error);
            throw error;
        }
    }

    private async postData<T>(url: string, data: any): Promise<T> {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error posting AI insights request:", error);
            throw error;
        }
    }

    async getAIInsight(request: AIInsightRequest): Promise<AIInsightResponse> {
        const url = `${BASE_URL}/simulate-ai-insight/`;
        return this.postData<AIInsightResponse>(url, request);
    }

    async getAIInsightByQuery(name: string, entityType: 'people' | 'planets'): Promise<AIInsightResponse> {
        const url = `${BASE_URL}/simulate-ai-insight/?name=${encodeURIComponent(name)}&entity_type=${entityType}`;
        return this.fetchData<AIInsightResponse>(url);
    }
}

// Create a singleton instance
export const insightsApiClient = new InsightsApiClient();
