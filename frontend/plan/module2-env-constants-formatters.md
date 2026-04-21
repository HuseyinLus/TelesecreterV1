# Module 2 — Environment Variables, Constants & Formatters

## Goal
Establish the single source of truth for all configuration values and pure utility functions used across every component.

## Files to create
- `.env.local` (project root of `frontend/`)
- `.env.example`
- `src/utils/constants.js`
- `src/utils/formatters.js`

---

## .env.local
```
VITE_API_BASE_URL=http://localhost:8000
```

## .env.example
```
VITE_API_BASE_URL=
```

---

## src/utils/constants.js
```js
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const POLLING_INTERVAL_DOCTORS      = 30_000
export const POLLING_INTERVAL_APPOINTMENTS = 5_000
export const POLLING_INTERVAL_AVAILABILITY = 10_000

export const LOG_MAX_ENTRIES = 200

// Assigned by index position from GET /doctors/ response array.
// index 0 → teal, 1 → sage, 2 → amber, 3 → indigo, 4 → rose (cycles if > 5)
export const DOCTOR_COLORS = ['teal', 'sage', 'amber', 'indigo', 'rose']

export const getDoctorColor = (index) => DOCTOR_COLORS[index % DOCTOR_COLORS.length]
```

---

## src/utils/formatters.js
```js
// "2026-04-16T10:30:00" → "Thu · Apr 16, 2026"
export function formatDate(isoString) {
  const d = new Date(isoString)
  return d.toLocaleDateString('en-US', {
    weekday: 'short', month: 'short', day: 'numeric', year: 'numeric'
  }).replace(',', ' ·')
}

// "10:30:00" → "10:30"
export function formatTime(hhmmss) {
  return hhmmss?.slice(0, 5) ?? '—'
}

// "3fa85f64-5717-4562-b3fc-2c963f66afa6" → "3fa85f64…"
export function truncateUUID(uuid) {
  return uuid ? uuid.slice(0, 8) + '…' : '—'
}

// "2026-04-16" → true/false
export function isToday(dateString) {
  const today = new Date().toISOString().slice(0, 10)
  return dateString === today
}

// "10:30:00" → 630 (minutes since midnight)
export function toMinutes(hhmmss) {
  const [h, m] = (hhmmss ?? '00:00').split(':').map(Number)
  return h * 60 + m
}

// "10:30:00" + 45 → "11:15"
export function addMinutes(hhmmss, mins) {
  const total = toMinutes(hhmmss) + mins
  const h = Math.floor(total / 60).toString().padStart(2, '0')
  const m = (total % 60).toString().padStart(2, '0')
  return `${h}:${m}`
}
```

---

## Test
In `src/App.jsx` temporarily import and log:

```jsx
import { API_BASE_URL, DOCTOR_COLORS, getDoctorColor } from './utils/constants'
import { formatTime, truncateUUID, isToday, addMinutes } from './utils/formatters'

export default function App() {
  console.log('API_BASE_URL:', API_BASE_URL)
  console.log('Color for index 0:', getDoctorColor(0))   // → 'teal'
  console.log('Color for index 6:', getDoctorColor(6))   // → 'sage' (cycles)
  console.log('formatTime:', formatTime('10:30:00'))      // → '10:30'
  console.log('truncateUUID:', truncateUUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')) // → '3fa85f64…'
  console.log('isToday:', isToday(new Date().toISOString().slice(0, 10))) // → true
  console.log('addMinutes:', addMinutes('10:30:00', 45))  // → '11:15'
  return <div>Module 2 test — check console</div>
}
```

**Pass criteria (browser console):**
- `API_BASE_URL` = `http://localhost:8000` (not undefined)
- `Color for index 0` = `teal`
- `Color for index 6` = `sage`
- All formatter outputs match expected values above
