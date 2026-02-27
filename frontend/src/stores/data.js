import { defineStore } from 'pinia';
import api from '../api';

export const useDataStore = defineStore('data', {
    state: () => ({
        stores: [],
        gasTypes: [],
        loading: false,
    }),
    actions: {
        async fetchReferenceData() {
            this.loading = true;
            try {
                const [storesRes, gasRes] = await Promise.all([
                    api.get('stores/'),
                    api.get('gastypes/')
                ]);
                this.stores = storesRes.data;
                this.gasTypes = gasRes.data;
            } catch (error) {
                console.error("Error fetching reference data", error);
            } finally {
                this.loading = false;
            }
        }
    }
});
