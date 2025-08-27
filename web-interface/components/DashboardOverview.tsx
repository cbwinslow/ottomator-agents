'use client'

import { useState, useEffect } from 'react'
import { BarChart3, TrendingUp, Activity, Zap, Users, Server, Cpu, HardDrive, Clock } from 'lucide-react'
import { AgentInfo, AgentStatus, SystemStats } from '@/types'

interface DashboardOverviewProps {
  agents: AgentInfo[]
  agentStatuses: Record<string, AgentStatus>
  systemStats: SystemStats | null
  onRefresh: () => void
}

export default function DashboardOverview({ 
  agents, 
  agentStatuses, 
  systemStats, 
  onRefresh 
}: DashboardOverviewProps) {
  
  const runningAgents = Object.values(agentStatuses).filter(status => status.status === 'running')
  const totalRequests = runningAgents.reduce((sum, status) => 
    sum + (status.metrics?.requests_count || 0), 0
  )
  const avgCpu = runningAgents.length > 0 
    ? runningAgents.reduce((sum, status) => sum + (status.metrics?.cpu_percent || 0), 0) / runningAgents.length
    : 0
  const totalMemory = runningAgents.reduce((sum, status) => 
    sum + (status.metrics?.memory_mb || 0), 0
  )

  // Get category distribution
  const categoryStats = systemStats?.agents_by_category || {}
  const topCategories = Object.entries(categoryStats)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Welcome to the Ottomator Agent Management System
          </p>
        </div>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
        >
          Refresh
        </button>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Agents</p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
                {agents.length}
              </p>
              <p className="text-sm text-green-600 dark:text-green-400 mt-1">
                {systemStats?.categories.length || 0} categories
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
              <Server className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Running Agents</p>
              <p className="text-3xl font-bold text-green-600 dark:text-green-400 mt-1">
                {runningAgents.length}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {((runningAgents.length / agents.length) * 100).toFixed(1)}% active
              </p>
            </div>
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
              <Activity className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Requests</p>
              <p className="text-3xl font-bold text-purple-600 dark:text-purple-400 mt-1">
                {totalRequests.toLocaleString()}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                All time
              </p>
            </div>
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Avg CPU Usage</p>
              <p className="text-3xl font-bold text-orange-600 dark:text-orange-400 mt-1">
                {avgCpu.toFixed(1)}%
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Running agents
              </p>
            </div>
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900 rounded-lg flex items-center justify-center">
              <Cpu className="w-6 h-6 text-orange-600 dark:text-orange-400" />
            </div>
          </div>
        </div>
      </div>

      {/* System Resources */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Resource Usage */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            System Resources
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600 dark:text-gray-400">CPU Usage</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">
                  {avgCpu.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min(avgCpu, 100)}%` }}
                ></div>
              </div>
            </div>
            
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600 dark:text-gray-400">Memory Usage</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">
                  {(totalMemory / 1024).toFixed(1)} GB
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-green-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min((totalMemory / 1024) * 10, 100)}%` }}
                ></div>
              </div>
            </div>
            
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600 dark:text-gray-400">Active Agents</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">
                  {runningAgents.length} / {agents.length}
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(runningAgents.length / agents.length) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Category Distribution */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Agent Categories
          </h3>
          <div className="space-y-3">
            {topCategories.map(([category, count]) => (
              <div key={category} className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400 capitalize">
                  {category}
                </span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-indigo-600 h-2 rounded-full"
                      style={{ width: `${(count / Math.max(...Object.values(categoryStats))) * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-medium text-gray-900 dark:text-white w-6 text-right">
                    {count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Recent Activity
          </h3>
          <div className="space-y-3">
            {runningAgents.slice(0, 5).map((status, index) => {
              const agentName = Object.keys(agentStatuses).find(key => 
                agentStatuses[key] === status
              )
              return (
                <div key={index} className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {agentName}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {status.metrics?.requests_count || 0} requests
                    </p>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    Running
                  </span>
                </div>
              )
            })}
            
            {runningAgents.length === 0 && (
              <p className="text-sm text-gray-500 dark:text-gray-400 text-center py-4">
                No active agents
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Quick Actions
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="flex flex-col items-center p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors">
            <Zap className="w-8 h-8 text-blue-600 dark:text-blue-400 mb-2" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              Deploy All
            </span>
          </button>
          
          <button className="flex flex-col items-center p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-green-500 hover:bg-green-50 dark:hover:bg-green-900/20 transition-colors">
            <Users className="w-8 h-8 text-green-600 dark:text-green-400 mb-2" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              Create Combo
            </span>
          </button>
          
          <button className="flex flex-col items-center p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-purple-500 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors">
            <BarChart3 className="w-8 h-8 text-purple-600 dark:text-purple-400 mb-2" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              View Analytics
            </span>
          </button>
          
          <button className="flex flex-col items-center p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-orange-500 hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors">
            <Activity className="w-8 h-8 text-orange-600 dark:text-orange-400 mb-2" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              Health Check
            </span>
          </button>
        </div>
      </div>
    </div>
  )
}