import axios from 'axios'
import { useRouter } from 'vue-router'
import { defineNuxtPlugin } from '#app'
import { useAuthStore } from '../../store/state'
export default defineNuxtPlugin(() => {
  const router = useRouter();
  const store = useAuthStore();
  const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 10000,
    withCredentials: true,
  });
  
  api.interceptors.request.use(
    (config) => {
        const token = store.getToken
        if (token) {
          config.headers = config.headers || {}
          config.headers.Authorization = `Bearer ${token}`;
        }
      return config;
    },
    (error) => Promise.reject(error)
  );

  api.interceptors.response.use(
    (response) => response,
    (error) => {
      const status = error.response?.status;

      if (status === 401) {

        if (router.currentRoute.value.path !== "/login") {
          router.push("/login");
        }
      }

      return Promise.reject(error);
    }
  );

  return {
    provide: {
      axios: api,
    },
  };
})