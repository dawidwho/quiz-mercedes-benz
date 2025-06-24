import * as React from "react";
import { Link } from "react-router";

interface EditionSection {
    title: string;
    items: EditionItem[];
}

interface EditionItem {
    label: string;
    name: string;
    value: any;
    type?: string; // 'text', 'number', 'select', etc.
    options?: { label: string; value: any }[]; // for select
    onChange?: (e: React.ChangeEvent<any>) => void;
}

interface EditionCardProps {
    title: string;
    sections: EditionSection[];
    backLink?: { to: string; label: string };
    onChange: (name: string, value: any) => void;
    onSubmit: (e: React.FormEvent) => void;
    submitLabel?: string;
    loading?: boolean;
}

export default function EditionCard({ title, sections, backLink, onChange, onSubmit, submitLabel = "Save", loading }: EditionCardProps) {
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
                {backLink && (
                    <Link to={backLink.to} className="inline-flex items-center mb-6 text-blue-600 hover:text-blue-400 font-medium">
                        ← {backLink.label}
                    </Link>
                )}
                <form onSubmit={onSubmit}>
                    <div className="bg-white text-gray-900 p-8 rounded-lg shadow-lg">
                        <h1 className="text-4xl font-bold mb-6 text-gray-900">{title}</h1>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            {sections.map((section, idx) => (
                                <div key={idx}>
                                    <h2 className="text-xl font-semibold mb-4 text-blue-900">{section.title}</h2>
                                    <div className="space-y-4">
                                        {section.items.map((item, i) => (
                                            <div key={i}>
                                                <label className="block font-semibold mb-1" htmlFor={item.name}>{item.label}:</label>
                                                {item.type === "select" && item.options ? (
                                                    <select
                                                        id={item.name}
                                                        name={item.name}
                                                        value={item.value}
                                                        onChange={item.onChange || ((e) => onChange(item.name, e.target.value))}
                                                        className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
                                                    >
                                                        {item.options.map((opt) => (
                                                            <option key={opt.value} value={opt.value}>{opt.label}</option>
                                                        ))}
                                                    </select>
                                                ) : (
                                                    <input
                                                        id={item.name}
                                                        name={item.name}
                                                        type={item.type || "text"}
                                                        value={item.value}
                                                        onChange={item.onChange || ((e) => onChange(item.name, e.target.value))}
                                                        className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
                                                    />
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="mt-8 flex justify-end">
                            <button
                                type="submit"
                                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded shadow disabled:opacity-50"
                                disabled={loading}
                            >
                                {loading ? "Saving..." : submitLabel}
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
} 