"use client"

import { useEffect, useRef } from 'react'
import Message from './Message'

export default function ChatBox({ messages, loading }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div style={{
      flex: 1,
      overflowY: 'auto',
      padding: '24px 28px',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      background: '#ffffff'
    }}>
      {messages.map((m, i) => (
        <Message key={i} sender={m.sender} text={m.text} time={m.time} />
      ))}

      {/* Typing indicator */}
      {loading && (
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: '10px' }}>
          <div style={{
            width: '34px', height: '34px',
            borderRadius: '50%',
            background: '#e6f4f4',
            border: '2px solid rgba(10,110,110,0.15)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '16px', flexShrink: 0
          }}>🤖</div>
          <div style={{
            background: 'white',
            border: '1px solid #e2e8f0',
            borderRadius: '20px',
            padding: '10px 16px',
            display: 'flex',
            gap: '4px',
            alignItems: 'center'
          }}>
            {[0, 0.2, 0.4].map((delay, i) => (
              <div key={i} style={{
                width: '6px', height: '6px',
                background: '#6b7a8d',
                borderRadius: '50%',
                animation: `bounce 1.2s ${delay}s infinite`
              }}></div>
            ))}
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}