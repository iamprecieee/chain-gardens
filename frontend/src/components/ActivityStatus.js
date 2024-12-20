import React from "react";

export function ActivityStatus({ garden }) {
  const lastActivity = garden?.last_activity
    ? new Date(garden.last_activity)
    : null;
  const daysSinceActivity = lastActivity
    ? Math.floor((new Date() - lastActivity) / (1000 * 60 * 60 * 24))
    : null;

  return (
    <div className="bg-indigo-700 p-4 rounded-lg mb-4">
      <h3 className="text-lg font-semibold text-white mb-2 text-center">
        Activity Status
      </h3>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-indigo-600 p-3 rounded">
          <p className="text-sm text-white">Total Actions</p>
          <p className="text-xl font-bold text-white">
            {garden?.total_onchain_actions || 0}
          </p>
        </div>
        <div className="bg-indigo-600 p-3 rounded">
          <p className="text-sm text-white">Last Activity</p>
          <p className="text-xl font-bold text-white">
            {daysSinceActivity !== null
              ? `${daysSinceActivity} days ago`
              : "Never"}
          </p>
        </div>
      </div>
    </div>
  );
}
