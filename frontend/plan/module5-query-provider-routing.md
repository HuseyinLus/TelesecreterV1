# Module 5 — TanStack Query Provider + Routing

## Goal
Wire `QueryClientProvider` and `BrowserRouter` into `main.jsx`, and define the two active routes (`/` → DashboardPage, `/calendar` → CalendarPage) in `App.jsx`. After this module the app has a working navigation shell — even with placeholder page components.

## Dependencies
- `@tanstack/react-query` + `@tanstack/react-query-devtools` (already installed)
- `react-router-dom` (already installed)

## Files to modify
- `src/main.jsx`
- `src/App.jsx`

## Files to create
- `src/pages/DashboardPage.jsx` (placeholder)
- `src/pages/CalendarPage.jsx` (placeholder)

---

## src/main.jsx
```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import './index.css'
import App from './App.jsx'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime:            10_000,
      refetchOnWindowFocus: false,
      retry:                2,
    },
  },
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  </StrictMode>
)
```

---

## src/App.jsx
```jsx
import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'
import CalendarPage from './pages/CalendarPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/calendar"  element={<CalendarPage />} />
    </Routes>
  )
}
```

---

## src/pages/DashboardPage.jsx
```jsx
export default function DashboardPage() {
  return (
    <div style={{ padding: 24 }}>
      <h2>Dashboard Page — placeholder</h2>
      <p>Route: /dashboard</p>
    </div>
  )
}
```

---

## src/pages/CalendarPage.jsx
```jsx
export default function CalendarPage() {
  return (
    <div style={{ padding: 24 }}>
      <h2>Calendar Page — placeholder</h2>
      <p>Route: /calendar</p>
    </div>
  )
}
```

---

## Test
1. Run `npm run dev`
2. Visit `http://localhost:5173/` → should redirect to `/dashboard` and show "Dashboard Page — placeholder"
3. Visit `http://localhost:5173/calendar` → should show "Calendar Page — placeholder"
4. Open React Query Devtools (bottom-right floating button in dev mode) → panel opens without errors

**Pass criteria:**
- Both routes render their placeholder text
- URL redirects from `/` to `/dashboard` automatically
- React Query Devtools panel is accessible (dev only)
- No console errors
