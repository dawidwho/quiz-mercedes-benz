export interface Person {
    name: string;
    height: string;
    mass: string;
    hair_color: string;
    skin_color: string;
    eye_color: string;
    birth_year: string;
    gender: string;
    id: number;
}

export interface PeopleResponse {
    items: Person[];
    total: number;
    page: number;
    size: number;
    pages: number;
    has_next: boolean;
    has_prev: boolean;
}

// Filter field options
export type FilterField = 'name' | 'height' | 'mass' | 'hair_color' | 'skin_color' | 'eye_color' | 'birth_year' | 'gender';

// Sort field options
export type SortField = 'name' | 'height' | 'mass' | 'birth_year';

// Sort order options
export type SortOrder = 'asc' | 'desc';
