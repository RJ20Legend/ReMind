import React from 'react'
import NavBar from '../components/NavBar'

export default function Home(){
  return (
    <div>
      <NavBar />
      <main className="p-8">
        <h1 className="text-3xl font-bold">ReMind — Landing</h1>
        <p className="mt-4">Welcome to ReMind. This is a scaffold.</p>
      </main>
    </div>
  )
}
