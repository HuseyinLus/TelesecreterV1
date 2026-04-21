# Integration Blueprint: Static Design → Dynamic React Application

---

## Critical Observation Before Mapping

The `Dashboard.html` is a **Calendar page** — it shows a week/day/list appointment calendar. The `frontend_plan.md` describes a **Live Monitoring page** (the Pulse/Registry/LogTrace dashboard). These are **two separate pages** within the same application, both sharing the `Sidebar` and shell. The Integration Blueprint must account for both simultaneously.

The Sidebar nav items (`dashboard`, `calendar`, `doctors`, `patients`, `slots`, `calls`) define the page routing. The plan's three-zone layout (`PulsePanel` / `RegistryPanel` / `LogTracePanel`) is the **Dashboard** page. The `WeekCalendar`, `DayView`, and `ListView` from the HTML are the **Calendar** page.

---

## 1. Component-Element Mapping Table

### 1.1 Shell — Shared Across All Pages

| HTML Element / Class | CSS Class | React Component (Plan) | Notes |
|---|---|---|---|
| `<aside class="sidebar">` | `.sidebar` | `Sidebar.jsx` | Full match. `.sb-ai-dot` becomes live data |
| `.sb-brand` | `.sb-brand` | `Sidebar.jsx` internal | Logo + clinic name — static, no data |
| `.sb-ai-card` (sidebar) | `.sb-ai-card` | `Sidebar.jsx` internal | `<b>142</b>` calls and `<b>38</b>` booked → driven by `useAppointments` count |
| `.sb-ai-dot` (animated dot) | `.sb-ai-dot` with `@keyframes pulse` | `StatusDot.jsx` | Pulse animation tied to `callStore.isCallActive` |
| `.sb-badge` on "Call log" | `.sb-badge` | `Sidebar.jsx` | Count = `logStore.logs.filter(l => l.statusCode >= 400).length` |
| `<header class="topbar">` | `.topbar` | `Header.jsx` | `.tb-eyebrow` = live date; `.tb-title` greeting = operator name |
| `.tb-search input` | `.tb-search` | Not in plan (add to `Header.jsx`) | Triggers `GET /doctors/search?q=` + `GET /appointments/search` |
| `.tb-primary` "New appointment" | `.tb-primary` | Not in plan (add to `Header.jsx`) | Opens `AppointmentDrawer` for creation |

### 1.2 Dashboard Page — The Three-Zone Layout

The plan's three-zone layout must be built as a new page component (`DashboardPage.jsx`). The HTML has its closest parallel in the **Right Rail cards** — specifically `AICallMonitor` and `TodayList` — which are the design source for Zone 1 and Zone 2.

