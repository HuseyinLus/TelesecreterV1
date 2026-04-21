# Module 12 — CalendarPage + CalendarToolbar + WeekCalendar

## Goal
Build the `/calendar` route: week-grid view with doctor-color-coded appointment blocks, now-indicator, toolbar with view switcher and doctor filter, and the doctor legend. This is a direct port of the `WeekCalendar` component from `Dashboard.html`.

## Dependencies
- `src/hooks/useDoctors.js` (Module 10)
- `src/hooks/useAppointments.js` (Module 10)
- `src/utils/constants.js` — `getDoctorColor`
- `src/utils/formatters.js` — `toMinutes`, `formatTime`

## Files to create
- `src/components/calendar/CalendarToolbar.jsx`
- `src/components/calendar/WeekCalendar.jsx`
- `src/components/calendar/AppointmentBlock.jsx`
- `src/components/calendar/NowIndicator.jsx`
- `src/components/calendar/DoctorLegend.jsx`

## Files to modify
- `src/pages/CalendarPage.jsx`

---

## Constants needed in this module
```js
// Add to src/utils/constants.js
export const HOUR_HEIGHT = 60   // px per hour in week/day grid
export const GRID_START_HOUR = 8
export const GRID_END_HOUR   = 19
export const GRID_HOURS = Array.from({ length: GRID_END_HOUR - GRID_START_HOUR }, (_, i) => GRID_START_HOUR + i)
```

---

## src/components/calendar/NowIndicator.jsx
```jsx
import { useEffect, useState } from 'react'
import { HOUR_HEIGHT, GRID_START_HOUR } from '../../utils/constants'

export default function NowIndicator() {
  const [top, setTop] = useState(null)

  useEffect(() => {
    const calc = () => {
      const now = new Date()
      const mins = now.getHours() * 60 + now.getMinutes()
      const offset = (mins - GRID_START_HOUR * 60) / 60 * HOUR_HEIGHT
      setTop(offset)
    }
    calc()
    const iv = setInterval(calc, 60_000)
    return () => clearInterval(iv)
  }, [])

  if (top === null || top < 0) return null

  return (
    <div style={{ position: 'absolute', left: -6, right: 0, top, zIndex: 3, pointerEvents: 'none' }}>
      <div style={{ position: 'absolute', left: 0, top: -4, width: 9, height: 9, borderRadius: '50%', background: 'var(--color-rose)', boxShadow: '0 0 0 3px oklch(66% 0.11 20 / 0.2)' }} />
      <div style={{ height: 1.5, background: 'var(--color-rose)', marginLeft: 10 }} />
    </div>
  )
}
```

---

