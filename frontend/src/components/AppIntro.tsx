import React, { useEffect, useState } from 'react'
import { Activity, Brain, Satellite } from 'lucide-react'

const AppIntro: React.FC = () => {
  const [isVisible, setIsVisible] = useState(() => {
    if (typeof window === 'undefined') {
      return false
    }
    return !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  })

  useEffect(() => {
    if (!isVisible) {
      return undefined
    }

    const timer = window.setTimeout(() => setIsVisible(false), 1800)
    return () => window.clearTimeout(timer)
  }, [isVisible])

  if (!isVisible) {
    return null
  }

  return (
    <div className="app-intro" aria-hidden="true">
      <div className="app-intro-grid" />
      <div className="app-intro-scan" />
      <div className="app-intro-content">
        <div className="app-intro-mark">
          <Satellite className="app-intro-icon app-intro-icon-one" size={22} />
          <Brain className="app-intro-icon app-intro-icon-two" size={26} />
          <Activity className="app-intro-icon app-intro-icon-three" size={22} />
        </div>
        <div className="app-intro-copy">
          <p className="app-intro-kicker">TerraPulse AI</p>
          <h1>Environmental Intelligence</h1>
        </div>
        <div className="app-intro-meter">
          <span />
        </div>
      </div>
    </div>
  )
}

export default AppIntro

