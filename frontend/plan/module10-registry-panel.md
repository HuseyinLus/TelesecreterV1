# Module 10 — RegistryPanel + TanStack Query Hooks

## Goal
Build Zone 2 (Registry): tabbed panel with Doctors and Appointments tabs, wired to real API data via `useDoctors` and `useAppointments` hooks with polling. Tables show real backend data with loading skeletons and empty states.

## Dependencies
- `src/services/apiClient.js` (Module 4)
- `src/utils/constants.js` (Module 2)
- `@tanstack/react-query`
- `lucide-react`

## Files to create
- `src/hooks/useDoctors.js`
- `src/hooks/useAppointments.js`
- `src/hooks/useDoctorAvailability.js`
- `src/components/registry/RegistryPanel.jsx`
- `src/components/registry/DoctorsTable.jsx`
- `src/components/registry/AvailabilityPill.jsx`
- `src/components/registry/AppointmentsTable.jsx`
- `src/components/registry/AppointmentRow.jsx`
- `src/components/registry/StatusPill.jsx`
- `src/components/shared/EmptyState.jsx`

## Files to modify
- `src/pages/DashboardPage.jsx` — replace Zone 2 placeholder with `<RegistryPanel />`

---

## src/hooks/useDoctors.js
```js
import { useQuery } from '@tanstack/react-query'
import apiClient from '../services/apiClient'
import { POLLING_INTERVAL_DOCTORS } from '../utils/constants'

export function useDoctors() {
  return useQuery({
    queryKey: ['doctors'],
    queryFn: () => apiClient.get('/doctors/').then((r) => r.data),
    refetchInterval: POLLING_INTERVAL_DOCTORS,
  })
}
```

---

## src/hooks/useAppointments.js
```js
import { useQuery } from '@tanstack/react-query'
import { useRef, useEffect } from 'react'
import apiClient from '../services/apiClient'
import { POLLING_INTERVAL_APPOINTMENTS } from '../utils/constants'

export function useAppointments(onNewEntry) {
  const prevLengthRef = useRef(null)

  const query = useQuery({
    queryKey: ['appointments'],
    queryFn: () => apiClient.get('/appointments/').then((r) => r.data),
    refetchInterval: POLLING_INTERVAL_APPOINTMENTS,
  })

  useEffect(() => {
    if (!query.data) return
    const len = query.data.length
    if (prevLengthRef.current !== null && len > prevLengthRef.current) {
      onNewEntry?.()
    }
    prevLengthRef.current = len
  }, [query.data])

  return query
}
```

---

## src/hooks/useDoctorAvailability.js
```js
import { useQuery } from '@tanstack/react-query'
import apiClient from '../services/apiClient'
import { POLLING_INTERVAL_AVAILABILITY } from '../utils/constants'

export function useDoctorAvailability(doctorId, dateStr) {
  return useQuery({
    queryKey: ['availability', doctorId, dateStr],
    queryFn: () => apiClient.get(`/scheduales/${doctorId}/availability`, { params: { date_str: dateStr } }).then((r) => r.data),
    refetchInterval: POLLING_INTERVAL_AVAILABILITY,
    enabled: Boolean(doctorId && dateStr),
  })
}
```

---

## src/components/shared/EmptyState.jsx
```jsx
export default function EmptyState({ icon: Icon, title, subtitle }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10, padding: 48, color: 'var(--color-ink-4)' }}>
      {Icon && <Icon size={40} strokeWidth={1.2} />}
      <p style={{ margin: 0, fontSize: 13, fontWeight: 500, color: 'var(--color-ink-3)', textAlign: 'center' }}>{title}</p>
      {subtitle && <p style={{ margin: 0, fontSize: 12, color: 'var(--color-ink-4)', textAlign: 'center', lineHeight: 1.5 }}>{subtitle}</p>}
    </div>
  )
}
```

---

## src/components/registry/StatusPill.jsx
```jsx
const STYLES = {
  pending:   { bg: 'var(--color-amber-soft)',  color: 'var(--color-amber)',    label: 'Pending' },
  confirmed: { bg: 'var(--color-sage-soft)',   color: 'var(--color-sage-ink)', label: 'Confirmed' },
  cancelled: { bg: 'var(--color-bg-subtle)',   color: 'var(--color-ink-4)',    label: 'Cancelled' },
}

export default function StatusPill({ status }) {
  const s = STYLES[status] ?? STYLES.pending
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, padding: '2px 8px', borderRadius: 5, fontSize: 11, fontWeight: 500, background: s.bg, color: s.color }}>
      {s.label}
    </span>
  )
}
```

