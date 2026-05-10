// JunctionMap.jsx — Visual top-down junction diagram with animated signals

export default function JunctionMap({ lanes, emergencyDirection }) {
  const getColor = (direction) => {
    if (!lanes || !lanes[direction]) return "#6b7280";
    const lane = lanes[direction];
    if (lane.has_emergency) return "#ef4444";
    const count = lane.vehicle_count || 0;
    if (count > 25) return "#ef4444";
    if (count > 12) return "#f59e0b";
    return "#22c55e";
  };

  const getOpacity = (direction) => {
    if (!lanes || !lanes[direction]) return 0.3;
    return 0.7 + (lanes[direction].vehicle_count || 0) / 100;
  };

  return (
    <div className="bg-gray-800 rounded-xl p-5">
      <h2 className="text-white font-semibold mb-4">🗺️ Junction Map</h2>
      <div className="flex justify-center">
        <svg viewBox="0 0 300 300" className="w-full max-w-xs" xmlns="http://www.w3.org/2000/svg">
          {/* Road background */}
          <rect x="0" y="0" width="300" height="300" fill="#1f2937" />

          {/* Horizontal road */}
          <rect x="0" y="120" width="300" height="60" fill="#374151" />
          {/* Vertical road */}
          <rect x="120" y="0" width="60" height="300" fill="#374151" />

          {/* Road center lines */}
          <line x1="0" y1="150" x2="110" y2="150" stroke="#6b7280" strokeWidth="1" strokeDasharray="8,8" />
          <line x1="190" y1="150" x2="300" y2="150" stroke="#6b7280" strokeWidth="1" strokeDasharray="8,8" />
          <line x1="150" y1="0" x2="150" y2="110" stroke="#6b7280" strokeWidth="1" strokeDasharray="8,8" />
          <line x1="150" y1="190" x2="150" y2="300" stroke="#6b7280" strokeWidth="1" strokeDasharray="8,8" />

          {/* Intersection box */}
          <rect x="120" y="120" width="60" height="60" fill="#4b5563" />

          {/* North lane traffic */}
          <rect x="125" y="20" width="40" height="90" fill={getColor("North")} opacity={getOpacity("North")} rx="4" />
          <text x="145" y="70" textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">
            {lanes?.North?.vehicle_count || 0}
          </text>
          <text x="145" y="82" textAnchor="middle" fill="white" fontSize="8">vehicles</text>

          {/* South lane traffic */}
          <rect x="125" y="190" width="40" height="90" fill={getColor("South")} opacity={getOpacity("South")} rx="4" />
          <text x="145" y="240" textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">
            {lanes?.South?.vehicle_count || 0}
          </text>
          <text x="145" y="252" textAnchor="middle" fill="white" fontSize="8">vehicles</text>

          {/* East lane traffic */}
          <rect x="190" y="125" width="90" height="40" fill={getColor("East")} opacity={getOpacity("East")} rx="4" />
          <text x="235" y="148" textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">
            {lanes?.East?.vehicle_count || 0}
          </text>
          <text x="235" y="158" textAnchor="middle" fill="white" fontSize="8">vehicles</text>

          {/* West lane traffic */}
          <rect x="20" y="125" width="90" height="40" fill={getColor("West")} opacity={getOpacity("West")} rx="4" />
          <text x="65" y="148" textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">
            {lanes?.West?.vehicle_count || 0}
          </text>
          <text x="65" y="158" textAnchor="middle" fill="white" fontSize="8">vehicles</text>

          {/* Direction labels */}
          <text x="145" y="12" textAnchor="middle" fill="#9ca3af" fontSize="10">NORTH</text>
          <text x="145" y="295" textAnchor="middle" fill="#9ca3af" fontSize="10">SOUTH</text>
          <text x="292" y="153" textAnchor="end" fill="#9ca3af" fontSize="10">EAST</text>
          <text x="8" y="153" textAnchor="start" fill="#9ca3af" fontSize="10">WEST</text>

          {/* Center AI icon */}
          <circle cx="150" cy="150" r="15" fill="#3b82f6" opacity="0.8" />
          <text x="150" y="154" textAnchor="middle" fill="white" fontSize="10" fontWeight="bold">AI</text>

          {/* Emergency indicator */}
          {emergencyDirection && (
            <circle cx="150" cy="150" r="20" fill="none" stroke="#ef4444" strokeWidth="2" opacity="0.8">
              <animate attributeName="r" values="15;25;15" dur="1s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.8;0.2;0.8" dur="1s" repeatCount="indefinite" />
            </circle>
          )}
        </svg>
      </div>

      {/* Legend */}
      <div className="flex justify-center gap-4 mt-3 text-xs text-gray-400">
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-green-500 inline-block"/> Low</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-yellow-500 inline-block"/> Medium</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-red-500 inline-block"/> High</span>
      </div>
    </div>
  );
}