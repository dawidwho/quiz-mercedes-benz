// Helper function to format dates
export const formatDate = (dateString: string | undefined) => {
    if (!dateString) return '';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    } catch {
        return dateString;
    }
}; 