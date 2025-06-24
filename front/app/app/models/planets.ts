export interface Planet {
    name: string;
    rotation_period: string;
    orbital_period: string;
    diameter: string;
    climate: string;
    gravity: string;
    terrain: string;
    surface_water: string;
    population: string;
    id: number;
    created_at?: string;
    updated_at?: string;
}

export interface PlanetsResponse {
    items: Planet[];
    total: number;
    page: number;
    size: number;
    pages: number;
    has_next: boolean;
    has_prev: boolean;
}
