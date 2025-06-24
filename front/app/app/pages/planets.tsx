import type { Route } from "./+types/planets";
import * as React from "react";
import { lazy, Suspense, useEffect, useState, useCallback } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import Paper from "@mui/material/Paper";
import { CircularProgress, Alert } from "@mui/material";
import { starWarsApiClient } from "../services/apiClientStarWars";
import { formatDate } from "../helpers/formatters";

// Dynamic import to avoid SSR issues
const DataGrid = lazy(() => import("@mui/x-data-grid").then(module => ({ default: module.DataGrid })));

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
    const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 15 });
    const [filterModel, setFilterModel] = useState<any>({ items: [] });
    const [sortModel, setSortModel] = useState<any>([]);

    const loadPlanets = useCallback(async () => {
        try {
            setLoading(true);

            // Prepare parameters for the API call
            const params: any = {
                page: paginationModel.page + 1, // DataGrid uses 0-based pagination, API uses 1-based
                size: paginationModel.pageSize
            };

            console.log('Planets page - paginationModel:', paginationModel);
            console.log('Planets page - params being sent:', params);

            // Add filter parameters if filter is applied
            if (filterModel.items && filterModel.items.length > 0) {
                const filter = filterModel.items[0];
                params.filterField = filter.columnField;
                params.filterValue = filter.value;
            }

            // Add sort parameters if sorting is applied
            if (sortModel.length > 0) {
                const sort = sortModel[0];
                params.sortBy = sort.field;
                params.sortOrder = sort.sort;
            }

            const data = await starWarsApiClient.getPlanets(params);
            console.log('Planets page - API response:', data);

            // Check if data exists and has the expected structure
            if (data && Array.isArray(data.items)) {
                setPlanets(data.items);
                setTotalCount(data.total || 0);
            } else {
                // Handle case where data structure is unexpected
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
    }, [paginationModel, filterModel, sortModel]);

    // Load data when pagination, filter, or sort changes
    useEffect(() => {
        loadPlanets();
    }, [paginationModel, filterModel, sortModel]);

    const handlePaginationModelChange = (newModel: any) => {
        setPaginationModel(newModel);
    };

    const handleFilterModelChange = (newModel: any) => {
        setFilterModel(newModel);
        // Reset to first page when filtering
        setPaginationModel(prev => ({ ...prev, page: 0 }));
    };

    const handleSortModelChange = (newModel: any) => {
        setSortModel(newModel);
        // Reset to first page when sorting
        setPaginationModel(prev => ({ ...prev, page: 0 }));
    };

    const columns: GridColDef[] = [
        { field: 'name', headerName: 'Name', width: 150, filterable: true },
        { field: 'rotation_period', headerName: 'Rotation Period', width: 140, type: 'number', filterable: true },
        { field: 'orbital_period', headerName: 'Orbital Period', width: 140, type: 'number', filterable: true },
        { field: 'diameter', headerName: 'Diameter (km)', width: 140, type: 'number', filterable: true },
        { field: 'climate', headerName: 'Climate', width: 120, filterable: true },
        { field: 'gravity', headerName: 'Gravity', width: 120, filterable: true },
        { field: 'terrain', headerName: 'Terrain', width: 150, filterable: true },
        { field: 'surface_water', headerName: 'Surface Water (%)', width: 150, type: 'number', filterable: true },
        { field: 'population', headerName: 'Population', width: 140, type: 'number', filterable: true },
        {
            field: 'created_at',
            headerName: 'Created',
            width: 150,
            filterable: true,
            valueFormatter: (params: any) => formatDate(params)
        },
        {
            field: 'updated_at',
            headerName: 'Updated',
            width: 150,
            filterable: true,
            valueFormatter: (params: any) => formatDate(params)
        },
    ];

    if (loading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-4xl mx-auto">
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
                <div className="max-w-4xl mx-auto">
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
            <div className="max-w-4xl mx-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-4">Star Wars Planets</h1>
                    <p className="text-gray-300 text-lg">
                        Discover and learn about planets from the Star Wars universe
                    </p>
                </header>
                <Paper sx={{ height: 600, width: '100%' }}>
                    <Suspense fallback={<div>Loading...</div>}>
                        <DataGrid
                            rows={planets}
                            columns={columns}
                            paginationModel={paginationModel}
                            onPaginationModelChange={handlePaginationModelChange}
                            filterModel={filterModel}
                            onFilterModelChange={handleFilterModelChange}
                            sortModel={sortModel}
                            onSortModelChange={handleSortModelChange}
                            pageSizeOptions={[15, 25, 50]}
                            paginationMode="server"
                            filterMode="server"
                            sortingMode="server"
                            rowCount={totalCount}
                            checkboxSelection
                            sx={{ border: 0 }}
                            getRowHeight={() => 'auto'}
                        />
                    </Suspense>
                </Paper>
            </div>
        </div>
    );
} 