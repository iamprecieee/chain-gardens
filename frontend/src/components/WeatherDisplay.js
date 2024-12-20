export function WeatherDisplay({ weather }) {
  if (!weather) {
    return (
      <div className="border-b border-indigo-900/10 pb-4 mb-4">
        <div className="flex justify-center mb-4">
          <h2 className="bg-grey-100 px-2 py-1 rounded-md text-md font-semibold text-white whitespace-nowrap text-center">
            Garden Weather
          </h2>
        </div>
        <div className="text-red-600/60 text-center text-sm font-bold">
          Weather data unavailable
        </div>
      </div>
    );
  }

  return (
    <div className="border-b border-indigo-900/10 pb-4 mb-4">
      <div className="flex justify-center mb-4">
        <h2 className="bg-indigo-700 px-2 py-1 rounded-md text-sm font-semibold text-white whitespace-nowrap text-center">
          Garden Weather
        </h2>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-green-500 p-2 rounded-lg text-center">
          <p className="text-indigo-900 text-sm mb-1 font-extrabold">Type</p>
          <p className="text-indigo-900 text-sm font-medium capitalize">
            {weather.weather_type || "Unknown"}
          </p>
        </div>
        <div className="bg-green-500 p-2 rounded-lg text-center">
          <p className="text-indigo-900 text-sm mb-1 font-extrabold">
            Temperature
          </p>
          <p className="text-indigo-900 text-sm font-medium">
            {weather.temperature ? `${weather.temperature}°C` : "Unknown"}
          </p>
        </div>
        <div className="bg-green-500 p-2 rounded-lg text-center">
          <p className="text-indigo-900 text-sm mb-1 font-extrabold">
            Rainfall
          </p>
          <p className="text-indigo-900 text-sm font-medium">
            {weather.rainfall ? `${weather.rainfall}mm` : "Unknown"}
          </p>
        </div>
        <div className="bg-green-500 p-2 rounded-lg text-center">
          <p className="text-indigo-900 text-xs mb-1 font-extrabold">
            Sunlight
          </p>
          <p className="text-indigo-900 text-sm font-medium">
            {weather.sunlight ? `${weather.sunlight}%` : "Unknown"}
          </p>
        </div>
      </div>
    </div>
  );
}
