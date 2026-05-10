// CongestionChart.jsx — Line chart showing vehicle counts over time

import { useState, useEffect } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer
} from "recharts";

export default function CongestionChart({ currentData }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!currentData || !currentData.lanes) return;

    const newPoint = {
      time: new Date().toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
      North: currentData.lanes.North?.vehicle_count || 0,
      South: currentData.lanes.South?.vehicle_count || 0,
      East:  currentData.lanes.East?.vehicle_count  || 0,
      West:  currentData.lanes.West?.vehicle_count  || 0,
    };

    setHistory((prev) => {
      const updated = [...prev, newPoint];
      return updated.slice(-15); // Keep last 15 data points
    });
  }, [currentData]);

  if (history.length < 2) {
    return (
      <div className="bg-gray-800 rounded-xl p-5 flex items-center justify-center h-48">
        <p className="text-gray-500 text-sm">Collecting data... start simulation first</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 rounded-xl p-5">
      <h2 className="text-white font-semibold mb-4">📈 Vehicle Count — Live History</h2>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={history}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="time" stroke="#6b7280" tick={{ fontSize: 10 }} interval="preserveStartEnd" />
          <YAxis stroke="#6b7280" tick={{ fontSize: 10 }} />
          <Tooltip
            contentStyle={{ backgroundColor: "#1f2937", border: "1px solid #374151", borderRadius: "8px" }}
            labelStyle={{ color: "#9ca3af" }}
          />
          <Legend />
          <Line type="monotone" dataKey="North" stroke="#3b82f6" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="South" stroke="#22c55e" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="East"  stroke="#f59e0b" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="West"  stroke="#a855f7" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}