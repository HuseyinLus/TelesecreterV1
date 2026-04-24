import { formatTime, isToday } from '../../utils/formatters'
import { getDoctorColor } from '../../utils/constants'
import StatusPill from '../registry/StatusPill'

const COLS = '80px 100px 1.2fr 1.2fr 2fr 80px 100px'
const HeadCell = ({ children }) => (
  <div style={{ fontSize: 10.5, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', fontWeight: 500 }}>{children}</div>
)
const DOT_BG = { teal: 'var(--color-teal)', sage: 'var(--color-sage)', amber: 'var(--color-amber)', indigo: 'var(--color-indigo)', rose: 'var(--color-rose)' }

export default function ListView({ appointments, doctors, filters, selectedId, onSelect }) {
  const doctorById = Object.fromEntries(doctors.map((d, i) => [d.id, { ...d, color: getDoctorColor(i) }]))
  const filtered = appointments
    .filter((a) => filters.doctorId === 'all' || a.doctor_id === filters.doctorId)
    .sort((a, b) => a.date.localeCompare(b.date) || a.start_time.localeCompare(b.start_time))

  return (
    <div style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 14, overflow: 'hidden' }}>
      <div style={{ display: 'grid', gridTemplateColumns: COLS, gap: 14, padding: '10px 18px', background: 'var(--color-surface-2)', borderBottom: '1px solid var(--color-border)' }}>
        <HeadCell>Date</HeadCell><HeadCell>Time</HeadCell><HeadCell>Patient</HeadCell>
        <HeadCell>Doctor</HeadCell><HeadCell>Dept</HeadCell><HeadCell>Source</HeadCell><HeadCell>Status</HeadCell>
      </div>
      {filtered.map((a) => {
        const doc = doctorById[a.doctor_id]
        const today = isToday(a.date)
        const docName = (doc?.full_name ?? doc?.name ?? '—').replace('Dr. ', '')
        return (
          <button key={a.id} onClick={() => onSelect(a)} style={{ display: 'grid', gridTemplateColumns: COLS, gap: 14, padding: '10px 18px', alignItems: 'center', width: '100%', textAlign: 'left', fontSize: 12.5, borderBottom: '1px solid var(--color-border)', borderLeft: today ? '3px solid var(--color-accent)' : '3px solid transparent', background: selectedId === a.id ? 'var(--color-accent-soft)' : 'transparent', transition: 'background 0.1s', cursor: 'pointer', border: 'none' }}>
            <div style={{ color: 'var(--color-ink-3)', fontWeight: today ? 600 : 400 }}>{a.date}</div>
            <div style={{ color: 'var(--color-ink)', fontWeight: 600, fontVariantNumeric: 'tabular-nums' }}>{formatTime(a.start_time)}</div>
            <div style={{ color: 'var(--color-ink-2)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontFamily: 'var(--font-mono)', fontSize: 11 }} title={a.user_id}>{a.user_id?.slice(0, 8)}…</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--color-ink-2)' }}>
              {doc && <span style={{ width: 8, height: 8, borderRadius: '50%', flexShrink: 0, background: DOT_BG[doc.color] }} />}
              <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{docName}</span>
            </div>
            <div style={{ color: 'var(--color-ink-3)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{doc?.department_name ?? '—'}</div>
            <div style={{ fontSize: 10, padding: '1px 5px', borderRadius: 4, background: 'var(--color-bg-subtle)', color: 'var(--color-ink-3)', fontWeight: 600, width: 'fit-content' }}>AI</div>
            <StatusPill status={a.status} />
          </button>
        )
      })}
    </div>
  )
}
