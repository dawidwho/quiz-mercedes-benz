import * as React from "react";
import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router";
import { starWarsApiClient } from "../services/apiClientStarWars";
import { formatDate } from "../helpers/formatters";
import DetailCard from "../components/DetailCard";

export default function PlanetsDetail() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [planet, setPlanet] = useState<any>(null);
    const [loading, setLoading] = useState(true);
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
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <Link to="/planets" className="inline-flex items-center text-blue-600 hover:text-blue-400 font-medium">
                        ← Back to Planets
                    </Link>
                    <Link
                        to={`/planets/${id}/edit`}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-5 py-2 rounded shadow"
                    >
                        Edit
                    </Link>
                </div>
                <DetailCard
                    title={planet.name}
                    sections={[
                        {
                            title: "Physical Characteristics",
                            items: [
                                { label: "Diameter", value: `${planet.diameter} km` },
                                { label: "Rotation Period", value: `${planet.rotation_period} hours` },
                                { label: "Orbital Period", value: `${planet.orbital_period} days` },
                                { label: "Gravity", value: planet.gravity },
                                { label: "Surface Water", value: `${planet.surface_water}%` },
                            ],
                        },
                        {
                            title: "Environmental Information",
                            items: [
                                { label: "Climate", value: planet.climate },
                                { label: "Terrain", value: planet.terrain },
                                { label: "Population", value: planet.population?.toLocaleString() || 'Unknown' },
                                { label: "Created", value: formatDate(planet.created_at) },
                                { label: "Updated", value: formatDate(planet.updated_at) },
                            ],
                        },
                    ]}
                />
            </div>
        </div>
    );
} 