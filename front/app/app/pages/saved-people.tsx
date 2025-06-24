import type { Route } from "./+types/saved-people";

export function meta({ }: Route.MetaArgs) {
    return [
        { title: "Saved People - Quiz Mercedes-Benz" },
        { name: "description", content: "Your saved Star Wars characters" },
    ];
}

export default function SavedPeople() {
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-4">Saved People</h1>
                    <p className="text-gray-300 text-lg">
                        Your favorite Star Wars characters that you've saved
                    </p>
                </header>

                <div className="bg-gray-800 rounded-lg p-8 text-center">
                    <div className="w-24 h-24 bg-gray-600 rounded-full mb-6 mx-auto"></div>
                    <h3 className="text-xl font-semibold text-white mb-4">
                        No saved people yet
                    </h3>
                    <p className="text-gray-400 mb-6">
                        Start exploring people and save your favorites to see them here
                    </p>
                    <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200">
                        Explore People
                    </button>
                </div>
            </div>
        </div>
    );
} 