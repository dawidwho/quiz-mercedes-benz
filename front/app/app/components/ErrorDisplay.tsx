import * as React from "react";
import { Box, Button, Typography } from "@mui/material";

interface ErrorDisplayProps {
    error: string;
    onRetry?: () => void;
    showRetry?: boolean;
    severity?: 'error' | 'warning' | 'info';
}

export default function ErrorDisplay({
    error,
    onRetry,
    showRetry = true,
    severity = 'error'
}: ErrorDisplayProps) {
    // Accent color for error
    const accentColor = severity === 'error' ? '#ef4444' : severity === 'warning' ? '#fbbf24' : '#3b82f6';
    const icon = (
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="12" fill={accentColor} fillOpacity="0.18" />
            <path d="M12 8v4m0 4h.01" stroke={accentColor} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
    );

    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: '260px',
                width: '100%',
            }}
        >
            <Box
                sx={{
                    background: 'rgba(24, 26, 32, 0.98)',
                    borderRadius: 3,
                    boxShadow: `0 4px 24px 0 rgba(229,57,53,0.10)`,
                    border: `1.5px solid ${accentColor}55`,
                    px: 5,
                    py: 4,
                    maxWidth: 400,
                    width: '100%',
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: 2,
                }}
            >
                <Box sx={{ mb: 1 }}>{icon}</Box>
                <Typography variant="h6" sx={{ color: accentColor, fontWeight: 700, mb: 0.5, fontSize: '1.25rem', letterSpacing: '-0.5px' }}>
                    Something went wrong
                </Typography>
                <Typography variant="body1" sx={{ color: '#fff', mb: 2, fontSize: '1.05rem', opacity: 0.92 }}>
                    {error}
                </Typography>
                {showRetry && onRetry && (
                    <Button
                        variant="contained"
                        onClick={onRetry}
                        sx={{
                            background: accentColor,
                            color: '#fff',
                            fontWeight: 700,
                            borderRadius: 2,
                            px: 3,
                            py: 1.2,
                            fontSize: '1rem',
                            boxShadow: '0 2px 8px 0 rgba(229,57,53,0.10)',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px',
                            '&:hover': {
                                background: '#dc2626',
                            },
                        }}
                    >
                        Try Again
                    </Button>
                )}
            </Box>
        </Box>
    );
} 