import * as React from "react";
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router";
import { starWarsApiClient } from "../services/apiClientStarWars";
import EditionCard from "../components/EditionCard";

export default function PlanetsEdit() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [planet, setPlanet] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [saveAsCopyLoading, setSaveAsCopyLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadPlanet = async () => {
            if (!id) return;
            try {
                setLoading(true);
                const data = await starWarsApiClient.getPlanet(id);
                setPlanet(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred');
            } finally {
                setLoading(false);
            }
        };
        loadPlanet();
    }, [id]);

    const handleChange = (name: string, value: any) => {
        setPlanet((prev: any) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        try {
            await starWarsApiClient.updatePlanet(id!, planet);
            navigate(`/planets/${id}`);
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
            // Create a copy of the planet data without the id
            const { id: _, ...planetData } = planet;
            const newPlanet = await starWarsApiClient.createPlanet(planetData);
            navigate(`/planets/${newPlanet.id}`);
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
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white"></div>
                    </div>
                </div>
            </div>
        );
    }

    if (error || !planet) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-4xl mx-auto">
                    <a href="/planets" className="inline-flex items-center mb-6 text-blue-600 hover:text-blue-400 font-medium">
                        ← Back to Planets
                    </a>
                    <div className="bg-red-500 text-white p-4 rounded">
                        {error || 'Planet not found'}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <EditionCard
            title={`Edit ${planet.name}`}
            backLink={{ to: `/planets/${id}`, label: "Back to Detail" }}
            onChange={handleChange}
            onSubmit={handleSubmit}
            onSaveAsCopy={handleSaveAsCopy}
            loading={saving}
            saveAsCopyLoading={saveAsCopyLoading}
            sections={[
                {
                    title: "Physical Characteristics",
                    items: [
                        { label: "Diameter", name: "diameter", value: planet.diameter, type: "number" },
                        { label: "Rotation Period", name: "rotation_period", value: planet.rotation_period, type: "number" },
                        { label: "Orbital Period", name: "orbital_period", value: planet.orbital_period, type: "number" },
                        { label: "Gravity", name: "gravity", value: planet.gravity },
                        { label: "Surface Water", name: "surface_water", value: planet.surface_water, type: "number" },
                    ],
                },
                {
                    title: "Environmental Information",
                    items: [
                        { label: "Climate", name: "climate", value: planet.climate },
                        { label: "Terrain", name: "terrain", value: planet.terrain },
                        { label: "Population", name: "population", value: planet.population, type: "number" },
                    ],
                },
            ]}
        />
    );
} 