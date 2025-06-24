import * as React from "react";
import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router";
import { starWarsApiClient } from "../services/apiClientStarWars";
import { formatDate } from "../helpers/formatters";
import DetailCard from "../components/DetailCard";

export default function PeopleDetail() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [person, setPerson] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadPerson = async () => {
            if (!id) return;
            try {
                setLoading(true);
                const data = await starWarsApiClient.getPerson(id);
                setPerson(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred');
            } finally {
                setLoading(false);
            }
        };
        loadPerson();
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

    if (error || !person) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-4xl mx-auto">
                    <a href="/people" className="inline-flex items-center mb-6 text-blue-600 hover:text-blue-400 font-medium">
                        ← Back to People
                    </a>
                    <div className="bg-red-500 text-white p-4 rounded">
                        {error || 'Person not found'}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <Link to="/people" className="inline-flex items-center text-blue-600 hover:text-blue-400 font-medium">
                        ← Back to People
                    </Link>
                    <Link
                        to={`/people/${id}/edit`}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-5 py-2 rounded shadow"
                    >
                        Edit
                    </Link>
                </div>
                <DetailCard
                    title={person.name}
                    sections={[
                        {
                            title: "Physical Characteristics",
                            items: [
                                { label: "Height", value: `${person.height} cm` },
                                { label: "Mass", value: `${person.mass} kg` },
                                { label: "Hair Color", value: person.hair_color },
                                { label: "Skin Color", value: person.skin_color },
                                { label: "Eye Color", value: person.eye_color },
                            ],
                        },
                        {
                            title: "Personal Information",
                            items: [
                                { label: "Birth Year", value: person.birth_year },
                                { label: "Gender", value: person.gender },
                                { label: "Created", value: formatDate(person.created_at) },
                                { label: "Updated", value: formatDate(person.updated_at) },
                            ],
                        },
                    ]}
                />
            </div>
        </div>
    );
} 