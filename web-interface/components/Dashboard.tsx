'use client'

import { useState } from 'react'
import { AgentInfo, AgentStatus, SystemStats } from '@/types'
import AgentGrid from './AgentGrid'
import CombinationManager from './CombinationManager'
import DeploymentManager from './DeploymentManager'
import MonitoringDashboard from './MonitoringDashboard'
import SettingsPanel from './SettingsPanel'
import DashboardOverview from './DashboardOverview'

interface DashboardProps {
  view: string
  agents: AgentInfo[]
  agentStatuses: Record<string, AgentStatus>
  systemStats: SystemStats | null
  onRefresh: () => void
}

export default function Dashboard({ 
  view, 
  agents, 
  agentStatuses, 
  systemStats, 
  onRefresh 
}: DashboardProps) {
  
  const renderView = () => {
    switch (view) {
      case 'dashboard':
        return (
          <DashboardOverview 
            agents={agents}
            agentStatuses={agentStatuses}
            systemStats={systemStats}
            onRefresh={onRefresh}
          />
        )
      case 'agents':
        return (
          <AgentGrid 
            agents={agents}
            agentStatuses={agentStatuses}
            onRefresh={onRefresh}
          />
        )
      case 'combinations':
        return (
          <CombinationManager 
            agents={agents}
            onRefresh={onRefresh}
          />
        )
      case 'deployment':
        return (
          <DeploymentManager 
            onRefresh={onRefresh}
          />
        )
      case 'monitoring':
        return (
          <MonitoringDashboard 
            agents={agents}
            agentStatuses={agentStatuses}
            systemStats={systemStats}
            onRefresh={onRefresh}
          />
        )
      case 'settings':
        return (
          <SettingsPanel 
            onRefresh={onRefresh}
          />
        )
      default:
        return (
          <DashboardOverview 
            agents={agents}
            agentStatuses={agentStatuses}
            systemStats={systemStats}
            onRefresh={onRefresh}
          />
        )
    }
  }

  return (
    <div className="w-full">
      {renderView()}
    </div>
  )
}