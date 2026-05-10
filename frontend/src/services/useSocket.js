// // useSocket.js
// // Custom React hook for WebSocket connection to Flask

// import { useState, useEffect, useRef } from "react";
// import { io } from "socket.io-client";

// export function useSocket() {
//   const [isConnected, setIsConnected] = useState(false);
//   const [junctionData, setJunctionData] = useState(null);
//   const [lastUpdate, setLastUpdate] = useState(null);
//   const socketRef = useRef(null);

//   useEffect(() => {
//     // Connect to Flask SocketIO server
//     const socket = io("http://localhost:5000", {
//       transports: ["websocket", "polling"],
//     });

//     socketRef.current = socket;

//     socket.on("connect", () => {
//       console.log("✅ Connected to Junction AI server");
//       setIsConnected(true);
//     });

//     socket.on("disconnect", () => {
//       console.log("❌ Disconnected from server");
//       setIsConnected(false);
//     });

//     // This fires every 3 seconds with new data
//     socket.on("junction_update", (data) => {
//       setJunctionData(data);
//       setLastUpdate(new Date().toLocaleTimeString());
//     });

//     // Cleanup when component unmounts
//     return () => {
//       socket.disconnect();
//     };
//   }, []);

//   return { isConnected, junctionData, lastUpdate };
// }


import { useState, useEffect } from "react";
import { io } from "socket.io-client";

export function useSocket() {
  const [isConnected, setIsConnected] = useState(false);
  const [junctionData, setJunctionData] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  useEffect(() => {
    const socket = io("http://localhost:5000", {
      transports: ["polling"],
      reconnection: true,
      reconnectionAttempts: 10,
      reconnectionDelay: 1000,
    });

    socket.on("connect", () => {
      console.log("✅ Connected");
      setIsConnected(true);
    });

    socket.on("disconnect", () => {
      console.log("❌ Disconnected");
      setIsConnected(false);
    });

    socket.on("junction_update", (data) => {
      console.log("📡 Data received:", data);

      setJunctionData(data);
      setLastUpdate(new Date().toLocaleTimeString());
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return {
    isConnected,
    junctionData,
    lastUpdate,
  };
}