---

## src/components/registry/AvailabilityPill.jsx
```jsx
import { useDoctorAvailability } from '../../hooks/useDoctorAvailability'

export default function AvailabilityPill({ doctorId }) {
  const dateStr = new Date().toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' }).replace('/', '.')
  const { data, isLoading } = useDoctorAvailability(doctorId, dateStr)

  if (isLoading) return (
    <span style={{ display: 'inline-block', width: 72, height: 22, borderRadius: 5, background: 'var(--color-border)', animation: 'pulse-sage 1.5s infinite' }} />
  )

  const available = data?.available
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', padding: '2px 8px', borderRadius: 5, fontSize: 11, fontWeight: 500,
      background: available ? 'var(--color-sage-soft)' : 'oklch(66% 0.11 20 / 0.1)',
      color: available ? 'var(--color-sage-ink)' : 'var(--color-rose)',
      border: `1px solid ${available ? 'oklch(62% 0.07 160 / 0.28)' : 'oklch(66% 0.11 20 / 0.25)'}`,
    }}>
      {available ? 'Available' : 'Booked'}
    </span>
  )
}
```

---

## src/components/registry/DoctorsTable.jsx
```jsx
import { getDoctorColor } from '../../utils/constants'
import AvailabilityPill from './AvailabilityPill'

const COL_WIDTHS = '2fr 1.5fr 1.5fr 100px'

const HeadCell = ({ children }) => (
  <div style={{ fontSize: 10.5, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', fontWeight: 500 }}>{children}</div>
)

export default function DoctorsTable({ doctors }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <div style={{ display: 'grid', gridTemplateColumns: COL_WIDTHS, gap: 14, padding: '10px 18px', background: 'var(--color-surface-2)', borderBottom: '1px solid var(--color-border)' }}>
        <HeadCell>Name</HeadCell>
        <HeadCell>Specialty</HeadCell>
        <HeadCell>Department</HeadCell>
        <HeadCell>Today</HeadCell>
      </div>
      {/* Rows */}
      {doctors.map((doc, i) => {
        const color = getDoctorColor(i)
        const initials = doc.name.split(' ').filter(w => w).slice(0, 2).map(w => w[0]).join('')
        return (
          <div key={doc.id} style={{ display: 'grid', gridTemplateColumns: COL_WIDTHS, gap: 14, padding: '10px 18px', borderBottom: '1px solid var(--color-border)', alignItems: 'center', fontSize: 12.5 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ width: 28, height: 28, borderRadius: '50%', background: `var(--color-${color})`, color: 'white', display: 'grid', placeItems: 'center', fontSize: 10, fontWeight: 600, flexShrink: 0 }}>{initials}</div>
              <span style={{ color: 'var(--color-ink)', fontWeight: 600 }}>{doc.name}</span>
            </div>
            <span style={{ color: 'var(--color-ink-2)' }}>{doc.specialty}</span>
            <span style={{ color: 'var(--color-ink-3)' }}>{doc.department_name ?? '—'}</span>
            <AvailabilityPill doctorId={doc.id} />
          </div>
        )
      })}
    </div>
  )
}
```

---

## src/components/registry/AppointmentRow.jsx
```jsx
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
```

---

## src/components/registry/AppointmentsTable.jsx
```jsx
import { Calendar } from 'lucide-react'
import AppointmentRow from './AppointmentRow'
import EmptyState from '../shared/EmptyState'

const COL_WIDTHS = '1.2fr 1.5fr 90px 110px 90px 90px'

const HeadCell = ({ children }) => (
  <div style={{ fontSize: 10.5, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', fontWeight: 500 }}>{children}</div>
)

export default function AppointmentsTable({ appointments }) {
  if (!appointments.length) return <EmptyState icon={Calendar} title="No appointments booked yet" subtitle="They will appear here the moment the AI agent confirms a booking." />

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'grid', gridTemplateColumns: COL_WIDTHS, gap: 14, padding: '10px 18px', background: 'var(--color-surface-2)', borderBottom: '1px solid var(--color-border)' }}>
        <HeadCell>Patient ID</HeadCell>
        <HeadCell>Doctor ID</HeadCell>
        <HeadCell>Date</HeadCell>
        <HeadCell>Start</HeadCell>
        <HeadCell>End</HeadCell>
        <HeadCell>Status</HeadCell>
      </div>
      {appointments.map((appt) => <AppointmentRow key={appt.id} appt={appt} />)}
    </div>
  )
}
```

