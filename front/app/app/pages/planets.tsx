import type { Route } from "./+types/planets";
import * as React from "react";
import { useEffect, useState, useCallback } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import { starWarsApiClient } from "../services/apiClientStarWars";
import { formatDate } from "../helpers/formatters";
import StarWarsTable from "../components/StarWarsTable";

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
    const [searchTerm, setSearchTerm] = useState("");

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

            // Add search parameter if search term exists
            if (searchTerm.trim()) {
                params.name = searchTerm.trim();
            }

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
    }, [paginationModel, filterModel, sortModel, searchTerm]);

    // Load data when pagination, filter, sort, or search changes
    useEffect(() => {
        loadPlanets();
    }, [paginationModel, filterModel, sortModel, searchTerm]);

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

    const handleSearchChange = (searchTerm: string) => {
        setSearchTerm(searchTerm);
        // Reset to first page when searching
        setPaginationModel(prev => ({ ...prev, page: 0 }));
    };

    const handleRetry = () => {
        setError(null);
        setLoading(true);
        loadPlanets();
    };

    const columns: GridColDef[] = [
        { field: 'name', headerName: 'Name', width: 150, filterable: false },
        { field: 'rotation_period', headerName: 'Rotation Period', width: 140, type: 'number', filterable: false },
        { field: 'orbital_period', headerName: 'Orbital Period', width: 140, type: 'number', filterable: false },
        { field: 'diameter', headerName: 'Diameter (km)', width: 140, type: 'number', filterable: false },
        { field: 'climate', headerName: 'Climate', width: 120, filterable: false },
        { field: 'gravity', headerName: 'Gravity', width: 120, filterable: false },
        { field: 'terrain', headerName: 'Terrain', width: 150, filterable: false },
        { field: 'surface_water', headerName: 'Surface Water (%)', width: 150, type: 'number', filterable: false },
        { field: 'population', headerName: 'Population', width: 140, type: 'number', filterable: false },
        {
            field: 'created_at',
            headerName: 'Created',
            width: 150,
            filterable: false,
            valueFormatter: (params: any) => formatDate(params)
        },
        {
            field: 'updated_at',
            headerName: 'Updated',
            width: 150,
            filterable: false,
            valueFormatter: (params: any) => formatDate(params)
        },
    ];

    return (
        <StarWarsTable
            title="Star Wars Planets"
            description="Discover and learn about planets from the Star Wars Universe"
            columns={columns}
            dataFetcher={starWarsApiClient.getPlanets}
            loading={loading}
            error={error}
            data={planets}
            totalCount={totalCount}
            paginationModel={paginationModel}
            filterModel={filterModel}
            sortModel={sortModel}
            onPaginationModelChange={handlePaginationModelChange}
            onFilterModelChange={handleFilterModelChange}
            onSortModelChange={handleSortModelChange}
            onSearchChange={handleSearchChange}
            detailRouteType="planets"
            onRetry={handleRetry}
        />
    );
} 