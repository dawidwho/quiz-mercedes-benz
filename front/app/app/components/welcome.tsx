import logoStarWars from "../assets/logo-starwars.svg";

export function Welcome() {
  return (
    <main className="flex items-center justify-center pt-16 pb-4">
      <div className="flex-1 flex flex-col items-center gap-16 min-h-0">
        <header className="flex flex-col items-center gap-9">
          <div className="w-[500px] max-w-[100vw] p-4">
            <img
              src={logoStarWars}
              alt="Star Wars"
              className="block w-full"
            />
          </div>
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white mb-4">
              Welcome to Mercedes-Benz Quiz
            </h1>
            <p className="text-xl text-gray-300 max-w-2xl">
              Explore the Star Wars Universe with our interactive quiz featuring people and planets.
              Test your knowledge and save your favorite characters and locations.
            </p>
          </div>
        </header>
      </div>
    </main>
  );
}
