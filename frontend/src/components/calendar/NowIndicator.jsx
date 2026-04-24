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
