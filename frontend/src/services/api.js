import axios from "axios";

// One Axios instance used everywhere. Change the URL in frontend/.env.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 15000,
});

export const fetchHomepage = () => api.get("/homepage/").then((r) => r.data);
export const fetchTitle = (id) => api.get(`/titles/${id}/`).then((r) => r.data);
export const searchTitles = (q) =>
  api.get("/search/", { params: { q } }).then((r) => r.data);

export default api;
