# Module 14 — TodayAgenda + AIStatsCard (Calendar Right Rail)

## Goal
Add the right-rail sidebar to the Calendar page: today's timeline list and the AI activity stats card. These mirror the `TodayList` and `AIStatsStrip` components from `Dashboard.html`.

## Dependencies
- `src/hooks/useAppointments.js` (Module 10)
- `src/utils/formatters.js` — `formatTime`, `toMinutes`, `isToday`
- `src/utils/constants.js` — `getDoctorColor`

## Files to create
- `src/components/calendar/TodayAgenda.jsx`
- `src/components/calendar/AIStatsCard.jsx`

## Files to modify
- `src/pages/CalendarPage.jsx` — restructure layout to add 360px right rail

---

## src/components/calendar/TodayAgenda.jsx
```jsx
import { formatTime, toMinutes, isToday } from '../../utils/formatters'
import { getDoctorColor } from '../../utils/constants'

const RAIL_BG = { teal: 'var(--color-teal)', sage: 'var(--color-sage)', amber: 'var(--color-amber)', indigo: 'var(--color-indigo)', rose: 'var(--color-rose)' }

export default function TodayAgenda({ appointments, doctors, selectedId, onSelect }) {
  const doctorById = Object.fromEntries(doctors.map((d, i) => [d.id, { ...d, color: getDoctorColor(i) }]))
  const now = new Date()
  const nowMins = now.getHours() * 60 + now.getMinutes()

  const today = appointments
    .filter((a) => isToday(a.date))
    .sort((a, b) => a.start_time.localeCompare(b.start_time))

  const aiBookedCount = today.filter((a) => a.status !== 'cancelled').length

  return (
    <div style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 14, padding: 14, boxShadow: '0 1px 2px oklch(20% 0.04 240 / 0.05)' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
        <div>
          <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--color-ink)', letterSpacing: '-0.005em' }}>Today</div>
          <div style={{ fontSize: 11, color: 'var(--color-ink-3)', marginTop: 2 }}>
            {today.length} appointments · {aiBookedCount} active
          </div>
        </div>
        <button style={{ fontSize: 11, color: 'var(--color-ink-3)', padding: '3px 8px', borderRadius: 6, fontWeight: 500 }}>View all</button>
      </div>

      {/* List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 1, margin: '0 -6px' }}>
        {today.length === 0 && (
          <div style={{ padding: '16px 8px', textAlign: 'center', color: 'var(--color-ink-4)', fontSize: 12 }}>No appointments today</div>
        )}
        {today.map((a) => {
          const doc = doctorById[a.doctor_id]
          const startMins = toMinutes(a.start_time)
          const endMins   = toMinutes(a.end_time)
          const isPast = endMins < nowMins
          const isNow  = startMins <= nowMins && endMins > nowMins

          return (
            <button
              key={a.id}
              onClick={() => onSelect(a)}
              style={{
                display: 'grid', gridTemplateColumns: '48px 3px 1fr', gap: 10,
                padding: '9px 8px', borderRadius: 8, textAlign: 'left', alignItems: 'start',
                opacity: isPast ? 0.5 : 1,
                background: isNow ? 'linear-gradient(90deg, oklch(66% 0.11 20 / 0.08), transparent 80%)' : selectedId === a.id ? 'var(--color-accent-soft)' : 'transparent',
                transition: 'background 0.12s',
                position: 'relative',
              }}
            >
              <div style={{ textAlign: 'right', paddingTop: 1 }}>
                <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-ink)', fontVariantNumeric: 'tabular-nums' }}>{formatTime(a.start_time)}</div>
                <div style={{ fontSize: 10, color: 'var(--color-ink-4)' }}>{Math.round((toMinutes(a.end_time) - toMinutes(a.start_time)))}m</div>
              </div>

              <div style={{ width: 3, borderRadius: 2, height: 28, marginTop: 2, background: doc ? RAIL_BG[doc.color] : 'var(--color-border)' }} />

              <div style={{ minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--color-ink)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {a.user_id?.slice(0, 8)}…
                  </span>
                  {a.status === 'pending' && <span style={{ background: 'var(--color-amber-soft)', color: 'var(--color-amber)', fontSize: 9, fontWeight: 600, padding: '1px 5px', borderRadius: 4 }}>Pending</span>}
                </div>
                <div style={{ fontSize: 11, color: 'var(--color-ink-3)', marginTop: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {doc?.name.replace('Dr. ', '') ?? '—'} · {doc?.specialty ?? ''}
                </div>
              </div>

              {isNow && (
                <div style={{ position: 'absolute', top: 12, right: 10, width: 6, height: 6, background: 'var(--color-rose)', borderRadius: '50%', boxShadow: '0 0 0 4px oklch(66% 0.11 20 / 0.2)', animation: 'pulse-rose 2s infinite' }} />
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}
```

