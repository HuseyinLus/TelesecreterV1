# Real-time AI Appointment Dashboard — Frontend Architecture Plan

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack Strategy](#2-tech-stack-strategy)
3. [Folder Structure](#3-folder-structure)
4. [Page Layout & Component Hierarchy](#4-page-layout--component-hierarchy)
5. [Real-time Synchronization Plan](#5-real-time-synchronization-plan)
6. [UI/UX Design System](#6-uiux-design-system)
7. [API Contracts](#7-api-contracts)
8. [Authentication Demo Flow](#8-authentication-demo-flow)
9. [State Management Blueprint](#9-state-management-blueprint)
10. [Empty States & Loading States](#10-empty-states--loading-states)

---

## 1. Project Overview

The dashboard is a **Live Monitoring & Admin Panel** that gives a real-time window into every interaction happening between the Retell AI Agent, the FastAPI backend, and the SQLite database. It is not a booking UI — it is an **observation and control plane** for operators running the AI medical secretary system.

**Core responsibilities:**
- Visualize active AI calls and the variables being extracted in real time
- Reflect new appointments the moment they are created by the AI agent
- Show doctor availability status dynamically
- Surface the raw HTTP request/response traffic between Retell and the backend
- Identify authenticated (recognized) users via a visual badge

---

## 2. Tech Stack Strategy

### 2.1 React + Vite

**Justification:**
- Vite's HMR (Hot Module Replacement) is significantly faster than Create React App for a dashboard that will be iterated on frequently
- React's component model maps cleanly to the three dashboard zones (Pulse / Registry / Logic Trace)
- The ecosystem around React (React Query, Zustand, Framer Motion) is the most mature for real-time dashboard patterns
- No SSR requirement — this is an operator-facing SPA, so Vite's pure client-side output is appropriate

### 2.2 Tailwind CSS

**Justification:**
- Utility-first approach allows rapid iteration on the dense, information-heavy layout a dashboard requires
- Dark mode via `dark:` variants is trivial to implement — medical/monitoring dashboards conventionally use dark themes
- No runtime CSS-in-JS overhead; critical for a panel that will have animated rows updating frequently
- JIT compiler means the final bundle only includes classes actually used

### 2.3 Lucide Icons

**Justification:**
- Consistent stroke-weight icon set that aligns with the clean, professional medical aesthetic
- Tree-shakeable — only imported icons are bundled
- Key icons used: `PhoneCall`, `PhoneOff`, `Activity`, `UserCheck`, `Calendar`, `Clock`, `AlertCircle`, `CheckCircle2`, `RefreshCw`, `Stethoscope`, `Database`, `Wifi`, `WifiOff`

### 2.5 Routing: React Router DOM

**Justification:**
- Two distinct pages exist in this app: the **Dashboard** (Pulse/Registry/LogTrace) and the **Calendar** (WeekCalendar/DayView/ListView), plus future stub pages for Doctors, Patients, Slots, and Call Log
- `DashboardShell.jsx` renders the shared `Sidebar` + `<Outlet />` so all pages inherit the shell without re-mounting it
- No SSR needed — `BrowserRouter` is sufficient

| Route | Page Component | Notes |
|---|---|---|
| `/` or `/dashboard` | `DashboardPage.jsx` | Default route — the three-zone monitoring view |
| `/calendar` | `CalendarPage.jsx` | Week/Day/List calendar view |
| `/doctors` | Stub page | Phase 2 |
| `/patients` | Stub page | Phase 2 |
| `/slots` | Stub page | Phase 2 |
| `/calls` | Stub page | Phase 2 |

---

### 2.4 State Management: Zustand + TanStack Query (React Query)

**Split responsibility:**

| Concern | Tool |
|---|---|
| Server state (doctors list, appointments, logs) | TanStack Query |
| UI state (active call data, sidebar open, badge visibility) | Zustand |
| Real-time polling lifecycle | TanStack Query `refetchInterval` |
| WebSocket connection state (future) | Zustand |

**Why not Redux:** Overkill for this scale. Zustand's API is minimal and the store can be read/written outside React components, which matters for the log interceptor service.

**Why TanStack Query over SWR:** `refetchInterval`, `staleTime`, `onSuccess` callbacks, and `invalidateQueries` give precise control over when and how polling triggers UI updates. The Appointments table specifically needs `invalidateQueries` fired when a mutation (new appointment) is detected.

---

## 3. Folder Structure

```
src/
├── assets/                        # Static assets (logo, favicon)
│
├── components/
│   ├── layout/
│   │   ├── DashboardShell.jsx     # Root layout: Sidebar + <Outlet /> (shared across all pages)
│   │   ├── Header.jsx             # Topbar: date eyebrow, greeting, search, New Appointment button
│   │   └── Sidebar.jsx            # Navigation: Dashboard / Calendar / Doctors / Patients / Slots / Calls
│   │
│   ├── pulse/                     # Zone 1: Live Call Status (right rail of DashboardPage)
│   │   ├── PulsePanel.jsx         # Container for the entire Pulse zone (w-[360px], right column)
│   │   ├── CallStatusBadge.jsx    # ACTIVE / IDLE indicator with pulse animation + waveform
│   │   ├── ExtractedVarsCard.jsx  # Shows Doctor ID, Date, Time as they are spoken
│   │   ├── DoctorInFocusCard.jsx  # Doctor name + specialty pulled from context
│   │   └── AuthBadge.jsx          # "Recognized User" badge (Ahmet Yılmaz scenario)
│   │
│   ├── registry/                  # Zone 2: Data Tables (left/center of DashboardPage)
│   │   ├── RegistryPanel.jsx      # Container with tab switcher (Doctors / Appointments)
│   │   ├── DoctorsTable.jsx       # Doctors list with real-time availability column
│   │   ├── AppointmentsTable.jsx  # Appointments list with animated new-row entry
│   │   ├── AvailabilityPill.jsx   # Green/Red pill showing available: true/false
│   │   ├── AppointmentRow.jsx     # Single row, accepts Framer Motion layout animation
│   │   └── StatusPill.jsx         # pending/confirmed/cancelled pill (amber/emerald/slate)
│   │
│   ├── logtrace/                  # Zone 3: Technical Logs (full-width bottom of DashboardPage)
│   │   ├── LogTracePanel.jsx      # Container with auto-scroll log window
│   │   ├── LogEntry.jsx           # Single log line: timestamp + method + path + status
│   │   ├── JsonViewer.jsx         # Collapsible JSON tree for request/response bodies
│   │   └── LogFilterBar.jsx       # Filter by: ALL / WEBHOOK / ERROR / SUCCESS
│   │
│   ├── calendar/                  # CalendarPage-specific components
│   │   ├── CalendarToolbar.jsx    # View switcher (Week/Day/List) + doctor filter + week nav
│   │   ├── WeekCalendar.jsx       # 7-column week grid, appointments positioned by time
│   │   ├── AppointmentBlock.jsx   # Single event block (.ev), color-coded by doctor slot
│   │   ├── NowIndicator.jsx       # Red now-line (.now-line / .now-dot / .now-bar)
│   │   ├── DayView.jsx            # Per-doctor column view for a single day
│   │   ├── ListView.jsx           # Dense table view of all appointments
│   │   ├── DoctorLegend.jsx       # Color legend strip below calendar
│   │   ├── AppointmentDrawer.jsx  # Slide-in detail/creation panel (.drawer-wrap)
│   │   ├── TodayAgenda.jsx        # Right-rail today timeline list (.rr-card / .rr-item)
│   │   └── AIStatsCard.jsx        # Right-rail AI activity stats (.rr-stats-grid)
│   │
│   └── shared/
│       ├── StatusDot.jsx          # Reusable colored dot (green/red/yellow/gray)
│       ├── SectionHeader.jsx      # Consistent zone title + subtitle
│       ├── Spinner.jsx            # Loading spinner for initial fetches
│       ├── EmptyState.jsx         # Generic empty state with icon + message
│       └── Tooltip.jsx            # Hover tooltip for truncated UUIDs
│
├── hooks/
│   ├── useDoctors.js              # TanStack Query: GET /doctors/ with polling
│   ├── useAppointments.js         # TanStack Query: GET /appointments/ with polling
│   ├── useDoctorAvailability.js   # TanStack Query: GET /scheduales/{id}/availability
│   ├── useSlotCheck.js            # TanStack Query: GET /appointments/slots/check
│   ├── useCallState.js            # Zustand selector: current call variables
│   └── useLogs.js                 # Zustand selector: log entries array
│
├── pages/
│   ├── DashboardPage.jsx          # Three-zone layout: Registry (1fr) | Pulse (360px) + LogTrace bottom
│   └── CalendarPage.jsx           # Calendar layout: CalendarToolbar + view + right rail
│
├── services/
│   ├── apiClient.js               # Axios instance with base URL + interceptors
│   ├── logInterceptor.js          # Axios interceptor that pushes to Zustand log store
│   └── retellWebhook.js           # (Future) WebSocket client for Retell call events
│
├── store/
│   ├── callStore.js               # Zustand: { isCallActive, doctorId, dateStr, timeStr, isAuthenticated, callerName }
│   └── logStore.js                # Zustand: { logs: [], pushLog(), clearLogs() }
│
├── utils/
│   ├── formatters.js              # formatDate(), formatTime(), truncateUUID(), isToday(), toMinutes(), addMinutes()
│   └── constants.js               # POLLING intervals, API_BASE_URL, LOG_MAX_ENTRIES, DOCTOR_COLORS
│
├── App.jsx                        # Route definitions: / → DashboardPage, /calendar → CalendarPage
├── main.jsx                       # Vite entry: QueryClientProvider + BrowserRouter + React root
└── index.css                      # Tailwind directives + CSS custom properties (@layer base)
```

---

## 4. Page Layout & Component Hierarchy

### 4.1 Overall Grid

The dashboard uses a **CSS Grid** layout with three zones arranged as follows:

```
┌─────────────────────────────────────────────────────────┐
│                      HEADER                              │
│  [Logo]  Real-time AI Dashboard    [●LIVE] [Clock]       │
├──────────────────────────────────┬──────────────────────┤
│                                  │                      │
│           THE REGISTRY           │    THE PULSE         │
│  [Doctors Tab]  [Appointments Tab│    (Zone 1)          │
│                                  │                      │
│  ┌──────────────────────────────┐│  Call Status         │
│  │  Table content (scrollable)  ││  Auth Badge          │
│  └──────────────────────────────┘│  Variables           │
│                                  │                      │
├──────────────────────────────────┴──────────────────────┤
│                  THE LOGIC TRACE (Zone 3)                │
│  [Filter: ALL | WEBHOOK | ERROR | SUCCESS]  [Clear]      │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Scrollable log console                             │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Grid spec (Tailwind):**
- Header: full width, fixed height `h-16`
- Zone 2 (Registry): `flex-grow`, `1fr`, full height minus header — left column
- Zone 1 (Pulse): fixed width `w-[360px]`, full height minus header — right column (mirrors `.rail-scroll` in HTML)
- Zone 3 (Logic Trace): full width, fixed height `h-64`, pinned to bottom

---

### 4.2 Zone 1 — The Pulse

**Component tree:**
```
PulsePanel
├── SectionHeader (title: "Live Call", icon: Activity)
├── CallStatusBadge
│   ├── Animated ring (CSS pulse when ACTIVE)
│   └── Status text: "CALL ACTIVE" / "WAITING..."
├── AuthBadge  (visible only when isAuthenticated = true)
│   └── UserCheck icon + caller name
├── DoctorInFocusCard  (visible only when doctorId is set)
│   ├── Stethoscope icon
│   ├── Doctor name (resolved from doctorsQuery cache)
│   └── Specialty label
└── ExtractedVarsCard
    ├── Variable row: Doctor ID  → value or "—"
    ├── Variable row: Date       → value or "—"
    └── Variable row: Time       → value or "—"
```

**Behavior:**
- `CallStatusBadge` reads `isCallActive` from `callStore`
- When `isCallActive` is `true`, a CSS `animate-ping` ring renders around the dot
- `ExtractedVarsCard` rows animate from opacity 0 → 1 via Framer Motion as each variable is set
- The entire Pulse panel has a left border accent that changes color: `border-slate-700` (idle) → `border-emerald-500` (active) — left border because the panel sits on the right edge of the layout

---

### 4.3 Zone 2 — The Registry

**Component tree:**
```
RegistryPanel
├── SectionHeader (title: "Registry", icon: Database)
├── TabBar
│   ├── Tab: "Doctors"        (with count badge)
│   └── Tab: "Appointments"   (with count badge, pulses on new entry)
│
├── [If Doctors tab active]
│   └── DoctorsTable
│       ├── TableHeader: Name | Specialty | Department | Availability
│       └── TableBody (mapped from useDoctors)
│           └── DoctorRow
│               ├── Doctor name + avatar initial
│               ├── Specialty text
│               └── AvailabilityPill  (queries useDoctorAvailability per row)
│
└── [If Appointments tab active]
    └── AppointmentsTable
        ├── TableHeader: Patient | Doctor | Date | Time | Status | Created
        └── AnimatePresence (Framer Motion)
            └── AppointmentRow × N
                ├── Patient user_id (truncated, tooltip for full)
                ├── Doctor name (resolved from cache)
                ├── Date
                ├── Start time → End time
                └── StatusPill: pending / confirmed / cancelled
```

**Behavior:**
- The Appointments tab badge number increments when a new row enters
- The tab label briefly pulses (ring animation) when `appointmentsQuery` detects a new entry
- `AvailabilityPill` in the Doctors table shows a loading skeleton while `useDoctorAvailability` is fetching

---

### 4.4 Zone 3 — The Logic Trace

**Component tree:**
```
LogTracePanel
├── SectionHeader (title: "Logic Trace", icon: Terminal)
├── LogFilterBar
│   ├── FilterChip: ALL
│   ├── FilterChip: WEBHOOK
│   ├── FilterChip: ERROR  (red accent)
│   └── [Clear Logs] button
└── LogWindow  (auto-scrolls to bottom on new entry)
    └── LogEntry × N
        ├── Timestamp (HH:MM:SS.ms)
        ├── MethodBadge: GET / POST (color coded)
        ├── Path string
        ├── StatusCode (200=green, 400=yellow, 500=red)
        └── JsonViewer (collapsed by default, click to expand)
            ├── Request body section
            └── Response body section
```

**Behavior:**
- Every call through `apiClient.js` is intercepted by `logInterceptor.js` and pushed to `logStore`
- Max `LOG_MAX_ENTRIES` (default: 200) entries kept; oldest are shifted out
- Auto-scroll is suspended when the user manually scrolls up; a "↓ Jump to latest" button appears
- Error entries (status >= 400) have a left border in `red-500` and are always visible regardless of filter

---

### 4.5 Zone 4 — The Calendar Page

The Calendar page is a **separate route** (`/calendar`) sharing the same `DashboardShell` sidebar. It is not part of the three-zone Dashboard layout. Its content area uses the HTML's existing layout:

```
CalendarPage
├── Header (shared, via DashboardShell)
├── main-body (grid: 1fr | 360px right rail)
│   ├── center-scroll
│   │   ├── CalendarToolbar        # Week nav + AI/Staff filter + view switcher
│   │   ├── [view === 'week'] WeekCalendar
│   │   ├── [view === 'day']  DayView
│   │   ├── [view === 'list'] ListView
│   │   └── DoctorLegend
│   └── rail-scroll (360px)
│       ├── TodayAgenda            # Today's appointments list
│       ├── AICallMonitor (mini)   # Reuse PulsePanel in compact mode
│       └── AIStatsCard            # Calls handled / booked / resolved stats
└── AppointmentDrawer              # Slide-in panel, portal-rendered
```

**Data sources:** All calendar views consume the same `useAppointments` and `useDoctors` query cache already maintained by the Dashboard page — no additional polling is needed when navigating between pages.

**View state:** `view` (week/day/list), `filters` (ai: all/ai/human, doctor: all/id), and `selectedAppt` are local `useState` within `CalendarPage` — they do not go into Zustand.

---

## 5. Real-time Synchronization Plan

### 5.1 Polling Strategy (Phase 1 — immediate)

TanStack Query's `refetchInterval` is used for all live data. No WebSocket infrastructure required to ship Phase 1.

| Query | Endpoint | Poll Interval | Reason |
|---|---|---|---|
| `useDoctors` | `GET /doctors/` | 30 000 ms | Doctors list is semi-static |
| `useAppointments` | `GET /appointments/` | 5 000 ms | Must catch new bookings quickly |
| `useDoctorAvailability` | `GET /scheduales/{id}/availability` | 10 000 ms | Per-doctor, batched |

**New appointment detection logic (inside `useAppointments`):**
1. On each successful refetch, compare the returned array length to the previous length stored in a `useRef`
2. If `newLength > previousLength`, fire `invalidateQueries(['appointments'])` immediately and trigger the tab badge pulse animation via a Zustand flag
3. The delta rows are the ones with `created_at` timestamps newer than the last known timestamp

### 5.2 WebSocket Integration (Phase 2 — future)

When Retell provides a real-time call event stream:

- `retellWebhook.js` opens a WebSocket connection to the Retell call events endpoint
- On event `call_started`: write `{ isCallActive: true }` to `callStore`
- On event `variable_extracted`: write the variable key/value to `callStore`
- On event `call_ended`: reset `callStore` to idle state, trigger a final `invalidateQueries(['appointments'])` to catch any last booking

**Fallback:** If WebSocket is unavailable, the Pulse zone falls back to showing the last known state from the most recent `useAppointments` poll.

### 5.3 Optimistic Updates

When `SetAppointmentCommand` is triggered (via `POST /appointments/set`):
- Immediately append a "pending confirmation" row to the Appointments table with a spinner in the status column
- On query settlement, replace the optimistic row with the real server data
- On error, remove the optimistic row and show a toast notification

---

## 6. UI/UX Design System

### 6.1 Color Palette

| Role | Color | Tailwind Token | Hex |
|---|---|---|---|
| Background (primary) | Near-black slate | `bg-slate-950` | #020817 |
| Background (panels) | Dark slate | `bg-slate-900` | #0f172a |
| Background (cards) | Mid slate | `bg-slate-800` | #1e293b |
| Border | Subtle slate | `border-slate-700` | #334155 |
| Text (primary) | White | `text-slate-50` | #f8fafc |
| Text (secondary) | Muted | `text-slate-400` | #94a3b8 |
| Accent (active/success) | Emerald | `text-emerald-400` | #34d399 |
| Accent (interactive) | Indigo | `text-indigo-400` | #818cf8 |
| Warning | Amber | `text-amber-400` | #fbbf24 |
| Error | Red | `text-red-400` | #f87171 |
| Call active ring | Emerald pulse | `bg-emerald-500` | #10b981 |

### 6.2 Typography

| Element | Size | Weight | Token |
|---|---|---|---|
| Zone headers | 14px | Semibold | `text-sm font-semibold` |
| Table headers | 11px | Medium + uppercase | `text-xs font-medium uppercase tracking-wider` |
| Table body | 13px | Normal | `text-sm` |
| Log entries | 12px | Mono | `text-xs font-mono` |
| Badge labels | 10px | Bold + uppercase | `text-[10px] font-bold uppercase` |

Font family: System font stack (`font-sans`) for UI, `font-mono` (JetBrains Mono or system mono) for log entries and UUIDs.

### 6.3 Framer Motion Animations

**New Appointment Row Entry:**
```
initial:  { opacity: 0, y: -8, backgroundColor: "rgba(52, 211, 153, 0.15)" }
animate:  { opacity: 1, y: 0,  backgroundColor: "rgba(52, 211, 153, 0)" }
transition: { duration: 0.4, ease: "easeOut" }
```
The brief green flash on background communicates "this row is new."

**Extracted Variable Reveal (ExtractedVarsCard):**
```
initial:  { opacity: 0, x: -4 }
animate:  { opacity: 1, x: 0 }
transition: { duration: 0.25, delay: staggered by index * 0.08 }
```

**Call Active Status Transition:**
```
CallStatusBadge wrapper:
initial:  { scale: 0.95, opacity: 0 }
animate:  { scale: 1,    opacity: 1 }
transition: { type: "spring", stiffness: 300, damping: 20 }
```

**Log Entry Appearance:**
```
initial:  { opacity: 0, height: 0 }
animate:  { opacity: 1, height: "auto" }
transition: { duration: 0.2 }
```

**AuthBadge Pop-in:**
```
initial:  { scale: 0, opacity: 0 }
animate:  { scale: 1, opacity: 1 }
transition: { type: "spring", stiffness: 400, damping: 17 }
```

### 6.4 Component Visual States

**AvailabilityPill:**
| State | Appearance |
|---|---|
| `available: true` | `bg-emerald-500/20 text-emerald-400 border border-emerald-500/30` — "Available" |
| `available: false` | `bg-red-500/20 text-red-400 border border-red-500/30` — "Booked" |
| Loading | Skeleton shimmer, same pill shape |

**StatusPill (Appointment):**
| Status | Appearance |
|---|---|
| `pending` | Amber, pulsing dot |
| `confirmed` | Emerald |
| `cancelled` | Slate, strikethrough text |

---

## 7. API Contracts

### 7.1 GET /doctors/

**Response:**
```
Array of:
{
  "id": string (UUID),
  "name": string,
  "specialty": string,
  "department_id": string (UUID),
  "department_name": string,
  "created_at": string (ISO 8601)
}
```

### 7.2 GET /appointments/

**Response:**
```
Array of:
{
  "id": string (UUID),
  "doctor_id": string (UUID),
  "user_id": string (UUID),
  "date": string (YYYY-MM-DD),
  "start_time": string (HH:MM:SS),
  "end_time": string (HH:MM:SS),
  "status": "pending" | "confirmed" | "cancelled",
  "cancelled_at": string | null,
  "created_at": string (ISO 8601),
  "updated_at": string (ISO 8601)
}
```

### 7.3 GET /scheduales/{doctor_id}/availability?date_str=MM.DD

**Response:**
```
{
  "available": boolean
}
```

### 7.4 GET /appointments/slots/check?doctor_id=UUID&date_str=MM.DD&requested_time=HH:MM

**Response:**
```
{
  "is_slot_available": boolean
}
```

### 7.5 POST /appointments/set

**Request body:**
```
{
  "doctor_id": string (UUID),
  "user_id": string (UUID),
  "date": string (YYYY-MM-DD),
  "start_time": string (HH:MM:SS)
}
```

**Response:**
```
{
  "id": string (UUID),
  "doctor_id": string (UUID),
  "user_id": string (UUID),
  "date": string (YYYY-MM-DD),
  "start_time": string (HH:MM:SS),
  "end_time": string (HH:MM:SS),
  "status": "pending",
  "created_at": string (ISO 8601),
  "updated_at": string (ISO 8601)
}
```

### 7.6 Auth Endpoint (Pre-Greeting, future)

**Expected response shape the frontend will consume:**
```
{
  "is_authenticated": boolean,
  "user": {
    "id": string (UUID),
    "name": string,
    "phone": string
  } | null
}
```

---

## 8. Authentication Demo Flow

### 8.1 The Ahmet Yılmaz Scenario

When a call begins and the backend's pre-greeting auth check returns `is_authenticated: true`, the dashboard must visually confirm the caller is recognized.

**Flow:**

```
Retell triggers pre-greeting webhook
        ↓
Backend responds: { is_authenticated: true, user: { name: "Ahmet Yılmaz", ... } }
        ↓
logInterceptor captures the response
        ↓
callStore.setAuthenticated(true, "Ahmet Yılmaz")
        ↓
AuthBadge springs into view in The Pulse zone
```

### 8.2 AuthBadge Specification

**Visual design:**
```
┌────────────────────────────────┐
│  ✓  Recognized Patient          │
│     Ahmet Yılmaz               │
└────────────────────────────────┘
```

- Background: `bg-emerald-500/10`
- Border: `border border-emerald-500/30`
- Left accent bar: 3px solid `emerald-500`
- Icon: `UserCheck` (Lucide, emerald)
- Title: "Recognized Patient" in `text-emerald-400 text-xs uppercase font-bold`
- Name: `text-slate-50 text-sm font-medium`

**Unrecognized state:**
```
┌────────────────────────────────┐
│  ?  Unknown Caller              │
│     Verifying identity...       │
└────────────────────────────────┘
```
- Background: `bg-slate-700/30`
- Border: `border border-slate-600`
- Icon: `UserX` (Lucide, slate)
- Shown only while `isCallActive` is true and `is_authenticated` is not yet determined

### 8.3 State Transitions

| Trigger | callStore state | AuthBadge |
|---|---|---|
| No call | `isCallActive: false` | Hidden |
| Call starts, auth pending | `isCallActive: true, isAuthenticated: null` | "Verifying..." |
| Auth returns true | `isAuthenticated: true, callerName: "Ahmet Yılmaz"` | "Recognized Patient" badge |
| Auth returns false | `isAuthenticated: false` | "Unknown Caller" badge |
| Call ends | Reset all to defaults | Hidden (fade out) |

---

## 9. State Management Blueprint

### 9.1 callStore (Zustand)

```
State shape:
{
  isCallActive: boolean          // default: false
  isAuthenticated: boolean|null  // null = unknown, true/false = determined
  callerName: string|null
  callerUserId: string|null
  extractedDoctorId: string|null
  extractedDateStr: string|null
  extractedTimeStr: string|null
}

Actions:
  startCall()                    // sets isCallActive: true, resets all extracted vars
  endCall()                      // resets entire store to defaults
  setAuthenticated(bool, name)   // sets isAuthenticated + callerName
  setExtractedVar(key, value)    // sets one of the three extracted variables
```

### 9.2 logStore (Zustand)

```
State shape:
{
  logs: Array<LogEntry>
  activeFilter: "ALL" | "WEBHOOK" | "ERROR" | "SUCCESS"
}

LogEntry shape:
{
  id: string (nanoid)
  timestamp: Date
  method: "GET" | "POST" | "PATCH" | "DELETE"
  path: string
  statusCode: number
  requestBody: object|null
  responseBody: object|null
  durationMs: number
}

Actions:
  pushLog(entry)                 // prepend to logs, enforce max cap
  clearLogs()
  setFilter(filter)
```

### 9.3 TanStack Query Keys

```
["doctors"]                            → useDoctors
["appointments"]                       → useAppointments
["availability", doctorId, dateStr]    → useDoctorAvailability
["slotCheck", doctorId, dateStr, time] → useSlotCheck
```

### 9.4 Doctor Color Slot System

Doctors are assigned a visual color deterministically by their position in the array returned by `GET /doctors/`. This is a frontend-only concern — the backend has no color field.

```
DOCTOR_COLORS = ['teal', 'sage', 'amber', 'indigo', 'rose']

doctor at index 0 → 'teal'  → .ev-teal, .av-teal, .legend-teal, .rr-rail-teal
doctor at index 1 → 'sage'  → .ev-sage, .av-sage, ...
...and so on, cycling if > 5 doctors
```

This constant lives in `utils/constants.js` and is consumed by any component that renders doctor-colored UI (AppointmentBlock, DayView column headers, DoctorLegend, TodayAgenda rail).

---

## 10. Empty States & Loading States

### 10.1 Dashboard Before First Call

The Pulse zone renders:
```
┌─────────────────────────────┐
│                             │
│     ( wifi-off icon )       │
│                             │
│   Waiting for first call    │
│   The AI agent is standing  │
│   by. No active sessions.   │
│                             │
└─────────────────────────────┘
```
- Icon: `PhoneOff` in `text-slate-600`, size 48
- Text: `text-slate-500 text-sm text-center`
- The Call Status dot is gray with no animation

### 10.2 Empty Appointments Table

```
┌─────────────────────────────────────────┐
│                                         │
│         ( calendar icon )               │
│                                         │
│     No appointments booked yet          │
│     They will appear here the moment    │
│     the AI agent confirms a booking.    │
│                                         │
└─────────────────────────────────────────┘
```

### 10.3 Empty Log Trace

```
[ Terminal icon ]  No requests logged yet.
                   API calls will appear here automatically.
```
Monospace font, `text-slate-600`, centered in the log window.

### 10.4 Loading Skeletons

**DoctorsTable loading state:** 5 rows of shimmer skeletons, matching the table column widths exactly. Prevents layout shift when real data arrives.

**AppointmentsTable loading state:** 3 rows of shimmer skeletons.

**AvailabilityPill loading state:** Pill-shaped shimmer, `w-20 h-5 rounded-full animate-pulse bg-slate-700`.

### 10.5 Error States

**Query error (e.g. server offline):**
- Replace the relevant zone content with:
```
[ AlertCircle icon, red ]
Backend unreachable
Last updated: {timestamp}
[ Retry button ]
```
- The Header connection indicator switches from green dot to red dot with label "OFFLINE"
- The Logic Trace automatically shows an ERROR log entry for the failed request

---

*Document version: 1.0 — Architecture only, no implementation code.*
