import { motion } from 'framer-motion'
import { formatTime, truncateUUID, isToday } from '../../utils/formatters'
import StatusPill from './StatusPill'

export default function AppointmentRow({ appt, isNew }) {
  return (
    <motion.div
      layout
      initial={isNew ? { opacity: 0, y: -8, backgroundColor: 'rgba(52, 211, 153, 0.15)' } : false}
      animate={{ opacity: 1, y: 0, backgroundColor: 'rgba(52, 211, 153, 0)' }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
      style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.5fr 90px 110px 90px 90px', gap: 14, padding: '10px 18px', borderBottom: '1px solid var(--color-border)', alignItems: 'center', fontSize: 12.5, borderLeft: isToday(appt.date) ? '3px solid var(--color-accent)' : '3px solid transparent' }}
    >
      <span style={{ color: 'var(--color-ink-2)', fontFamily: 'var(--font-mono)', fontSize: 11 }} title={appt.user_id}>{truncateUUID(appt.user_id)}</span>
      <span style={{ color: 'var(--color-ink-3)', fontSize: 11 }} title={appt.doctor_id}>{truncateUUID(appt.doctor_id)}</span>
      <span style={{ color: 'var(--color-ink-2)' }}>{appt.date}</span>
      <span style={{ color: 'var(--color-ink)', fontWeight: 600, fontVariantNumeric: 'tabular-nums' }}>{formatTime(appt.start_time)}</span>
      <span style={{ color: 'var(--color-ink-3)' }}>{formatTime(appt.end_time)}</span>
      <StatusPill status={appt.status} />
    </motion.div>
  )
}
