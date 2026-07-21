import { useState } from 'react'
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
  
  const [message, setMessage] = useState<string>('')
  const [res, setRes] = useState<responseMessage>(EMPTY_RESPONSE_MESSAGE)

  function handleMessageChange(e: React.ChangeEvent<HTMLTextAreaElement>){
    setMessage(e.target.value)
  }

  async function getReport(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setRes(EMPTY_RESPONSE_MESSAGE)
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
    }
  }

  return (
    <main className="app">
      <h1>Mind &amp; Health &amp; Agents</h1>
      <section className="card">
        <h2>Chat with the Agent</h2>
        <form onSubmit={getReport}>
          <textarea placeholder="Enter your message here" onChange={handleMessageChange} value={message} />
          <button type="submit">Send</button>
        </form>
      </section>
      <section className="card">
        <h2>Messages</h2>
        <div id="messages">
          {res.content.length === 0 ? (<p className="message-content">No message yet</p>
            ) : (
            <p className="message-content">{res.content}</p>
            )
          }
        </div>
      </section>
      <section className="card">
        <h2>Report</h2>
        <div id="report">
          {res.report.length === 0 ? (<p className="report-content">No report yet</p>
            ) : (
            <p className="report-content">{res.report}</p>
            )
          }
        </div>
      </section>
    </main>
  )
}

export default App
