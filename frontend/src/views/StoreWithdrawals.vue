<template>
  <div class="h-full bg-gray-50 flex flex-col items-center printable-container">
    <div class="w-full max-w-2xl p-6 mt-4">
        <div class="flex items-center justify-between pl-0 mb-6 non-printable print:hidden">
            <div class="flex items-center">
                <router-link :to="`/loja/${storeId}`" class="text-gasBlue hover:text-gasBlueDark flex items-center font-medium transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    Voltar
                </router-link>
                <h1 class="text-xl font-bold text-gray-800 ml-4">Gás Já Retirados</h1>
            </div>
            
            <button 
                @click="printA4"
                class="bg-gasBlue hover:bg-gasBlueDark text-white px-5 py-2 rounded-lg font-bold text-sm shadow flex items-center gap-2 transition-all active:scale-95"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                Imprimir A4
            </button>
        </div>

        <!-- Print Header Only -->
        <div class="hidden print:block mb-8 text-center w-full">
            <h1 class="text-2xl font-bold text-black border-b border-gray-400 pb-2">Extrato de Retiradas</h1>
            <p class="text-sm mt-2 text-gray-700">Loja nº {{ storeId }} • Emitido em: {{ new Date().toLocaleString('pt-BR') }}</p>
        </div>

        <div v-if="loading" class="flex justify-center my-10">
            <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-gasBlue"></div>
        </div>
        
        <div v-else-if="error" class="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100">
            {{ error }}
        </div>

        <div v-else class="space-y-4">
            <div v-if="withdrawals.length === 0" class="bg-white p-8 rounded-2xl shadow-sm text-center text-gray-500 border border-gray-100">
                Ainda não há nenhuma retirada registrada para esta loja.
            </div>

            <div v-for="w in withdrawals" :key="w.id" class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:shadow-md transition-shadow no-print-layout print:shadow-none print:border-b-2 print:border-x-0 print:border-t-0 print:border-gray-300 print:rounded-none">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="px-2 py-1 bg-green-100 text-green-800 text-xs font-bold rounded-md print:bg-transparent print:border print:border-gray-500 print:text-black">
                           {{ w.gas_type_name }}
                        </span>
                        <span class="text-sm text-gray-500 print:text-black print:font-semibold">{{ getFormattedDate(w.created_at) }}</span>
                    </div>
                    <p class="font-medium text-gray-800 print:text-black">Retirado por: <span class="font-bold print:text-black">{{ w.retriever_name }}</span></p>
                    <p class="text-sm text-gray-600 print:text-black">PDV: {{ w.pdv }} | Operador: {{ w.operator }}</p>
                </div>
                <div class="text-right">
                    <p class="text-2xl font-bold text-gasBlue print:text-black">{{ w.quantity }}x</p>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const storeId = route.params.storeId

const withdrawals = ref([])
const loading = ref(true)
const error = ref('')

const fetchStoreWithdrawals = async () => {
    try {
        const response = await api.get(`withdrawals/?store=${storeId}`)
        // As API returns paginated resposne or direct array depending on setting, we check:
        withdrawals.value = response.data.results || response.data
    } catch (err) {
        console.error("Erro ao buscar retiradas da loja", err)
        error.value = 'Houve um erro ao carregar o histórico de retiradas.'
    } finally {
        loading.value = false
    }
}

const getFormattedDate = (dateString) => {
    if (!dateString) return '';
    const d = new Date(dateString);
    return d.toLocaleDateString('pt-BR') + ' ' + d.toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'});
}

onMounted(() => {
    fetchStoreWithdrawals()
})

const printA4 = () => {
    window.print();
}
</script>

<style>
@media print {
  body {
    background-color: white !important;
  }
  .printable-container {
    display: block !important;
    height: auto !important;
  }
}
</style>
