import type { PeopleResponse, Person, FilterField, SortField, SortOrder } from "../models/people";
import type { PlanetsResponse, Planet } from "../models/planets";

const BASE_URL = "http://localhost:8000/api";

export class StarWarsApiClient {
    private async fetchData<T>(url: string): Promise<T> {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching data:", error);
            throw error;
        }
    }

    private async updateData<T>(url: string, data: any): Promise<T> {
        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error updating data:", error);
            throw error;
        }
    }

    async getPeople(params: {
        page?: number;
        size?: number;
        filterField?: FilterField;
        filterValue?: string;
        sortBy?: SortField;
        sortOrder?: SortOrder;
    }): Promise<PeopleResponse> {
        const {
            page = 1,
            size = 15,
            filterField,
            filterValue,
            sortBy,
            sortOrder = 'asc'
        } = params;

        // Build query parameters for the API
        const queryParams = new URLSearchParams();
        queryParams.append('page', page.toString());
        queryParams.append('size', size.toString());
        
        if (filterField && filterValue) {
            queryParams.append('filterField', filterField);
            queryParams.append('filterValue', filterValue);
        }
        
        if (sortBy) {
            queryParams.append('sort_by', sortBy);
            queryParams.append('sort_order', sortOrder);
        }

        // Call the enhanced API endpoint that handles pagination, filtering, and sorting server-side
        const url = `${BASE_URL}/people/?${queryParams.toString()}`;
        const response = await this.fetchData<PeopleResponse>(url);
        console.log('SWAPI response:', response);
        return response;
    }

    async getPerson(id: string): Promise<Person> {
        const url = `${BASE_URL}/people/${id}/`;
        return this.fetchData<Person>(url);
    }

    async updatePerson(id: string, personData: Partial<Person>): Promise<Person> {
        const url = `${BASE_URL}/people/${id}/`;
        return this.updateData<Person>(url, personData);
    }

    async getPlanets(params: {
        page?: number;
        size?: number;
        filterField?: string;
        filterValue?: string;
        sortBy?: string;
        sortOrder?: string;
    }): Promise<PlanetsResponse> {
        const {
            page = 1,
            size = 15,
            filterField,
            filterValue,
            sortBy,
            sortOrder = 'asc'
        } = params;

        // Build query parameters for the API
        const queryParams = new URLSearchParams();
        queryParams.append('page', page.toString());
        queryParams.append('size', size.toString());
        
        if (filterField && filterValue) {
            queryParams.append('filterField', filterField);
            queryParams.append('filterValue', filterValue);
        }
        
        if (sortBy) {
            queryParams.append('sort_by', sortBy);
            queryParams.append('sort_order', sortOrder);
        }

        const url = `${BASE_URL}/planets/?${queryParams.toString()}`;
        return this.fetchData<PlanetsResponse>(url);
    }

    async getPlanet(id: string): Promise<Planet> {
        const url = `${BASE_URL}/planets/${id}/`;
        return this.fetchData<Planet>(url);
    }

    async updatePlanet(id: string, planetData: Partial<Planet>): Promise<Planet> {
        const url = `${BASE_URL}/planets/${id}/`;
        return this.updateData<Planet>(url, planetData);
    }

    async searchPeople(query: string): Promise<PeopleResponse> {
        const url = `${BASE_URL}/people/?search=${encodeURIComponent(query)}`;
        return this.fetchData<PeopleResponse>(url);
    }

    async searchPlanets(query: string): Promise<PlanetsResponse> {
        const url = `${BASE_URL}/planets/?search=${encodeURIComponent(query)}`;
        return this.fetchData<PlanetsResponse>(url);
    }
}

// Create a singleton instance
export const starWarsApiClient = new StarWarsApiClient();