| HTML Element / Card | CSS Class | React Component (Plan) | Notes |
|---|---|---|---|
| `.rr-card.rr-call-card` (AICallMonitor) | `.rr-call-card` | `PulsePanel.jsx` → root container | This card is the design DNA for the entire Zone 1 |
| `.rr-call-live` + `.rr-pulse` dot | `.rr-pulse` with `@keyframes pulse` | `CallStatusBadge.jsx` | The "LIVE" indicator becomes ACTIVE/IDLE toggle |
| `.rr-call-caller` row (phone + state) | `.rr-call-caller` | `AuthBadge.jsx` | Caller identity + auth state. `.rr-call-state` = "Verifying identity…" |
| `.rr-waveform` + `.rr-wave-bar` | `.rr-wave-bar` with `@keyframes wave` | `CallStatusBadge.jsx` internal | Waveform bars = visual confirmation of active call |
| `.rr-transcript` + `.rr-t-line` rows | `.rr-transcript` | `ExtractedVarsCard.jsx` | Each `rr-t-line` maps to an extracted variable row (Doctor ID / Date / Time) |
| `.rr-typing` animation (3 dots) | `@keyframes typing` | `ExtractedVarsCard.jsx` | Shown while `callStore.extractedDoctorId` is still `null` |
| `.rr-call-timer` | `.rr-call-timer` | `PulsePanel.jsx` internal | Call duration timer, local `useEffect` interval |
| `.rr-call-actions` (Listen in / Take over) | `.rr-call-actions` | `PulsePanel.jsx` (future buttons) | Phase 2 — WebSocket takeover controls |
| **None in HTML** | — | `DoctorInFocusCard.jsx` | New card below `CallStatusBadge` — no HTML equivalent yet |
| `.rr-card` (TodayList) | `.rr-card` | `RegistryPanel.jsx` → root container | Zone 2 design source |
| `.lv` (ListView table) | `.lv`, `.lv-head`, `.lv-row` | `AppointmentsTable.jsx` | Column headers map exactly: Day→Date, Time→Start/End, Patient→user_id, Doctor→doctor name, Status→StatusPill |
| `.lv-day-label` + `.lv-time` | `.lv-time`, `.lv-day` | `AppointmentRow.jsx` cells | `date` + `start_time` / `end_time` from API |
| `.rr-ai-chip` "AI" badge | `.rr-ai-chip` | `AppointmentRow.jsx` | Shown when appointment originates from AI |
| `.dr-chip.dr-chip-ok/.dr-chip-pending` | `.dr-chip-ok`, `.dr-chip-pending` | `StatusPill.jsx` (maps to `AvailabilityPill.jsx` pattern) | Status column in Appointments tab |
| **None in HTML** | — | `DoctorsTable.jsx` | Doctors tab — HTML has no equivalent table for doctors in isolation |
| **None in HTML** | — | `AvailabilityPill.jsx` | Pill for doctor availability — closest visual is `.dr-chip-ok` in the Drawer |
| `.rr-card.rr-stats` (AIStatsStrip) | `.rr-stats-grid`, `.rr-stat` | Not in plan (optional Zone 2 header card) | Three stat boxes (calls/booked/resolved%) — derive from `useAppointments` |
| `.rr-sparkline svg` | `.rr-sparkline` | Not in plan — omit Phase 1 | Decorative; Phase 2 addition |
| **None in HTML** | — | `LogTracePanel.jsx` | Zone 3 has zero equivalent in HTML. Build fresh from plan spec |
| **None in HTML** | — | `LogEntry.jsx` | No log UI in HTML |
| **None in HTML** | — | `JsonViewer.jsx` | No JSON viewer in HTML |

### 1.3 Calendar Page — Existing HTML Components

These form the **Calendar** page (`CalendarPage.jsx`) — fully implemented in the HTML prototype:

| HTML Component | CSS Class | New React Component Needed | Notes |
|---|---|---|---|
| `CalendarToolbar` | `.ct`, `.ct-seg`, `.ct-filter` | `CalendarToolbar.jsx` | Port directly — view mode switch + doctor filter + week nav |
| `WeekCalendar` | `.wk-wrap`, `.wk-body`, `.wk-col` | `WeekCalendar.jsx` | Port directly — appointment blocks positioned absolutely by time |
| `AppointmentBlock` | `.ev`, `.ev-${color}`, `.ev-stripe` | `AppointmentBlock.jsx` | Dynamic color from doctor's assigned color slot |
| `NowIndicator` | `.now-line`, `.now-dot`, `.now-bar` | `NowIndicator.jsx` | Driven by `new Date()` interval, not Zustand |
| `DayView` | `.dv`, `.dv-col`, `.dv-col-head` | `DayView.jsx` | Per-doctor column view |
| `ListView` | `.lv`, `.lv-row` | `ListView.jsx` (or reuse `AppointmentsTable`) | Shares visual design with `AppointmentsTable` — consider extracting a shared `AppointmentRow` |
| `DoctorLegend` | `.legend`, `.legend-item` | `DoctorLegend.jsx` | Driven by `useDoctors` color assignments |
| `AppointmentDrawer` | `.drawer-wrap`, `.drawer` | `AppointmentDrawer.jsx` | Slide-in detail panel — triggered by selecting any appointment block |
| `TodayList` (right rail) | `.rr-card`, `.rr-item` | `TodayAgenda.jsx` | Right-rail sidebar of Calendar page showing today's timeline |
| `AICallMonitor` (right rail) | `.rr-call-card` | Reuse `PulsePanel.jsx` in mini mode | Same component, embedded in Calendar page's right rail |
| `AIStatsStrip` | `.rr-stats-grid` | `AIStatsCard.jsx` | Calendar page right rail stat card |

