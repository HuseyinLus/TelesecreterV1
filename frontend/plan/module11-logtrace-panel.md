# Module 11 — LogTracePanel

## Goal
Build Zone 3 (full-width bottom panel). Auto-scrolling log console that displays every API call captured by the Axios interceptor. Includes filter bar and collapsible JSON viewer.

## Dependencies
- `src/store/logStore.js` (Module 3)
- `src/services/logInterceptor.js` (Module 4) — already pushing to logStore
- `lucide-react`

## Files to create
- `src/components/logtrace/LogTracePanel.jsx`
- `src/components/logtrace/LogFilterBar.jsx`
- `src/components/logtrace/LogEntry.jsx`
- `src/components/logtrace/JsonViewer.jsx`

## Files to modify
- `src/pages/DashboardPage.jsx` — replace Zone 3 placeholder with `<LogTracePanel />`

---

## src/components/logtrace/JsonViewer.jsx
```jsx
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
```

---

## src/components/logtrace/LogEntry.jsx
```jsx
import JsonViewer from './JsonViewer'

const METHOD_COLORS = {
  GET:    { bg: 'oklch(56% 0.09 210 / 0.15)', color: 'var(--color-accent-ink)' },
  POST:   { bg: 'oklch(62% 0.07 160 / 0.15)', color: 'var(--color-sage-ink)' },
  PATCH:  { bg: 'oklch(72% 0.11 70 / 0.15)',  color: 'var(--color-amber)' },
  DELETE: { bg: 'oklch(66% 0.11 20 / 0.15)',  color: 'var(--color-rose)' },
}

const statusColor = (code) => {
  if (!code || code === 0) return 'var(--color-ink-4)'
  if (code < 300) return 'var(--color-sage-ink)'
  if (code < 400) return 'var(--color-amber)'
  return 'var(--color-rose)'
}

export default function LogEntry({ entry }) {
  const m = METHOD_COLORS[entry.method] ?? { bg: 'var(--color-bg-subtle)', color: 'var(--color-ink-3)' }
  const ts = new Date(entry.timestamp)
  const timeStr = `${ts.getHours().toString().padStart(2,'0')}:${ts.getMinutes().toString().padStart(2,'0')}:${ts.getSeconds().toString().padStart(2,'0')}.${ts.getMilliseconds().toString().padStart(3,'0')}`
  const isError = entry.statusCode >= 400

  return (
    <div style={{
      padding: '5px 14px',
      borderLeft: isError ? '3px solid var(--color-rose)' : '3px solid transparent',
      borderBottom: '1px solid var(--color-border)',
      fontFamily: 'var(--font-mono)',
      fontSize: 11,
    }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, flexWrap: 'wrap' }}>
        <span style={{ color: 'var(--color-ink-4)', flexShrink: 0 }}>{timeStr}</span>
        <span style={{ padding: '1px 5px', borderRadius: 4, fontSize: 9.5, fontWeight: 700, background: m.bg, color: m.color, flexShrink: 0 }}>{entry.method}</span>
        <span style={{ color: 'var(--color-ink-2)', flex: 1, minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{entry.path}</span>
        <span style={{ color: statusColor(entry.statusCode), fontWeight: 600, flexShrink: 0 }}>{entry.statusCode}</span>
        <span style={{ color: 'var(--color-ink-4)', flexShrink: 0 }}>{entry.durationMs}ms</span>
      </div>
      <JsonViewer label="request"  data={entry.requestBody} />
      <JsonViewer label="response" data={entry.responseBody} />
    </div>
  )
}
```

---

## src/components/logtrace/LogFilterBar.jsx
```jsx
import { Terminal, Trash2 } from 'lucide-react'
import { useLogStore } from '../../store/logStore'

const FILTERS = ['ALL', 'WEBHOOK', 'ERROR', 'SUCCESS']

export default function LogFilterBar() {
  const { activeFilter, setFilter, clearLogs, logs } = useLogStore()

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 14px', borderBottom: '1px solid var(--color-border)', flexShrink: 0 }}>
      <Terminal size={13} color="var(--color-ink-3)" />
      <span style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-3)', marginRight: 4 }}>Logic Trace</span>
      <div style={{ display: 'flex', gap: 4 }}>
        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            style={{
              padding: '3px 9px', borderRadius: 5, fontSize: 10.5, fontWeight: 500, border: '1px solid var(--color-border)',
              background: activeFilter === f ? 'var(--color-accent-soft)' : 'transparent',
              color: activeFilter === f ? 'var(--color-accent-ink)' : 'var(--color-ink-3)',
              cursor: 'pointer',
            }}
          >
            {f}
            {f === 'ERROR' && logs.filter(l => l.statusCode >= 400).length > 0 && (
              <span style={{ marginLeft: 4, background: 'var(--color-rose)', color: 'white', fontSize: 9, padding: '0 4px', borderRadius: 4 }}>
                {logs.filter(l => l.statusCode >= 400).length}
              </span>
            )}
          </button>
        ))}
      </div>
      <button
        onClick={clearLogs}
        style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 5, padding: '3px 9px', borderRadius: 5, fontSize: 10.5, color: 'var(--color-ink-3)', border: '1px solid var(--color-border)', cursor: 'pointer' }}
      >
        <Trash2 size={11} />
        Clear
      </button>
    </div>
  )
}
```