---

## src/components/calendar/AIStatsCard.jsx
```jsx
import { useAppointments } from '../../hooks/useAppointments'

export default function AIStatsCard() {
  const { data: appointments = [] } = useAppointments()

  const total     = appointments.length
  const confirmed = appointments.filter((a) => a.status === 'confirmed').length
  const pending   = appointments.filter((a) => a.status === 'pending').length
  const pct       = total > 0 ? Math.round((confirmed / total) * 100) : 0

  return (
    <div style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 14, padding: 14, boxShadow: '0 1px 2px oklch(20% 0.04 240 / 0.05)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--color-ink)' }}>AI activity</div>
        <button style={{ fontSize: 11, color: 'var(--color-ink-3)', padding: '3px 8px', borderRadius: 6, fontWeight: 500 }}>Details</button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10 }}>
        {[
          { num: total,     label: 'Total booked',  delta: null },
          { num: confirmed, label: 'Confirmed',      delta: null },
          { num: `${pct}%`, label: 'Confirmed rate', delta: null },
        ].map(({ num, label }) => (
          <div key={label} style={{ padding: '10px 10px 8px', borderRadius: 9, background: 'var(--color-bg-subtle)', border: '1px solid var(--color-border)' }}>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: 24, color: 'var(--color-ink)', lineHeight: 1.1, fontVariantNumeric: 'tabular-nums' }}>{num}</div>
            <div style={{ fontSize: 10, color: 'var(--color-ink-3)', marginTop: 2, lineHeight: 1.2 }}>{label}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## CalendarPage.jsx — updated layout with right rail
```jsx
import { useState } from 'react'
import { useDoctors } from '../hooks/useDoctors'
import { useAppointments } from '../hooks/useAppointments'
import CalendarToolbar from '../components/calendar/CalendarToolbar'
import WeekCalendar from '../components/calendar/WeekCalendar'
import DayView from '../components/calendar/DayView'
import ListView from '../components/calendar/ListView'
import DoctorLegend from '../components/calendar/DoctorLegend'
import AppointmentDrawer from '../components/calendar/AppointmentDrawer'
import TodayAgenda from '../components/calendar/TodayAgenda'
import AIStatsCard from '../components/calendar/AIStatsCard'

function getWeekLabel() {
  const now = new Date()
  const mon = new Date(now)
  mon.setDate(now.getDate() - ((now.getDay() + 6) % 7))
  const sun = new Date(mon)
  sun.setDate(mon.getDate() + 6)
  const fmt = (d) => d.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })
  return `${fmt(mon)} – ${fmt(sun).split(' ')[1]}, ${sun.getFullYear()}`
}

export default function CalendarPage() {
  const [view, setView]         = useState('week')
  const [filters, setFilters]   = useState({ doctorId: 'all' })
  const [selected, setSelected] = useState(null)

  const { data: doctors = [] }      = useDoctors()
  const { data: appointments = [] } = useAppointments()

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 360px', height: '100%', overflow: 'hidden' }}>
      {/* Main calendar area */}
      <div style={{ overflow: 'auto', padding: '0 24px 24px' }}>
        <CalendarToolbar view={view} onView={setView} filters={filters} setFilters={setFilters} doctors={doctors} weekLabel={getWeekLabel()} />

        {view === 'week' && <WeekCalendar appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} />}
        {view === 'day'  && <DayView     appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} />}
        {view === 'list' && <ListView    appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} />}

        <DoctorLegend doctors={doctors} />
      </div>

      {/* Right rail */}
      <div style={{ overflow: 'auto', borderLeft: '1px solid var(--color-border)', display: 'flex', flexDirection: 'column', gap: 14, padding: '18px 16px' }}>
        <TodayAgenda appointments={appointments} doctors={doctors} selectedId={selected?.id} onSelect={setSelected} />
        <AIStatsCard />
      </div>

      <AppointmentDrawer appt={selected} doctors={doctors} onClose={() => setSelected(null)} />
    </div>
  )
}
```

---

## Test
1. Visit `/calendar`

**Pass criteria:**
- Right rail is visible (360px wide) with today's appointment list
- Each agenda item shows: time, duration, colored rail bar, truncated patient ID, doctor name
- Current appointment (if within time range) has a pulsing rose dot and gradient background
- Past appointments are dimmed (opacity 0.5)
- Clicking an agenda item selects it (highlighted) and opens the drawer
- AI Stats card shows real counts derived from the appointments array
- Layout: calendar takes remaining width, right rail is fixed 360px, no overflow
