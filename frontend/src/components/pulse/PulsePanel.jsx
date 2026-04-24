import { useEffect, useState } from 'react'
import { Activity } from 'lucide-react'
import { AnimatePresence } from 'framer-motion'
import { useCallStore } from '../../store/callStore'
import CallStatusBadge from './CallStatusBadge'
import AuthBadge from './AuthBadge'
import ExtractedVarsCard from './ExtractedVarsCard'
import DoctorInFocusCard from './DoctorInFocusCard'

export default function PulsePanel() {
  const store = useCallStore()
  const { isCallActive, isAuthenticated, callerName, extractedDoctorId, startCall, endCall, setAuthenticated, setExtractedVar } = store
  const [seconds, setSeconds] = useState(0)

  useEffect(() => {
    if (!isCallActive) { setSeconds(0); return }
    const iv = setInterval(() => setSeconds((s) => s + 1), 1000)
    return () => clearInterval(iv)
  }, [isCallActive])

  return (
    <div style={{
      height: '100%', display: 'flex', flexDirection: 'column', padding: 20, gap: 16, overflowY: 'auto',
      background: isCallActive ? 'linear-gradient(180deg, oklch(62% 0.07 160 / 0.06), var(--color-surface) 30%)' : 'var(--color-surface)',
      borderLeft: `3px solid ${isCallActive ? 'var(--color-sage)' : 'var(--color-border)'}`,
      transition: 'border-color 0.3s, background 0.3s',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <Activity size={15} color="var(--color-ink-3)" />
        <span style={{ fontSize: 12, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-3)' }}>Live Call</span>
      </div>

      <CallStatusBadge isCallActive={isCallActive} seconds={seconds} />

      <AnimatePresence>
        {isCallActive && (
          <>
            <AuthBadge isAuthenticated={isAuthenticated} callerName={callerName} />
            {extractedDoctorId && <DoctorInFocusCard doctorName="Dr. Aysel Demir" specialty="Cardiology" />}
            <ExtractedVarsCard callState={store} />
          </>
        )}
      </AnimatePresence>

      {/* Dev controls — remove in production */}
      <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: 6 }}>
        <div style={{ display: 'flex', gap: 6 }}>
          <button onClick={startCall} style={{ flex: 1, padding: 6, fontSize: 11, border: '1px solid var(--color-border)', borderRadius: 6, color: 'var(--color-sage-ink)', background: 'var(--color-sage-soft)', cursor: 'pointer' }}>Start</button>
          <button onClick={endCall}   style={{ flex: 1, padding: 6, fontSize: 11, border: '1px solid var(--color-border)', borderRadius: 6, color: 'var(--color-ink-3)', background: 'var(--color-surface)', cursor: 'pointer' }}>End</button>
        </div>
        {isCallActive && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            <button onClick={() => setAuthenticated(true, 'Ahmet Yılmaz')} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)', cursor: 'pointer' }}>Set: Recognized patient</button>
            <button onClick={() => setAuthenticated(false)} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)', cursor: 'pointer' }}>Set: Unknown caller</button>
            <button onClick={() => setExtractedVar('extractedDoctorId', 'dr-001')} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)', cursor: 'pointer' }}>Set: Doctor ID</button>
            <button onClick={() => setExtractedVar('extractedDateStr', '04.21')} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)', cursor: 'pointer' }}>Set: Date</button>
            <button onClick={() => setExtractedVar('extractedTimeStr', '10:30')} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)', cursor: 'pointer' }}>Set: Time</button>
          </div>
        )}
      </div>
    </div>
  )
}
