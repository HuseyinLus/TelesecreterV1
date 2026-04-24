import { HOUR_HEIGHT, GRID_HOURS, GRID_START_HOUR, getDoctorColor } from '../../utils/constants'
import { toMinutes, formatTime } from '../../utils/formatters'
import NowIndicator from './NowIndicator'

const COLOR_STYLES = {
  teal:   { bg: 'var(--color-teal-soft)',   stripe: 'var(--color-teal)'   },
  sage:   { bg: 'var(--color-sage-soft)',   stripe: 'var(--color-sage)'   },
  amber:  { bg: 'var(--color-amber-soft)',  stripe: 'var(--color-amber)'  },
  indigo: { bg: 'var(--color-indigo-soft)', stripe: 'var(--color-indigo)' },
  rose:   { bg: 'var(--color-rose-soft)',   stripe: 'var(--color-rose)'   },
}

export default function DayView({ appointments, doctors, filters, selectedId, onSelect }) {
  const todayDate = new Date().toISOString().slice(0, 10)
  const doctorById = Object.fromEntries(doctors.map((d, i) => [d.id, { ...d, color: getDoctorColor(i) }]))

  const filtered = appointments.filter((a) => {
    if (a.date !== todayDate) return false
    if (filters.doctorId !== 'all' && a.doctor_id !== filters.doctorId) return false
    return true
  })

  const activeDoctors = doctors.filter((d) =>
    filters.doctorId === 'all' || d.id === filters.doctorId
  )

  return (
    <div style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 14, overflow: 'hidden' }}>
      {/* Header — one column per doctor */}
      <div style={{ display: 'grid', gridTemplateColumns: `64px repeat(${activeDoctors.length}, 1fr)`, borderBottom: '1px solid var(--color-border)', background: 'var(--color-surface-2)' }}>
        <div />
        {activeDoctors.map((d) => {
          const color = getDoctorColor(doctors.indexOf(d))
          const c = COLOR_STYLES[color]
          const fullName = d.full_name ?? d.name ?? ''
          const initials = fullName.split(' ').filter(Boolean).slice(0, 2).map(w => w[0]).join('')
          return (
            <div key={d.id} style={{ padding: '12px 10px', borderLeft: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{ width: 30, height: 30, borderRadius: '50%', background: c.stripe, color: 'white', display: 'grid', placeItems: 'center', fontSize: 11, fontWeight: 600 }}>{initials}</div>
              <div>
                <div style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--color-ink)' }}>{fullName.replace('Dr. ', '')}</div>
                <div style={{ fontSize: 10.5, color: 'var(--color-ink-3)' }}>{d.specialty}</div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Body */}
      <div style={{ display: 'grid', gridTemplateColumns: `64px repeat(${activeDoctors.length}, 1fr)`, position: 'relative' }}>
        {/* Hour gutter */}
        <div>
          {GRID_HOURS.map((h) => (
            <div key={h} style={{ height: HOUR_HEIGHT, paddingRight: 8, textAlign: 'right', fontSize: 10.5, color: 'var(--color-ink-4)' }}>
              <span style={{ position: 'relative', top: -6, fontVariantNumeric: 'tabular-nums' }}>{String(h).padStart(2, '0')}:00</span>
            </div>
          ))}
        </div>

        {/* Doctor columns */}
        {activeDoctors.map((d) => {
          const color = getDoctorColor(doctors.indexOf(d))
          const c = COLOR_STYLES[color]
          const colAppts = filtered.filter((a) => a.doctor_id === d.id)
          return (
            <div key={d.id} style={{ position: 'relative', borderLeft: '1px solid var(--color-border)', minHeight: HOUR_HEIGHT * GRID_HOURS.length }}>
              {GRID_HOURS.map((h) => <div key={h} style={{ height: HOUR_HEIGHT, borderTop: h === GRID_START_HOUR ? 'none' : '1px solid var(--color-border)' }} />)}
              <NowIndicator />
              {colAppts.map((a) => {
                const startMins = toMinutes(a.start_time)
                const endMins   = toMinutes(a.end_time)
                const topPx     = (startMins - GRID_START_HOUR * 60) / 60 * HOUR_HEIGHT + 8
                const heightPx  = Math.max((endMins - startMins) / 60 * HOUR_HEIGHT - 4, 22)
                return (
                  <button
                    key={a.id}
                    onClick={() => onSelect(a)}
                    style={{ position: 'absolute', left: 4, right: 4, top: topPx, height: heightPx, borderRadius: 7, background: c.bg, border: `1px solid ${c.stripe}30`, display: 'flex', overflow: 'hidden', cursor: 'pointer', boxShadow: selectedId === a.id ? `0 0 0 2px var(--color-accent)` : 'none' }}
                  >
                    <div style={{ width: 3, flexShrink: 0, background: c.stripe }} />
                    <div style={{ padding: '4px 7px', minWidth: 0 }}>
                      <div style={{ fontSize: 10, fontWeight: 600, color: 'var(--color-ink-2)' }}>{formatTime(a.start_time)}</div>
                      <div style={{ fontSize: 11, color: 'var(--color-ink)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{a.user_id?.slice(0, 6)}…</div>
                    </div>
                  </button>
                )
              })}
            </div>
          )
        })}
      </div>
    </div>
  )
}
