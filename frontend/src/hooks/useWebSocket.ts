import { useEffect, useRef, useCallback } from 'react'

export const useWebSocket = (url: string) => {
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()

  const connect = useCallback(() => {
    try {
      console.log(`🔌 Connecting to WebSocket: ${url}`)
      wsRef.current = new WebSocket(url)

      wsRef.current.onopen = () => {
        console.log('✅ WebSocket connected')
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

      wsRef.current.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
      }

      wsRef.current.onclose = () => {
        console.log('❌ WebSocket disconnected')
        // Reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(connect, 3000)
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
