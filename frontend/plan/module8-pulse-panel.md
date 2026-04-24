# Module 8 — PulsePanel + CallStatusBadge

## Goal
Build Zone 1 (right rail of Dashboard). Shows live call status: ACTIVE/IDLE indicator, animated waveform, call timer, and the empty states. Reads from `callStore` — no API calls.

## Dependencies
- `src/store/callStore.js` (Module 3)
- `lucide-react`
- `framer-motion`

## Files to create
- `src/components/pulse/PulsePanel.jsx`
- `src/components/pulse/CallStatusBadge.jsx`

## Files to modify
- `src/pages/DashboardPage.jsx` — replace Zone 1 placeholder with `<PulsePanel />`

---

## src/components/pulse/CallStatusBadge.jsx
```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { PhoneOff } from 'lucide-react'

export default function CallStatusBadge({ isCallActive, seconds }) {
  const mm = String(Math.floor(seconds / 60)).padStart(2, '0')
  const ss = String(seconds % 60).padStart(2, '0')

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {/* Status row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{ position: 'relative', width: 10, height: 10 }}>
          <span style={{
            display: 'block', width: 10, height: 10, borderRadius: '50%',
            background: isCallActive ? 'var(--color-sage)' : 'var(--color-ink-4)',
            animation: isCallActive ? 'pulse-sage 1.6s infinite' : 'none',
          }} />
        </div>
        <span style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: isCallActive ? 'var(--color-sage-ink)' : 'var(--color-ink-3)' }}>
          {isCallActive ? 'Call active' : 'Waiting…'}
        </span>
        {isCallActive && (
          <span style={{ marginLeft: 'auto', fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--color-ink-2)', fontWeight: 500 }}>
            {mm}:{ss}
          </span>
        )}
      </div>

      {/* Waveform — only when active */}
      <AnimatePresence>
        {isCallActive && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 40 }}
            exit={{ opacity: 0, height: 0 }}
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2 }}
          >
            {Array.from({ length: 28 }).map((_, i) => (
              <span key={i} style={{
                width: 2, borderRadius: 2,
                background: 'var(--color-sage)',
                opacity: 0.65,
                animation: `wave 1s ease-in-out ${i * 0.06}s infinite`,
                height: `${20 + Math.sin(i * 0.7) * 12}%`,
              }} />
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Idle empty state */}
      {!isCallActive && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8, padding: '24px 0', color: 'var(--color-ink-4)' }}>
          <PhoneOff size={40} strokeWidth={1.2} />
          <p style={{ margin: 0, fontSize: 12, textAlign: 'center', color: 'var(--color-ink-3)', lineHeight: 1.5 }}>
            Waiting for first call.<br />The AI agent is standing by.
          </p>
        </div>
      )}
    </div>
  )
}
```

---

## src/components/pulse/PulsePanel.jsx
```jsx
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
        <button onClick={startCall} style={{ flex: 1, padding: '6px', fontSize: 11, border: '1px solid var(--color-border)', borderRadius: 6, color: 'var(--color-sage-ink)', background: 'var(--color-sage-soft)' }}>
          Simulate start
        </button>
        <button onClick={endCall} style={{ flex: 1, padding: '6px', fontSize: 11, border: '1px solid var(--color-border)', borderRadius: 6, color: 'var(--color-ink-3)', background: 'var(--color-surface)' }}>
          Simulate end
        </button>
      </div>
    </div>
  )
}
```

---

## DashboardPage.jsx — Zone 1 update
Replace the Zone 1 placeholder div with:
```jsx
import PulsePanel from '../components/pulse/PulsePanel'
// ...
{/* Zone 1 — Pulse */}
<div style={{ gridRow: 1, gridColumn: 2, overflow: 'hidden' }}>
  <PulsePanel />
</div>
```

---

## Test
1. Visit `/dashboard`

**Pass criteria:**
- Right rail shows "Live Call" header with Activity icon
- Idle state: phone-off icon + "Waiting for first call" message visible
- Click "Simulate start":
  - Left border turns sage-green
  - Background gets subtle green gradient
  - "CALL ACTIVE" text appears with sage dot pulsing
  - Call timer counts up (00:01, 00:02…)
  - Waveform bars animate in with staggered wave motion
- Click "Simulate end":
  - Everything resets to idle state
  - Timer resets to 00:00
  - Waveform disappears (animated out)
