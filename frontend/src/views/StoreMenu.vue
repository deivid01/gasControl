<template>
  <div class="h-full bg-gray-50 flex flex-col items-center">
    <div class="w-full max-w-md p-6 mt-8">
      <div v-if="loading" class="flex justify-center my-10">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-gasBlue"></div>
      </div>
      <div v-else-if="store" class="space-y-6">
        <div class="flex items-center justify-between mb-8">
            <router-link to="/" class="text-gasBlue hover:text-gasBlueDark flex items-center font-medium transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
                </svg>
                Trocar Loja
            </router-link>
        </div>

        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center p-3 bg-blue-100 rounded-full mb-3 text-gasBlue">
             <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-800">{{ store.name }}</h2>
          <p class="text-sm text-gray-500 mt-1">Selecione uma ação abaixo</p>
        </div>

        <div class="space-y-4">
            <router-link :to="`/loja/${storeId}/registro`" class="block w-full text-left bg-white p-5 rounded-2xl shadow-sm border border-gray-100 hover:border-gasBlue hover:shadow-md transition-all group">
                <div class="flex items-center">
                    <div class="p-3 rounded-xl bg-blue-50 text-gasBlue group-hover:bg-gasBlue group-hover:text-white transition-colors mr-4">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                    </div>
                    <div>
                        <h3 class="font-bold text-gray-800">Registrar Retirada de Gás</h3>
                        <p class="text-sm text-gray-500 mt-1">Nova saída de Gás Nacional ou Azul</p>
                    </div>
                </div>
            </router-link>

            <router-link :to="`/loja/${storeId}/retirados`" class="block w-full text-left bg-white p-5 rounded-2xl shadow-sm border border-gray-100 hover:border-gasBlue hover:shadow-md transition-all group">
                <div class="flex items-center">
                    <div class="p-3 rounded-xl bg-indigo-50 text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors mr-4">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                        </svg>
                    </div>
                    <div>
                        <h3 class="font-bold text-gray-800">Gás Já Retirados</h3>
                        <p class="text-sm text-gray-500 mt-1">Ver histórico de saídas desta loja</p>
                    </div>
                </div>
            </router-link>

            <router-link :to="`/loja/${storeId}/reimprimir`" class="block w-full text-left bg-white p-5 rounded-2xl shadow-sm border border-gray-100 hover:border-gasBlue hover:shadow-md transition-all group">
                <div class="flex items-center">
                    <div class="p-3 rounded-xl bg-gray-50 text-gray-700 group-hover:bg-gray-800 group-hover:text-white transition-colors mr-4">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                        </svg>
                    </div>
                    <div>
                        <h3 class="font-bold text-gray-800">Reimprimir Cupons</h3>
                        <p class="text-sm text-gray-500 mt-1">Emitir 2ª via de comprovantes</p>
                    </div>
                </div>
            </router-link>
        </div>
      </div>
      <div v-else class="text-center p-8 bg-white rounded-xl shadow-sm text-red-500">
          Loja não encontrada
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDataStore } from '../stores/data'

const route = useRoute()
const dataStore = useDataStore()

const storeId = route.params.storeId
const store = ref(null)
const loading = ref(true)

onMounted(async () => {
    if (dataStore.stores.length === 0) {
        await dataStore.fetchStores()
    }
    store.value = dataStore.stores.find(s => s.id == storeId)
    loading.value = false
})
</script>
