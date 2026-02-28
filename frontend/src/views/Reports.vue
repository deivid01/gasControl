<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const authStore = useAuthStore()
const fileInput = ref(null)
const isImporting = ref(false)

const historyLogs = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const error = ref('')
const nextUrl = ref(null)

const fetchLogs = async (url = 'withdrawals/history/?limit=50') => {
    try {
        const response = await api.get(url)
        if (url.includes('offset')) {
            historyLogs.value = [...historyLogs.value, ...response.data.results]
        } else {
            historyLogs.value = response.data.results
        }
        nextUrl.value = response.data.next ? response.data.next.replace(api.defaults.baseURL, '') : null
    } catch (err) {
        console.error("Erro ao buscar histórico", err)
        error.value = 'Você não tem permissão para visualizar a auditoria ou ocorreu um erro.'
    }
}

onMounted(async () => {
    await fetchLogs()
    loading.value = false
})

const loadMore = async () => {
    if (!nextUrl.value || loadingMore.value) return;
    loadingMore.value = true;
    await fetchLogs(nextUrl.value);
    loadingMore.value = false;
}

const getFormattedDate = (dateString) => {
    if (!dateString) return '';
    const d = new Date(dateString);
    return d.toLocaleString('pt-BR');
}

const getActionType = (type) => {
    switch(type) {
        case '+': return { label: 'CRIADO', color: 'bg-green-100 text-green-700' }
        case '~': return { label: 'ALTERADO', color: 'bg-blue-100 text-blue-700' }
        case '-': return { label: 'DELETADO', color: 'bg-red-100 text-red-700' }
        default: return { label: 'DESCONHECIDO', color: 'bg-gray-100 text-gray-700' }
    }
}

const printA4 = () => {
    window.print();
}

const triggerImport = () => {
    fileInput.value.click();
}

const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    isImporting.value = true;
    try {
        const response = await api.post('withdrawals/import_legacy/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        alert(response.data.message || 'Importação realizada com sucesso!');
        // Refresh logs
        loading.value = true;
        await fetchLogs();
        loading.value = false;
    } catch (err) {
        console.error("Erro na importação:", err);
        alert(err.response?.data?.error || 'Erro ao importar o arquivo. Verifique o formato do CSV.');
    } finally {
        isImporting.value = false;
        if (fileInput.value) fileInput.value.value = '';
    }
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

<template>
  <div class="h-full flex flex-col gap-6 printable-container">
    <div class="flex items-center justify-between non-printable print:hidden">
        <div>
            <h1 class="text-2xl font-bold text-gray-900">Logs de Auditoria</h1>
            <p class="text-gray-500 text-sm mt-1">Histórico completo de ações no sistema de retiradas.</p>
        </div>
        <div class="flex items-center gap-3">
            <input type="file" ref="fileInput" class="hidden" accept=".csv" @change="handleFileUpload" />
            <button 
                v-if="authStore.user?.role === 'MASTER'"
                @click="triggerImport"
                :disabled="isImporting"
                class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white px-5 py-2.5 rounded-xl font-bold text-sm shadow flex items-center gap-2 transition-all active:scale-95"
            >
                <svg v-if="!isImporting" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                <svg v-else class="animate-spin w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                {{ isImporting ? 'Importando...' : 'Importar CSV Legado' }}
            </button>

            <button 
                @click="printA4"
                class="bg-gasBlue hover:bg-gasBlueDark text-white px-5 py-2.5 rounded-xl font-bold text-sm shadow flex items-center gap-2 transition-all active:scale-95"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                Imprimir A4
            </button>
        </div>
    </div>

    <!-- Print Header Only -->
    <div class="hidden print:block mb-6 text-center">
        <h1 class="text-2xl font-bold text-black border-b border-gray-400 pb-2">Relatório Consolidado de Retiradas e Estoque</h1>
        <p class="text-sm mt-2 text-gray-700">Emitido em: {{ new Date().toLocaleString('pt-BR') }}</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="bg-red-50 text-red-600 p-6 rounded-2xl flex flex-col items-center justify-center border border-red-100 text-center gap-2">
        <svg class="w-12 h-12 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        <span class="font-semibold">{{ error }}</span>
    </div>

    <!-- Loading State -->
    <div v-else-if="loading" class="flex-grow flex items-center justify-center p-12">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-gasBlue"></div>
    </div>

    <!-- Table content -->
    <div v-else class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden no-print-layout print:shadow-none print:border-none print:overflow-visible">
        <div class="overflow-x-auto print:overflow-visible">
            <table class="w-full text-left border-collapse print:text-xs">
                <thead>
                    <tr class="bg-gray-50 border-b border-gray-100 text-gray-500 text-sm uppercase tracking-wider">
                        <th class="p-4 font-semibold whitespace-nowrap">Data/Hora</th>
                        <th class="p-4 font-semibold whitespace-nowrap">Ação</th>
                        <th class="p-4 font-semibold whitespace-nowrap">Usuário (Backend)</th>
                        <th class="p-4 font-semibold whitespace-nowrap">Detalhes da Retirada</th>
                        <th class="p-4 font-semibold whitespace-nowrap">Operador/PDV</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                    <tr v-for="log in historyLogs" :key="log.history_id" class="hover:bg-gray-50/50 transition-colors">
                        <td class="p-4 text-sm text-gray-600 whitespace-nowrap">
                            {{ getFormattedDate(log.history_date) }}
                        </td>
                        <td class="p-4 text-sm whitespace-nowrap">
                            <span :class="['px-2.5 py-1 rounded-md text-xs font-bold leading-none', getActionType(log.history_type).color]">
                                {{ getActionType(log.history_type).label }}
                            </span>
                        </td>
                        <td class="p-4 text-sm font-medium text-gray-900 border-x border-gray-50">
                            {{ log.history_user || 'Sistema' }}
                        </td>
                        <td class="p-4 text-sm">
                            <div class="font-medium text-gray-800">{{ log.quantity }}x Gás {{ log.gas_type }}</div>
                            <div class="text-gasBlue text-xs font-semibold mt-0.5">{{ log.store }}</div>
                        </td>
                        <td class="p-4 text-sm text-gray-600">
                            <div class="font-medium text-gray-800 uppercase text-xs">{{ log.retriever_name }}</div>
                            <div class="text-xs text-gray-500 mt-0.5">PDV: {{ log.pdv }} | Op: {{ log.operator }}</div>
                        </td>
                    </tr>
                    <tr v-if="historyLogs.length === 0">
                        <td colspan="5" class="p-10 text-center text-gray-500">
                            Nenhum log de auditoria encontrado.
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Pagination UI -->
        <div v-if="nextUrl" class="p-4 border-t border-gray-100 bg-gray-50 flex justify-center non-printable print:hidden">
            <button 
                @click="loadMore" 
                :disabled="loadingMore"
                class="px-6 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gasBlue shadow-sm hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
                <span v-if="loadingMore">Carregando...</span>
                <span v-else>Carregar Mais Registros</span>
            </button>
        </div>
    </div>
  </div>
</template>
