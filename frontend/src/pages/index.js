import { useEffect, useState } from "react";

export default function Home() {
  const [dashboard, setDashboard] = useState({});
  const [studyPlan, setStudyPlan] = useState([]);
  const [memoryMap, setMemoryMap] = useState([]);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const dashRes = await fetch("http://127.0.0.1:8000/memory/dashboard");
        const dashData = await dashRes.json();
        setDashboard(dashData);
        
        // Additional endpoints can be added as needed
        setLoading(false);
      } catch (error) {
        console.error("Error fetching dashboard:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleStartRecall = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/memory/submit-recall", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "u1",
          concept_id: "integration_by_parts",
          correctness: "slow_correct",
          response_time: 7.2,
          hint_used: true,
          failure_type: null,
          transfer_flag: false,
          fatigue_state: "normal",
        }),
      });
      const data = await response.json();
      console.log("Recall response:", data);
      
      // Update frontend state with returned data
      if (data.dashboard) setDashboard(data.dashboard);
      if (data.next_study_plan) setStudyPlan(data.next_study_plan);
    } catch (error) {
      console.error("Error submitting recall:", error);
    }
  };

  if (loading) {
    return <div className="p-8">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-bold mb-2 text-gray-900">🧠 ReMind Dashboard</h1>
        <p className="text-gray-600 mb-8">Cognitive learning with exponential memory decay</p>

        {/* Recall Button */}
        <button
          className="mb-8 px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-purple-800 transition shadow-lg"
          onClick={handleStartRecall}
        >
          ▶ Start Recall
        </button>

        {/* Dashboard Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Overall Retention</h3>
            <p className="text-3xl font-bold text-purple-600">
              {(dashboard.overall_retention * 100).toFixed(1)}%
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Weak Concepts</h3>
            <p className="text-2xl font-bold text-red-600">
              {dashboard.weak_concepts?.length || 0}
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Reviews Due</h3>
            <p className="text-2xl font-bold text-blue-600">
              {dashboard.reviews_due_today || 0}
            </p>
          </div>
        </div>

        {/* Weak Concepts */}
        {dashboard.weak_concepts && dashboard.weak_concepts.length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow mb-8">
            <h2 className="text-xl font-bold mb-4 text-gray-900">⚠️ Weak Concepts</h2>
            <ul className="space-y-2">
              {dashboard.weak_concepts.map((concept, idx) => (
                <li key={idx} className="text-gray-700 flex items-center">
                  <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-3"></span>
                  {concept}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Study Plan */}
        {studyPlan && studyPlan.length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow mb-8">
            <h2 className="text-xl font-bold mb-4 text-gray-900">📚 Today's Study Plan</h2>
            <ul className="space-y-3">
              {studyPlan.map((item, idx) => (
                <li key={item.concept_id || idx} className="flex justify-between items-center p-3 bg-blue-50 rounded">
                  <div>
                    <p className="font-semibold text-gray-900">{item.concept_id}</p>
                    <p className="text-sm text-gray-600">{item.review_type}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-blue-600">Priority: {item.priority?.toFixed(2)}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Raw Dashboard Data */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4 text-gray-900">📊 Dashboard Data</h2>
          <pre className="bg-gray-50 p-4 rounded overflow-auto max-h-96 text-sm">
            {JSON.stringify(dashboard, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}
