import { motion } from 'framer-motion'
import { UserCheck, UserX } from 'lucide-react'

export default function AuthBadge({ isAuthenticated, callerName }) {
  const recognized = isAuthenticated === true
  const unknown    = isAuthenticated === false

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
