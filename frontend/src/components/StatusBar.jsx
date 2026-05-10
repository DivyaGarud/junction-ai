// StatusBar.jsx — Top bar showing connection status and controls

import { Wifi, WifiOff, Play, Square, Siren } from "lucide-react";
import { startSimulation, stopSimulation, triggerEmergency, clearEmergency } from "../services/api";
import { useState } from "react";

export default function StatusBar({ isConnected, lastUpdate, totalVehicles }) {
  const [simRunning, setSimRunning] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleStartSim = async () => {
    setLoading(true);
    await startSimulation();
    setSimRunning(true);
    setLoading(false);
  };

  const handleStopSim = async () => {
    setLoading(true);
    await stopSimulation();
    setSimRunning(false);
    setLoading(false);
  };

  const handleEmergency = async () => {
    const directions = ["North", "South", "East", "West"];
    const dir = directions[Math.floor(Math.random() * directions.length)];
    await triggerEmergency(dir);
    setTimeout(() => clearEmergency(), 15000); // Auto-clear after 15s
  };

  return (
    <div className="bg-gray-900 border-b border-gray-700 px-6 py-3 flex items-center justify-between">
      {/* Left: Title */}
      <div className="flex items-center gap-3">
        <div className="text-2xl">🚦</div>
        <div>
          <h1 className="text-white font-bold text-lg leading-none">
            AI Junction Optimizer
          </h1>
          <p className="text-gray-400 text-xs">Real-time traffic management</p>
        </div>
      </div>

      {/* Center: Stats */}
      <div className="flex items-center gap-8 text-sm">
        <div className="text-center">
          <div className="text-white font-bold text-xl">{totalVehicles || 0}</div>
          <div className="text-gray-400 text-xs">Total Vehicles</div>
        </div>
        <div className="text-center">
          <div className="text-green-400 font-mono text-sm">{lastUpdate || "—"}</div>
          <div className="text-gray-400 text-xs">Last Update</div>
        </div>
      </div>

      {/* Right: Controls */}
      <div className="flex items-center gap-3">
        {/* Connection indicator */}
        <div className={`flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full ${
          isConnected ? "bg-green-500/20 text-green-400" : "bg-red-500/20 text-red-400"
        }`}>
          {isConnected ? <Wifi size={12} /> : <WifiOff size={12} />}
          {isConnected ? "Live" : "Offline"}
        </div>

        {/* Emergency button */}
        <button
          onClick={handleEmergency}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white text-xs rounded-lg transition-colors"
        >
          <Siren size={12} />
          Test Emergency
        </button>

        {/* Start/Stop Simulation */}
        {!simRunning ? (
          <button
            onClick={handleStartSim}
            disabled={loading}
            className="flex items-center gap-1.5 px-4 py-1.5 bg-green-600 hover:bg-green-700 text-white text-xs rounded-lg transition-colors disabled:opacity-50"
          >
            <Play size={12} />
            {loading ? "Starting..." : "Start Simulation"}
          </button>
        ) : (
          <button
            onClick={handleStopSim}
            disabled={loading}
            className="flex items-center gap-1.5 px-4 py-1.5 bg-gray-600 hover:bg-gray-700 text-white text-xs rounded-lg transition-colors disabled:opacity-50"
          >
            <Square size={12} />
            Stop
          </button>
        )}
      </div>
    </div>
  );
}