import * as React from "react";
import { lazy, Suspense, useEffect, useState, useCallback } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import Paper from "@mui/material/Paper";
import { CircularProgress, Alert } from "@mui/material";
import { useNavigate } from "react-router";
import { formatDate } from "../helpers/formatters";

// Dynamic import to avoid SSR issues
const DataGrid = lazy(() => import("@mui/x-data-grid").then(module => ({ default: module.DataGrid })));

interface StarWarsTableProps {
    title: string;
    description: string;
    columns: GridColDef[];
    dataFetcher: (params: any) => Promise<any>;
    loading: boolean;
    error: string | null;
    data: any[];
    totalCount: number;
    paginationModel: { page: number; pageSize: number };
    filterModel: any;
    sortModel: any;
    onPaginationModelChange: (model: any) => void;
    onFilterModelChange: (model: any) => void;
    onSortModelChange: (model: any) => void;
    detailRouteType: 'people' | 'planets';
}

export default function StarWarsTable({
    title,
    description,
    columns,
    dataFetcher,
    loading,
    error,
    data,
    totalCount,
    paginationModel,
    filterModel,
    sortModel,
    onPaginationModelChange,
    onFilterModelChange,
    onSortModelChange,
    detailRouteType
}: StarWarsTableProps) {
    const navigate = useNavigate();

    const handleRowClick = (params: any) => {
        navigate(`/${detailRouteType}/${params.row.id}`);
    };

    if (loading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-7xl mx-auto">
                    <header className="mb-8">
                        <h1 className="text-3xl font-bold text-white mb-4">{title}</h1>
                        <p className="text-gray-300 text-lg">{description}</p>
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
                <div className="max-w-7xl mx-auto">
                    <header className="mb-8">
                        <h1 className="text-3xl font-bold text-white mb-4">{title}</h1>
                        <p className="text-gray-300 text-lg">{description}</p>
                    </header>
                    <Alert severity="error">{error}</Alert>
                </div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-7xl mx-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-4">{title}</h1>
                    <p className="text-gray-300 text-lg">{description}</p>
                </header>
                <Paper sx={{ height: 700, width: '100%' }}>
                    <Suspense fallback={<div>Loading...</div>}>
                        <DataGrid
                            rows={data}
                            columns={columns}
                            paginationModel={paginationModel}
                            onPaginationModelChange={onPaginationModelChange}
                            filterModel={filterModel}
                            onFilterModelChange={onFilterModelChange}
                            sortModel={sortModel}
                            onSortModelChange={onSortModelChange}
                            pageSizeOptions={[15, 25, 50, 100]}
                            paginationMode="server"
                            filterMode="server"
                            sortingMode="server"
                            rowCount={totalCount}
                            checkboxSelection
                            sx={{ border: 0 }}
                            getRowHeight={() => 'auto'}
                            onRowClick={handleRowClick}
                        />
                    </Suspense>
                </Paper>
            </div>
        </div>
    );
} 