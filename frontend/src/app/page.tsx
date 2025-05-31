'use client'

import { useState, useEffect } from 'react'
import { Loader2, User, Brain, MessageCircle, Search, Download } from 'lucide-react'

interface WorkExperience {
  employee_title?: string
  employer_name?: string
  employee_description?: string
  start_date?: string
  end_date?: string
  [key: string]: any
}

interface Education {
  degree_name?: string
  institute_name?: string
  field_of_study?: string
  [key: string]: any
}

interface PersonData {
  name?: string
  current_position_title?: string
  current_company_name?: string
  headline?: string
  location?: string
  email?: string
  summary?: string
  past_employers?: WorkExperience[]
  current_employers?: WorkExperience[]
  education_background?: Education[]
  skills?: string[]
  [key: string]: any
}

export default function Dashboard() {
  const [personData, setPersonData] = useState<PersonData | null>(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('fetch')
  const [chatMessages, setChatMessages] = useState<Array<{role: 'user' | 'assistant', content: string}>>([])
  const [chatInput, setChatInput] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [analysisResult, setAnalysisResult] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    // Load existing person data on component mount
    loadPersonData()
  }, [])

  const loadPersonData = async () => {
    try {
      const response = await fetch('/api/load-data')
      if (response.ok) {
        const data = await response.json()
        // Handle array format from CrustData API
        if (Array.isArray(data.person_data) && data.person_data.length > 0) {
          setPersonData(data.person_data[0])
        } else {
          setPersonData(data.person_data)
        }
      }
    } catch (error) {
      console.error('Error loading person data:', error)
    }
  }

  const fetchPersonData = async () => {
    if (!searchQuery.trim()) return
    
    setLoading(true)
    try {
      const response = await fetch('/api/fetch-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery })
      })
      
      const data = await response.json()
      if (response.ok) {
        setPersonData(data.person_data)
      } else {
        alert(data.error || 'Failed to fetch data')
      }
    } catch (error: unknown) {
      alert('Error fetching data')
      console.error('Fetch error:', error)
    } finally {
      setLoading(false)
    }
  }

  const sendChatMessage = async () => {
    if (!chatInput.trim() || !personData) return
    
    const userMessage = chatInput
    setChatInput('')
    setChatMessages(prev => [...prev, { role: 'user', content: userMessage }])
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      })
      
      const data = await response.json()
      setChatMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (error: unknown) {
      setChatMessages(prev => [...prev, { role: 'assistant', content: 'Error processing your message' }])
      console.error('Chat error:', error)
    }
  }

  const analyzeJobFit = async () => {
    if (!jobDescription.trim() || !personData) return
    
    setLoading(true)
    try {
      const response = await fetch('/api/analyze-job', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_description: jobDescription })
      })
      
      const data = await response.json()
      setAnalysisResult(data.analysis)
    } catch (error: unknown) {
      setAnalysisResult('Error analyzing job fit')
      console.error('Job analysis error:', error)
    } finally {
      setLoading(false)
    }
  }

  const performGeneralAnalysis = async () => {
    if (!personData) return
    
    setLoading(true)
    try {
      const response = await fetch('/api/general-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      
      const data = await response.json()
      setAnalysisResult(data.analysis)
    } catch (error: unknown) {
      setAnalysisResult('Error performing general analysis')
      console.error('General analysis error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-cyan-600 bg-clip-text text-transparent mb-2">
            AI-Powered Talent Analyzer
          </h1>
          <p className="text-gray-600">Fetch person data, chat with AI, and analyze professional profiles</p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg p-1 shadow-lg">
            {[
              { id: 'fetch', label: 'Fetch Data', icon: Search },
              { id: 'chat', label: 'AI Chat', icon: MessageCircle },
              { id: 'analyze', label: 'Analysis', icon: Brain }
            ].map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`px-6 py-3 rounded-md font-medium flex items-center gap-2 transition-all ${
                  activeTab === id
                    ? 'bg-indigo-600 text-white shadow-md'
                    : 'text-gray-600 hover:text-indigo-600'
                }`}
              >
                <Icon size={20} />
                {label}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Person Data Card */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <User className="text-indigo-600" size={24} />
                <h2 className="text-xl font-semibold">Person Profile</h2>
              </div>
              
              {personData ? (
                <div className="space-y-3">
                  <div>
                    <h3 className="font-semibold text-lg">{personData.name || 'Unknown'}</h3>
                    <p className="text-gray-600">{personData.headline || personData.current_position_title || 'No title'}</p>
                    <p className="text-gray-500">{personData.location || 'Location unknown'}</p>
                    {personData.email && (
                      <p className="text-gray-500 text-sm">{personData.email}</p>
                    )}
                  </div>
                  
                  {((personData.past_employers && personData.past_employers.length > 0) || 
                   (personData.current_employers && personData.current_employers.length > 0)) && (
                    <div>
                      <h4 className="font-medium text-sm text-gray-700 mb-2">Recent Experience:</h4>
                      <div className="space-y-1">
                        {personData.current_employers?.slice(0, 1).map((exp: WorkExperience, idx: number) => (
                          <p key={`current-${idx}`} className="text-sm text-gray-600">
                            • {exp.employee_title} at {exp.employer_name} (Current)
                          </p>
                        ))}
                        {personData.past_employers?.slice(0, 2).map((exp: WorkExperience, idx: number) => (
                          <p key={`past-${idx}`} className="text-sm text-gray-600">
                            • {exp.employee_title} at {exp.employer_name}
                          </p>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {personData.education_background && personData.education_background.length > 0 && (
                    <div>
                      <h4 className="font-medium text-sm text-gray-700 mb-2">Education:</h4>
                      <div className="space-y-1">
                        {personData.education_background.slice(0, 2).map((edu: Education, idx: number) => (
                          <p key={idx} className="text-sm text-gray-600">
                            • {edu.degree_name} from {edu.institute_name}
                          </p>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {personData.skills && personData.skills.length > 0 && (
                    <div>
                      <h4 className="font-medium text-sm text-gray-700 mb-2">Key Skills:</h4>
                      <div className="flex flex-wrap gap-1">
                        {personData.skills.slice(0, 6).map((skill: string, idx: number) => (
                          <span key={idx} className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <User size={48} className="mx-auto mb-3 opacity-50" />
                  <p>No person data loaded</p>
                  <p className="text-sm">Use the Fetch Data tab to search for someone</p>
                </div>
              )}
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6">
              {activeTab === 'fetch' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-semibold flex items-center gap-2">
                    <Search className="text-indigo-600" size={24} />
                    Fetch Person Data
                  </h3>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Search Query (name, email, LinkedIn profile, etc.)
                      </label>
                      <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Enter person's name, email, or LinkedIn URL..."
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        onKeyPress={(e) => e.key === 'Enter' && fetchPersonData()}
                      />
                    </div>
                    
                    <button
                      onClick={fetchPersonData}
                      disabled={loading || !searchQuery.trim()}
                      className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
                    >
                      {loading ? <Loader2 className="animate-spin" size={20} /> : <Download size={20} />}
                      {loading ? 'Fetching Data...' : 'Fetch Person Data'}
                    </button>
                  </div>
                </div>
              )}

              {activeTab === 'chat' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-semibold flex items-center gap-2">
                    <MessageCircle className="text-indigo-600" size={24} />
                    AI Chat
                  </h3>
                  
                  {!personData ? (
                    <div className="text-center py-8 text-gray-500">
                      <MessageCircle size={48} className="mx-auto mb-3 opacity-50" />
                      <p>Please fetch person data first to start chatting</p>
                    </div>
                  ) : (
                    <>
                      <div className="h-96 overflow-y-auto border border-gray-200 rounded-lg p-4 space-y-4">
                        {chatMessages.length === 0 ? (
                          <div className="text-center text-gray-500 py-8">
                            <MessageCircle size={32} className="mx-auto mb-2 opacity-50" />
                            <p>Ask me anything about {personData.name || 'this person'}!</p>
                          </div>
                        ) : (
                          chatMessages.map((msg, idx) => (
                            <div
                              key={idx}
                              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                              <div
                                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                                  msg.role === 'user'
                                    ? 'bg-indigo-600 text-white'
                                    : 'bg-gray-100 text-gray-800'
                                }`}
                              >
                                {msg.content}
                              </div>
                            </div>
                          ))
                        )}
                      </div>
                      
                      <div className="flex gap-2">
                        <input
                          type="text"
                          value={chatInput}
                          onChange={(e) => setChatInput(e.target.value)}
                          placeholder="Ask about their experience, skills, etc..."
                          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                          onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
                        />
                        <button
                          onClick={sendChatMessage}
                          disabled={!chatInput.trim()}
                          className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                          Send
                        </button>
                      </div>
                    </>
                  )}
                </div>
              )}

              {activeTab === 'analyze' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-semibold flex items-center gap-2">
                    <Brain className="text-indigo-600" size={24} />
                    Professional Analysis
                  </h3>
                  
                  {!personData ? (
                    <div className="text-center py-8 text-gray-500">
                      <Brain size={48} className="mx-auto mb-3 opacity-50" />
                      <p>Please fetch person data first to perform analysis</p>
                    </div>
                  ) : (
                    <div className="space-y-6">
                      {/* General Analysis */}
                      <div className="p-4 border border-gray-200 rounded-lg">
                        <h4 className="font-medium mb-3">General Professional Analysis</h4>
                        <button
                          onClick={performGeneralAnalysis}
                          disabled={loading}
                          className="bg-cyan-600 text-white px-6 py-2 rounded-lg hover:bg-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                          {loading ? <Loader2 className="animate-spin" size={16} /> : <Brain size={16} />}
                          Generate Analysis
                        </button>
                      </div>
                      
                      {/* Job Fit Analysis */}
                      <div className="p-4 border border-gray-200 rounded-lg">
                        <h4 className="font-medium mb-3">Job Fit Analysis</h4>
                        <textarea
                          value={jobDescription}
                          onChange={(e) => setJobDescription(e.target.value)}
                          placeholder="Paste the job description here..."
                          rows={4}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent mb-3"
                        />
                        <button
                          onClick={analyzeJobFit}
                          disabled={loading || !jobDescription.trim()}
                          className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                          {loading ? <Loader2 className="animate-spin" size={16} /> : <Brain size={16} />}
                          Analyze Job Fit
                        </button>
                      </div>
                      
                      {/* Analysis Results */}
                      {analysisResult && (
                        <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                          <h4 className="font-medium mb-3">Analysis Results</h4>
                          <div className="whitespace-pre-wrap text-sm text-gray-700">
                            {analysisResult}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
