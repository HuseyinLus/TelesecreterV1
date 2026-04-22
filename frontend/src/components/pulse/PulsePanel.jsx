import { useEffect, useState } from 'react'
import { Activity } from 'lucide-react'
import { useCallStore } from '../../store/callStore'
import CallStatusBadge from './CallStatusBadge'

export default function PulsePanel() {
  const { isCallActive, startCall, endCall } = useCallStore()
  const [seconds, setSeconds] = useState(0)

  useEffect(() => {
    if (!isCallActive) { setSeconds(0); return }
    const iv = setInterval(() => setSeconds((s) => s + 1), 1000)
    return () => clearInterval(iv)
  }, [isCallActive])

  return (
    <div style={{
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      padding: 20,
      gap: 16,
      background: isCallActive
        ? 'linear-gradient(180deg, oklch(62% 0.07 160 / 0.06), var(--color-surface) 30%)'
        : 'var(--color-surface)',
      borderLeft: `3px solid ${isCallActive ? 'var(--color-sage)' : 'var(--color-border)'}`,
      transition: 'border-color 0.3s, background 0.3s',
    }}>
      {/* Section header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <Activity size={15} color="var(--color-ink-3)" />
        <span style={{ fontSize: 12, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-3)' }}>Live Call</span>
      </div>

      <CallStatusBadge isCallActive={isCallActive} seconds={seconds} />

      {/* Dev toggle — remove in production */}
      <div style={{ marginTop: 'auto', display: 'flex', gap: 8 }}>
        <button onClick={startCall} style={{ flex: 1, padding: '6px', fontSize: 11, border: '1px solid var(--color-border)', borderRadius: 6, color: 'var(--color-sage-ink)', background: 'var(--color-sage-soft)', cursor: 'pointer' }}>
          Simulate start
        </button>
        <button onClick={endCall} style={{ flex: 1, padding: '6px', fontSize: 11, border: '1px solid var(--color-border)', borderRadius: 6, color: 'var(--color-ink-3)', background: 'var(--color-surface)', cursor: 'pointer' }}>
          Simulate end
        </button>
      </div>
    </div>
  )
}
