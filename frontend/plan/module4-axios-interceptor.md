# Module 4 — Axios Client + Log Interceptor

## Goal
Create the Axios instance and attach the request/response interceptors that automatically push every API call into `logStore`. After this module, every HTTP call is logged with no extra code needed in hooks or components.

## Dependencies
- `axios` (already installed)
- `src/utils/constants.js` (Module 2)
- `src/store/logStore.js` (Module 3)

## Files to create
- `src/services/apiClient.js`
- `src/services/logInterceptor.js`

---

## src/services/apiClient.js
```js
import axios from 'axios'
import { API_BASE_URL } from '../utils/constants'
import { attachLogInterceptor } from './logInterceptor'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10_000,
})

attachLogInterceptor(apiClient)

export default apiClient
```

---

## src/services/logInterceptor.js
```js
import { useLogStore } from '../store/logStore'

export function attachLogInterceptor(client) {
  // REQUEST — start timer, record metadata
  client.interceptors.request.use((config) => {
    config._logStart = performance.now()
    config._logMethod = config.method?.toUpperCase()
    config._logPath   = config.url
    return config
  })

  // RESPONSE SUCCESS
  client.interceptors.response.use(
    (response) => {
      useLogStore.getState().pushLog({
        timestamp:    new Date(),
        method:       response.config._logMethod,
        path:         response.config._logPath,
        statusCode:   response.status,
        requestBody:  response.config.data ? JSON.parse(response.config.data) : null,
        responseBody: response.data,
        durationMs:   Math.round(performance.now() - response.config._logStart),
      })
      return response
    },
    // RESPONSE ERROR
    (error) => {
      useLogStore.getState().pushLog({
        timestamp:    new Date(),
        method:       error.config?._logMethod,
        path:         error.config?._logPath,
        statusCode:   error.response?.status ?? 0,
        requestBody:  error.config?.data ? JSON.parse(error.config.data) : null,
        responseBody: error.response?.data ?? { message: error.message },
        durationMs:   Math.round(performance.now() - (error.config?._logStart ?? performance.now())),
      })
      return Promise.reject(error)
    }
  )
}
```

---

## Test
In `src/App.jsx`:

```jsx
import { useEffect } from 'react'
import apiClient from './services/apiClient'
import { useLogStore } from './store/logStore'

export default function App() {
  const { logs } = useLogStore()

  useEffect(() => {
    // Fire a real request to the running backend
    apiClient.get('/doctors/').catch(() => {})
  }, [])

  return (
    <div style={{ padding: 24, fontFamily: 'monospace' }}>
      <h3>Log entries: {logs.length}</h3>
      {logs.map((l) => (
        <div key={l.id} style={{ marginBottom: 8, fontSize: 11 }}>
          <strong>{l.method}</strong> {l.path} → {l.statusCode} ({l.durationMs}ms)
        </div>
      ))}
    </div>
  )
}
```

**Pass criteria (backend must be running on port 8000):**
- On page load, one log entry appears automatically
- Entry shows: `GET /doctors/ → 200 (Xms)`
- No manual `pushLog()` call was made — the interceptor handled it
- If backend is offline: entry still appears with `statusCode: 0` or `503`