---

## src/components/logtrace/LogTracePanel.jsx
```jsx
import { useEffect, useRef, useState } from 'react'
import { ChevronsDown } from 'lucide-react'
import { useLogStore } from '../../store/logStore'
import LogFilterBar from './LogFilterBar'
import LogEntry from './LogEntry'

function applyFilter(logs, filter) {
  if (filter === 'ALL')     return logs
  if (filter === 'ERROR')   return logs.filter(l => l.statusCode >= 400)
  if (filter === 'SUCCESS') return logs.filter(l => l.statusCode >= 200 && l.statusCode < 300)
  if (filter === 'WEBHOOK') return logs.filter(l => l.path?.includes('/scheduales') || l.path?.includes('/appointments/set'))
  return logs
}

export default function LogTracePanel() {
  const { logs, activeFilter } = useLogStore()
  const bottomRef = useRef(null)
  const scrollRef = useRef(null)
  const [userScrolledUp, setUserScrolledUp] = useState(false)

  const visible = applyFilter(logs, activeFilter)

  // Auto-scroll to bottom on new log entry
  useEffect(() => {
    if (!userScrolledUp) bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs.length, userScrolledUp])

  const handleScroll = () => {
    const el = scrollRef.current
    if (!el) return
    const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 20
    setUserScrolledUp(!atBottom)
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden', background: 'var(--color-surface-2)' }}>
      <LogFilterBar />

      <div ref={scrollRef} onScroll={handleScroll} style={{ flex: 1, overflowY: 'auto', position: 'relative' }}>
        {visible.length === 0 ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '12px 14px', color: 'var(--color-ink-4)', fontFamily: 'var(--font-mono)', fontSize: 11 }}>
            No requests logged yet. API calls will appear here automatically.
          </div>
        ) : (
          visible.map((entry) => <LogEntry key={entry.id} entry={entry} />)
        )}
        <div ref={bottomRef} />
      </div>

      {userScrolledUp && (
        <button
          onClick={() => { setUserScrolledUp(false); bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }}
          style={{ position: 'absolute', bottom: 268, right: 16, display: 'flex', alignItems: 'center', gap: 5, padding: '5px 10px', borderRadius: 7, fontSize: 11, background: 'var(--color-ink)', color: 'var(--color-bg)', border: 'none', cursor: 'pointer', boxShadow: '0 4px 12px oklch(20% 0.04 240 / 0.15)' }}
        >
          <ChevronsDown size={12} />
          Jump to latest
        </button>
      )}
    </div>
  )
}
```

---

## DashboardPage.jsx — Zone 3 update
```jsx
import LogTracePanel from '../components/logtrace/LogTracePanel'
// replace Zone 3 placeholder div:
<div style={{ gridRow: 2, gridColumn: '1 / -1', overflow: 'hidden', borderTop: '1px solid var(--color-border)' }}>
  <LogTracePanel />
</div>
```

---

## Test
**Backend must be running.**

1. Visit `/dashboard`
2. The Logic Trace panel (bottom) immediately shows log entries for `/doctors/` and `/appointments/` from the polling hooks

**Pass criteria:**
- Log entries appear automatically with timestamp, method badge (GET in blue), path, status code (200 in green), and duration
- Clicking "response" toggle on any entry expands the JSON tree
- Switching to ERROR filter shows only failed requests (red badge count)
- Switching to WEBHOOK filter shows only `/scheduales/` and `/appointments/set` paths
- Clicking "Clear" empties the log
- Scroll up manually → "↓ Jump to latest" button appears; click it → scrolls back to bottom
