import { motion, AnimatePresence } from 'framer-motion'
import { X } from 'lucide-react'
import { formatTime } from '../../utils/formatters'
import { getDoctorColor } from '../../utils/constants'
import StatusPill from '../registry/StatusPill'

const COLOR_BG = { teal: 'var(--color-teal)', sage: 'var(--color-sage)', amber: 'var(--color-amber)', indigo: 'var(--color-indigo)', rose: 'var(--color-rose)' }

export default function AppointmentDrawer({ appt, doctors, onClose }) {
  const doctorById = Object.fromEntries(doctors.map((d, i) => [d.id, { ...d, color: getDoctorColor(i) }]))
  const doc = appt ? doctorById[appt.doctor_id] : null
  const docName = doc?.full_name ?? doc?.name ?? '—'

  return (
    <AnimatePresence>
      {appt && (
        <motion.div
          key="backdrop"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
          onClick={onClose}
          style={{ position: 'fixed', inset: 0, background: 'oklch(18% 0.02 240 / 0.32)', zIndex: 40, display: 'flex', justifyContent: 'flex-end', backdropFilter: 'blur(3px)' }}
        >
          <motion.div
            key="drawer"
            initial={{ x: 20, opacity: 0 }} animate={{ x: 0, opacity: 1 }} exit={{ x: 20, opacity: 0 }}
            transition={{ duration: 0.24, ease: [0.2, 0.8, 0.2, 1] }}
            onClick={(e) => e.stopPropagation()}
            style={{ width: 440, maxWidth: '95vw', height: '100%', background: 'var(--color-surface)', borderLeft: '1px solid var(--color-border)', padding: '22px 24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 16, boxShadow: '0 24px 48px oklch(20% 0.04 240 / 0.10)' }}
          >
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                <div style={{ width: 40, height: 40, borderRadius: '50%', background: doc ? COLOR_BG[doc.color] : 'var(--color-border)', color: 'white', display: 'grid', placeItems: 'center', fontWeight: 600, fontSize: 12.5 }}>
                  {docName.split(' ').filter(Boolean).slice(0, 2).map(w => w[0]).join('')}
                </div>
                <div>
                  <div style={{ fontSize: 17, fontWeight: 600, color: 'var(--color-ink)', letterSpacing: '-0.005em' }}>{appt.user_id?.slice(0, 8)}…</div>
                  <div style={{ fontSize: 12, color: 'var(--color-ink-3)', marginTop: 1 }}>{docName} · {doc?.specialty}</div>
                </div>
              </div>
              <button onClick={onClose} style={{ width: 28, height: 28, borderRadius: 7, display: 'grid', placeItems: 'center', color: 'var(--color-ink-3)', border: 'none', background: 'none', cursor: 'pointer' }}><X size={14} /></button>
            </div>

            {/* Status */}
            <div style={{ display: 'flex', gap: 6 }}>
              <StatusPill status={appt.status} />
            </div>

            {/* Details grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, padding: 14, background: 'var(--color-bg-subtle)', borderRadius: 10 }}>
              {[
                { label: 'Date',       value: appt.date },
                { label: 'Start time', value: formatTime(appt.start_time) },
                { label: 'End time',   value: formatTime(appt.end_time) },
                { label: 'Doctor',     value: docName },
                { label: 'Department', value: doc?.department_name ?? '—' },
                { label: 'Patient ID', value: (appt.user_id?.slice(0, 12) ?? '') + '…' },
              ].map(({ label, value }) => (
                <div key={label}>
                  <div style={{ fontSize: 10, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', fontWeight: 500, marginBottom: 3 }}>{label}</div>
                  <div style={{ fontSize: 13, color: 'var(--color-ink)', fontWeight: 500 }}>{value}</div>
                </div>
              ))}
            </div>

            {/* Actions */}
            <div style={{ marginTop: 'auto', display: 'flex', gap: 8, paddingTop: 12, borderTop: '1px solid var(--color-border)' }}>
              <button style={{ flex: 1, padding: '9px 14px', borderRadius: 8, fontSize: 12.5, fontWeight: 500, background: 'var(--color-accent-soft)', color: 'var(--color-accent-ink)', border: 'none', cursor: 'pointer' }}>Reschedule</button>
              <button style={{ padding: '9px 14px', borderRadius: 8, fontSize: 12.5, fontWeight: 500, color: 'var(--color-danger)', border: '1px solid oklch(58% 0.18 25 / 0.28)', background: 'none', cursor: 'pointer' }}>Cancel</button>
              <button onClick={onClose} style={{ padding: '9px 14px', borderRadius: 8, fontSize: 12.5, fontWeight: 500, color: 'var(--color-ink-2)', border: 'none', background: 'none', cursor: 'pointer' }}>Close</button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
