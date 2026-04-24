import { HOUR_HEIGHT, GRID_START_HOUR, GRID_HOURS, getDoctorColor } from '../../utils/constants'
import AppointmentBlock from './AppointmentBlock'
import NowIndicator from './NowIndicator'

const WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

function getWeekDates(baseDate) {
  const ref = baseDate ?? new Date()
  const mon = new Date(ref)
  mon.setDate(ref.getDate() - ((ref.getDay() + 6) % 7))
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(mon)
    d.setDate(mon.getDate() + i)
    return d
  })
}

export default function WeekCalendar({ appointments, doctors, filters, selectedId, onSelect, baseDate }) {
  const weekDates = getWeekDates(baseDate)
  const todayDate = new Date().toISOString().slice(0, 10)

  const doctorById = Object.fromEntries(doctors.map((d, i) => [d.id, { ...d, color: getDoctorColor(i) }]))

  const filtered = appointments.filter((a) => {
    if (filters.doctorId !== 'all' && a.doctor_id !== filters.doctorId) return false
    return true
  })

  return (
    <div style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 14, overflow: 'hidden', boxShadow: '0 1px 2px oklch(20% 0.04 240 / 0.05)' }}>
      {/* Header row */}
      <div style={{ display: 'grid', gridTemplateColumns: '64px repeat(7, 1fr)', borderBottom: '1px solid var(--color-border)', background: 'var(--color-surface-2)' }}>
        <div />
        {weekDates.map((d, i) => {
          const isToday = d.toISOString().slice(0, 10) === todayDate
          return (
            <div key={i} style={{ padding: '12px 10px', textAlign: 'center', borderLeft: '1px solid var(--color-border)' }}>
              <div style={{ fontSize: 10.5, textTransform: 'uppercase', letterSpacing: '0.08em', color: isToday ? 'var(--color-accent)' : 'var(--color-ink-3)', fontWeight: 500 }}>{WEEK_DAYS[i]}</div>
              <div style={isToday ? { display: 'inline-grid', placeItems: 'center', width: 30, height: 30, borderRadius: '50%', background: 'var(--color-accent)', color: 'white', fontSize: 15, fontWeight: 600, marginTop: 2 } : { fontFamily: 'var(--font-serif)', fontSize: 22, color: 'var(--color-ink)', marginTop: 2, lineHeight: 1 }}>
                {d.getDate()}
              </div>
            </div>
          )
        })}
      </div>

      {/* Body */}
      <div style={{ display: 'grid', gridTemplateColumns: '64px repeat(7, 1fr)', position: 'relative' }}>
        {/* Hour gutter */}
        <div>
          {GRID_HOURS.map((h) => (
            <div key={h} style={{ height: HOUR_HEIGHT, paddingRight: 8, textAlign: 'right', fontSize: 10.5, color: 'var(--color-ink-4)', position: 'relative', paddingTop: 0 }}>
              <span style={{ position: 'relative', top: -6, fontVariantNumeric: 'tabular-nums' }}>{String(h).padStart(2, '0')}:00</span>
            </div>
          ))}
        </div>

        {/* Day columns */}
        {weekDates.map((d, colIdx) => {
          const colDate = d.toISOString().slice(0, 10)
          const isToday = colDate === todayDate
          const colAppts = filtered.filter((a) => a.date === colDate)

          return (
            <div key={colIdx} style={{ position: 'relative', borderLeft: '1px solid var(--color-border)', minHeight: HOUR_HEIGHT * GRID_HOURS.length, background: isToday ? 'linear-gradient(180deg, oklch(56% 0.09 210 / 0.04), transparent 30%)' : 'transparent' }}>
              {GRID_HOURS.map((h) => (
                <div key={h} style={{ height: HOUR_HEIGHT, borderTop: h === GRID_START_HOUR ? 'none' : '1px solid var(--color-border)' }} />
              ))}
              {isToday && <NowIndicator />}
              {colAppts.map((a) => {
                const doc = doctorById[a.doctor_id]
                return (
                  <AppointmentBlock
                    key={a.id}
                    appt={a}
                    color={doc?.color ?? 'teal'}
                    doctorName={doc?.full_name}
                    onClick={onSelect}
                    isSelected={selectedId === a.id}
                  />
                )
              })}
            </div>
          )
        })}
      </div>
    </div>
  )
}
