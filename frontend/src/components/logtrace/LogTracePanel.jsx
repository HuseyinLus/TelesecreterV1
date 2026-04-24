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
