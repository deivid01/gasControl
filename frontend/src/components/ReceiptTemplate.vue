<script setup>
import { computed } from "vue";

const props = defineProps({
  withdrawal: {
    type: Object,
    required: true,
  },
  storeName: {
    type: String,
    required: true,
  },
});

const getFormattedDate = () => {
  if (!props.withdrawal?.created_at) return "";
  const d = new Date(props.withdrawal.created_at);
  return d.toLocaleString("pt-BR");
};
</script>

<template>
  <div
    class="printable-receipt hidden bg-white text-black p-4 w-[58mm] mx-auto text-xs font-mono leading-tight"
  >
    <!-- Este elemento só é visível na impressão (vide style.css / index.css media query) -->
    <div class="text-center mb-4 border-b-2 border-dashed border-black pb-2">
      <h2 class="font-bold text-lg uppercase mb-1">{{ storeName }}</h2>
      <p>Comprovante de Retirada de Gás</p>
    </div>

    <div class="space-y-1 mb-4">
      <p class="flex justify-between">
        <span>Data/Hora:</span>
        <span>{{
          getFormattedDate() || new Date().toLocaleString("pt-BR")
        }}</span>
      </p>
      <p class="flex justify-between">
        <span>Cod. Ref:</span> <span>#{{ withdrawal?.id }}</span>
      </p>
    </div>

    <div class="border-y border-dashed border-black py-2 mb-4 space-y-1">
      <p class="flex justify-between">
        <span>PDV:</span>
        <span class="uppercase font-bold">{{ withdrawal?.pdv }}</span>
      </p>
      <p class="flex justify-between">
        <span>Operador:</span>
        <span class="uppercase">{{ withdrawal?.operator }}</span>
      </p>
      <p class="flex justify-between">
        <span>Retirou:</span>
        <span class="uppercase font-bold">{{
          withdrawal?.retriever_name
        }}</span>
      </p>
    </div>

    <div class="mb-6 font-bold text-sm">
      <p class="flex justify-between pt-1 border-t border-black">
        <span>Gás {{ withdrawal?.gas_type_name }}:</span>
        <span>{{ withdrawal?.quantity }} un</span>
      </p>
    </div>

    <div class="text-center mt-12 mb-4">
      <div class="w-full border-t border-black pt-1 mb-1"></div>
      <p class="text-[10px]">Assinatura de quem retirou</p>
    </div>

    <div class="text-center text-[9px] mt-6">
      <p>Gerado via GásControl App</p>
    </div>
  </div>
</template>

<style>
@media print {
  .printable-receipt {
    display: block !important;
    width: 100% !important;
    max-width: 80mm !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  html,
  body {
    margin: 0 !important;
    padding: 0 !important;
    background-color: white !important;
  }

  body * {
    visibility: hidden;
  }

  .printable-receipt,
  .printable-receipt * {
    visibility: visible;
  }

  .printable-receipt {
    position: absolute;
    left: 0;
    top: 0;
  }
}
</style>
