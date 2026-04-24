export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const POLLING_INTERVAL_DOCTORS      = 30_000
export const POLLING_INTERVAL_APPOINTMENTS = 5_000
export const POLLING_INTERVAL_AVAILABILITY = 10_000

export const LOG_MAX_ENTRIES = 200

// Assigned by index position from GET /doctors/ response array.
// index 0 → teal, 1 → sage, 2 → amber, 3 → indigo, 4 → rose (cycles if > 5)
export const DOCTOR_COLORS = ['teal', 'sage', 'amber', 'indigo', 'rose']

export const getDoctorColor = (index) => DOCTOR_COLORS[index % DOCTOR_COLORS.length]

export const HOUR_HEIGHT      = 60
export const GRID_START_HOUR  = 8
export const GRID_END_HOUR    = 19
export const GRID_HOURS       = Array.from({ length: GRID_END_HOUR - GRID_START_HOUR }, (_, i) => GRID_START_HOUR + i)