## src/components/calendar/AppointmentBlock.jsx
```jsx
import { toMinutes, formatTime } from '../../utils/formatters'
import { HOUR_HEIGHT, GRID_START_HOUR } from '../../utils/constants'

const COLOR_STYLES = {
  teal:   { bg: 'var(--color-teal-soft)',   stripe: 'var(--color-teal)',   border: 'oklch(58% 0.09 200 / 0.18)' },
  sage:   { bg: 'var(--color-sage-soft)',   stripe: 'var(--color-sage)',   border: 'oklch(62% 0.07 160 / 0.20)' },
  amber:  { bg: 'var(--color-amber-soft)',  stripe: 'var(--color-amber)',  border: 'oklch(72% 0.11 70 / 0.24)'  },
  indigo: { bg: 'var(--color-indigo-soft)', stripe: 'var(--color-indigo)', border: 'oklch(56% 0.11 270 / 0.20)' },
  rose:   { bg: 'var(--color-rose-soft)',   stripe: 'var(--color-rose)',   border: 'oklch(66% 0.11 20 / 0.22)'  },
}

export default function AppointmentBlock({ appt, color, doctorName, onClick, isSelected }) {
  const startMins = toMinutes(appt.start_time)
  const endMins   = toMinutes(appt.end_time)
  const dur       = endMins - startMins
  const topPx     = (startMins - GRID_START_HOUR * 60) / 60 * HOUR_HEIGHT + 8
  const heightPx  = Math.max(dur / 60 * HOUR_HEIGHT - 3, 22)
  const c         = COLOR_STYLES[color] ?? COLOR_STYLES.teal
  const isShort   = dur <= 30

  return (
    <button
      onClick={() => onClick?.(appt)}
      style={{
        position: 'absolute', left: 4, right: 4, top: topPx, height: heightPx,
        borderRadius: 7, background: c.bg, border: `1px solid ${c.border}`,
        display: 'flex', overflow: 'hidden', cursor: 'pointer', textAlign: 'left',
        boxShadow: isSelected ? `0 0 0 2px var(--color-accent)` : 'none',
        borderStyle: appt.status === 'pending' ? 'dashed' : 'solid',
        transition: 'box-shadow 0.15s, transform 0.1s',
        minHeight: 26,
      }}
    >
      <div style={{ width: 3, flexShrink: 0, background: c.stripe }} />
      <div style={{ flex: 1, padding: '4px 7px', minWidth: 0 }}>
        <div style={{ fontSize: 10, fontWeight: 600, color: 'var(--color-ink-2)', fontVariantNumeric: 'tabular-nums' }}>{formatTime(appt.start_time)}</div>
        <div style={{ fontSize: 11.5, fontWeight: 600, color: 'var(--color-ink)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {appt.user_id?.slice(0, 6)}…
        </div>
        {!isShort && <div style={{ fontSize: 10, color: 'var(--color-ink-3)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{doctorName?.replace('Dr. ', '')}</div>}
        {appt.status === 'pending' && <div style={{ fontSize: 9.5, color: 'var(--color-amber)', fontWeight: 500 }}>Pending</div>}
      </div>
    </button>
  )
}
```

---

## src/components/calendar/DoctorLegend.jsx
```jsx
import { getDoctorColor } from '../../utils/constants'

const DOT_BG = { teal: 'var(--color-teal)', sage: 'var(--color-sage)', amber: 'var(--color-amber)', indigo: 'var(--color-indigo)', rose: 'var(--color-rose)' }

export default function DoctorLegend({ doctors }) {
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 14, padding: '14px 2px', marginTop: 8, borderTop: '1px solid var(--color-border)', fontSize: 11.5 }}>
      {doctors.map((d, i) => (
        <div key={d.id} style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--color-ink-3)' }}>
          <span style={{ width: 9, height: 9, borderRadius: '50%', flexShrink: 0, background: DOT_BG[getDoctorColor(i)] }} />
          <span style={{ fontWeight: 500, color: 'var(--color-ink-2)' }}>{d.name.replace('Dr. ', '')}</span>
          <span style={{ color: 'var(--color-ink-4)' }}>{d.specialty}</span>
        </div>
      ))}
    </div>
  )
}
```

---

## src/components/calendar/WeekCalendar.jsx
```jsx
import { HOUR_HEIGHT, GRID_START_HOUR, GRID_HOURS, getDoctorColor } from '../../utils/constants'
import AppointmentBlock from './AppointmentBlock'
import NowIndicator from './NowIndicator'

const WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

function getWeekDates() {
  const now = new Date()
  const mon = new Date(now)
  mon.setDate(now.getDate() - ((now.getDay() + 6) % 7))
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(mon)
    d.setDate(mon.getDate() + i)
    return d
  })
}

export default function WeekCalendar({ appointments, doctors, filters, selectedId, onSelect }) {
  const weekDates = getWeekDates()
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
              {/* Hour lines */}
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
                    doctorName={doc?.name}
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
```

---

