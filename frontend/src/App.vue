<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'
import { onMounted, onUnmounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}

// Inactivity Timeout Logic (10 minutes = 600000 ms)
let timeoutId = null;

const resetTimer = () => {
    if (timeoutId) clearTimeout(timeoutId);
    if (authStore.isAuthenticated) {
        timeoutId = setTimeout(() => {
            console.log("Logged out due to 10 minutes of inactivity.");
            logout();
        }, 600000); 
    }
}

const setupInactivityTimer = () => {
    window.addEventListener('mousemove', resetTimer);
    window.addEventListener('keydown', resetTimer);
    window.addEventListener('click', resetTimer);
    window.addEventListener('scroll', resetTimer);
}

const cleanupInactivityTimer = () => {
    window.removeEventListener('mousemove', resetTimer);
    window.removeEventListener('keydown', resetTimer);
    window.removeEventListener('click', resetTimer);
    window.removeEventListener('scroll', resetTimer);
    if (timeoutId) clearTimeout(timeoutId);
}

onMounted(() => {
    setupInactivityTimer();
    resetTimer(); // Start the timer initial countdown
});

onUnmounted(() => {
    cleanupInactivityTimer();
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-800 print:block print:min-h-0 print:h-auto print:bg-white">
    <nav v-if="authStore.isAuthenticated" class="bg-white shadow-sm px-4 py-3 flex justify-between items-center sticky top-0 z-50 print:hidden">
      <div class="flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gasBlue" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2A10 10 0 1 0 22 12 10 10 0 0 0 12 2Z"></path><path d="M12 18a6 6 0 1 0-6-6"></path><path d="M12 14a2 2 0 1 0-2-2"></path></svg>
        <span class="font-bold text-lg tracking-tight">Gás<span class="text-gasBlue">Control</span></span>
      </div>
      <div class="flex gap-4 text-sm font-medium items-center">
         <span class="hidden sm:inline text-gray-500">Olá, {{ authStore.user?.first_name || authStore.user?.username }}</span>
         <router-link to="/" class="text-gray-600 hover:text-gasBlue transition-colors px-2 py-1 rounded-md">Lojas</router-link>
         <router-link v-if="authStore.user?.role === 'MASTER' || authStore.user?.role === 'ENCARREGADO'" to="/reports" class="text-gray-600 hover:text-gasBlue transition-colors px-2 py-1 rounded-md">Auditoria</router-link>
         <button @click="logout" class="text-red-500 hover:bg-red-50 transition-colors px-3 py-1.5 rounded-md flex items-center gap-1">
             <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
             <span class="hidden sm:inline">Sair</span>
         </button>
      </div>
    </nav>

    <main class="flex-grow flex flex-col p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full print:block print:p-0 print:m-0 print:max-w-none print:w-full">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Esconder barra na impressão */
@media print {
  nav {
    display: none !important;
  }
  main {
    padding: 0 !important;
  }
}
</style>
