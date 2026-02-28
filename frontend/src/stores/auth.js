import { defineStore } from 'pinia';
import api from '../api';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isAuthenticated: false,
    }),
    actions: {
        async login(username, password) {
            try {
                const response = await api.post('token/', { username, password });
                sessionStorage.setItem('access_token', response.data.access);
                sessionStorage.setItem('refresh_token', response.data.refresh);
                this.isAuthenticated = true;
                await this.fetchUser();
                return true;
            } catch (error) {
                console.error('Login error', error);
                return false;
            }
        },
        async fetchUser() {
            try {
                const response = await api.get('users/me/');
                this.user = response.data;
                this.isAuthenticated = true;
            } catch (error) {
                this.logout();
            }
        },
        logout() {
            this.user = null;
            this.isAuthenticated = false;
            sessionStorage.removeItem('access_token');
            sessionStorage.removeItem('refresh_token');
        }
    }
});