---

## 2. State & CSS Animation Bridge

### 2.1 Master Animation → State Map

| CSS Animation | Defined On | Trigger Condition | Zustand/State Source |
|---|---|---|---|
| `@keyframes pulse` | `.sb-ai-dot`, `.rr-pulse` (inner dot) | Apply when `callStore.isCallActive === true`; remove otherwise | `callStore.isCallActive` |
| `@keyframes wave` | `.rr-wave-bar` (waveform bars) | Render the entire `.rr-waveform` block only when `callStore.isCallActive === true` | `callStore.isCallActive` |
| `@keyframes typing` | `.rr-typing span` (3 bouncing dots) | Show when `callStore.isCallActive === true && callStore.extractedDoctorId === null` | `callStore.isCallActive` + `callStore.extractedDoctorId` |
| `@keyframes pulse-rose` | `.rr-now-pulse` | Purely time-derived: show on whichever appointment is currently in progress per wall clock | Local `Date.now()` interval, no Zustand |
| `@keyframes fadein` | `.drawer-wrap` (modal backdrop) | Apply when `selectedAppt !== null` (local UI state in `CalendarPage`) | Local `useState` |
| `@keyframes slidein` | `.drawer` (drawer panel), `.tweaks` panel | Same as `fadein` | Local `useState` |
| `transition: background .25s` | `body` element | Apply `.dark` class to `<html>` when dark mode toggle is active | Local `useState` in `DashboardShell` |
| `.ev-pending { border-style: dashed }` | `.ev` appointment blocks | Apply when appointment `status === "pending"` from API | Derived from `useAppointments` data |
| `.rr-call-card` gradient background | `.rr-card.rr-call-card` | Apply this class to `PulsePanel`'s root `div` when `callStore.isCallActive === true` | `callStore.isCallActive` |
| `.sb-active` nav highlight | `.sb-item` | Apply when current page route matches nav item id | React Router `useLocation` or local `useState` |
| `.lv-today { border-left: 3px solid var(--accent) }` | `.lv-row` | Apply when `appointment.date === today's date` | Derived: `formatters.isToday(appointment.date)` |
| `.rr-now { background: gradient }` | `.rr-item` in TodayList | Apply when appointment spans the current minute | Derived: `start_time <= now < end_time` |
| `.rr-past { opacity: 0.5 }` | `.rr-item` in TodayList | Apply when appointment `end_time < now` | Derived: `end_time < now` |

### 2.2 Color Token Bridge

The `styles.css` uses `oklch()` custom properties. Tailwind must be configured to match them:

| CSS Variable | Semantic Role | Tailwind Token | Activated By |
|---|---|---|---|
| `--sage` / `--sage-soft` | AI active / AI booked | `text-emerald-*` family | `callStore.isCallActive`, `aiBooked` prop |
| `--accent` / `--accent-soft` | Interactive / selected | `text-indigo-*` / `bg-indigo-*` | `selectedAppt`, active nav |
| `--amber` / `--amber-soft` | Warning / pending | `text-amber-*` | `appointment.status === "pending"` |
| `--rose` / `--rose-soft` | Error / now indicator | `text-red-*` | Error query states, now-line |
| `--ink-4` | Disabled / loading | `text-slate-500` | Skeleton shimmer states |

### 2.3 Doctor Color Slot System

The HTML assigns each doctor a color slot (`teal`, `sage`, `amber`, `indigo`, `rose`) deterministically. This cannot come from the API. **Strategy**: maintain a `DOCTOR_COLOR_MAP` in `constants.js` that assigns colors by array index position from the `GET /doctors/` response. Index 0 = teal, 1 = sage, etc. This ensures the CSS classes `.ev-teal`, `.av-teal`, `.legend-teal`, `.rr-rail-teal` all stay consistent without backend changes.

