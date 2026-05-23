import { useEffect, useRef, useCallback } from 'react'

const MAX_RECONNECT_ATTEMPTS = 3

export const useWebSocket = (url: string) => {
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()
  const reconnectCountRef = useRef(0)

  const connect = useCallback(() => {
    try {
      if (reconnectCountRef.current >= MAX_RECONNECT_ATTEMPTS) {
        console.warn(
          `⚠️ WebSocket: Stopped reconnecting after ${MAX_RECONNECT_ATTEMPTS} attempts. ` +
          'Real-time updates unavailable — data will refresh via polling.'
        )
        return
      }

      console.log(`🔌 Connecting to WebSocket: ${url}`)
      wsRef.current = new WebSocket(url)

      wsRef.current.onopen = () => {
        console.log('✅ WebSocket connected')
        reconnectCountRef.current = 0
        // Request initial data
        wsRef.current?.send('get_cities')
        console.log('📨 Sent get_cities request')
      }

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          console.log('📡 Received:', data)
        } catch (error) {
          console.error('Failed to parse message:', error)
        }
      }

      wsRef.current.onerror = () => {
        // Error is logged on close — avoid duplicate noise
      }

      wsRef.current.onclose = () => {
        reconnectCountRef.current += 1
        if (reconnectCountRef.current < MAX_RECONNECT_ATTEMPTS) {
          const delay = 3000 * Math.pow(2, reconnectCountRef.current - 1) // 3s, 6s, 12s
          console.log(
            `🔄 WebSocket disconnected. Reconnecting in ${delay / 1000}s ` +
            `(attempt ${reconnectCountRef.current}/${MAX_RECONNECT_ATTEMPTS})...`
          )
          reconnectTimeoutRef.current = setTimeout(connect, delay)
        } else {
          console.warn(
            '⚠️ WebSocket: Max reconnect attempts reached. Falling back to polling.'
          )
        }
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
    }
  }, [url])

  const send = useCallback((message: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(message)
      console.log(`📤 Sent: ${message}`)
    } else {
      console.warn('WebSocket not ready to send')
    }
  }, [])

  useEffect(() => {
    connect()

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [connect])

  return { send }
}
