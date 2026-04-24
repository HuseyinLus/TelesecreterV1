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
