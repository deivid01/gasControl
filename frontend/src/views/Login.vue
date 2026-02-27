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
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Usuário</label>
          <input 
            v-model="username" 
            type="text" 
            placeholder="master, encarregado..." 
            class="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-gasBlue/50 focus:border-gasBlue transition-all"
            required
          />
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
  </div>
</template>
