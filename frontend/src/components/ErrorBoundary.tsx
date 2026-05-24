import { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
  pageName?: string
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error(`[ErrorBoundary: ${this.props.pageName}]`, error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center min-h-64 text-center p-8">
          <div className="text-4xl mb-4">⚠️</div>
          <h2 className="text-lg font-medium text-gray-800 mb-2">
            Something went wrong on the {this.props.pageName || 'this'} page
          </h2>
          <p className="text-sm text-gray-500 mb-4">{this.state.error?.message}</p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
          >
            Try again
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
