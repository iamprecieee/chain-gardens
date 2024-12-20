import React from "react";

export function PlantDetails({ plant, onClose }) {
  if (!plant) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center p-4">
      <div className="bg-green-500 rounded-lg max-w-2xl w-full p-6 border-2 border-indigo-900/20">
        <div className="flex justify-between items-start mb-6 border-b border-indigo-900/10 pb-4">
          <div>
            <h3 className="text-xl font-bold text-white">
              {plant.plant_type.name}
            </h3>
            <p className="text-green-900">{plant.plant_type.description}</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-green-200 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-6">
          <div className="bg-black/20 p-4 rounded-lg">
            <h4 className="font-medium mb-2 text-white">Growth Stats</h4>
            <div className="space-y-2">
              <div>
                <div className="text-sm text-green-300">Stage</div>
                <div className="font-medium text-white">
                  {plant.growth_stage}
                </div>
              </div>
              <div>
                <div className="text-sm text-green-300">Growth Progress</div>
                <div className="font-medium text-white">
                  {plant.growth_progress}%
                </div>
              </div>
              <div>
                <div className="text-sm text-green-300">Planted On</div>
                <div className="font-medium text-white">
                  {new Date(plant.created).toLocaleDateString()}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-black/20 p-4 rounded-lg">
            <h4 className="font-medium mb-2 text-white">Health Stats</h4>
            <div className="space-y-2">
              <div>
                <div className="text-sm text-green-300">Current Health</div>
                <div className="font-medium text-white">{plant.health}%</div>
              </div>
              <div>
                <div className="text-sm text-green-300">
                  Required Soil Quality
                </div>
                <div className="font-medium text-white">
                  {plant.plant_type.required_soil_quality}%
                </div>
              </div>
              <div>
                <div className="text-sm text-green-300">Growth Rate</div>
                <div className="font-medium text-white">
                  {plant.plant_type.growth_rate}x
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
