import { useState } from 'react'
import { api } from './lib/api'
import './App.css'

type HealthState =
  | { kind: 'idle' }
  | { kind: 'loading' }
  | { kind: 'ok'; status: string }
  | { kind: 'error'; message: string }

function App() {
  const [health, setHealth] = useState<HealthState>({ kind: 'idle' })

  async function checkHealth() {
    setHealth({ kind: 'loading' })
    try {
      const res = await api.health()
      setHealth({ kind: 'ok', status: res.status })
    } catch (err) {
      const message = (err as { message?: string }).message ?? '请求失败'
      setHealth({ kind: 'error', message })
    }
  }

  return (
    <main className="app">
      <h1>Mind &amp; Health &amp; Agents</h1>
      <p className="subtitle">前后端框架已就绪，具体功能待开发。</p>

      <section className="card">
        <h2>后端连通性检查</h2>
        <button type="button" onClick={checkHealth} disabled={health.kind === 'loading'}>
          {health.kind === 'loading' ? '检查中…' : '检查后端状态'}
        </button>

        {health.kind === 'ok' && (
          <p className="status ok">后端正常：{health.status}</p>
        )}
        {health.kind === 'error' && (
          <p className="status error">连接失败：{health.message}</p>
        )}
      </section>
    </main>
  )
}

export default App
