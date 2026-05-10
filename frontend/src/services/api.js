// api.js
// All API calls to Flask backend go through this file

import axios from "axios";

// const BASE_URL = "http://localhost:5000";
const BASE_URL = "https://divyagarud-junction-ai.onrender.com";

// Create axios instance with base URL
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
});

// API functions
export const checkStatus = () => api.get("/api/status");

export const getCurrentData = () => api.get("/api/junction/current");

export const getHistory = (limit = 20) =>
  api.get(`/api/junction/history?limit=${limit}`);

export const getAnalytics = () => api.get("/api/analytics");

export const startSimulation = () => api.post("/api/simulate/start");

export const stopSimulation = () => api.post("/api/simulate/stop");

export const triggerEmergency = (direction) =>
  api.post("/api/emergency/trigger", { direction });

export const clearEmergency = () => api.post("/api/emergency/clear");

export const predictCongestion = (data) => api.post("/api/predict", data);

export default api;