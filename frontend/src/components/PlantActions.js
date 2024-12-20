import React, { useState } from "react";

export function PlantActions({ position, onPlant, onRemove, availablePlants }) {
  const [showPlantMenu, setShowPlantMenu] = useState(false);

  return (
    <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 rounded-lg opacity-0 hover:opacity-100 transition-opacity">
      {showPlantMenu ? (
        <div className="bg-white p-4 rounded-lg shadow-xl">
          <h4 className="font-bold mb-2">Select Plant</h4>
          <div className="space-y-2">
            {availablePlants.map((plant) => (
              <button
                key={plant.id}
                onClick={() => {
                  onPlant(position, plant.id);
                  setShowPlantMenu(false);
                }}
                className="w-full text-left p-2 hover:bg-gray-100 rounded"
              >
                <div className="font-medium">{plant.name}</div>
                <div className="text-sm text-gray-600">
                  Growth Rate: {plant.growth_rate}x
                </div>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="space-x-2">
          <button
            onClick={() => setShowPlantMenu(true)}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Plant
          </button>
          <button
            onClick={() => onRemove(position)}
            className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
          >
            Harvest
          </button>
        </div>
      )}
    </div>
  );
}
