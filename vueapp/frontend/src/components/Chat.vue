<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const messages = ref([
  { role: 'assistant', content: 'Hello! I am your Bedrock Doc Assistant. How can I help you today?' }
])
const newMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return

  const userMsg = newMessage.value.trim()
  messages.value.push({ role: 'user', content: userMsg })
  newMessage.value = ''
  isLoading.value = true
  await scrollToBottom()

  try {
    const response = await axios.post('http://127.0.0.1:8000/chat', {
      query: userMsg
      // kb_id and model_arn are handled by backend defaults from .env
    })
    
    messages.value.push({ role: 'assistant', content: response.data.response })
  } catch (error) {
    console.error(error)
    messages.value.push({ role: 'assistant', content: 'Sorry, I encountered an error connecting to the Knowledge Base.' })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}
</script>

<template>
  <div class="chat-container">
    <div class="messages-area" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <div class="message-bubble">
          {{ msg.content }}
        </div>
      </div>
      <div v-if="isLoading" class="message assistant">
        <div class="message-bubble loading">
          <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        </div>
      </div>
    </div>

    <div class="input-area">
      <input 
        v-model="newMessage" 
        @keyup.enter="sendMessage"
        type="text" 
        placeholder="Ask a question..."
        :disabled="isLoading"
      />
      <button @click="sendMessage" :disabled="isLoading || !newMessage.trim()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="send-icon">
          <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 900px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scroll-behavior: smooth;
}

.message {
  display: flex;
  margin-bottom: 8px;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 18px;
  border-radius: 18px;
  font-size: 1rem;
  line-height: 1.5;
  position: relative;
  word-wrap: break-word;
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
  box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4);
}

.message.assistant .message-bubble {
  background: rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
  border-bottom-left-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.input-area {
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  gap: 12px;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

input {
  flex: 1;
  padding: 14px 20px;
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.3);
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
}

input:focus {
  border-color: #764ba2;
  box-shadow: 0 0 0 2px rgba(118, 75, 162, 0.3);
  background: rgba(0, 0, 0, 0.5);
}

button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  color: white;
}

button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(118, 75, 162, 0.5);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(100%);
}

.send-icon {
  width: 24px;
  height: 24px;
}

/* Loading animation */
.loading {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 60px;
  justify-content: center;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: #a0aec0;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>
