import { create } from 'zustand'

const useChatStore = create((set) => ({
  conversations: {},
  currentConversationId: null,
  messages: [],
  loading: false,
  error: null,

  setCurrentConversation: (id) => set({ currentConversationId: id }),
  
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
  clearMessages: () => set({ messages: [] }),
}))

export default useChatStore
