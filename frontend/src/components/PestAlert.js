import React from "react";

export function PestAlert({ garden }) {
  if (!garden?.pest_infestation) return null;

  const pestSolutions = {
    aphids: "Transfer tokens to combat aphids",
    slugs: "Transfer tokens to remove slugs", // Temporary solution
    fungus: "Transfer tokens to cure fungus",
  };

  return (
    <div className="bg-indigo-700 p-6 rounded-lg shadow-lg mb-6">
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <svg
            className="h-6 w-6 text-red-500"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-bold text-white mb-2">
            Garden Alert: Pest Infestation!
          </h3>
          <div className="space-y-2">
            <p className="text-green-300">
              {garden.pest_type.charAt(0).toUpperCase() +
                garden.pest_type.slice(1)}{" "}
              are damaging your plants!
            </p>
            <div className="bg-black/20 p-3 rounded-lg">
              <div className="text-sm text-green-300 mb-1">
                Infestation Severity
              </div>
              <div className="h-2 bg-red-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-red-500 transition-all duration-500"
                  style={{ width: `${garden.pest_severity}%` }}
                />
              </div>
            </div>
            <p className="text-white font-medium mt-2">
              Solution: {pestSolutions[garden.pest_type]}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
