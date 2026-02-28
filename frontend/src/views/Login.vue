<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const isLoading = ref(false)
const showUserModal = ref(false)

const predefinedUsers = [
  { name: 'Deivid', username: 'deivid', role: 'MASTER', color: 'bg-red-50 text-gasBrandRed' },
  { name: 'Wellington', username: 'wellington', role: 'MASTER', color: 'bg-red-50 text-gasBrandRed' },
  { name: 'Paulo', username: 'paulo', role: 'MASTER', color: 'bg-red-50 text-gasBrandRed' },
  { name: 'Sandra', username: 'sandra', role: 'ENCARREGADO', color: 'bg-blue-50 text-gasBlue' },
  { name: 'Alessandra', username: 'alessandra', role: 'ENCARREGADO', color: 'bg-blue-50 text-gasBlue' },
  { name: 'Yasmin', username: 'yasmin', role: 'OPERADOR', color: 'bg-indigo-50 text-indigo-600' },
  { name: 'Otilia', username: 'otilia', role: 'OPERADOR', color: 'bg-indigo-50 text-indigo-600' },
]

const selectUser = (selectedUsername) => {
  username.value = selectedUsername
  showUserModal.value = false
}

const handleLogin = async () => {
  isLoading.value = true
  errorMsg.value = ''
  
  const success = await authStore.login(username.value, password.value)
  if (success) {
    router.push('/')
  } else {
    errorMsg.value = 'Usuário ou senha incorretos'
  }
  
  isLoading.value = false
}
</script>

<template>
  <div class="flex-grow flex items-center justify-center p-4">
    <div class="bg-white/70 backdrop-blur-md p-8 md:p-10 rounded-2xl shadow-xl border border-white/50 w-full max-w-md transform transition-all hover:shadow-2xl">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gasBlue text-white rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-gasBlue/30">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2A10 10 0 1 0 22 12 10 10 0 0 0 12 2Z"></path><path d="M12 18a6 6 0 1 0-6-6"></path><path d="M12 14a2 2 0 1 0-2-2"></path></svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">Gás<span class="text-gasBlue">Control</span></h1>
        <p class="text-gray-500 mt-2 text-sm">Controle sua retirada de gás com eficiência</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div class="relative">
          <label class="block text-sm font-semibold text-gray-700 mb-1">Usuário</label>
          <div 
            @click="showUserModal = true"
            class="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50/50 hover:bg-white focus:outline-none focus:ring-2 focus:ring-gasBlue/50 focus:border-gasBlue transition-all cursor-pointer flex justify-between items-center"
          >
            <span v-if="username" class="text-gray-900 font-medium">{{ username }}</span>
            <span v-else class="text-gray-400">Clique para selecionar o usuário...</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Senha</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="••••••••" 
            class="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-gasBlue/50 focus:border-gasBlue transition-all"
            required
          />
        </div>

        <div v-if="errorMsg" class="p-3 bg-red-50 text-red-600 rounded-lg text-sm text-center font-medium border border-red-100 animate-pulse">
          {{ errorMsg }}
        </div>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full bg-gasBlue hover:bg-gasBlue/90 active:scale-[0.98] text-white font-bold py-3.5 px-4 rounded-xl shadow-lg shadow-gasBlue/30 transition-all flex justify-center items-center gap-2 disabled:opacity-70 disabled:active:scale-100"
        >
          <span v-if="isLoading">Entrando...</span>
          <span v-else>Entrar no Sistema</span>
          <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
        </button>
      </form>
    </div>

    <!-- User Selection Modal -->
    <div v-if="showUserModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm" @click.self="showUserModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden animate-fade-in flex flex-col max-h-[90vh]">
        <div class="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <h3 class="font-bold text-gray-800">Selecione seu Usuário</h3>
          <button @click="showUserModal = false" class="text-gray-400 hover:text-red-500 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="overflow-y-auto p-4 flex-grow custom-scrollbar">
          <div class="grid grid-cols-1 gap-2">
            <button 
              v-for="u in predefinedUsers" 
              :key="u.username"
              @click="selectUser(u.username)"
              type="button"
              class="flex items-center p-3 rounded-xl hover:bg-gray-50 border border-transparent hover:border-gray-200 transition-all text-left group"
            >
              <div :class="`w-10 h-10 rounded-full flex items-center justify-center mr-3 font-bold text-sm ${u.color}`">
                {{ u.name.charAt(0) }}
              </div>
              <div class="flex-grow">
                <div class="font-bold text-gray-800 group-hover:text-gasBlue transition-colors">{{ u.name }}</div>
                <div class="text-xs text-gray-400">{{ u.role }}</div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.2s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 20px;
}
</style>
