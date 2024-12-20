import React from "react";
import { WeatherDisplay } from "./WeatherDisplay";
import { PlantSlot } from "./PlantSlot";

export function GardenView({
  garden,
  weather,
  onPlant,
  onRemove,
  availablePlants,
  onSelectPlant,
}) {
  if (!garden) return null;

  return (
    <div>
      <WeatherDisplay weather={weather} />
      <div className="flex flex-col mb-6 border-b border-indigo-700/10 pb-4">
        <div className="flex justify-center items-center gap-5">
          <span className="bg-indigo-700 px-2 py-1 rounded-md text-md font-semibold text-white whitespace-nowrap">
            Level {garden.level}
          </span>
          <span className="bg-indigo-700 px-2 py-1 rounded-md text-md font-semibold text-white whitespace-nowrap">
            Soil Quality: {garden.soil_quality}%
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {Array.from({ length: garden.plot_size }).map((_, index) => (
          <PlantSlot
            key={index}
            position={index}
            plant={garden.plants.find((p) => p.slot_position === index)}
            onPlant={onPlant}
            onRemove={onRemove}
            availablePlants={availablePlants}
            onSelectPlant={onSelectPlant}
          />
        ))}
      </div>
    </div>
  );
}
