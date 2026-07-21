import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import './App.css'
import { API, type responseMessage } from './api'

type responseMessageForm = {
  content: string;
  report: string;
}

const EMPTY_RESPONSE_MESSAGE: responseMessageForm = {
  content: 'No message yet',
  report: 'No report yet',
}

function App() {
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState<string>('')
  const [res, setRes] = useState<responseMessage>(EMPTY_RESPONSE_MESSAGE)

  function handleMessageChange(e: React.ChangeEvent<HTMLTextAreaElement>){
    setMessage(e.target.value)
  }

  async function getReport(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setRes(EMPTY_RESPONSE_MESSAGE)
    setIsLoading(true)
    try{
      const resPost = await fetch(`${API}/analyze`, { 
        method: "POST" ,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })
      if (!resPost.ok) {
        throw new Error('Failed to get report')
      }
      const data: responseMessage = await resPost.json()
      setRes(data)
    } catch (error) {
      console.error('Error getting report:', error)
      setRes(EMPTY_RESPONSE_MESSAGE)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="app">
      <h1>Mind &amp; Health &amp; Agents</h1>
      <section className="card">
        <h2>Chat with the Agent</h2>
        <form onSubmit={getReport}>
          <textarea placeholder="Enter your message here" onChange={handleMessageChange} value={message} />
          <button type="submit" disabled={isLoading}>{isLoading ? 'Getting report...' : 'Send'}</button>
        </form>
      </section>
      <section className="card">
        <h2>Messages</h2>
        <div id="messages" className="markdown">
          {res.content.length === 0 ? (
            <p className="message-content">No message yet</p>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{res.content}</ReactMarkdown>
          )}
        </div>
      </section>
      <section className="card">
        <h2>Report</h2>
        <div id="report" className="markdown">
          {res.report.length === 0 ? (
            <p className="report-content">No report yet</p>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{res.report}</ReactMarkdown>
          )}
        </div>
      </section>
    </main>
  )
}

export default App
