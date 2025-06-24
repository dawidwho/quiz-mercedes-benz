import * as React from "react";
import { lazy, Suspense, useEffect, useState, useCallback, useRef } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import Paper from "@mui/material/Paper";
import { CircularProgress, Alert, TextField, Box, InputAdornment, IconButton } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
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
    onSearchChange?: (searchTerm: string) => void;
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
    onSearchChange,
    detailRouteType
}: StarWarsTableProps) {
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState("");
    const searchInputRef = useRef<HTMLInputElement>(null);

    const handleSearchChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value;
        setSearchTerm(value);
    }, []);

    const handleSearchSubmit = useCallback(() => {
        if (onSearchChange) {
            onSearchChange(searchTerm);
        }
        // Return focus to search field after search
        if (searchInputRef.current) {
            searchInputRef.current.focus();
        }
    }, [onSearchChange, searchTerm]);

    const handleKeyPress = useCallback((event: React.KeyboardEvent) => {
        if (event.key === 'Enter') {
            handleSearchSubmit();
        }
    }, [handleSearchSubmit]);

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

                {/* Search Input */}
                <Box sx={{ mb: 3 }}>
                    <TextField
                        ref={searchInputRef}
                        fullWidth
                        variant="outlined"
                        placeholder={`Search ${detailRouteType} by name...`}
                        value={searchTerm}
                        onChange={handleSearchChange}
                        onKeyPress={handleKeyPress}
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        onClick={handleSearchSubmit}
                                        sx={{
                                            color: 'rgba(255, 255, 255, 0.7)',
                                            '&:hover': {
                                                color: 'white',
                                            },
                                        }}
                                    >
                                        <SearchIcon />
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                        sx={{
                            '& .MuiOutlinedInput-root': {
                                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                                color: 'white',
                                '& fieldset': {
                                    borderColor: 'rgba(255, 255, 255, 0.3)',
                                },
                                '&:hover fieldset': {
                                    borderColor: 'rgba(255, 255, 255, 0.5)',
                                },
                                '&.Mui-focused fieldset': {
                                    borderColor: 'white',
                                },
                            },
                            '& .MuiInputLabel-root': {
                                color: 'rgba(255, 255, 255, 0.7)',
                            },
                            '& .MuiInputBase-input': {
                                color: 'white',
                                '&::placeholder': {
                                    color: 'rgba(255, 255, 255, 0.5)',
                                    opacity: 1,
                                },
                            },
                        }}
                    />
                </Box>

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