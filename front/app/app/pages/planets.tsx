import type { Route } from "./+types/planets";
import * as React from "react";
import { useEffect, useState, useCallback } from "react";
import { CircularProgress, Alert, TextField, Select, MenuItem, FormControl, InputLabel, Button, Box, Typography } from "@mui/material";
import { starWarsApiClient } from "../services/apiClientStarWars";
import { formatDate } from "../helpers/formatters";
import { Table, Thead, Tbody, Tr, Th, Td } from "react-super-responsive-table";
import "react-super-responsive-table/dist/SuperResponsiveTableStyle.css";
import StarWarsTable from "../components/StarWarsTable";
import type { StarWarsTableColumn } from "../components/StarWarsTable";

export function meta({ }: Route.MetaArgs) {
    return [
        { title: "Planets - Quiz Mercedes-Benz" },
        { name: "description", content: "Explore Star Wars planets" },
    ];
}

export default function Planets() {
    const [planets, setPlanets] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [totalCount, setTotalCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const [pageSize, setPageSize] = useState(15);
    const [sortField, setSortField] = useState<string>('');
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
    const [filterField, setFilterField] = useState<string>('');
    const [filterValue, setFilterValue] = useState<string>('');

    const loadPlanets = useCallback(async () => {
        try {
            setLoading(true);

            const params: any = {
                page: currentPage,
                size: pageSize
            };

            if (filterField && filterValue) {
                params.filterField = filterField;
                params.filterValue = filterValue;
            }

            if (sortField) {
                params.sortBy = sortField;
                params.sortOrder = sortOrder;
            }

            const data = await starWarsApiClient.getPlanets(params);

            if (data && Array.isArray(data.items)) {
                const planetsWithIds = data.items.map((planet: any, index: number) => ({
                    ...planet,
                    id: index + 1,
                }));
                setPlanets(planetsWithIds);
                setTotalCount(data.total || 0);
            } else {
                setPlanets([]);
                setTotalCount(0);
                setError('No data available from the API');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
            setPlanets([]);
            setTotalCount(0);
        } finally {
            setLoading(false);
        }
    }, [currentPage, pageSize, sortField, sortOrder, filterField, filterValue]);

    useEffect(() => {
        loadPlanets();
    }, [loadPlanets]);

    const handleSort = (field: string) => {
        if (sortField === field) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            setSortField(field);
            setSortOrder('asc');
        }
        setCurrentPage(1);
    };

    const handleFilter = () => {
        setCurrentPage(1);
    };

    const clearFilter = () => {
        setFilterField('');
        setFilterValue('');
        setCurrentPage(1);
    };

    const totalPages = Math.ceil(totalCount / pageSize);

    const columns: StarWarsTableColumn[] = [
        { key: 'name', label: 'Name', sortable: true },
        { key: 'rotation_period', label: 'Rotation Period', sortable: true },
        { key: 'orbital_period', label: 'Orbital Period', sortable: true },
        { key: 'diameter', label: 'Diameter (km)', sortable: true },
        { key: 'climate', label: 'Climate', sortable: true },
        { key: 'gravity', label: 'Gravity', sortable: true },
        { key: 'terrain', label: 'Terrain', sortable: true },
        { key: 'surface_water', label: 'Surface Water (%)', sortable: true },
        { key: 'population', label: 'Population', sortable: true },
        { key: 'created_at', label: 'Created', sortable: true, render: (row) => formatDate(row.created_at) },
        { key: 'updated_at', label: 'Updated', sortable: true, render: (row) => formatDate(row.updated_at) },
    ];

    if (loading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-6xl mx-auto">
                    <header className="mb-8">
                        <h1 className="text-3xl font-bold text-white mb-4">Star Wars Planets</h1>
                        <p className="text-gray-300 text-lg">
                            Discover and learn about planets from the Star Wars universe
                        </p>
                    </header>
                    <div className="flex justify-center items-center h-64">
                        <CircularProgress />
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-6xl mx-auto">
                    <header className="mb-8">
                        <h1 className="text-3xl font-bold text-white mb-4">Star Wars Planets</h1>
                        <p className="text-gray-300 text-lg">
                            Discover and learn about planets from the Star Wars universe
                        </p>
                    </header>
                    <Alert severity="error">{error}</Alert>
                </div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-6xl mx-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-4">Star Wars Planets</h1>
                    <p className="text-gray-300 text-lg">
                        Discover and learn about planets from the Star Wars universe
                    </p>
                </header>

                {/* Filter Controls */}
                <Box sx={{ mb: 3, p: 2, bgcolor: 'rgba(255, 255, 255, 0.05)', borderRadius: 1 }}>
                    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
                        <FormControl sx={{ minWidth: 120 }}>
                            <InputLabel sx={{ color: 'white' }}>Filter Field</InputLabel>
                            <Select
                                value={filterField}
                                onChange={(e) => setFilterField(e.target.value)}
                                sx={{ color: 'white', '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255, 255, 255, 0.3)' } }}
                            >
                                <MenuItem value="name">Name</MenuItem>
                                <MenuItem value="rotation_period">Rotation Period</MenuItem>
                                <MenuItem value="orbital_period">Orbital Period</MenuItem>
                                <MenuItem value="diameter">Diameter</MenuItem>
                                <MenuItem value="climate">Climate</MenuItem>
                                <MenuItem value="gravity">Gravity</MenuItem>
                                <MenuItem value="terrain">Terrain</MenuItem>
                                <MenuItem value="surface_water">Surface Water</MenuItem>
                                <MenuItem value="population">Population</MenuItem>
                            </Select>
                        </FormControl>
                        <TextField
                            label="Filter Value"
                            value={filterValue}
                            onChange={(e) => setFilterValue(e.target.value)}
                            sx={{
                                color: 'white',
                                '& .MuiOutlinedInput-root': {
                                    '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                                    '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                                    '& input': { color: 'white' },
                                    '& label': { color: 'rgba(255, 255, 255, 0.7)' }
                                }
                            }}
                        />
                        <Button variant="contained" onClick={handleFilter} sx={{ bgcolor: '#1976d2' }}>
                            Filter
                        </Button>
                        <Button variant="outlined" onClick={clearFilter} sx={{ borderColor: 'rgba(255, 255, 255, 0.3)', color: 'white' }}>
                            Clear
                        </Button>
                    </Box>
                </Box>

                {/* Responsive Table */}
                <StarWarsTable
                    columns={columns}
                    data={planets}
                    sortField={sortField}
                    sortOrder={sortOrder}
                    onSort={handleSort}
                />

                {/* Pagination */}
                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'white' }}>
                    <Typography>
                        Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, totalCount)} of {totalCount} results
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                        <FormControl sx={{ minWidth: 80 }}>
                            <Select
                                value={pageSize}
                                onChange={(e) => setPageSize(Number(e.target.value))}
                                sx={{ color: 'white', '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255, 255, 255, 0.3)' } }}
                            >
                                <MenuItem value={15}>15</MenuItem>
                                <MenuItem value={25}>25</MenuItem>
                                <MenuItem value={50}>50</MenuItem>
                            </Select>
                        </FormControl>
                        <Button
                            variant="outlined"
                            disabled={currentPage === 1}
                            onClick={() => setCurrentPage(currentPage - 1)}
                            sx={{ borderColor: 'rgba(255, 255, 255, 0.3)', color: 'white' }}
                        >
                            Previous
                        </Button>
                        <Typography sx={{ px: 2 }}>
                            Page {currentPage} of {totalPages}
                        </Typography>
                        <Button
                            variant="outlined"
                            disabled={currentPage === totalPages}
                            onClick={() => setCurrentPage(currentPage + 1)}
                            sx={{ borderColor: 'rgba(255, 255, 255, 0.3)', color: 'white' }}
                        >
                            Next
                        </Button>
                    </Box>
                </Box>
            </div>
        </div>
    );
} 