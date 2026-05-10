// // EmergencyAlert.jsx — Flashing alert banner for emergency vehicles

// import { Siren, X } from "lucide-react";
// import { useState } from "react";

// export default function EmergencyAlert({ emergency, emergencyOverride }) {
//   const [dismissed, setDismissed] = useState(false);

//   if (!emergencyOverride || !emergency || dismissed) return null;

//   return (
//     <div className="bg-red-600 border-b-2 border-red-400 px-6 py-3 flex items-center justify-between animate-pulse">
//       <div className="flex items-center gap-3">
//         <Siren className="text-white" size={20} />
//         <div>
//           <p className="text-white font-bold text-sm">
//             🚨 EMERGENCY VEHICLE DETECTED — PRIORITY OVERRIDE ACTIVE
//           </p>
//           <p className="text-red-200 text-xs">
//             {emergency.direction} lane cleared | All other signals held RED
//             | AI automatically rerouted traffic
//           </p>
//         </div>
//       </div>
//       <button
//         onClick={() => setDismissed(true)}
//         className="text-red-200 hover:text-white"
//       >
//         <X size={16} />
//       </button>
//     </div>
//   );
// }





// EmergencyAlert.jsx - FIXED

import { Siren, X } from "lucide-react";
import { useState } from "react";

export default function EmergencyAlert({ emergency, emergencyOverride }) {
  const [dismissed, setDismissed] = useState(false);

  if (!emergencyOverride || !emergency || dismissed) return null;

  return (
    <div className="bg-red-600 border-b-2 border-red-400 px-6 py-3 flex items-center justify-between animate-pulse">
      
      <div className="flex items-center gap-3">
        <Siren className="text-white" size={20} />

        <div>
          <p className="text-white font-bold text-sm">
            🚨 EMERGENCY VEHICLE DETECTED
          </p>

          <p className="text-red-200 text-xs">
            {emergency?.direction || "Unknown"} lane cleared | AI override active
          </p>
        </div>
      </div>

      <button
        onClick={() => setDismissed(true)}
        className="text-red-200 hover:text-white"
      >
        <X size={16} />
      </button>
    </div>
  );
}