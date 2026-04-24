import { useState } from 'react'
import { ChevronRight, ChevronDown } from 'lucide-react'

export default function JsonViewer({ label, data }) {
  const [open, setOpen] = useState(false)
  if (!data) return null

  return (
    <div style={{ marginTop: 4 }}>
      <button
        onClick={() => setOpen((o) => !o)}
        style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 10, color: 'var(--color-ink-4)', background: 'none', border: 'none', cursor: 'pointer', padding: 0, fontFamily: 'var(--font-mono)' }}
      >
        {open ? <ChevronDown size={11} /> : <ChevronRight size={11} />}
        {label}
      </button>
      {open && (
        <pre style={{ margin: '4px 0 0 14px', fontSize: 10, color: 'var(--color-ink-3)', fontFamily: 'var(--font-mono)', whiteSpace: 'pre-wrap', wordBreak: 'break-all', lineHeight: 1.4 }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  )
}