---

## 3. Data Flow & Endpoint Mapping

### 3.1 `GET /doctors/` → UI Elements

**Hook**: `useDoctors` | **Poll**: 30,000ms | **Query Key**: `["doctors"]`

| API Field | Populates HTML Element | React Component |
|---|---|---|
| `doctors[].name` | `.dv-col-name`, `.ev-doctor` text, `.legend-name`, `CalendarToolbar` filter `<option>` labels | `DayView`, `AppointmentBlock`, `DoctorLegend`, `CalendarToolbar` |
| `doctors[].specialty` | `.dv-col-spec`, `.legend-spec`, `AppointmentDrawer` `.dr-sub` | `DayView`, `DoctorLegend`, `AppointmentDrawer` |
| `doctors[].id` | Foreign key used to resolve all `appointment.doctor_id` → doctor name lookups | `DOCTOR_BY_ID` lookup map (built from query cache in `App.jsx`) |
| `doctors[].name` (first letter pair) | `.sb-avatar`, `.dv-avatar`, `.dr-doctor-avatar` | Avatar initials: `name.split(' ').map(n=>n[0]).join('')` |
| `doctors.length` | `.ct-filter <option>` "All doctors (N)" label | `CalendarToolbar` |
| Full array | `DoctorsTable` in Registry (Doctors tab) | `DoctorsTable.jsx` |

### 3.2 `GET /appointments/` → UI Elements

**Hook**: `useAppointments` | **Poll**: 5,000ms | **Query Key**: `["appointments"]`

| API Field | Populates HTML Element | React Component |
|---|---|---|
| `appointments[]` (full array) | `<thead>` + `<tbody>` of the Appointments tab in Registry | `AppointmentsTable.jsx` |
| `appointment.date` + `start_time` | `.ev` block `top` + `height` CSS position calculation | `AppointmentBlock.jsx` (via `toMinutes()`) |
| `appointment.date` + `start_time` | `.lv-time`, `.rr-time-start` | `ListView`, `TodayAgenda` |
| `appointment.end_time` | `.dr-value-sub` "{start} — {end}" in Drawer | `AppointmentDrawer.jsx` |
| `appointment.user_id` | `.lv-patient`, `.rr-patient` (truncated UUID with Tooltip) | `AppointmentRow.jsx`, `TodayAgenda` |
| `appointment.doctor_id` | Resolved via `DOCTOR_BY_ID` cache → doctor name + color | All appointment-displaying components |
| `appointment.status` | `.dr-chip-ok` vs `.dr-chip-pending` / `.ev-pending` class | `StatusPill.jsx`, `AppointmentBlock.jsx` |
| `appointments.length` | `.rr-card-sub` "N appointments" count | `TodayAgenda.jsx` |
| `appointments.filter(a => isToday(a.date)).length` | `.sb-badge` on Calendar nav item | `Sidebar.jsx` |
| `appointments.filter(a => a.status === 'pending').length` | Appointments tab badge pulse | `RegistryPanel.jsx` tab bar |

**New appointment detection** (inside `useAppointments`):
Compare returned `data.length` to `prevLengthRef.current`. On increase: `setNewRowFlash(true)` → triggers `.ct-seg-active` pulse on Appointments tab badge. Reset after 2 seconds.

### 3.3 `GET /scheduales/{doctor_id}/availability?date_str=MM.DD` → UI Elements

**Hook**: `useDoctorAvailability(doctorId, dateStr)` | **Poll**: 10,000ms | **Query Key**: `["availability", doctorId, dateStr]`

| API Field | Populates HTML Element | React Component |
|---|---|---|
| `available: true` | `.dr-chip-ok` style pill — "Available" text, emerald | `AvailabilityPill.jsx` in `DoctorsTable` |
| `available: false` | `.dr-chip-pending` style pill — "Booked" text, red | `AvailabilityPill.jsx` in `DoctorsTable` |
| Loading state | Shimmer skeleton — same pill dimensions as `.dr-chip`, `animate-pulse bg-slate-700` | `AvailabilityPill.jsx` skeleton branch |

