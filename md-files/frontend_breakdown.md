# Frontend Breakdown

## Big Picture

The frontend is a **React** application. Instead of building one giant HTML page, you build many small reusable "components" (like Lego bricks) and compose them into pages.

---

## Layer 1 — Entry Point (`main.jsx`)

The **first file that runs**. Three jobs:
1. Mounts React into the HTML page (`index.html` has a `<div id="root">` — this file fills it)
2. Wraps the app in global providers:
   - `QueryClientProvider` — manages all backend API calls (caching, polling, retries)
   - `BrowserRouter` — enables URL navigation (`/dashboard`, `/calendar`, etc.)
3. Renders `<App />` as the root of everything

```
Browser opens → index.html loads → main.jsx runs → App appears
```

---

## Layer 2 — Router (`App.jsx`)

Defines **which URL shows which page**:

```
/            → redirects to /dashboard
/dashboard   → shows DashboardPage
/calendar    → shows CalendarPage
```

All pages are wrapped inside `DashboardShell`, so the sidebar and header always stay visible — only the main content area changes when you navigate.

---

## Layer 3 — Layout (the frame around every page)

### `components/layout/DashboardShell.jsx`
The permanent wrapper. A 3-part frame:
- Left: `<Sidebar />`
- Top right: `<Header />`
- Main area: `<Outlet />` — placeholder replaced by the current page's content

Think of it like a picture frame — the frame never changes, only the picture inside does.

### `components/layout/Sidebar.jsx`
The left navigation bar. Defines nav items (Dashboard, Calendar, Doctors, Patients, etc.) and renders them as clickable links. When you click a link, the URL changes → `App.jsx` notices → shows the correct page in `<Outlet />`.

### `components/layout/Header.jsx`
The top bar (title bar, search, date display).

---

## Layer 4 — Pages (the full screens)

Pages are assembled from components. They don't do logic themselves — they just arrange panels.

### `pages/DashboardPage.jsx`
Divides the screen into a 3-zone grid:
```
┌──────────────────┬──────────┐
│  RegistryPanel   │  Pulse   │
│  (tables)        │  Panel   │
├──────────────────┴──────────┤
│       LogTracePanel         │
└─────────────────────────────┘
```

### `pages/CalendarPage.jsx`
Shows the calendar view (week/day/list views, appointment blocks, toolbar).

---

## Layer 5 — Components (the Lego bricks)

### `components/pulse/` — Live Call Monitor
Displays the real-time state of an active AI phone call.

| File | What it shows |
|---|---|
| `PulsePanel.jsx` | Container that holds all pulse cards |
| `CallStatusBadge.jsx` | "Call active" / "Idle" indicator |
| `AuthBadge.jsx` | Whether the caller was recognized |
| `DoctorInFocusCard.jsx` | Which doctor the caller asked for |
| `ExtractedVarsCard.jsx` | What the AI extracted (date, time, doctor name) |

### `components/registry/` — Data Tables
Shows doctors and appointments from the backend.

| File | What it shows |
|---|---|
| `RegistryPanel.jsx` | Tab switcher between Doctors and Appointments |
| `DoctorsTable.jsx` | List of all doctors |
| `AppointmentsTable.jsx` | List of all appointments |
| `AppointmentRow.jsx` | A single row in the appointments table |
| `StatusPill.jsx` | Colored badge: PENDING / CONFIRMED / CANCELLED |
| `AvailabilityPill.jsx` | Colored badge for doctor slot availability |

### `components/logtrace/` — API Request Log
Shows every HTTP request made to the backend, like a developer console.

| File | What it does |
|---|---|
| `LogTracePanel.jsx` | Container with filter buttons + scrollable log list |
| `LogEntry.jsx` | One row: method, path, status code, duration |
| `LogFilterBar.jsx` | Buttons to filter by ALL / WEBHOOK / ERROR / SUCCESS |
| `JsonViewer.jsx` | Expandable JSON display of request/response bodies |

### `components/calendar/` — Calendar View

| File | What it does |
|---|---|
| `CalendarToolbar.jsx` | Navigation arrows, date display, view switcher (Week/Day/List) |
| `WeekCalendar.jsx` | 7-column grid showing appointments across the week |
| `DayView.jsx` | Single-day hourly grid |
| `ListView.jsx` | Flat list of upcoming appointments |
| `AppointmentBlock.jsx` | One colored appointment block inside the grid |
| `AppointmentDrawer.jsx` | Side panel that opens when you click an appointment |
| `DoctorLegend.jsx` | Color key (teal = Dr. X, amber = Dr. Y, etc.) |
| `NowIndicator.jsx` | The red "current time" line in the grid |
| `TodayAgenda.jsx` | Summary card of today's appointments |
| `AIStatsCard.jsx` | Stats card showing AI booking performance |

