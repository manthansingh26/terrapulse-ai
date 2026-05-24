export interface Advisory {
  label: string
  bgClass: string
  textClass: string
  advice: string
  emoji: string
}

export function getAdvisory(aqi: number): Advisory {
  if (aqi <= 50) {
    return {
      label: 'Good',
      bgClass: 'bg-green-50',
      textClass: 'text-green-800',
      emoji: '😊',
      advice: 'Air quality is satisfactory. Outdoor activities are safe.',
    }
  }
  if (aqi <= 100) {
    return {
      label: 'Moderate',
      bgClass: 'bg-yellow-50',
      textClass: 'text-yellow-800',
      emoji: '😐',
      advice: 'Acceptable. Sensitive people should consider limiting extended outdoor exertion.',
    }
  }
  if (aqi <= 150) {
    return {
      label: 'Unhealthy for Sensitive Groups',
      bgClass: 'bg-orange-50',
      textClass: 'text-orange-800',
      emoji: '😷',
      advice: 'Sensitive groups (elderly, children, asthma) should reduce outdoor activity.',
    }
  }
  if (aqi <= 200) {
    return {
      label: 'Unhealthy',
      bgClass: 'bg-red-50',
      textClass: 'text-red-800',
      emoji: '🚫',
      advice: 'Everyone may experience health effects. Limit outdoor activity.',
    }
  }
  if (aqi <= 300) {
    return {
      label: 'Very Unhealthy',
      bgClass: 'bg-purple-50',
      textClass: 'text-purple-800',
      emoji: '☣️',
      advice: 'Health alert. Everyone should avoid outdoor activity.',
    }
  }
  return {
    label: 'Hazardous',
    bgClass: 'bg-gray-900',
    textClass: 'text-red-300',
    emoji: '🆘',
    advice: 'Emergency conditions. Stay indoors. Keep windows closed.',
  }
}
