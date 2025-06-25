import * as React from "react";
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router";
import { starWarsApiClient } from "../services/apiClientStarWars";
import EditionCard from "../components/EditionCard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorDisplay from "../components/ErrorDisplay";

export default function PeopleEdit() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [person, setPerson] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [saveAsCopyLoading, setSaveAsCopyLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const loadPerson = async () => {
        if (!id) return;
        try {
            setLoading(true);
            setError(null);
            const data = await starWarsApiClient.getPerson(id);
            setPerson(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred while loading the person');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadPerson();
    }, [id]);

    const handleChange = (name: string, value: any) => {
        setPerson((prev: any) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        try {
            await starWarsApiClient.updatePerson(id!, person);
            navigate(`/people/${id}`);
        } catch (err) {
            setError("Failed to save changes");
        } finally {
            setSaving(false);
        }
    };

    const handleSaveAsCopy = async (e: React.MouseEvent) => {
        e.preventDefault();
        setSaveAsCopyLoading(true);
        try {
            // Create a copy of the person data without the id
            const { id: _, ...personData } = person;
            const newPerson = await starWarsApiClient.createPerson(personData);
            navigate(`/people/${newPerson.id}`);
        } catch (err) {
            setError("Failed to create copy");
        } finally {
            setSaveAsCopyLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-4xl mx-auto">
                    <LoadingSpinner message="Loading person for editing..." />
                </div>
            </div>
        );
    }

    if (error || !person) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-4xl mx-auto">
                    <a href="/people" className="inline-flex items-center mb-6 text-blue-600 hover:text-blue-400 font-medium">
                        ← Back to People
                    </a>
                    <ErrorDisplay
                        error={error || 'Person not found'}
                        onRetry={loadPerson}
                    />
                </div>
            </div>
        );
    }

    return (
        <EditionCard
            title={`Edit ${person.name}`}
            backLink={{ to: `/people/${id}`, label: "Back to Detail" }}
            onChange={handleChange}
            onSubmit={handleSubmit}
            onSaveAsCopy={handleSaveAsCopy}
            loading={saving}
            saveAsCopyLoading={saveAsCopyLoading}
            sections={[
                {
                    title: "Physical Characteristics",
                    items: [
                        { label: "Height", name: "height", value: person.height, type: "number" },
                        { label: "Mass", name: "mass", value: person.mass, type: "number" },
                        { label: "Hair Color", name: "hair_color", value: person.hair_color },
                        { label: "Skin Color", name: "skin_color", value: person.skin_color },
                        { label: "Eye Color", name: "eye_color", value: person.eye_color },
                    ],
                },
                {
                    title: "Personal Information",
                    items: [
                        { label: "Birth Year", name: "birth_year", value: person.birth_year },
                        { label: "Gender", name: "gender", value: person.gender },
                    ],
                },
            ]}
        />
    );
} 