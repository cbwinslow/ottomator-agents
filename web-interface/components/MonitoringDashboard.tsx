'use client'

import { AgentInfo, AgentStatus, SystemStats } from '@/types'

interface MonitoringDashboardProps {
  agents: AgentInfo[]
  agentStatuses: Record<string, AgentStatus>
  systemStats: SystemStats | null
  onRefresh: () => void
}

export default function MonitoringDashboard({ agents, agentStatuses, systemStats, onRefresh }: MonitoringDashboardProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Monitoring Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Real-time monitoring and analytics
          </p>
        </div>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
        >
          Refresh
        </button>
      </div>
      
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8 text-center">
        <p className="text-gray-500 dark:text-gray-400">
          Monitoring dashboard coming soon...
        </p>
      </div>
    </div>
  )
}