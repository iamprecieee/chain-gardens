import axios from "axios";
import environment from "../config/environment";

export const api = axios.create({
  baseURL: environment.API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// Set token in authorization headers
export const setAuthToken = (token) => {
  api.defaults.headers.common["Authorization"] = `Token ${token}`;
};

// Authenticate user endpoint call
export const authenticate = async (address, signature) => {
  const response = await api.post("/user/authenticate/", {
    wallet_address: address,
    signature,
  });
  return response.data.data;
};

// Disconnect user endpoint call
export const disconnect = async (token) => {
  const response = await api.post("/user/disconnect/", {});
  return response;
};

// Retrieve garden details (get_or_create)
export const getGardenDetails = async () => {
  const response = await api.get("/garden/");
  return response.data.data;
};

// Retrieve garden weather details
export const getCurrentWeather = async () => {
  const response = await api.get("/garden/status/");
  return response.data.data.weather_data || null;
};

// Create plant
export const plantSeed = async (slotPosition, plantTypeId) => {
  const response = await api.post("/garden/plants/", {
    plant_type_id: plantTypeId,
    slot_position: slotPosition,
  });
  return response.data.data.plant_data;
};

// Remove plant
export const removePlant = async (plantId) => {
  const response = await api.delete(`/garden/plants/${plantId}/`);
  return response.data;
};

// Plant types
export const getPlantTypes = async () => {
  const response = await api.get("/garden/plant-types/");
  return response.data.data.plant_types_data;
};
