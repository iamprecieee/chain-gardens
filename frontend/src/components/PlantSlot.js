import React, { useState } from "react";

export function PlantSlot({
  position,
  plant,
  onPlant,
  onRemove,
  availablePlants,
  onSelectPlant,
}) {
  const [showPlantMenu, setShowPlantMenu] = useState(false);
  const getPestDamageColor = (damage) => {
    if (damage > 70) return "bg-red-600";
    if (damage > 40) return "bg-orange-500";
    if (damage > 0) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="aspect-square bg-indigo-700 rounded-lg p-4 relative">
      {plant ? (
        <div
          className="h-full flex flex-col cursor-pointer"
          onClick={() => onSelectPlant(plant)}
        >
          <div className="mb-4">
            <h3 className="font-bold text-white">{plant.plant_type.name}</h3>
            <p className="text-sm text-green-600">
              Stage: {plant.growth_stage}
            </p>
          </div>

          <div className="space-y-4 mt-auto">
            <div>
              <div className="flex justify-between text-sm mb-1 text-white">
                <span>Growth</span>
                <span>{plant.growth_progress.toFixed(2)}%</span>
              </div>
              <div className="h-2 bg-yellow-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-green-600 transition-all duration-500"
                  style={{ width: `${plant.growth_progress}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1 text-white">
                <span>Health</span>
                <span>{plant.health.toFixed(2)}%</span>
              </div>
              <div className="h-2 bg-red-500 rounded-full overflow-hidden">
                <div
                  className="h-full bg-green-600 transition-all duration-500"
                  style={{ width: `${plant.health}%` }}
                />
              </div>
            </div>
          </div>

          {plant.growth_stage === "harvest" && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onRemove(plant.id);
              }}
              className="absolute inset-0 flex items-center justify-center bg-yellow-500 bg-opacity-90 text-white font-bold rounded-lg"
            >
              Ready to Harvest!
            </button>
          )}

          {plant.pest_damage > 0 && (
            <div className="mt-2">
              <div className="flex justify-between text-sm mb-1 text-white">
                <span>Pest Damage</span>
                <span>{plant.pest_damage}%</span>
              </div>
              <div className="h-2 bg-yellow-200 rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all duration-500 ${getPestDamageColor(
                    plant.pest_damage
                  )}`}
                  style={{ width: `${plant.pest_damage}%` }}
                />
              </div>
            </div>
          )}
          <div className="mt-2 text-sm text-white">
            Growth Rate: {plant.growth_multiplier.toFixed(2)}x
          </div>
        </div>
      ) : (
        <div className="absolute inset-0 flex items-center justify-center">
          {showPlantMenu ? (
                          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
              <div className="w-full max-w-sm bg-indigo-700 p-4 rounded-lg shadow-xl border-2 border-green-500">
                <div className="flex justify-between items-center mb-4 border-b border-green-500 pb-2">
                  <h4 className="text-lg font-bold text-white">Select Plant</h4>
                  <button 
                    onClick={() => setShowPlantMenu(false)}
                    className="text-white hover:text-green-500 text-xl"
                  >
                    ×
                  </button>
                </div>
                <div className="space-y-2 max-h-64 overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
                  {availablePlants.map((plantType) => (
                    <button
                      key={plantType.id}
                      onClick={() => {
                        onPlant(position, plantType.id);
                        setShowPlantMenu(false);
                      }}
                      className="w-full bg-indigo-600 hover:bg-indigo-500 p-3 rounded-lg transition-colors duration-200 group"
                    >
                      <div className="flex justify-between items-center">
                        <div className="text-left">
                          <div className="font-medium text-white group-hover:text-green-400">
                            {plantType.name}
                          </div>
                          <div className="text-sm text-green-400 group-hover:text-green-300">
                            Growth Rate: {plantType.growth_rate}x
                          </div>
                          <div className="text-xs text-green-400 group-hover:text-green-300">
                            Required Soil: {plantType.required_soil_quality}%
                          </div>
                        </div>
                        <div className="text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                          →
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <button
              onClick={() => setShowPlantMenu(true)}
              className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors duration-200 font-medium"
            >
              Plant
            </button>
          )}
        </div>
      )}
    </div>
  );
}