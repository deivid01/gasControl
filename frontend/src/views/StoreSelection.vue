<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'

const router = useRouter()
const dataStore = useDataStore()

onMounted(() => {
  dataStore.fetchReferenceData()
})

const selectStore = (storeId) => {
  router.push(`/loja/${storeId}`)
}
</script>

<template>
  <div class="h-full flex flex-col items-center">
    <div class="w-full mb-8 text-center pt-8">
      <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight sm:text-4xl relative inline-block">
        <span class="relative z-10">Selecione sua Loja</span>
        <div class="absolute bottom-1 left-0 w-full h-3 bg-gasBlue/20 -z-0 transform -rotate-1 rounded-full"></div>
      </h1>
      <p class="mt-3 text-lg text-gray-500">Escolha o local da retirada para continuar</p>
    </div>

    <div v-if="dataStore.loading" class="flex-grow flex items-center justify-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gasBlue"></div>
    </div>
    
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-4xl px-2 pb-10">
      <button 
        v-for="store in dataStore.stores" 
        :key="store.id"
        @click="selectStore(store.id)"
        class="group relative bg-white border border-gray-100 p-8 rounded-2xl shadow-sm hover:shadow-xl hover:border-gasBlue/30 transition-all duration-300 transform hover:-translate-y-1 text-left flex flex-col justify-between h-40 overflow-hidden"
      >
        <div class="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transform translate-x-4 group-hover:translate-x-0 transition-all duration-300">
          <svg class="h-6 w-6 text-gasBlue" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </div>
        
        <!-- Decoration element -->
        <div class="absolute -bottom-6 -right-6 w-24 h-24 bg-gradient-to-br from-gasBlue/5 to-gasNacional/5 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-700"></div>

        <div>
          <div class="flex items-center gap-3 mb-2">
            <div class="bg-gray-50 p-2 rounded-xl text-gray-400 group-hover:bg-gasBlue/10 group-hover:text-gasBlue transition-colors duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            </div>
            <span class="text-sm font-semibold text-gasBlue tracking-wider uppercase opacity-80 group-hover:opacity-100 transition-opacity">Filial #{{ store.id }}</span>
          </div>
          <h2 class="text-2xl font-bold text-gray-800 group-hover:text-gray-900 transition-colors">{{ store.name }}</h2>
        </div>
      </button>
      
      <div v-if="dataStore.stores.length === 0" class="col-span-full py-12 text-center text-gray-500 bg-white rounded-2xl border border-dashed border-gray-300">
        Nenhuma loja cadastrada no sistema.
      </div>
    </div>
  </div>
</template>
