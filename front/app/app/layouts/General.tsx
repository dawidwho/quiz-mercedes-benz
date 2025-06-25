import {
    Links,
    Meta,
    Scripts,
    ScrollRestoration,
} from "react-router";
import { Navigation } from "../components/Navigation";

export function Layout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en" className="dark">
            <head>
                <meta charSet="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <Meta />
                <Links />
            </head>
            <body className="bg-gray-950 text-white min-h-screen">
                <Navigation />
                <main>
                    {children}
                </main>
                <ScrollRestoration />
                <Scripts />
                <script src="/mobile-menu.js"></script>
            </body>
        </html>
    );
} 