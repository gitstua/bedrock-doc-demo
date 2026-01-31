<script setup>
import Chat from './components/Chat.vue'
</script>

<template>
  <div class="app-layout">
    <header>
      <h1>Bedrock Doc Assistant</h1>
      <p>Your AI-powered knowledge companion</p>
    </header>
    <main>
      <Chat />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 20px;
  gap: 20px;
}

header {
  text-align: center;
  margin-bottom: 10px;
}

h1 {
  font-size: 2.5rem;
  background: linear-gradient(to right, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 8px;
  font-weight: 800;
  letter-spacing: -1px;
}

p {
  color: #a0aec0;
  font-size: 1.1rem;
}

main {
  flex: 1;
  height: calc(100vh - 140px); /* Adjust based on header height */
}
</style>
