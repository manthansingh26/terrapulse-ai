export interface AQIAdvisory {
  label: string
  color: string       // Tailwind bg class
  textColor: string   // Tailwind text class
  advice: string
  emoji: string
}

export function getAQIAdvisory(aqi: number): AQIAdvisory {
  if (aqi <= 50)  return {
    label: 'Good',
    color: 'bg-green-100',
    textColor: 'text-green-800',
    advice: 'Air quality is satisfactory. Enjoy outdoor activities.',
    emoji: '😊'
  }
  if (aqi <= 100) return {
    label: 'Moderate',
    color: 'bg-yellow-100',
    textColor: 'text-yellow-800',
    advice: 'Acceptable air quality. Unusually sensitive people should limit outdoor exertion.',
    emoji: '😐'
  }
  if (aqi <= 150) return {
    label: 'Unhealthy for Sensitive Groups',
    color: 'bg-orange-100',
    textColor: 'text-orange-800',
    advice: 'Sensitive groups should reduce prolonged outdoor exertion.',
    emoji: '😷'
  }
  if (aqi <= 200) return {
    label: 'Unhealthy',
    color: 'bg-red-100',
    textColor: 'text-red-800',
    advice: 'Everyone may begin to experience health effects. Limit outdoor activity.',
    emoji: '🚫'
  }
  if (aqi <= 300) return {
    label: 'Very Unhealthy',
    color: 'bg-purple-100',
    textColor: 'text-purple-800',
    advice: 'Health alert: everyone may experience serious effects. Avoid outdoor activity.',
    emoji: '☣️'
  }
  return {
    label: 'Hazardous',
    color: 'bg-red-900',
    textColor: 'text-red-100',
    advice: 'Emergency conditions. Stay indoors and keep windows closed.',
    emoji: '🆘'
  }
}
