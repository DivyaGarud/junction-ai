// AnalyticsPanel.jsx — Summary statistics panel

export default function AnalyticsPanel({ lanes }) {
  if (!lanes) return null;

  const directions = ["North", "South", "East", "West"];
  const totalVehicles = directions.reduce((sum, d) => sum + (lanes[d]?.vehicle_count || 0), 0);
  const avgWait = directions.reduce((sum, d) => sum + (lanes[d]?.avg_wait_time || 0), 0) / 4;
  const busiest = directions.reduce((max, d) =>
    (lanes[d]?.vehicle_count || 0) > (lanes[max]?.vehicle_count || 0) ? d : max, "North"
  );
  const highCongestion = directions.filter(d => lanes[d]?.congestion?.label === "HIGH").length;

  const stats = [
    { label: "Total Vehicles", value: totalVehicles, icon: "🚗", color: "text-blue-400" },
    { label: "Avg Wait Time", value: `${Math.round(avgWait)}s`, icon: "⏱️", color: "text-yellow-400" },
    { label: "Busiest Lane", value: busiest, icon: "🔥", color: "text-red-400" },
    { label: "High Congestion", value: `${highCongestion}/4`, icon: "⚠️", color: "text-orange-400" },
  ];

  return (
    <div className="bg-gray-800 rounded-xl p-5">
      <h2 className="text-white font-semibold mb-4">📊 Live Analytics</h2>
      <div className="grid grid-cols-2 gap-3">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-gray-700/50 rounded-lg p-3">
            <div className="text-xl mb-1">{stat.icon}</div>
            <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
            <div className="text-gray-400 text-xs mt-1">{stat.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}