import { useEffect } from 'react'
import apiClient from './services/apiClient'
import { useLogStore } from './store/logStore'

export default function App() {
  const { logs } = useLogStore()

  useEffect(() => {
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
