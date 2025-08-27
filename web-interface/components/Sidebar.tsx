'use client'

import { useState } from 'react'
import { 
  Home, 
  Bot, 
  Settings, 
  Activity,
  Layers,
  Rocket,
  BarChart3,
  Server,
  Cpu,
  HardDrive,
  Users
} from 'lucide-react'
import { SystemStats } from '@/types'

interface SidebarProps {
  selectedView: string
  onViewChange: (view: string) => void
  systemStats: SystemStats | null
}

export default function Sidebar({ selectedView, onViewChange, systemStats }: SidebarProps) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'agents', label: 'Agents', icon: Bot },
    { id: 'combinations', label: 'Combinations', icon: Layers },
    { id: 'deployment', label: 'Deployment', icon: Rocket },
    { id: 'monitoring', label: 'Monitoring', icon: Activity },
    { id: 'settings', label: 'Settings', icon: Settings },
  ]

  return (
    <div className="fixed left-0 top-0 h-full w-64 bg-white dark:bg-gray-800 shadow-lg border-r border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900 dark:text-white">
              Ottomator
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Agent Manager
            </p>
          </div>
        </div>
      </div>

      {/* System Status */}
      {systemStats && (
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            System Status
          </h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="flex items-center space-x-2">
                <Server className="w-4 h-4 text-blue-500" />
                <span className="text-gray-600 dark:text-gray-400">Agents</span>
              </span>
              <span className="font-medium text-gray-900 dark:text-white">
                {systemStats.running_agents || 0}/{systemStats.total_agents}
              </span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="flex items-center space-x-2">
                <Layers className="w-4 h-4 text-green-500" />
                <span className="text-gray-600 dark:text-gray-400">Combinations</span>
              </span>
              <span className="font-medium text-gray-900 dark:text-white">
                {systemStats.running_combinations || 0}/{systemStats.total_combinations}
              </span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="flex items-center space-x-2">
                <BarChart3 className="w-4 h-4 text-purple-500" />
                <span className="text-gray-600 dark:text-gray-400">Categories</span>
              </span>
              <span className="font-medium text-gray-900 dark:text-white">
                {systemStats.categories.length}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isSelected = selectedView === item.id
            
            return (
              <li key={item.id}>
                <button
                  onClick={() => onViewChange(item.id)}
                  className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                    isSelected
                      ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${
                    isSelected 
                      ? 'text-blue-700 dark:text-blue-400' 
                      : 'text-gray-500 dark:text-gray-400'
                  }`} />
                  <span className="font-medium">{item.label}</span>
                </button>
              </li>
            )
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 dark:border-gray-700">
        <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
          <p>Ottomator Agents v1.0</p>
          <p>Web Interface</p>
        </div>
      </div>
    </div>
  )
}