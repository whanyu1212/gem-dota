<script setup lang="ts">
import { computed, ref } from "vue";

type ParseResponse = {
  ok: boolean;
  summary?: unknown;
  error?: string;
};

const endpoint = ref("/api/parse");
const replayFile = ref<File | null>(null);
const loading = ref(false);
const error = ref("");
const response = ref<ParseResponse | null>(null);

const canSubmit = computed(() => !loading.value && replayFile.value !== null && endpoint.value !== "");

function onFileChange(event: Event): void {
  const input = event.target as HTMLInputElement;
  replayFile.value = input.files?.[0] ?? null;
}

async function parseReplay(): Promise<void> {
  if (!canSubmit.value || replayFile.value === null) {
    return;
  }

  loading.value = true;
  error.value = "";
  response.value = null;

  try {
    const formData = new FormData();
    formData.append("replay", replayFile.value);

    const result = await fetch(endpoint.value, {
      method: "POST",
      body: formData,
    });

    const json = (await result.json()) as ParseResponse;
    if (!result.ok) {
      throw new Error(json.error ?? `Request failed with status ${result.status}`);
    }

    response.value = json;
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Unknown parsing error";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="parser-layout">
    <section class="parser-panel">
      <h2>Parse a replay in this docs app</h2>
      <p>
        This is a real upload workflow. The frontend sends your <code>.dem</code> file to a backend parser endpoint
        and renders the returned JSON summary.
      </p>
      <form class="parser-form" @submit.prevent="parseReplay">
        <div class="parser-row">
          <label for="endpoint">Parser API endpoint</label>
          <input id="endpoint" v-model="endpoint" type="url" placeholder="https://your-domain/api/parse" />
        </div>

        <div class="parser-row">
          <label for="replay">Replay file</label>
          <input id="replay" accept=".dem" type="file" @change="onFileChange" />
        </div>

        <button class="parser-cta" :disabled="!canSubmit" type="submit">
          {{ loading ? "Parsing..." : "Parse Replay" }}
        </button>
      </form>
    </section>

    <section v-if="error" class="parser-panel">
      <p class="parser-error">{{ error }}</p>
    </section>

    <section v-if="response" class="parser-panel">
      <h3>Response</h3>
      <div class="parser-output">
        <pre>{{ JSON.stringify(response, null, 2) }}</pre>
      </div>
    </section>
  </div>
</template>
