import React, { useState } from 'react'
import MemoryHeatmap from '../components/MemoryHeatmap'
import RecallInterface from '../components/RecallInterface'

export default function Dashboard(){
  const [showRecallSession, setShowRecallSession] = useState(false)

  if (showRecallSession) {
    return (
      <div>
        <button
          onClick={() => setShowRecallSession(false)}
          className="fixed top-4 left-4 z-50 bg-gray-800 text-white px-4 py-2 rounded hover:bg-gray-700"
        >
          ← Back to Dashboard
        </button>
        <RecallInterface userId="u1" />
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold mb-4">Dashboard</h2>
        <button
          onClick={() => setShowRecallSession(true)}
          className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-bold py-3 px-6 rounded-lg inline-flex items-center gap-2 text-lg transition duration-200 transform hover:scale-105"
        >
          🧠 Start Recall Session
        </button>
      </div>
      <MemoryHeatmap />
    </div>
  )
}
