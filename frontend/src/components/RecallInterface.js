import React, { useState, useEffect } from 'react'

/**
 * RecallInterface Component
 * The main study interface where users answer questions
 * and watch their memory grow/decay in real-time.
 */
export default function RecallInterface({ userId = 'u1' }) {
  const [sessionActive, setSessionActive] = useState(false)
  const [studyPlan, setStudyPlan] = useState([])
  const [currentConceptIndex, setCurrentConceptIndex] = useState(0)
  const [currentConcept, setCurrentConcept] = useState(null)
  const [question, setQuestion] = useState('')
  const [userAnswer, setUserAnswer] = useState('')
  const [responseTime, setResponseTime] = useState(0)
  const [sessionStartTime, setSessionStartTime] = useState(null)
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(false)
  const [hintUsed, setHintUsed] = useState(false)
  const [sessionStats, setSessionStats] = useState({
    totalConcepts: 0,
    completed: 0,
    averageScore: 0
  })

  // Initialize study session
  const startRecallSession = async () => {
    setSessionActive(true)
    setSessionStartTime(Date.now())
    setFeedback(null)

    // Load the initial study plan
    await loadNextConcept()
  }

  // Load next concept from study plan
  const loadNextConcept = async () => {
    if (currentConceptIndex < studyPlan.length) {
      const concept = studyPlan[currentConceptIndex]
      setCurrentConcept(concept)
      setUserAnswer('')
      setHintUsed(false)
      setResponseTime(0)
      setQuestion(generateQuestion(concept))
      setFeedback(null)
    } else {
      // Session complete - get new plan
      await generateStudyPlan()
    }
  }

  // Generate a study plan (in real implementation, comes from backend)
  const generateStudyPlan = async () => {
    // This would call backend to get personalized study plan
    // For now, return mock data
    const mockPlan = [
      { concept_id: 'integration_by_parts', priority_score: 0.95, reason: 'Very weak memory - needs practice', estimated_time_minutes: 8 },
      { concept_id: 'partial_fractions', priority_score: 0.87, reason: 'Due for review tomorrow', estimated_time_minutes: 8 },
      { concept_id: 'limits', priority_score: 0.82, reason: 'High decay rate', estimated_time_minutes: 5 },
      { concept_id: 'derivatives', priority_score: 0.76, reason: 'Regular review scheduled', estimated_time_minutes: 8 },
      { concept_id: 'arima_models', priority_score: 0.71, reason: 'Weak memory - needs practice', estimated_time_minutes: 12 }
    ]

    setStudyPlan(mockPlan)
    setCurrentConceptIndex(0)
    setSessionStats({
      totalConcepts: mockPlan.length,
      completed: 0,
      averageScore: 0
    })
  }

  // Generate a question for a concept
  const generateQuestion = (concept) => {
    const questions = {
      integration_by_parts: 'Solve: ∫ x·e^x dx using integration by parts',
      partial_fractions: 'Decompose: 5/(x² - 1) into partial fractions',
      limits: 'Find: lim(x→0) sin(x)/x',
      derivatives: 'Find the derivative of: f(x) = ln(x² + 1)',
      arima_models: 'What does the "I" stand for in ARIMA modeling?'
    }
    return questions[concept.concept_id] || 'Answer this question'
  }

  // Submit an answer
  const submitAnswer = async () => {
    if (!userAnswer.trim()) {
      alert('Please enter an answer')
      return
    }

    setLoading(true)

    // Determine correctness (mock - in real app, would use AI evaluation)
    const isCorrect = userAnswer.toLowerCase().includes('correct') ||
                     userAnswer.length > 10 // Mock evaluation

    const correctness = isCorrect ? 'slow_correct' : 'incorrect'
    const time = responseTime || (Date.now() - sessionStartTime) / 1000

    try {
      // Call the backend /submit-recall endpoint
      const response = await fetch('http://localhost:8000/memory/submit-recall', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          concept_id: currentConcept.concept_id,
          correctness: correctness,
          response_time: time,
          hint_used: hintUsed,
          failure_type: isCorrect ? null : 'wrong',
          transfer_flag: false,
          fatigue_state: 'normal'
        })
      })

      const result = await response.json()

      if (result.success) {
        const memoryUpdate = result.memory_update
        const nextConcept = result.study_plan.next_concept

        // Show feedback
        setFeedback({
          correct: isCorrect,
          score: memoryUpdate.actual_score,
          memoryStrength: memoryUpdate.memory_strength,
          confidenceLevel: memoryUpdate.confidence_level,
          nextReview: memoryUpdate.next_review_window
        })

        // Update session stats
        setSessionStats(prev => ({
          ...prev,
          completed: prev.completed + 1,
          averageScore: (prev.averageScore * prev.completed + memoryUpdate.actual_score) / (prev.completed + 1)
        }))

        // Move to next concept
        setTimeout(() => {
          setCurrentConceptIndex(prev => prev + 1)
          if (nextConcept) {
            loadNextConcept()
          } else {
            setSessionActive(false)
          }
        }, 2000)
      }
    } catch (error) {
      console.error('Error submitting recall:', error)
      setFeedback({ error: 'Failed to submit answer' })
    }

    setLoading(false)
  }

  // Show hint
  const showHint = () => {
    const hints = {
      integration_by_parts: 'Use LIATE rule: Logarithmic, Inverse trig, Algebraic, Trig, Exponential',
      partial_fractions: 'Factor the denominator first: x² - 1 = (x-1)(x+1)',
      limits: 'This is a famous limit - think Taylor series',
      derivatives: 'Use chain rule with d/dx[ln(u)] = 1/u · du/dx',
      arima_models: 'I = Integrated (differencing order)'
    }
    alert('Hint: ' + (hints[currentConcept.concept_id] || 'Think about the fundamentals'))
    setHintUsed(true)
  }

  // End session
  const endSession = () => {
    setSessionActive(false)
    setUserAnswer('')
    setFeedback(null)
  }

  if (!sessionActive) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="bg-white rounded-lg shadow-2xl p-12 max-w-md">
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🧠</div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Cognitive Loop</h1>
            <p className="text-gray-600">Watch your memory rise and decay in real-time</p>
          </div>

          <button
            onClick={startRecallSession}
            className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-bold py-4 px-6 rounded-lg text-lg transition duration-200 transform hover:scale-105"
          >
            🧠 Start Recall Session
          </button>

          <div className="mt-6 text-sm text-gray-600">
            <p className="mb-2">📚 Study optimal concepts</p>
            <p className="mb-2">✅ Get instant feedback</p>
            <p>📊 Track memory decay</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-slate-800 rounded-lg p-6 mb-6 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-3xl font-bold text-white">🧠 Recall Session</h1>
            <button
              onClick={endSession}
              className="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded"
            >
              End Session
            </button>
          </div>

          <div className="grid grid-cols-4 gap-4 text-white">
            <div>
              <p className="text-sm text-gray-400">Completed</p>
              <p className="text-2xl font-bold">{sessionStats.completed}/{sessionStats.totalConcepts}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Average Score</p>
              <p className="text-2xl font-bold">{(sessionStats.averageScore * 100).toFixed(0)}%</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Session Time</p>
              <p className="text-2xl font-bold">{((Date.now() - sessionStartTime) / 1000 / 60).toFixed(1)}m</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Next Review</p>
              <p className="text-2xl font-bold">{currentConcept?.concept_id || '—'}</p>
            </div>
          </div>
        </div>

        {/* Concept Card */}
        {currentConcept && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-sm font-semibold text-gray-600 uppercase">Concept</h2>
                <span className="text-xs bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full">
                  {currentConcept.reason}
                </span>
              </div>
              <p className="text-2xl font-bold text-gray-900 mb-2">{currentConcept.concept_id}</p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 h-2 rounded-full"
                  style={{ width: `${currentConcept.priority_score * 100}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Priority: {(currentConcept.priority_score * 100).toFixed(0)}%
              </p>
            </div>

            {/* Question */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 mb-6 border-2 border-indigo-200">
              <p className="text-gray-600 text-sm uppercase tracking-wide mb-2">Question</p>
              <p className="text-2xl font-semibold text-gray-900">{question}</p>
            </div>

            {/* Answer Input */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Your Answer</label>
              <textarea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                disabled={loading}
                placeholder="Type your answer here..."
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 disabled:bg-gray-100"
                rows="4"
              />
            </div>

            {/* Feedback */}
            {feedback && (
              <div className={`rounded-lg p-4 mb-6 ${feedback.correct ? 'bg-green-50 border-2 border-green-300' : 'bg-red-50 border-2 border-red-300'}`}>
                <div className="flex items-center mb-2">
                  <span className="text-2xl mr-2">{feedback.correct ? '✅' : '❌'}</span>
                  <p className={`font-bold ${feedback.correct ? 'text-green-700' : 'text-red-700'}`}>
                    {feedback.correct ? 'Correct!' : 'Incorrect'}
                  </p>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Score</p>
                    <p className="text-lg font-bold">{(feedback.score * 100).toFixed(0)}%</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Memory Strength</p>
                    <p className="text-lg font-bold">{(feedback.memoryStrength * 100).toFixed(0)}%</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Confidence</p>
                    <p className="text-lg font-bold">{feedback.confidenceLevel}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Next Review</p>
                    <p className="text-lg font-bold">{feedback.nextReview}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                onClick={showHint}
                disabled={loading || hintUsed || feedback}
                className="flex-1 bg-yellow-500 hover:bg-yellow-600 disabled:bg-gray-300 text-white font-bold py-3 px-4 rounded-lg transition"
              >
                💡 {hintUsed ? 'Hint Used' : 'Show Hint'}
              </button>
              <button
                onClick={submitAnswer}
                disabled={loading || feedback}
                className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-3 px-4 rounded-lg transition"
              >
                {loading ? 'Submitting...' : '✓ Submit Answer'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
