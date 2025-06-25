export interface AIInsightRequest {
    name: string;
    entity_type: 'people' | 'planets';
}

export interface AIInsightResponse {
    name: string;
    entity_type: 'people' | 'planets';
    insight: string;
    confidence_score: number;
    generated_at: string;
    model_version: string;
} 