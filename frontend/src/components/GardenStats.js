import React from "react";

function calculateAverageHealth(plants) {
  if (!plants?.length) return 0;
  const total = plants.reduce((sum, plant) => sum + plant.health, 0);
  return Math.round(total / plants.length);
}

function calculateGrowthEfficiency(plants = [], weather = null) {
  if (!plants.length || !weather) return 0;

  const weatherMultipliers = {
    sunny: 0.5,
    cloudy: 0.3,
    rainy: 0.2,
    stormy: 0.1,
  };

  const weatherMultiplier = weatherMultipliers[weather?.type] || 1.0;
  const averageHealth = calculateAverageHealth(plants);
  const healthMultiplier = averageHealth / 100;

  return Math.round(weatherMultiplier * healthMultiplier * 100);
}

function getGrowthStageStats(plants = []) {
  const stages = {
    seed: 0,
    sprout: 0,
    growing: 0,
    mature: 0,
    flowering: 0,
    harvest: 0,
  };

  plants.forEach((plant) => {
    if (stages.hasOwnProperty(plant.growth_stage)) {
      stages[plant.growth_stage]++;
    }
  });

  return stages;
}

export function GardenStats({ garden, weather }) {
  if (!garden?.plants) return null;

  const stats = {
    totalPlants: garden.plants.length,
    harvestReady: garden.plants.filter((p) => p.growth_stage === "harvest")
      .length,
    averageHealth: calculateAverageHealth(garden.plants),
    growthEfficiency: calculateGrowthEfficiency(garden.plants, weather),
  };

  return (
    <div>
      <div className="bg-indigo-700 p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-extrabold mb-8 text-center text-white">
          Garden Statistics
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <div className="text-sm font-semibold text-white">Total Plants</div>
            <div className="text-2xl font-bold text-white">
              {stats.totalPlants}
            </div>
            <div className="text-sm font-semibold text-green-600">
              {stats.harvestReady} ready to harvest
            </div>
          </div>

          <div>
            <div className="text-sm font-semibold text-white">
              Average Health
            </div>
            <div className="text-2xl font-bold text-white">
              {stats.averageHealth}%
            </div>
            <div className="text-sm font-semibold text-green-600">
              across all plants
            </div>
          </div>

          <div>
            <div className="text-sm font-semibold text-white">
              Growth Efficiency
            </div>
            <div className="text-2xl font-bold text-white">
              {stats.growthEfficiency}%
            </div>
            <div className="text-sm font-semibold text-green-600">
              based on conditions
            </div>
          </div>

          <div>
            <div className="text-sm font-semibold text-white">
              Current Weather
            </div>
            <div className="text-2xl font-bold text-white capitalize">
              {weather?.weather_type || "Unknown"}
            </div>
            <div className="text-sm font-semibold text-green-600">
              affects growth rate
            </div>
          </div>
        </div>

        <div className="mt-12">
          <h3 className="text-xl font-extrabold mb-8 text-center text-white">
            Plant Growth Stages
          </h3>
          <div className="space-y-6 max-w-4xl mx-auto">
            {Object.entries(getGrowthStageStats(garden.plants)).map(
              ([stage, count]) => (
                <div key={stage}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="capitalize font-bold text-white">
                      {stage}
                    </span>
                    <span className="text-white">{count} plants</span>
                  </div>
                  <div className="h-2 bg-yellow-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-600"
                      style={{
                        width: `${
                          (count / Math.max(stats.totalPlants, 1)) * 100
                        }%`,
                      }}
                    />
                  </div>
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
