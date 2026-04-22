import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardShell from './components/layout/DashboardShell'
import DashboardPage from './pages/DashboardPage'
import CalendarPage from './pages/CalendarPage'

export default function App() {
  return (
    <Routes>
      <Route element={<DashboardShell />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/calendar"  element={<CalendarPage />} />
      </Route>
    </Routes>
  )
}
