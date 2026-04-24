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
