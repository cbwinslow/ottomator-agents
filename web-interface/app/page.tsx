'use client'

import { useState, useEffect } from 'react'
import Dashboard from '@/components/Dashboard'
import Sidebar from '@/components/Sidebar'
import { AgentInfo, AgentStatus, SystemStats } from '@/types'

export default function Home() {
  const [selectedView, setSelectedView] = useState('dashboard')
  const [agents, setAgents] = useState<AgentInfo[]>([])
  const [agentStatuses, setAgentStatuses] = useState<Record<string, AgentStatus>>({})
  const [systemStats, setSystemStats] = useState<SystemStats | null>(null)
  const [loading, setLoading] = useState(true)

  // Fetch data from API
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch agents
        const agentsResponse = await fetch('http://localhost:8000/api/agents')
        const agentsData = await agentsResponse.json()
        setAgents(agentsData)

        // Fetch agent statuses
        const statusResponse = await fetch('http://localhost:8000/api/agents/status')
        const statusData = await statusResponse.json()
        setAgentStatuses(statusData)

        // Fetch system statistics
        const statsResponse = await fetch('http://localhost:8000/api/statistics')
        const statsData = await statsResponse.json()
        setSystemStats(statsData)

        setLoading(false)
      } catch (error) {
        console.error('Error fetching data:', error)
        setLoading(false)
      }
    }

    fetchData()
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">Loading Agent Dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex">
      <Sidebar 
        selectedView={selectedView} 
        onViewChange={setSelectedView}
        systemStats={systemStats}
      />
      
      <main className="flex-1 ml-64">
        <div className="p-8">
          <Dashboard 
            view={selectedView}
            agents={agents}
            agentStatuses={agentStatuses}
            systemStats={systemStats}
            onRefresh={() => window.location.reload()}
          />
        </div>
      </main>
    </div>
  )
}
