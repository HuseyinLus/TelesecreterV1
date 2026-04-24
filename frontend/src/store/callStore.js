import { create } from 'zustand'

const defaultState = {
  isCallActive:       false,
  isAuthenticated:    null,   // null = unknown, true = recognized, false = unknown caller
  callerName:         null,
  callerUserId:       null,
  extractedDoctorId:  null,
  extractedDateStr:   null,
  extractedTimeStr:   null,
}

export const useCallStore = create((set) => ({
  ...defaultState,

  startCall: () => set({ ...defaultState, isCallActive: true }),

  endCall: () => set({ ...defaultState }),

  setAuthenticated: (bool, name = null, userId = null) =>
    set({ isAuthenticated: bool, callerName: name, callerUserId: userId }),

  setExtractedVar: (key, value) => set({ [key]: value }),
}))
