<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const historyLogs = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    try {
        const response = await api.get('withdrawals/history/')
        historyLogs.value = response.data
    } catch (err) {
        console.error("Erro ao buscar histórico", err)
        error.value = 'Você não tem permissão para visualizar a auditoria ou ocorreu um erro.'
    } finally {
        loading.value = false
    }
})

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
</script>

<template>
  <div class="h-full flex flex-col gap-6">
    <div class="flex items-center justify-between">
        <div>
            <h1 class="text-2xl font-bold text-gray-900">Logs de Auditoria</h1>
            <p class="text-gray-500 text-sm mt-1">Histórico completo de ações no sistema de retiradas.</p>
        </div>
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
    <div v-else class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
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
    </div>
  </div>
</template>
