import axios from "axios";

const http = axios.create({
  baseURL: "/api/",
});

http.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

http.interceptors.response.use(
  (res) => {
    const { status, data } = res;
    const { code } = data;

    if (status === 200 && code === 0) return data;

    return res;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default http;
