<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useDataStore } from "../stores/data";
import { useAuthStore } from "../stores/auth";
import api from "../api";

import ReceiptTemplate from "../components/ReceiptTemplate.vue";

const route = useRoute();
const router = useRouter();
const dataStore = useDataStore();
const authStore = useAuthStore();

const storeId = parseInt(route.params.storeId);

const store = computed(() => {
  return dataStore.stores.find((s) => s.id === storeId);
});

const form = ref({
  store: storeId,
  pdv: "",
  operator: "",
  retriever_name: "",
  gas_type: null,
  quantity: 1,
});

const isSubmitting = ref(false);
const showSuccess = ref(false);
const savedWithdrawal = ref(null);
const stocks = ref([]);

const fetchStocks = async () => {
  try {
    const response = await api.get(`stocks/?store=${storeId}`);
    stocks.value = response.data.results || response.data;
  } catch (error) {
    console.error("Erro ao carregar estoques:", error);
  }
};

const getGasStock = (gasId) => {
  const stock = stocks.value.find((s) => s.gas_type === gasId);
  return stock ? stock.quantity : 0;
};

onMounted(() => {
  if (dataStore.stores.length === 0) {
    dataStore.fetchReferenceData();
  }
  fetchStocks();
});

const submitWithdrawal = async () => {
  // O Operador será sempre o usuário logado no momento do preenchimento
  const activeOperator = authStore.user?.first_name || authStore.user?.username || "Operador Desconhecido";
  form.value.operator = activeOperator;

  if (
    !form.value.pdv ||
    !form.value.retriever_name ||
    !form.value.gas_type
  )
    return;

  isSubmitting.value = true;
  try {
    const response = await api.post("withdrawals/", form.value);
    savedWithdrawal.value = response.data;
    showSuccess.value = true;
    fetchStocks(); // Atualiza o saldo após a retirada
  } catch (error) {
    console.error("Error creating withdrawal", error);
    const errorMsg = error.response?.data?.error || "Erro ao registrar retirada. Tente novamente.";
    alert(errorMsg);
  } finally {
    isSubmitting.value = false;
  }
};

const printReceipt = () => {
  window.print();
};

const newWithdrawal = () => {
  form.value = {
    store: storeId,
    pdv: "",
    operator: "",
    retriever_name: "",
    gas_type: null,
    quantity: 1,
  };
  savedWithdrawal.value = null;
  showSuccess.value = false;
};
</script>

