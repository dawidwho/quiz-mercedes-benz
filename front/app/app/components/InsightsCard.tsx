import { useState } from "react";
import type { AIInsightResponse } from "../models/insights";
import { insightsApiClient } from "../services/apiClientInsights";

interface InsightsCardProps {
    entityType: 'people' | 'planets';
    entityName: string;
    onInsightGenerated?: (insight: AIInsightResponse) => void;
}

export function InsightsCard({ entityType, entityName, onInsightGenerated }: InsightsCardProps) {
    const [insight, setInsight] = useState<AIInsightResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const generateInsight = async () => {
        if (!entityName.trim()) {
            setError("Please enter a name first");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await insightsApiClient.getAIInsight({
                name: entityName.trim(),
                entity_type: entityType
            });

            setInsight(response);
            onInsightGenerated?.(response);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to generate insight");
        } finally {
            setLoading(false);
        }
    };

    const clearInsight = () => {
        setInsight(null);
        setError(null);
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-gray-900">
                    AI Insights for {entityType === 'people' ? 'Person' : 'Planet'}
                </h2>
                <div className="flex space-x-2">
                    <button
                        onClick={generateInsight}
                        disabled={loading || !entityName.trim()}
                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors duration-200"
                    >
                        {loading ? (
                            <div className="flex items-center space-x-2">
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                <span>Generating...</span>
                            </div>
                        ) : (
                            "Generate Insight"
                        )}
                    </button>
                    {insight && (
                        <button
                            onClick={clearInsight}
                            className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors duration-200"
                        >
                            Clear
                        </button>
                    )}
                </div>
            </div>

            {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
                    <p className="text-red-800">{error}</p>
                </div>
            )}

            {insight && (
                <div className="space-y-4">
                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                            <h3 className="text-lg font-semibold text-gray-900">
                                AI Analysis for {insight.name}
                            </h3>
                            <div className="flex items-center space-x-2">
                                <span className="text-sm text-gray-600">Confidence:</span>
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${insight.confidence_score >= 0.8
                                    ? 'bg-green-100 text-green-800'
                                    : insight.confidence_score >= 0.6
                                        ? 'bg-yellow-100 text-yellow-800'
                                        : 'bg-red-100 text-red-800'
                                    }`}>
                                    {(insight.confidence_score * 100).toFixed(0)}%
                                </span>
                            </div>
                        </div>

                        <div className="prose prose-sm max-w-none">
                            <p className="text-gray-700 leading-relaxed">{insight.insight}</p>
                        </div>

                        <div className="mt-4 pt-4 border-t border-blue-200 flex items-center justify-between text-sm text-gray-500">
                            <span>Generated: {new Date(insight.generated_at).toLocaleString()}</span>
                            <span>Model: {insight.model_version}</span>
                        </div>
                    </div>
                </div>
            )}

            {!insight && !loading && (
                <div className="text-center py-8 text-gray-500">
                    <div className="mb-4">
                        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                    </div>
                    <p className="text-lg font-medium">Ready to generate AI insights</p>
                    <p className="text-sm">Click "Generate Insight" to get an AI-powered analysis</p>
                </div>
            )}
        </div>
    );
} 