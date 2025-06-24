import * as React from "react";
import { Link } from "react-router";

interface DetailSection {
    title: string;
    items: { label: string; value: React.ReactNode }[];
}

interface DetailCardProps {
    title: string;
    sections: DetailSection[];
    backLink?: { to: string; label: string };
}

export default function DetailCard({ title, sections, backLink }: DetailCardProps) {
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
                {backLink && (
                    <Link to={backLink.to} className="inline-flex items-center mb-6 text-blue-600 hover:text-blue-400 font-medium">
                        ← {backLink.label}
                    </Link>
                )}
                <div className="bg-white text-gray-900 p-8 rounded-lg shadow-lg">
                    <h1 className="text-4xl font-bold mb-6 text-gray-900">{title}</h1>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {sections.map((section, idx) => (
                            <div key={idx}>
                                <h2 className="text-xl font-semibold mb-4 text-blue-900">{section.title}</h2>
                                <div className="space-y-2">
                                    {section.items.map((item, i) => (
                                        <p key={i}>
                                            <span className="font-semibold">{item.label}:</span> {item.value}
                                        </p>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
} 