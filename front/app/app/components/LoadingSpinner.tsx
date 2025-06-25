import * as React from "react";
import { CircularProgress, Box, Typography } from "@mui/material";

interface LoadingSpinnerProps {
    message?: string;
    size?: number;
    fullHeight?: boolean;
}

export default function LoadingSpinner({
    message = "Loading...",
    size = 40,
    fullHeight = false
}: LoadingSpinnerProps) {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: fullHeight ? '100vh' : '400px',
                gap: 2,
            }}
        >
            <CircularProgress
                size={size}
                color="inherit"
                sx={{
                    color: '#fff',
                    '& .MuiCircularProgress-circle': {
                        strokeLinecap: 'round',
                    },
                }}
            />
            <Typography
                variant="body1"
                sx={{
                    color: 'rgba(255, 255, 255, 0.8)',
                    fontSize: '1rem',
                    fontWeight: 500,
                }}
            >
                {message}
            </Typography>
        </Box>
    );
} 