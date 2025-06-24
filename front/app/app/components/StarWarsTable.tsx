import React from "react";
import { Table, Thead, Tbody, Tr, Th, Td } from "react-super-responsive-table";
import "react-super-responsive-table/dist/SuperResponsiveTableStyle.css";

export interface StarWarsTableColumn {
    key: string;
    label: string;
    sortable?: boolean;
    className?: string;
    render?: (row: any) => React.ReactNode;
}

interface StarWarsTableProps {
    columns: StarWarsTableColumn[];
    data: any[];
    sortField?: string;
    sortOrder?: "asc" | "desc";
    onSort?: (field: string) => void;
}

const StarWarsTable: React.FC<StarWarsTableProps> = ({ columns, data, sortField, sortOrder, onSort }) => {
    return (
        <div className="starwars-table-container">
            <Table className="starwars-table">
                <Thead>
                    <Tr>
                        {columns.map((col) => (
                            <Th
                                key={col.key}
                                className={col.className + (col.sortable ? " cursor-pointer" : "")}
                                onClick={col.sortable && onSort ? () => onSort(col.key) : undefined}
                            >
                                {col.label}
                                {col.sortable && sortField === col.key && (
                                    <span style={{ marginLeft: 4 }}>{sortOrder === "asc" ? "↑" : "↓"}</span>
                                )}
                            </Th>
                        ))}
                    </Tr>
                </Thead>
                <Tbody>
                    {data.map((row, idx) => (
                        <Tr key={row.id || idx}>
                            {columns.map((col) => (
                                <Td key={col.key} className={col.className}>
                                    {col.render ? col.render(row) : row[col.key]}
                                </Td>
                            ))}
                        </Tr>
                    ))}
                </Tbody>
            </Table>
        </div>
    );
};

export default StarWarsTable; 