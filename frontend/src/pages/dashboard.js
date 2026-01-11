import React from 'react'
import MemoryHeatmap from '../components/MemoryHeatmap'

export default function Dashboard(){
  return (
    <div className="p-8">
      <h2 className="text-2xl">Dashboard</h2>
      <MemoryHeatmap />
    </div>
  )
}
