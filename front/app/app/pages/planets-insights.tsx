import { useState, useRef } from "react";
import { InsightsCard, type InsightsCardRef } from "../components/InsightsCard";
import type { AIInsightResponse } from "../models/insights";

export default function PlanetsInsights() {
    const [entityName, setEntityName] = useState("");
    const [savedInsights, setSavedInsights] = useState<AIInsightResponse[]>([]);
    const insightsCardRef = useRef<InsightsCardRef>(null);

    const handleInsightGenerated = (insight: AIInsightResponse) => {
        // Add the new insight to the saved insights
        setSavedInsights(prev => [insight, ...prev]);
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && entityName.trim()) {
            insightsCardRef.current?.generateInsight();
        }
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

                {/* Search Input Section */}
                <div className="mb-8">
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <label htmlFor="planetName" className="block text-sm font-medium text-gray-700 mb-2">
                            Search for a Planet
                        </label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                            </div>
                            <input
                                type="text"
                                id="planetName"
                                value={entityName}
                                onChange={(e) => setEntityName(e.target.value)}
                                onKeyDown={handleKeyPress}
                                placeholder="e.g., Tatooine, Alderaan, Coruscant..."
                                className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-black placeholder-gray-500 shadow-sm"
                            />
                            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                                <button
                                    onClick={() => insightsCardRef.current?.generateInsight()}
                                    disabled={!entityName.trim()}
                                    className="p-2 text-gray-400 hover:text-blue-600 disabled:text-gray-300 disabled:cursor-not-allowed transition-colors duration-200"
                                    title="Generate insight"
                                >
                                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                        <p className="mt-2 text-sm text-gray-500">
                            Press Enter or click the lightning icon to generate insights
                        </p>
                    </div>
                </div>

                {/* Insights Card */}
                <div className="mb-8">
                    <InsightsCard
                        ref={insightsCardRef}
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