### `components/shared/`

| File | What it does |
|---|---|
| `EmptyState.jsx` | The "no data" placeholder shown when tables are empty |

---

## Layer 6 — Hooks (the data fetchers)

Hooks are JavaScript functions that fetch data from the backend and keep it up to date. They use React Query, which handles caching, polling, and retries automatically.

| File | Endpoint | Polling interval |
|---|---|---|
| `useAppointments.js` | `GET /appointments/` | Every 5 seconds |
| `useDoctorAvailability.js` | `GET /availability/` | Every 10 seconds |
| `useDoctors.js` | `GET /doctors/` | Every 30 seconds |
| `useToday.js` | — | Returns today's date for the calendar |

`useAppointments` has a bonus: if the count increases between polls, it fires an `onNewEntry()` callback to alert the UI.

---

## Layer 7 — Services (the network layer)

### `services/apiClient.js`
Creates one shared Axios HTTP client configured with:
- `baseURL` = your FastAPI server address (from environment variable `VITE_API_BASE_URL`)
- `timeout` = 10 seconds

Every hook uses this client. You never write raw `fetch()` calls.

### `services/logInterceptor.js`
Hooks into Axios with interceptors — code that runs automatically before every request and after every response:
- **Before request**: records the start time
- **After response**: pushes a log entry into `logStore` (method, path, status, duration, response body)
- **On error**: pushes an error log entry

This is how LogTracePanel gets populated automatically.

---

## Layer 8 — Stores (the global memory)

Stores hold shared state that multiple components need. Uses Zustand.

### `store/callStore.js`
Holds the live call state:

| Field | Meaning |
|---|---|
| `isCallActive` | Is a phone call happening right now? |
| `isAuthenticated` | Did the AI recognize the caller? |
| `callerName`, `callerUserId` | Who is calling? |
| `extractedDoctorId` | Which doctor did the AI hear? |
| `extractedDateStr`, `extractedTimeStr` | What date/time did the AI extract? |

Functions: `startCall()`, `endCall()`, `setAuthenticated()`, `setExtractedVar()`

### `store/logStore.js`
Holds the log entries shown in LogTracePanel:

| Field | Meaning |
|---|---|
| `logs[]` | Array of up to 200 log entries |
| `activeFilter` | Which filter is selected (ALL/WEBHOOK/ERROR/SUCCESS) |

Functions: `pushLog()`, `clearLogs()`, `setFilter()`

---

## Layer 9 — Utils (shared config and helpers)

### `utils/constants.js`
All magic numbers and settings in one place:
- `API_BASE_URL` — backend address (read from `.env` file)
- Polling intervals (5s / 10s / 30s)
- Calendar grid settings (8am–7pm, 60px per hour)
- Doctor color palette (teal, sage, amber, indigo, rose)

### `utils/formatters.js`
Helper functions for displaying data (formatting dates, times, names, etc.)

---

## How It All Connects to the Backend

```
FastAPI backend (Python)
        ↑  HTTP requests
        │
  apiClient.js  ←── baseURL from VITE_API_BASE_URL in .env file
        │
        │  used by
        ↓
  hooks/useDoctors.js            → GET /doctors/
  hooks/useAppointments.js       → GET /appointments/
  hooks/useDoctorAvailability.js → GET /availability/
        │
        │  data flows into
        ↓
  DoctorsTable, AppointmentsTable, WeekCalendar, etc.
        │
        │  every response also goes through
        ↓
  logInterceptor.js → logStore → LogTracePanel
```

The `.env` file (in the `frontend/` folder) sets `VITE_API_BASE_URL=http://localhost:8000` so the frontend knows where to find the FastAPI server.

---

## Data Flow: A Complete Example

Here is exactly what happens when the Dashboard loads the doctors table:

1. URL is `/dashboard` → `App.jsx` renders `DashboardPage`
2. `DashboardPage` renders `RegistryPanel`
3. `RegistryPanel` calls `useDoctors()` hook
4. `useDoctors()` asks `apiClient` to call `GET /doctors/`
5. `apiClient` sends HTTP request to `http://localhost:8000/doctors/`
6. FastAPI backend responds with JSON list of doctors
7. `logInterceptor` captures the response and adds it to `logStore`
8. React Query caches the data and gives it to `DoctorsTable`
9. `DoctorsTable` renders one row per doctor
10. `LogTracePanel` (bottom of screen) shows the request that just happened