---

## src/components/registry/RegistryPanel.jsx
```jsx
import { useState } from 'react'
import { Database } from 'lucide-react'
import { useDoctors } from '../../hooks/useDoctors'
import { useAppointments } from '../../hooks/useAppointments'
import DoctorsTable from './DoctorsTable'
import AppointmentsTable from './AppointmentsTable'
import EmptyState from '../shared/EmptyState'

export default function RegistryPanel() {
  const [tab, setTab] = useState('doctors')
  const [newFlash, setNewFlash] = useState(false)

  const { data: doctors = [], isLoading: loadingDoctors } = useDoctors()
  const { data: appointments = [], isLoading: loadingAppts } = useAppointments(() => {
    setNewFlash(true)
    setTimeout(() => setNewFlash(false), 2000)
  })

  const Tab = ({ id, label, count }) => (
    <button
      onClick={() => setTab(id)}
      style={{
        padding: '6px 14px', borderRadius: 7, fontSize: 12.5, fontWeight: 500, border: 'none', cursor: 'pointer',
        background: tab === id ? 'var(--color-bg-subtle)' : 'transparent',
        color: tab === id ? 'var(--color-ink)' : 'var(--color-ink-3)',
        boxShadow: tab === id ? '0 1px 2px oklch(20% 0.04 240 / 0.05)' : 'none',
        outline: id === 'appointments' && newFlash ? '2px solid var(--color-accent)' : 'none',
        transition: 'all 0.15s',
      }}
    >
      {label}
      {count != null && (
        <span style={{ marginLeft: 6, background: 'var(--color-accent)', color: 'white', fontSize: 10, fontWeight: 600, padding: '1px 6px', borderRadius: 10 }}>{count}</span>
      )}
    </button>
  )

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 18px', borderBottom: '1px solid var(--color-border)', flexShrink: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Database size={15} color="var(--color-ink-3)" />
          <span style={{ fontSize: 12, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-3)' }}>Registry</span>
        </div>
        <div style={{ display: 'flex', background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 9, padding: 3, gap: 2 }}>
          <Tab id="doctors"      label="Doctors"      count={doctors.length} />
          <Tab id="appointments" label="Appointments" count={appointments.length} />
        </div>
      </div>

      {/* Table area */}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {tab === 'doctors' && (
          loadingDoctors
            ? <div style={{ padding: 24, color: 'var(--color-ink-3)', fontSize: 12 }}>Loading doctors…</div>
            : <DoctorsTable doctors={doctors} />
        )}
        {tab === 'appointments' && (
          loadingAppts
            ? <div style={{ padding: 24, color: 'var(--color-ink-3)', fontSize: 12 }}>Loading appointments…</div>
            : <AppointmentsTable appointments={appointments} />
        )}
      </div>
    </div>
  )
}
```

---

## DashboardPage.jsx — Zone 2 update
```jsx
import RegistryPanel from '../components/registry/RegistryPanel'
// replace Zone 2 placeholder div:
<div style={{ gridRow: 1, gridColumn: 1, overflow: 'hidden', borderRight: '1px solid var(--color-border)', borderBottom: '1px solid var(--color-border)' }}>
  <RegistryPanel />
</div>
```

---

## Test
**Backend must be running.**

1. Visit `/dashboard`, click "Doctors" tab
   - Real doctor names from the database appear in the table
   - Each row has a colored avatar initial
   - `AvailabilityPill` shows shimmer skeleton then resolves to Available/Booked
2. Click "Appointments" tab
   - Real appointments appear (or empty state if none exist)
   - Appointment rows show truncated UUIDs, date, start/end time, status pill
3. Open React Query Devtools — `["doctors"]` and `["appointments"]` queries are visible and green
4. Check browser network tab — `/doctors/` refetches automatically every 30s, `/appointments/` every 5s

**Pass criteria:** Real data from the FastAPI backend renders in both tables with no console errors.
