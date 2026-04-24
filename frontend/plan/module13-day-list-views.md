# Module 13 — DayView + ListView + AppointmentDrawer

## Goal
Complete the Calendar page with the Day and List views, and the slide-in appointment detail drawer. This is the final Calendar page module.

## Dependencies
- `src/hooks/useDoctors.js` (Module 10)
- `src/hooks/useAppointments.js` (Module 10)
- `src/utils/constants.js` — `HOUR_HEIGHT`, `GRID_HOURS`, `getDoctorColor`
- `src/utils/formatters.js` — `formatTime`, `toMinutes`, `isToday`
- `framer-motion`

## Files to create
- `src/components/calendar/DayView.jsx`
- `src/components/calendar/ListView.jsx`
- `src/components/calendar/AppointmentDrawer.jsx`

## Files to modify
- `src/pages/CalendarPage.jsx` — wire DayView, ListView, AppointmentDrawer

---

## src/components/calendar/DayView.jsx
```jsx
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
        {activeDoctors.map((d, i) => {
          const color = getDoctorColor(doctors.indexOf(d))
          const c = COLOR_STYLES[color]
          const initials = d.name.split(' ').filter(Boolean).slice(0, 2).map(w => w[0]).join('')
          return (
            <div key={d.id} style={{ padding: '12px 10px', borderLeft: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{ width: 30, height: 30, borderRadius: '50%', background: c.stripe, color: 'white', display: 'grid', placeItems: 'center', fontSize: 11, fontWeight: 600 }}>{initials}</div>
              <div>
                <div style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--color-ink)' }}>{d.name.replace('Dr. ', '')}</div>
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
```

---

## src/components/calendar/ListView.jsx
```jsx
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
        return (
          <button
            key={a.id}
            onClick={() => onSelect(a)}
            style={{ display: 'grid', gridTemplateColumns: COLS, gap: 14, padding: '10px 18px', alignItems: 'center', width: '100%', textAlign: 'left', fontSize: 12.5, borderBottom: '1px solid var(--color-border)', borderLeft: today ? '3px solid var(--color-accent)' : '3px solid transparent', background: selectedId === a.id ? 'var(--color-accent-soft)' : 'transparent', transition: 'background 0.1s' }}
          >
            <div style={{ color: 'var(--color-ink-3)', fontWeight: today ? 600 : 400 }}>{a.date}</div>
            <div style={{ color: 'var(--color-ink)', fontWeight: 600, fontVariantNumeric: 'tabular-nums' }}>{formatTime(a.start_time)}</div>
            <div style={{ color: 'var(--color-ink-2)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontFamily: 'var(--font-mono)', fontSize: 11 }} title={a.user_id}>{a.user_id?.slice(0, 8)}…</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--color-ink-2)' }}>
              {doc && <span style={{ width: 8, height: 8, borderRadius: '50%', flexShrink: 0, background: DOT_BG[doc.color] }} />}
              <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{doc?.name.replace('Dr. ', '') ?? '—'}</span>
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
```

---

## src/components/calendar/AppointmentDrawer.jsx
```jsx
import { motion, AnimatePresence } from 'framer-motion'
import { X } from 'lucide-react'
import { formatTime } from '../../utils/formatters'
import { getDoctorColor } from '../../utils/constants'
import StatusPill from '../registry/StatusPill'

const COLOR_BG = { teal: 'var(--color-teal)', sage: 'var(--color-sage)', amber: 'var(--color-amber)', indigo: 'var(--color-indigo)', rose: 'var(--color-rose)' }

export default function AppointmentDrawer({ appt, doctors, onClose }) {
  const doctorById = Object.fromEntries(doctors.map((d, i) => [d.id, { ...d, color: getDoctorColor(i) }]))
  const doc = appt ? doctorById[appt.doctor_id] : null

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
                  {doc?.name.split(' ').filter(Boolean).slice(0, 2).map(w => w[0]).join('') ?? '?'}
                </div>
                <div>
                  <div style={{ fontSize: 17, fontWeight: 600, color: 'var(--color-ink)', letterSpacing: '-0.005em' }}>{appt.user_id?.slice(0, 8)}…</div>
                  <div style={{ fontSize: 12, color: 'var(--color-ink-3)', marginTop: 1 }}>{doc?.name} · {doc?.specialty}</div>
                </div>
              </div>
              <button onClick={onClose} style={{ width: 28, height: 28, borderRadius: 7, display: 'grid', placeItems: 'center', color: 'var(--color-ink-3)' }}><X size={14} /></button>
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
                { label: 'Doctor',     value: doc?.name ?? '—' },
                { label: 'Department', value: doc?.department_name ?? '—' },
                { label: 'Patient ID', value: appt.user_id?.slice(0, 12) + '…' },
              ].map(({ label, value }) => (
                <div key={label}>
                  <div style={{ fontSize: 10, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', fontWeight: 500, marginBottom: 3 }}>{label}</div>
                  <div style={{ fontSize: 13, color: 'var(--color-ink)', fontWeight: 500 }}>{value}</div>
                </div>
              ))}
            </div>

            {/* Actions */}
            <div style={{ marginTop: 'auto', display: 'flex', gap: 8, paddingTop: 12, borderTop: '1px solid var(--color-border)' }}>
              <button style={{ flex: 1, padding: '9px 14px', borderRadius: 8, fontSize: 12.5, fontWeight: 500, background: 'var(--color-accent-soft)', color: 'var(--color-accent-ink)' }}>Reschedule</button>
              <button style={{ padding: '9px 14px', borderRadius: 8, fontSize: 12.5, fontWeight: 500, color: 'var(--color-danger)', border: '1px solid oklch(58% 0.18 25 / 0.28)' }}>Cancel</button>
              <button onClick={onClose} style={{ padding: '9px 14px', borderRadius: 8, fontSize: 12.5, fontWeight: 500, color: 'var(--color-ink-2)' }}>Close</button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

---

## CalendarPage.jsx — final version
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
    <div style={{ padding: '0 24px 24px', overflow: 'auto', height: '100%' }}>
      <CalendarToolbar
        view={view} onView={setView}
        filters={filters} setFilters={setFilters}
        doctors={doctors} weekLabel={getWeekLabel()}
      />

      {view === 'week' && <WeekCalendar appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} />}
      {view === 'day'  && <DayView     appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} />}
      {view === 'list' && <ListView    appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} />}

      <DoctorLegend doctors={doctors} />

      <AppointmentDrawer appt={selected} doctors={doctors} onClose={() => setSelected(null)} />
    </div>
  )
}
```

---

## Test
1. Visit `/calendar`

**Pass criteria:**
- Week view: clicking an appointment block opens the drawer sliding in from the right
- Drawer shows date, start/end time, doctor name, department, status pill
- Clicking backdrop or "Close" dismisses the drawer with slide-out animation
- Switching to "Day" view: shows per-doctor columns for today only, appointments in correct time slots
- Switching to "List" view: dense table of all appointments sorted by date then time
- Doctor filter applies across all three views
- No console errors in any view
