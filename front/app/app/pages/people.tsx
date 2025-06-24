import type { Route } from "./+types/people";
import * as React from "react";
import { useEffect, useState, useCallback } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import { starWarsApiClient } from "../services/apiClientStarWars";
import { formatDate } from "../helpers/formatters";
import StarWarsTable from "../components/StarWarsTable";

export function meta({ }: Route.MetaArgs) {
    return [
        { title: "People - Quiz Mercedes-Benz" },
        { name: "description", content: "Explore Star Wars characters" },
    ];
}

export default function People() {
    const [people, setPeople] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [totalCount, setTotalCount] = useState(0);
    const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 15 });
    const [filterModel, setFilterModel] = useState<any>({ items: [] });
    const [sortModel, setSortModel] = useState<any>([]);

    const loadPeople = useCallback(async () => {
        try {
            setLoading(true);

            // Prepare parameters for the API call
            const params: any = {
                page: paginationModel.page + 1, // DataGrid uses 0-based pagination, API uses 1-based
                size: paginationModel.pageSize
            };

            console.log('People page - paginationModel:', paginationModel);
            console.log('People page - params being sent:', params);

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

            const data = await starWarsApiClient.getPeople(params);
            console.log('People page - API response:', data);

            // Check if data exists and has the expected structure
            if (data && Array.isArray(data.items)) {
                const peopleWithIds = data.items.map((person: any) => ({
                    ...person,
                    // Extract name parts for better display
                    firstName: person.name.split(' ')[0] || '',
                    lastName: person.name.split(' ').slice(1).join(' ') || '',
                }));
                setPeople(peopleWithIds);
                setTotalCount(data.total || 0);
            } else {
                // Handle case where data structure is unexpected
                setPeople([]);
                setTotalCount(0);
                setError('No data available from the API');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
            setPeople([]);
            setTotalCount(0);
        } finally {
            setLoading(false);
        }
    }, [paginationModel, filterModel, sortModel]);

    // Load data when pagination, filter, or sort changes
    useEffect(() => {
        loadPeople();
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
        { field: 'name', headerName: 'Name', width: 200, filterable: true },
        { field: 'height', headerName: 'Height (cm)', width: 120, type: 'number', filterable: true },
        { field: 'mass', headerName: 'Mass (kg)', width: 120, type: 'number', filterable: true },
        { field: 'hair_color', headerName: 'Hair Color', width: 120, filterable: true },
        { field: 'skin_color', headerName: 'Skin Color', width: 120, filterable: true },
        { field: 'eye_color', headerName: 'Eye Color', width: 120, filterable: true },
        { field: 'birth_year', headerName: 'Birth Year', width: 120, filterable: true },
        { field: 'gender', headerName: 'Gender', width: 100, filterable: true },
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

    return (
        <StarWarsTable
            title="Star Wars People"
            description="Discover and learn about characters from the Star Wars universe"
            columns={columns}
            dataFetcher={starWarsApiClient.getPeople}
            loading={loading}
            error={error}
            data={people}
            totalCount={totalCount}
            paginationModel={paginationModel}
            filterModel={filterModel}
            sortModel={sortModel}
            onPaginationModelChange={handlePaginationModelChange}
            onFilterModelChange={handleFilterModelChange}
            onSortModelChange={handleSortModelChange}
        />
    );
}