This query is called **per row** in `DoctorsTable`, one per visible doctor. The `dateStr` defaults to today's date in `MM.DD` format.

### 3.4 `GET /appointments/slots/check` → UI Elements

**Hook**: `useSlotCheck(doctorId, dateStr, requestedTime)` | **Query Key**: `["slotCheck", doctorId, dateStr, time]`

| API Field | Populates HTML Element | React Component |
|---|---|---|
| `is_slot_available: true` | Enables the "Confirm" button in `AppointmentDrawer` | `AppointmentDrawer.jsx` |
| `is_slot_available: false` | Disables confirm, shows amber warning text | `AppointmentDrawer.jsx` |

This query is only fired when the `AppointmentDrawer` is open in **creation mode** and the user selects a time slot.

### 3.5 `POST /appointments/set` → UI Elements

**Mutation**: `useMutation` in `AppointmentDrawer` | **On success**: `invalidateQueries(["appointments"])`

| Phase | HTML Element Affected | Component |
|---|---|---|
| Optimistic (immediate) | New `.ev.ev-pending` block in `WeekCalendar` with spinner in `.ev-pending-tag` slot | `AppointmentBlock.jsx` with `isOptimistic` prop |
| Settled (server confirms) | Replace optimistic block with real data; `.ev-pending` → `.ev` | `useAppointments` refetch replaces the row |
| Error | Remove optimistic block; toast notification via local state | `AppointmentDrawer.jsx` |

---

## 4. Logic Trace Interception Plan

### 4.1 The Interception Chain

```
User action or polling timer fires
        ↓
TanStack Query calls the relevant query function
  (e.g. useDoctors → GET /doctors/)
        ↓
Query function calls apiClient.js
  (Axios instance configured with baseURL = VITE_API_BASE_URL)
        ↓
Axios REQUEST INTERCEPTOR fires (in logInterceptor.js):
  — Record: { id (nanoid), timestamp: Date.now(), method, path, requestBody }
  — Start a high-resolution timer (performance.now())
  — Annotate the Axios config with { _logId, _startTime }
        ↓
Axios sends the actual HTTP request to FastAPI
        ↓
FastAPI processes the request and returns a response
        ↓
Axios RESPONSE INTERCEPTOR fires (success path):
  — Read config._logId and config._startTime
  — Compute durationMs = performance.now() - config._startTime
  — Build complete LogEntry: { id, timestamp, method, path, statusCode,
      requestBody, responseBody: response.data, durationMs }
  — Call logStore.pushLog(entry)
  — Return response normally so TanStack Query receives it
        ↓
Axios RESPONSE INTERCEPTOR fires (error path, status >= 400):
  — Same steps as success but extract statusCode from error.response.status
  — responseBody = error.response.data
  — logStore.pushLog(entry) with error data
  — Re-throw the error so TanStack Query error state is set correctly
        ↓
logStore.pushLog(entry):
  — Prepend entry to logs array (newest first)
  — If logs.length > LOG_MAX_ENTRIES (200), drop the oldest entry
        ↓
LogTracePanel is subscribed to logStore via Zustand selector
  — React re-renders LogTracePanel with new logs array
  — LogFilterBar.activeFilter is applied: ALL shows all; WEBHOOK shows paths
    matching /scheduales/ or /appointments/set; ERROR shows statusCode >= 400
  — LogEntry components render the new entry
  — Auto-scroll to bottom (if user has not manually scrolled up)
```

### 4.2 Special Case: Auth Webhook Response

When the pre-greeting auth endpoint fires (Phase 2):

```
POST /auth/check fires (triggered by Retell webhook → future)
        ↓
Axios RESPONSE INTERCEPTOR captures the response
        ↓
logInterceptor.js checks: if path matches '/auth/check'
  — Extract is_authenticated and user from responseBody
  — Call callStore.setAuthenticated(is_authenticated, user?.name ?? null)
  — Log entry is still pushed to logStore normally (visible as a WEBHOOK entry)
        ↓
callStore state update → AuthBadge component re-renders
  — isAuthenticated: true  → "Recognized Patient" card springs into view
  — isAuthenticated: false → "Unknown Caller" card appears
```

