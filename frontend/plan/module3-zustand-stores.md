# Module 3 — Zustand Stores

## Goal
Create the two client-side state stores: `callStore` (live call variables) and `logStore` (API log entries). No UI yet — pure state logic.

## Dependencies
- `zustand` (already installed)
- `nanoid` (already installed)

## Files to create
- `src/store/callStore.js`
- `src/store/logStore.js`

---

## src/store/callStore.js
```js
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
```

---

## src/store/logStore.js
```js
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
```

---

## Test
In `src/App.jsx`:

```jsx
import { useCallStore } from './store/callStore'
import { useLogStore } from './store/logStore'

export default function App() {
  const { isCallActive, callerName, startCall, setAuthenticated, endCall } = useCallStore()
  const { logs, pushLog, clearLogs } = useLogStore()

  return (
    <div style={{ padding: 24, fontFamily: 'monospace' }}>
      <h3>callStore</h3>
      <p>isCallActive: {String(isCallActive)}</p>
      <p>callerName: {callerName ?? 'null'}</p>
      <button onClick={startCall}>startCall()</button>{' '}
      <button onClick={() => setAuthenticated(true, 'Ahmet Yılmaz')}>setAuthenticated()</button>{' '}
      <button onClick={endCall}>endCall()</button>

      <h3 style={{ marginTop: 24 }}>logStore</h3>
      <p>entries: {logs.length}</p>
      <button onClick={() => pushLog({ method: 'GET', path: '/doctors/', statusCode: 200, timestamp: new Date(), requestBody: null, responseBody: [], durationMs: 42 })}>
        pushLog()
      </button>{' '}
      <button onClick={clearLogs}>clearLogs()</button>
      <pre style={{ fontSize: 11 }}>{JSON.stringify(logs[0], null, 2)}</pre>
    </div>
  )
}
```

**Pass criteria:**
- Clicking `startCall()` → `isCallActive` becomes `true`
- Clicking `setAuthenticated()` → `callerName` becomes "Ahmet Yılmaz"
- Clicking `endCall()` → both reset to defaults
- Clicking `pushLog()` → `entries` increments, log object appears in `<pre>`
- Clicking `clearLogs()` → `entries` back to 0
