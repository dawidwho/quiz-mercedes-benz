import { useState } from "react";
import { InsightsCard } from "../components/InsightsCard";
import type { AIInsightResponse } from "../models/insights";

export default function PlanetsInsights() {
    const [entityName, setEntityName] = useState("");
    const [savedInsights, setSavedInsights] = useState<AIInsightResponse[]>([]);

    const handleInsightGenerated = (insight: AIInsightResponse) => {
        // Add the new insight to the saved insights
        setSavedInsights(prev => [insight, ...prev]);
    };

    const removeInsight = (index: number) => {
        setSavedInsights(prev => prev.filter((_, i) => i !== index));
    };

    const clearAllInsights = () => {
        setSavedInsights([]);
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Planets AI Insights
                    </h1>
                    <p className="text-gray-600">
                        Generate AI-powered insights about Star Wars planets
                    </p>
                </div>

                {/* Input Section */}
                <div className="mb-8">
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <label htmlFor="planetName" className="block text-sm font-medium text-gray-700 mb-2">
                            Enter Planet Name
                        </label>
                        <div className="flex space-x-4">
                            <input
                                type="text"
                                id="planetName"
                                value={entityName}
                                onChange={(e) => setEntityName(e.target.value)}
                                placeholder="e.g., Tatooine, Alderaan, Coruscant..."
                                className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-black placeholder-gray-500"
                            />
                        </div>
                    </div>
                </div>

                {/* Insights Card */}
                <div className="mb-8">
                    <InsightsCard
                        entityType="planets"
                        entityName={entityName}
                        onInsightGenerated={handleInsightGenerated}
                    />
                </div>

                {/* Saved Insights */}
                {savedInsights.length > 0 && (
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold text-gray-900">
                                Saved Insights ({savedInsights.length})
                            </h2>
                            <button
                                onClick={clearAllInsights}
                                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors duration-200"
                            >
                                Clear All
                            </button>
                        </div>

                        <div className="space-y-4">
                            {savedInsights.map((insight, index) => (
                                <div
                                    key={`${insight.name}-${insight.generated_at}-${index}`}
                                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
                                >
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center space-x-2 mb-2">
                                                <h3 className="text-lg font-medium text-gray-900">
                                                    {insight.name}
                                                </h3>
                                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${insight.confidence_score >= 0.8
                                                    ? 'bg-green-100 text-green-800'
                                                    : insight.confidence_score >= 0.6
                                                        ? 'bg-yellow-100 text-yellow-800'
                                                        : 'bg-red-100 text-red-800'
                                                    }`}>
                                                    {(insight.confidence_score * 100).toFixed(0)}% confidence
                                                </span>
                                            </div>
                                            <p className="text-gray-700 mb-2 line-clamp-3">
                                                {insight.insight}
                                            </p>
                                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                                                <span>Generated: {new Date(insight.generated_at).toLocaleString()}</span>
                                                <span>Model: {insight.model_version}</span>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => removeInsight(index)}
                                            className="ml-4 p-2 text-gray-400 hover:text-red-600 transition-colors duration-200"
                                            title="Remove insight"
                                        >
                                            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
} 