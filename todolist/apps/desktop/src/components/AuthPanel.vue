<script setup lang="ts">
import { ref } from "vue";
import { sendAuthCode, verifyAuthCode } from "../api";

const emit = defineEmits<{
  (e: "login", token: string): void;
}>();

const email = ref("");
const code = ref("");
const codeSent = ref(false);
const loading = ref(false);
const error = ref("");

async function request() {
  if (!email.value) return;
  loading.value = true;
  error.value = "";
  try {
    await sendAuthCode(email.value);
    codeSent.value = true;
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to send code";
  } finally {
    loading.value = false;
  }
}

async function verify() {
  if (!email.value || !code.value) return;
  loading.value = true;
  error.value = "";
  try {
    const res = await verifyAuthCode(email.value, code.value);
    if (res?.accessToken) {
      emit("login", res.accessToken);
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to verify code";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="auth-panel p-4 rounded bg-gray-50 border">
    <h2 class="text-lg font-bold mb-4">Login to continue</h2>
    
    <div v-if="error" class="error-banner mb-2 text-red-500">
      {{ error }}
    </div>

    <form @submit.prevent="codeSent ? verify() : request()" class="flex flex-col gap-2">
      <input 
        v-model="email" 
        type="email" 
        placeholder="Enter your email" 
        required 
        class="p-2 border rounded w-full"
        :disabled="codeSent || loading"
      />
      
      <input 
        v-if="codeSent"
        v-model="code" 
        type="text" 
        placeholder="Enter 6-digit code" 
        required 
        class="p-2 border rounded w-full"
        :disabled="loading"
      />

      <button 
        type="submit" 
        class="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:opacity-50"
        :disabled="loading"
      >
        {{ loading ? "Processing..." : (codeSent ? "Verify" : "Send Code") }}
      </button>
    </form>
  </div>
</template>
