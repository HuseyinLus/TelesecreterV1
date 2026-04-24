import { create } from 'zustand'
import { nanoid } from 'nanoid'
import { LOG_MAX_ENTRIES } from '../utils/constants'

export const useLogStore = create((set) => ({
  logs: [],
  activeFilter: 'ALL',  // 'ALL' | 'WEBHOOK' | 'ERROR' | 'SUCCESS'

  pushLog: (entry) =>
    set((state) => {
      const next = [{ ...entry, id: nanoid() }, ...state.logs]
      return { logs: next.length > LOG_MAX_ENTRIES ? next.slice(0, LOG_MAX_ENTRIES) : next }
    }),

  clearLogs: () => set({ logs: [] }),

  setFilter: (filter) => set({ activeFilter: filter }),
}))
