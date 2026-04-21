# Module 9 — AuthBadge + ExtractedVarsCard + DoctorInFocusCard

## Goal
Complete Zone 1 (Pulse panel) with the three information cards that appear during an active call: caller identity badge, extracted variables (Doctor ID / Date / Time), and the resolved doctor card.

## Dependencies
- `src/store/callStore.js` (Module 3)
- `framer-motion`
- `lucide-react`

## Files to create
- `src/components/pulse/AuthBadge.jsx`
- `src/components/pulse/ExtractedVarsCard.jsx`
- `src/components/pulse/DoctorInFocusCard.jsx`

## Files to modify
- `src/components/pulse/PulsePanel.jsx` — add the three cards below `CallStatusBadge`

---

## src/components/pulse/AuthBadge.jsx
```jsx
import { motion } from 'framer-motion'
import { UserCheck, UserX } from 'lucide-react'

export default function AuthBadge({ isAuthenticated, callerName }) {
  const recognized = isAuthenticated === true
  const unknown    = isAuthenticated === false
  const pending    = isAuthenticated === null

  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
      style={{
        padding: '10px 12px',
        borderRadius: 10,
        borderLeft: `3px solid ${recognized ? 'var(--color-sage)' : 'var(--color-border-strong)'}`,
        background: recognized ? 'oklch(62% 0.07 160 / 0.08)' : 'oklch(28% 0.016 240 / 0.3)',
        border: `1px solid ${recognized ? 'oklch(62% 0.07 160 / 0.28)' : 'var(--color-border)'}`,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
        {recognized ? <UserCheck size={14} color="var(--color-sage-ink)" /> : <UserX size={14} color="var(--color-ink-3)" />}
        <span style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: recognized ? 'var(--color-sage-ink)' : 'var(--color-ink-3)' }}>
          {recognized ? 'Recognized Patient' : unknown ? 'Unknown Caller' : 'Verifying identity…'}
        </span>
      </div>
      {recognized && callerName && (
        <div style={{ fontSize: 13, fontWeight: 500, color: 'var(--color-ink)' }}>{callerName}</div>
      )}
    </motion.div>
  )
}
```

---

## src/components/pulse/ExtractedVarsCard.jsx
```jsx
import { motion, AnimatePresence } from 'framer-motion'

const VAR_ROWS = [
  { key: 'extractedDoctorId', label: 'Doctor ID' },
  { key: 'extractedDateStr',  label: 'Date' },
  { key: 'extractedTimeStr',  label: 'Time' },
]

export default function ExtractedVarsCard({ callState }) {
  const hasAny = VAR_ROWS.some(({ key }) => callState[key])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
      <span style={{ fontSize: 10, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)' }}>
        Extracted Variables
      </span>
      {VAR_ROWS.map(({ key, label }, i) => (
        <div key={key} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '6px 10px', background: 'var(--color-bg-subtle)', borderRadius: 7, fontSize: 12 }}>
          <span style={{ color: 'var(--color-ink-3)' }}>{label}</span>
          <AnimatePresence mode="wait">
            {callState[key] ? (
              <motion.span
                key={callState[key]}
                initial={{ opacity: 0, x: -4 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.25, delay: i * 0.08 }}
                style={{ fontWeight: 600, color: 'var(--color-ink)', fontFamily: 'var(--font-mono)', fontSize: 11 }}
              >
                {callState[key]}
              </motion.span>
            ) : (
              <motion.span key="empty" style={{ color: 'var(--color-ink-4)' }}>—</motion.span>
            )}
          </AnimatePresence>
        </div>
      ))}

      {/* Typing dots while waiting */}
      {!hasAny && (
        <div style={{ display: 'flex', gap: 3, padding: '4px 10px' }}>
          {[0, 1, 2].map((i) => (
            <span key={i} style={{ width: 5, height: 5, background: 'var(--color-ink-4)', borderRadius: '50%', display: 'inline-block', animation: `typing 1.4s ${i * 0.2}s infinite` }} />
          ))}
        </div>
      )}
    </div>
  )
}
```

---

## src/components/pulse/DoctorInFocusCard.jsx
```jsx
import { motion } from 'framer-motion'
import { Stethoscope } from 'lucide-react'

export default function DoctorInFocusCard({ doctorName, specialty }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 4 }}
      transition={{ duration: 0.25 }}
      style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px', background: 'var(--color-accent-soft)', borderRadius: 10, border: '1px solid var(--color-border)' }}
    >
      <Stethoscope size={16} color="var(--color-accent-ink)" />
      <div>
        <div style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--color-ink)' }}>{doctorName}</div>
        <div style={{ fontSize: 11, color: 'var(--color-ink-3)', marginTop: 1 }}>{specialty}</div>
      </div>
    </motion.div>
  )
}
```

---

## PulsePanel.jsx — updated (replace full file)
```jsx
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
          <button onClick={startCall} style={{ flex: 1, padding: 6, fontSize: 11, border: '1px solid var(--color-border)', borderRadius: 6, color: 'var(--color-sage-ink)', background: 'var(--color-sage-soft)' }}>Start</button>
          <button onClick={endCall}   style={{ flex: 1, padding: 6, fontSize: 11, border: '1px solid var(--color-border)', borderRadius: 6, color: 'var(--color-ink-3)', background: 'var(--color-surface)' }}>End</button>
        </div>
        {isCallActive && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            <button onClick={() => setAuthenticated(true, 'Ahmet Yılmaz')} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)' }}>Set: Recognized patient</button>
            <button onClick={() => setAuthenticated(false)} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)' }}>Set: Unknown caller</button>
            <button onClick={() => setExtractedVar('extractedDoctorId', 'dr-001')} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)' }}>Set: Doctor ID</button>
            <button onClick={() => setExtractedVar('extractedDateStr', '04.21')} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)' }}>Set: Date</button>
            <button onClick={() => setExtractedVar('extractedTimeStr', '10:30')} style={{ padding: 5, fontSize: 10, border: '1px solid var(--color-border)', borderRadius: 5, color: 'var(--color-ink-2)', background: 'var(--color-surface)' }}>Set: Time</button>
          </div>
        )}
      </div>
    </div>
  )
}
```

---

## Test
1. Visit `/dashboard`, click "Start"
2. Click "Set: Recognized patient" → AuthBadge springs in showing "Ahmet Yılmaz"
3. Click "Set: Unknown caller" → AuthBadge switches to "Unknown Caller" style
4. Click "Set: Doctor ID" → DoctorInFocusCard appears; Doctor ID row in ExtractedVarsCard fills in
5. Click "Set: Date" and "Set: Time" → remaining rows fill in with slide-in animation
6. Click "End" → all cards disappear, panel returns to idle state

**Pass criteria:** All six interactions above work with smooth Framer Motion transitions and no console errors.
