// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import heroImg from './assets/hero.png'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <section id="center">
//         <div className="hero">
//           <img src={heroImg} className="base" width="170" height="179" alt="" />
//           <img src={reactLogo} className="framework" alt="React logo" />
//           <img src={viteLogo} className="vite" alt="Vite logo" />
//         </div>
//         <div>
//           <h1>Get started</h1>
//           <p>
//             Edit <code>src/App.jsx</code> and save to test <code>HMR</code>
//           </p>
//         </div>
//         <button
//           type="button"
//           className="counter"
//           onClick={() => setCount((count) => count + 1)}
//         >
//           Count is {count}
//         </button>
//       </section>

//       <div className="ticks"></div>

//       <section id="next-steps">
//         <div id="docs">
//           <svg className="icon" role="presentation" aria-hidden="true">
//             <use href="/icons.svg#documentation-icon"></use>
//           </svg>
//           <h2>Documentation</h2>
//           <p>Your questions, answered</p>
//           <ul>
//             <li>
//               <a href="https://vite.dev/" target="_blank">
//                 <img className="logo" src={viteLogo} alt="" />
//                 Explore Vite
//               </a>
//             </li>
//             <li>
//               <a href="https://react.dev/" target="_blank">
//                 <img className="button-icon" src={reactLogo} alt="" />
//                 Learn more
//               </a>
//             </li>
//           </ul>
//         </div>
//         <div id="social">
//           <svg className="icon" role="presentation" aria-hidden="true">
//             <use href="/icons.svg#social-icon"></use>
//           </svg>
//           <h2>Connect with us</h2>
//           <p>Join the Vite community</p>
//           <ul>
//             <li>
//               <a href="https://github.com/vitejs/vite" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#github-icon"></use>
//                 </svg>
//                 GitHub
//               </a>
//             </li>
//             <li>
//               <a href="https://chat.vite.dev/" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#discord-icon"></use>
//                 </svg>
//                 Discord
//               </a>
//             </li>
//             <li>
//               <a href="https://x.com/vite_js" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#x-icon"></use>
//                 </svg>
//                 X.com
//               </a>
//             </li>
//             <li>
//               <a href="https://bsky.app/profile/vite.dev" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#bluesky-icon"></use>
//                 </svg>
//                 Bluesky
//               </a>
//             </li>
//           </ul>
//         </div>
//       </section>

//       <div className="ticks"></div>
//       <section id="spacer"></section>
//     </>
//   )
// }

// export default App




// App.jsx — Main dashboard that brings everything together

import { useSocket } from "./services/useSocket";
import StatusBar from "./components/StatusBar";
import SignalPanel from "./components/SignalPanel";
import JunctionMap from "./components/JunctionMap";
import CongestionChart from "./components/CongestionChart";
import EmergencyAlert from "./components/EmergencyAlert";
import AnalyticsPanel from "./components/AnalyticsPanel";

export default function App() {
  const { isConnected, junctionData, lastUpdate } = useSocket();

  const lanes = junctionData?.lanes || null;
  const emergency = junctionData?.emergency || null;
  const emergencyOverride = junctionData?.emergency_override || false;
  const emergencyDirection = junctionData?.lanes
    ? Object.keys(junctionData.lanes).find(d => junctionData.lanes[d]?.has_emergency)
    : null;
  const totalVehicles = junctionData?.total_vehicles || 0;

  return (
    <div className="min-h-screen bg-gray-900 font-sans">
      {/* Top bar */}
      <StatusBar
        isConnected={isConnected}
        lastUpdate={lastUpdate}
        totalVehicles={totalVehicles}
      />

      {/* Emergency alert banner */}
      <EmergencyAlert emergency={emergency} emergencyOverride={emergencyOverride} />

      {/* Main dashboard grid */}
      <div className="p-5 grid grid-cols-1 lg:grid-cols-3 gap-5 max-w-7xl mx-auto">
        {/* Left column */}
        <div className="lg:col-span-1 space-y-5">
          <JunctionMap lanes={lanes} emergencyDirection={emergencyDirection} />
          <AnalyticsPanel lanes={lanes} />
        </div>

        {/* Right column */}
        <div className="lg:col-span-2 space-y-5">
          <SignalPanel
            lanes={lanes}
            emergencyOverride={emergencyOverride}
            emergencyDirection={emergencyDirection}
          />
          <CongestionChart currentData={junctionData} />

          {/* AI Suggestions */}
          {lanes && (
            <div className="bg-gray-800 rounded-xl p-5">
              <h2 className="text-white font-semibold mb-3">💡 AI Suggestions</h2>
              <div className="space-y-2">
                {Object.entries(lanes).map(([dir, lane]) => {
                  const suggestions = [];
                  if (lane.vehicle_count > 28)
                    suggestions.push(`⚠️ ${dir} lane heavily congested — extend green time by 20s`);
                  if (lane.avg_wait_time > 80)
                    suggestions.push(`🕐 ${dir} vehicles waiting too long — consider opening parallel lane`);
                  if (lane.has_emergency)
                    suggestions.push(`🚨 Emergency on ${dir} — all other lanes holding`);
                  return suggestions.map((s, i) => (
                    <div key={`${dir}-${i}`} className="text-sm text-gray-300 bg-gray-700/50 px-3 py-2 rounded-lg">
                      {s}
                    </div>
                  ));
                }).flat()}
                {Object.values(lanes).every(l => l.vehicle_count <= 28 && l.avg_wait_time <= 80 && !l.has_emergency) && (
                  <div className="text-sm text-green-400 bg-green-500/10 px-3 py-2 rounded-lg">
                    ✅ Junction operating efficiently — no interventions required
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="text-center py-4 text-gray-600 text-xs">
        AI Junction Optimizer — Powered by YOLOv8 + Flask + React + MongoDB
      </div>
    </div>
  );
}