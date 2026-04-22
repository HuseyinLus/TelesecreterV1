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
