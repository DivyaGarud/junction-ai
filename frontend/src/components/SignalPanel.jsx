// SignalPanel.jsx — Shows signal timers for all 4 lanes

export default function SignalPanel({ lanes, emergencyOverride, emergencyDirection }) {
  if (!lanes) {
    return (
      <div className="bg-gray-800 rounded-xl p-5 flex items-center justify-center h-64">
        <p className="text-gray-500">Start simulation to see signals</p>
      </div>
    );
  }

  const directions = ["North", "South", "East", "West"];
  const directionEmojis = { North: "⬆️", South: "⬇️", East: "➡️", West: "⬅️" };

  const getCongestionColor = (level) => {
    const colors = {
      LOW: "text-green-400 bg-green-500/10 border-green-500/30",
      MEDIUM: "text-yellow-400 bg-yellow-500/10 border-yellow-500/30",
      HIGH: "text-red-400 bg-red-500/10 border-red-500/30",
    };
    return colors[level] || colors.LOW;
  };

  const getSignalColor = (direction, greenTime) => {
    if (emergencyOverride && direction === emergencyDirection) return "bg-green-500";
    if (emergencyOverride) return "bg-red-500";
    if (greenTime > 60) return "bg-green-500";
    if (greenTime > 30) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="bg-gray-800 rounded-xl p-5">
      <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
        🚦 Signal Status
        {emergencyOverride && (
          <span className="text-xs bg-red-500 text-white px-2 py-0.5 rounded-full animate-pulse">
            EMERGENCY OVERRIDE
          </span>
        )}
      </h2>

      <div className="grid grid-cols-2 gap-3">
        {directions.map((dir) => {
          const lane = lanes[dir];
          if (!lane) return null;
          const congestion = lane.congestion || {};

          return (
            <div
              key={dir}
              className={`rounded-lg p-4 border ${
                emergencyOverride && dir === emergencyDirection
                  ? "border-red-500 bg-red-500/10 animate-pulse"
                  : "border-gray-700 bg-gray-750"
              }`}
            >
              {/* Direction header */}
              <div className="flex items-center justify-between mb-3">
                <span className="text-white font-medium">
                  {directionEmojis[dir]} {dir}
                </span>
                {/* Traffic light dots */}
                <div className="flex gap-1">
                  <div className={`w-3 h-3 rounded-full ${getSignalColor(dir, lane.green_time)}`} />
                </div>
              </div>

              {/* Green time */}
              <div className="text-3xl font-bold text-white mb-1">
                {lane.green_time || 0}
                <span className="text-sm text-gray-400 ml-1">sec</span>
              </div>

              {/* Stats */}
              <div className="space-y-1 text-xs text-gray-400">
                <div className="flex justify-between">
                  <span>Vehicles</span>
                  <span className="text-white">{lane.vehicle_count || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span>Queue</span>
                  <span className="text-white">{Math.round(lane.queue_length || 0)}m</span>
                </div>
                <div className="flex justify-between">
                  <span>Wait</span>
                  <span className="text-white">{Math.round(lane.avg_wait_time || 0)}s</span>
                </div>
              </div>

              {/* Congestion badge */}
              <div className={`mt-2 px-2 py-0.5 rounded text-xs font-medium border w-fit ${getCongestionColor(congestion.label)}`}>
                {congestion.label || "LOADING"}
              </div>

              {/* Emergency indicator */}
              {lane.has_emergency && (
                <div className="mt-2 text-xs text-red-400 font-medium animate-pulse">
                  🚨 EMERGENCY VEHICLE
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}