## src/components/calendar/CalendarToolbar.jsx
```jsx
import { ChevronLeft, ChevronRight } from 'lucide-react'

export default function CalendarToolbar({ view, onView, filters, setFilters, doctors, weekLabel }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', alignItems: 'center', padding: '14px 0', gap: 12 }}>
      {/* Left: week nav */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 2, background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 9, padding: 2 }}>
          <button style={{ width: 28, height: 28, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', borderRadius: 7 }}><ChevronLeft size={14} /></button>
          <button style={{ padding: '5px 12px', fontSize: 12, fontWeight: 500, color: 'var(--color-ink-2)', borderRadius: 7 }}>Today</button>
          <button style={{ width: 28, height: 28, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', borderRadius: 7 }}><ChevronRight size={14} /></button>
        </div>
        <span style={{ fontFamily: 'var(--font-serif)', fontSize: 20, color: 'var(--color-ink)', letterSpacing: '-0.005em', whiteSpace: 'nowrap' }}>{weekLabel}</span>
      </div>

      {/* Center: doctor filter */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <select
          value={filters.doctorId}
          onChange={(e) => setFilters({ ...filters, doctorId: e.target.value })}
          style={{ border: '1px solid var(--color-border)', borderRadius: 9, padding: '6px 10px', fontSize: 12, color: 'var(--color-ink-2)', background: 'var(--color-surface)', fontFamily: 'var(--font-sans)' }}
        >
          <option value="all">All doctors ({doctors.length})</option>
          {doctors.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
      </div>

      {/* Right: view switcher */}
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <div style={{ display: 'flex', background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 9, padding: 3 }}>
          {['week', 'day', 'list'].map((v) => (
            <button key={v} onClick={() => onView(v)} style={{ padding: '5px 12px', fontSize: 12, fontWeight: 500, borderRadius: 6, background: view === v ? 'var(--color-bg-subtle)' : 'transparent', color: view === v ? 'var(--color-ink)' : 'var(--color-ink-3)', boxShadow: view === v ? '0 1px 2px oklch(20% 0.04 240 / 0.05)' : 'none', transition: 'all 0.15s' }}>
              {v[0].toUpperCase() + v.slice(1)}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
```

---

## src/pages/CalendarPage.jsx
```jsx
import { useState } from 'react'
import { useDoctors } from '../hooks/useDoctors'
import { useAppointments } from '../hooks/useAppointments'
import CalendarToolbar from '../components/calendar/CalendarToolbar'
import WeekCalendar from '../components/calendar/WeekCalendar'
import DoctorLegend from '../components/calendar/DoctorLegend'

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
  const [view, setView]       = useState('week')
  const [filters, setFilters] = useState({ doctorId: 'all' })
  const [selected, setSelected] = useState(null)

  const { data: doctors = [] }      = useDoctors()
  const { data: appointments = [] } = useAppointments()

  return (
    <div style={{ padding: '0 24px 24px', overflow: 'auto', height: '100%' }}>
      <CalendarToolbar
        view={view} onView={setView}
        filters={filters} setFilters={setFilters}
        doctors={doctors}
        weekLabel={getWeekLabel()}
      />

      {view === 'week' && (
        <WeekCalendar
          appointments={appointments}
          doctors={doctors}
          filters={filters}
          selectedId={selected?.id}
          onSelect={setSelected}
        />
      )}
      {view !== 'week' && (
        <div style={{ padding: 32, textAlign: 'center', color: 'var(--color-ink-3)', fontSize: 13 }}>
          {view === 'day' ? 'Day view — Module 13' : 'List view — Module 13'}
        </div>
      )}

      <DoctorLegend doctors={doctors} />
    </div>
  )
}
```

---

## Test
1. Visit `http://localhost:5173/calendar`

**Pass criteria:**
- Week grid renders with 7 day columns and hour rows from 08:00–19:00
- Real appointments from the database appear as colored blocks in the correct time slots
- Today's column has a subtle blue gradient and a red now-indicator line
- Today's date has a filled blue circle
- Doctor filter dropdown shows real doctor names; selecting one filters visible appointments
- Week/Day/List switcher works; Day and List show placeholder text (built in Module 13)
- Doctor legend shows at the bottom with correct colors matching appointment blocks
- No console errors
