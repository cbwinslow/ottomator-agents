'use client'

import { useState } from 'react'
import { Play, Square, Settings, Eye, Activity, Clock, Cpu, HardDrive } from 'lucide-react'
import { AgentInfo, AgentStatus } from '@/types'

interface AgentGridProps {
  agents: AgentInfo[]
  agentStatuses: Record<string, AgentStatus>
  onRefresh: () => void
}

interface AgentCardProps {
  agent: AgentInfo
  status: AgentStatus
  onAction: (action: string, agentName: string) => void
}

function AgentCard({ agent, status, onAction }: AgentCardProps) {
  const isRunning = status?.status === 'running'
  
  const formatUptime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours}h ${minutes}m`
  }

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      'mcp': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
      'research': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      'content': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
      'business': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
      'knowledge': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-300',
      'task': 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300',
    }
    return colors[category] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {agent.name}
            </h3>
            <div className={`px-2 py-1 rounded-full text-xs font-medium ${
              isRunning 
                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
            }`}>
              {isRunning ? 'Running' : 'Stopped'}
            </div>
          </div>
          <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(agent.category)}`}>
            {agent.category}
          </div>
        </div>
        
        {/* Status Indicator */}
        <div className={`w-3 h-3 rounded-full ${
          isRunning ? 'bg-green-500' : 'bg-gray-400'
        }`}></div>
      </div>

      {/* Description */}
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-3">
        {agent.description}
      </p>

      {/* Metrics */}
      {isRunning && status.metrics && (
        <div className="grid grid-cols-2 gap-4 mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div className="flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-blue-500" />
            <div>
              <p className="text-xs text-gray-500 dark:text-gray-400">CPU</p>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {status.metrics.cpu_percent.toFixed(1)}%
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <HardDrive className="w-4 h-4 text-green-500" />
            <div>
              <p className="text-xs text-gray-500 dark:text-gray-400">Memory</p>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {(status.metrics.memory_mb / 1024).toFixed(1)} GB
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Activity className="w-4 h-4 text-purple-500" />
            <div>
              <p className="text-xs text-gray-500 dark:text-gray-400">Requests</p>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {status.metrics.requests_count}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-orange-500" />
            <div>
              <p className="text-xs text-gray-500 dark:text-gray-400">Uptime</p>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {status.uptime ? formatUptime(status.uptime) : '0m'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* API Keys Required */}
      {agent.api_keys_required.length > 0 && (
        <div className="mb-4">
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Required API Keys:</p>
          <div className="flex flex-wrap gap-1">
            {agent.api_keys_required.map((key) => (
              <span key={key} className="text-xs bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300 px-2 py-1 rounded">
                {key}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex space-x-2">
        {isRunning ? (
          <button
            onClick={() => onAction('stop', agent.name)}
            className="flex items-center space-x-1 px-3 py-1.5 bg-red-100 hover:bg-red-200 dark:bg-red-900 dark:hover:bg-red-800 text-red-700 dark:text-red-300 rounded-md text-sm font-medium transition-colors"
          >
            <Square className="w-4 h-4" />
            <span>Stop</span>
          </button>
        ) : (
          <button
            onClick={() => onAction('start', agent.name)}
            className="flex items-center space-x-1 px-3 py-1.5 bg-green-100 hover:bg-green-200 dark:bg-green-900 dark:hover:bg-green-800 text-green-700 dark:text-green-300 rounded-md text-sm font-medium transition-colors"
          >
            <Play className="w-4 h-4" />
            <span>Start</span>
          </button>
        )}
        
        <button
          onClick={() => onAction('configure', agent.name)}
          className="flex items-center space-x-1 px-3 py-1.5 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900 dark:hover:bg-blue-800 text-blue-700 dark:text-blue-300 rounded-md text-sm font-medium transition-colors"
        >
          <Settings className="w-4 h-4" />
          <span>Config</span>
        </button>
        
        <button
          onClick={() => onAction('view', agent.name)}
          className="flex items-center space-x-1 px-3 py-1.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-md text-sm font-medium transition-colors"
        >
          <Eye className="w-4 h-4" />
          <span>View</span>
        </button>
      </div>
    </div>
  )
}

export default function AgentGrid({ agents, agentStatuses, onRefresh }: AgentGridProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [searchTerm, setSearchTerm] = useState('')

  // Get unique categories
  const categories = ['all', ...Array.from(new Set(agents.map(agent => agent.category)))]
  
  // Filter agents
  const filteredAgents = agents.filter(agent => {
    const matchesCategory = selectedCategory === 'all' || agent.category === selectedCategory
    const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         agent.description.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const handleAgentAction = async (action: string, agentName: string) => {
    try {
      if (action === 'start') {
        await fetch(`http://localhost:8000/api/agents/${agentName}/launch`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ agent_name: agentName, background: true })
        })
      } else if (action === 'stop') {
        await fetch(`http://localhost:8000/api/agents/${agentName}/stop`, {
          method: 'POST'
        })
      } else if (action === 'configure') {
        // TODO: Open configuration modal
        console.log('Configure', agentName)
      } else if (action === 'view') {
        // TODO: Open agent details modal
        console.log('View', agentName)
      }
      
      // Refresh data after action
      setTimeout(onRefresh, 1000)
    } catch (error) {
      console.error(`Error performing ${action} on ${agentName}:`, error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            AI Agents
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage and monitor your AI agents
          </p>
        </div>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
        >
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search agents..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {categories.map(category => (
            <option key={category} value={category}>
              {category === 'all' ? 'All Categories' : category.charAt(0).toUpperCase() + category.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Total Agents</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{agents.length}</p>
            </div>
            <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
              <Settings className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Running</p>
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                {Object.values(agentStatuses).filter(status => status.status === 'running').length}
              </p>
            </div>
            <div className="w-10 h-10 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
              <Play className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Stopped</p>
              <p className="text-2xl font-bold text-gray-600 dark:text-gray-400">
                {Object.values(agentStatuses).filter(status => status.status === 'stopped').length}
              </p>
            </div>
            <div className="w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
              <Square className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </div>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Categories</p>
              <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">{categories.length - 1}</p>
            </div>
            <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
              <Activity className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
        </div>
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredAgents.map(agent => (
          <AgentCard
            key={agent.name}
            agent={agent}
            status={agentStatuses[agent.name] || { status: 'stopped' }}
            onAction={handleAgentAction}
          />
        ))}
      </div>

      {filteredAgents.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">No agents found matching your search criteria.</p>
        </div>
      )}
    </div>
  )
}