<template>
  <div class="h-full relative overflow-x-hidden">
    <button
      @click="router.push(`/loja/${storeId}`)"
      class="non-printable inline-flex items-center text-sm font-medium text-gasBlue hover:text-gasBlue/80 mb-6 group transition-colors"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5 mr-1 transform group-hover:-translate-x-1 transition-transform"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
          clip-rule="evenodd"
        />
      </svg>
      Menu da Loja
    </button>

    <div
      v-if="store"
      class="non-printable bg-white shadow-xl shadow-gray-200/50 rounded-3xl overflow-hidden max-w-2xl mx-auto border border-gray-100"
    >
      <div
        class="bg-gradient-to-r from-gasBlue to-gasBlue/80 p-6 sm:p-8 text-white relative overflow-hidden"
      >
        <div
          class="absolute -right-6 -top-6 w-32 h-32 bg-white/10 rounded-full blur-2xl"
        ></div>
        <h2 class="text-3xl font-extrabold tracking-tight relative z-10">
          Nova Retirada
        </h2>
        <div class="flex items-center gap-2 mt-2 text-white/90 relative z-10">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
              clip-rule="evenodd"
            />
          </svg>
          <span class="font-medium text-lg">{{ store.name }}</span>
        </div>
      </div>

      <!-- Success View -->
      <div v-if="showSuccess" class="p-8 text-center animate-fade-in">
        <div
          class="w-20 h-20 bg-green-100 text-green-500 rounded-full flex items-center justify-center mx-auto mb-6"
        >
          <svg
            class="w-10 h-10"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="3"
              d="M5 13l4 4L19 7"
            ></path>
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">
          Registrado com Sucesso!
        </h3>
        <p class="text-gray-500 mb-8">
          A retirada de gás foi registrada no sistema.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            @click="printReceipt"
            class="bg-gray-900 hover:bg-black text-white px-6 py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg shadow-gray-900/30 transition-all active:scale-95"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
              ></path>
            </svg>
            Imprimir Comprovante
          </button>
          <button
            @click="router.push(`/loja/${storeId}`)"
            class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 px-6 py-3.5 rounded-xl font-bold transition-all active:scale-95"
          >
            Menu da Loja
          </button>
        </div>
      </div>

      <!-- Form View -->
      <form
        v-else
        @submit.prevent="submitWithdrawal"
        class="p-6 sm:p-8 space-y-6"
      >
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <!-- PDV -->
          <div class="space-y-1.5 focus-within:text-gasBlue">
            <label
              class="text-sm font-bold text-gray-700 block transition-colors"
              >Identificação do PDV</label
            >
            <input
              v-model="form.pdv"
              type="text"
              required
              placeholder="Ex: CX 01"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-gasBlue/30 focus:border-gasBlue transition-all text-gray-900 font-medium"
            />
          </div>

          <div class="space-y-1.5 pt-7">
            <span class="text-sm font-bold text-gray-500 block">Identificação do Operador</span>
            <div class="flex items-center gap-2 p-3 bg-blue-50/50 border border-blue-100 rounded-xl text-gasBlue font-bold shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 opacity-70" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                </svg>
                {{ authStore.user?.first_name || authStore.user?.username || "Carregando..." }}
            </div>
            <p class="text-xs text-gray-400 mt-1">* Registrado automaticamente via perfil de login.</p>
          </div>
        </div>

        <!-- Quem Retirou -->
        <div class="space-y-1.5 focus-within:text-gasBlue">
          <label class="text-sm font-bold text-gray-700 block transition-colors"
            >Nome de Quem Retirou o Gás</label
          >
          <input
            v-model="form.retriever_name"
            type="text"
            required
            placeholder="Nome do cliente ou entregador"
            class="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-gasBlue/30 focus:border-gasBlue transition-all text-gray-900 font-medium"
          />
        </div>

        <div class="border-t border-gray-100 my-6"></div>

        <!-- Tipo de Gás -->
        <div class="space-y-3">
          <label class="text-sm font-bold text-gray-700 block"
            >Tipo de Gás</label
          >
          <div class="grid grid-cols-2 gap-4">
            <label
              v-for="gt in dataStore.gasTypes"
              :key="gt.id"
              class="relative cursor-pointer"
            >
              <input
                type="radio"
                v-model="form.gas_type"
                :value="gt.id"
                required
                class="peer sr-only"
              />
              <div
                class="p-4 sm:p-5 rounded-xl border-2 peer-checked:bg-gasBlue/5 peer-checked:border-gasBlue hover:bg-gray-50 transition-all text-center h-full flex flex-col justify-center gap-1"
              >
                <span
                  class="block font-bold mt-1 tracking-wide"
                  :class="
                    form.gas_type === gt.id ? 'text-gasBlue' : 'text-gray-700'
                  "
                  >{{ gt.name }}</span
                >
                <div
                  v-if="form.gas_type === gt.id"
                  class="absolute top-2 right-2 text-gasBlue"
                >
                  <svg
                    class="w-5 h-5 md:w-6 md:h-6"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                </div>
                <!-- Estoque Badge -->
                <div class="mt-1 text-xs font-bold" :class="getGasStock(gt.id) > 0 ? 'text-emerald-500' : 'text-red-500'">
                  Estoque: {{ getGasStock(gt.id) }} un
                </div>
              </div>
            </label>
          </div>
        </div>

        <div class="pt-4">
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full bg-gasBlue hover:bg-gasBlue/90 active:scale-[0.98] text-white font-bold py-4 px-6 rounded-xl shadow-xl shadow-gasBlue/20 transition-all flex justify-center items-center gap-2 text-lg disabled:opacity-70 disabled:active:scale-100"
          >
            <span v-if="isSubmitting">Salvando...</span>
            <span v-else>Confirmar Retirada</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Printable Area, visível apenas na impressão -->
    <ReceiptTemplate
      v-if="savedWithdrawal && showSuccess"
      :withdrawal="savedWithdrawal"
      :store-name="store?.name || ''"
    />
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media print {
  .non-printable {
    display: none !important;
  }
}
</style>
