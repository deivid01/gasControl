import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || '/api/';

const api = axios.create({
    baseURL: baseURL,
});

api.interceptors.request.use((config) => {
    const token = sessionStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshToken = sessionStorage.getItem('refresh_token');
                const res = await axios.post(`${baseURL}token/refresh/`, { refresh: refreshToken });
                if (res.status === 200) {
                    sessionStorage.setItem('access_token', res.data.access);
                    api.defaults.headers.common['Authorization'] = `Bearer ${sessionStorage.getItem('access_token')}`;
                    return api(originalRequest);
                }
            } catch (err) {
                sessionStorage.removeItem('access_token');
                sessionStorage.removeItem('refresh_token');
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