### 4.3 Scroll Suspension Logic

The `LogWindow` component tracks a `isUserScrolledUp` boolean via a scroll event listener on the log container ref. When the user scrolls upward, `isUserScrolledUp = true` and the "↓ Jump to latest" button appears (overlaying the bottom of the log window). Auto-scroll via `containerRef.scrollTo({ bottom: 0, behavior: 'smooth' })` is only called when `isUserScrolledUp === false`. Clicking the jump button sets `isUserScrolledUp = false` and triggers the auto-scroll.

---

## 5. Refined Project Roadmap

### Phase 0 — Project Bootstrap

- [ ] **0.1** Scaffold with Vite: `npm create vite@latest telesecreter-frontend -- --template react`
- [ ] **0.2** Install all production dependencies in one command: `tailwindcss postcss autoprefixer @tanstack/react-query @tanstack/react-query-devtools zustand framer-motion axios lucide-react nanoid react-router-dom`
- [ ] **0.3** Install dev dependencies: `@tailwindcss/vite` (or PostCSS plugin), `eslint`, `prettier`

### Phase 1 — Tailwind Configuration

- [ ] **1.1** Initialize Tailwind: `npx tailwindcss init -p`
- [ ] **1.2** In `tailwind.config.js`: set `darkMode: 'class'` (matches the HTML's `document.documentElement.classList.toggle('dark', dark)` pattern)
- [ ] **1.3** Extend the Tailwind theme with the color variables from `styles.css` mapped to semantic token names:
  - `sage` → the oklch green (AI color) → `#34d399` range
  - `accent` → the teal-blue → `#6366f1` range
  - `ink` → near-black text → `#0f172a` range
  - Define these as CSS custom properties inside `index.css` using `@layer base`, **not** as hardcoded hex in Tailwind config, so they respond to the `.dark` class automatically
- [ ] **1.4** Add `JetBrains Mono` or system mono to `fontFamily.mono` in Tailwind config (for log entries)
- [ ] **1.5** Register custom `@keyframes` for `wave` and `typing` animations in `tailwind.config.js` `extend.keyframes` + `extend.animation` so they are available as `animate-wave` and `animate-typing` utilities

### Phase 2 — Environment Variables

- [ ] **2.1** Create `.env.local` at project root with `VITE_API_BASE_URL=http://localhost:8000`
- [ ] **2.2** Create `.env.example` with the same key but empty value (commit this, not `.env.local`)
- [ ] **2.3** Verify Vite exposes it: `import.meta.env.VITE_API_BASE_URL` must not be undefined

### Phase 3 — Constants & Utilities

- [ ] **3.1** Create `src/utils/constants.js` and define:
  - `POLLING_INTERVAL_DOCTORS = 30000`
  - `POLLING_INTERVAL_APPOINTMENTS = 5000`
  - `POLLING_INTERVAL_AVAILABILITY = 10000`
  - `LOG_MAX_ENTRIES = 200`
  - `API_BASE_URL = import.meta.env.VITE_API_BASE_URL`
  - `DOCTOR_COLORS = ['teal', 'sage', 'amber', 'indigo', 'rose']` (color slot array)
- [ ] **3.2** Create `src/utils/formatters.js` and define:
  - `formatDate(isoString)` → `"Thu · Apr 16, 2026"`
  - `formatTime(hhmmss)` → `"HH:MM"` (strips seconds)
  - `truncateUUID(uuid)` → first 8 chars + `…`
  - `isToday(dateString)` → boolean
  - `toMinutes(hhmmss)` → integer minutes since midnight
  - `addMinutes(hhmmss, mins)` → `"HH:MM"` (for end_time display)

### Phase 4 — Axios & Interceptor Setup

- [ ] **4.1** Create `src/services/apiClient.js`: Axios instance with `baseURL = API_BASE_URL` and `timeout: 10000`
- [ ] **4.2** Create `src/store/logStore.js`: Zustand store with `logs`, `activeFilter`, `pushLog()`, `clearLogs()`, `setFilter()` actions (implement the max-cap logic in `pushLog`)
- [ ] **4.3** Create `src/services/logInterceptor.js` and attach both request and response/error interceptors to the `apiClient` Axios instance. This file must `import { useLogStore } from '../store/logStore'` and call `useLogStore.getState().pushLog(entry)` (note: use `.getState()` since this is called outside a React component)

### Phase 5 — Zustand Stores

- [ ] **5.1** Create `src/store/callStore.js` with full state shape and all four actions from plan Section 9.1: `startCall`, `endCall`, `setAuthenticated`, `setExtractedVar`
- [ ] **5.2** Verify `logStore.js` is complete from Phase 4.2 with all three actions

### Phase 6 — TanStack Query Provider

- [ ] **6.1** In `src/main.jsx`: wrap `<App />` with `<QueryClientProvider client={queryClient}>` where `queryClient` is created with:
  - `defaultOptions.queries.staleTime = 10000` (10 seconds — prevents refetching on component mount if data is fresh)
  - `defaultOptions.queries.refetchOnWindowFocus = false` (prevents bursts of requests when operator alt-tabs)
  - `defaultOptions.queries.retry = 2` (retry failed requests twice before showing error state)
- [ ] **6.2** Add `<ReactQueryDevtools initialIsOpen={false} />` inside the provider (dev only, removed in production build via Vite's `import.meta.env.DEV` guard)

### Phase 7 — Routing

- [ ] **7.1** Install `react-router-dom` (already in Phase 0.2)
- [ ] **7.2** Define routes in `src/App.jsx`:
  - `/` or `/dashboard` → `DashboardPage.jsx` (Pulse/Registry/LogTrace)
  - `/calendar` → `CalendarPage.jsx` (WeekCalendar/DayView/ListView)
  - Additional routes for `doctors`, `patients`, `slots`, `calls` can be placeholder pages initially
- [ ] **7.3** `DashboardShell.jsx` renders `<Sidebar>` + `<Outlet />` so all pages share the sidebar

### Phase 8 — Smoke Test Gate

Before the first UI component is written, verify this checklist manually:

- [ ] **8.1** `uvicorn Telesecreter_API.main:app --reload` starts and `GET http://localhost:8000/doctors/` returns a JSON array
- [ ] **8.2** The Vite dev server starts on `npm run dev` with no console errors
- [ ] **8.3** A bare `useQuery({ queryKey: ['doctors'], queryFn: () => apiClient.get('/doctors/').then(r => r.data) })` call in a test component resolves successfully and `logStore.logs` contains one entry after the request
- [ ] **8.4** `callStore.startCall()` followed by `callStore.setAuthenticated(true, 'Ahmet Yılmaz')` correctly updates the store and `callStore.getState().callerName === 'Ahmet Yılmaz'`

**All eight phases must be green before the first JSX component file is created.**

---

## Summary Diagram

```
Browser
  │
  ├── CalendarPage.jsx
  │     ├── WeekCalendar  ← GET /appointments/ (5s poll)
  │     ├── DayView       ← GET /appointments/ (same cache)
  │     ├── ListView      ← GET /appointments/ (same cache)
  │     ├── TodayAgenda   ← GET /appointments/ filtered to today
  │     └── AppointmentDrawer ← POST /appointments/set (mutation)
  │
  └── DashboardPage.jsx
        ├── PulsePanel    ← callStore (Zustand, no polling)
        ├── RegistryPanel
        │     ├── DoctorsTable      ← GET /doctors/ (30s) + GET /scheduales/{id}/availability (10s)
        │     └── AppointmentsTable ← GET /appointments/ (5s)
        └── LogTracePanel ← logStore (Zustand, populated by Axios interceptor)

Every API call → apiClient.js → logInterceptor.js → logStore.pushLog()
                                                          ↓
                                                   LogTracePanel renders
```
