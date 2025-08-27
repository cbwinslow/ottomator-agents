'use client'

import { useState, useEffect } from 'react'
import { Plus, Play, Settings, Trash2, Users } from 'lucide-react'
import { AgentInfo, Combination } from '@/types'

interface CombinationManagerProps {
  agents: AgentInfo[]
  onRefresh: () => void
}

export default function CombinationManager({ agents, onRefresh }: CombinationManagerProps) {
  const [combinations, setCombinations] = useState<Combination[]>([])
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newCombination, setNewCombination] = useState({
    name: '',
    description: '',
    agents: [] as string[],
    workflow_type: 'sequential'
  })

  useEffect(() => {
    fetchCombinations()
  }, [])

  const fetchCombinations = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/combinations')
      const data = await response.json()
      setCombinations(data)
    } catch (error) {
      console.error('Error fetching combinations:', error)
    }
  }

  const createCombination = async () => {
    try {
      await fetch('http://localhost:8000/api/combinations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newCombination)
      })
      
      setShowCreateModal(false)
      setNewCombination({
        name: '',
        description: '',
        agents: [],
        workflow_type: 'sequential'
      })
      fetchCombinations()
    } catch (error) {
      console.error('Error creating combination:', error)
    }
  }

  const executeCombination = async (name: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/combinations/${name}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: 'Test execution' })
      })
      const result = await response.json()
      console.log('Combination result:', result)
      // TODO: Show result in modal
    } catch (error) {
      console.error('Error executing combination:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Agent Combinations
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Create and manage multi-agent workflows
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Create Combination</span>
        </button>
      </div>

      {/* Combinations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {combinations.map((combination) => (
          <div key={combination.name} className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {combination.name}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {combination.description}
                </p>
              </div>
              <div className="flex items-center space-x-1">
                <Users className="w-4 h-4 text-gray-500" />
                <span className="text-sm text-gray-500">{combination.agents.length}</span>
              </div>
            </div>

            <div className="mb-4">
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Agents:</p>
              <div className="flex flex-wrap gap-1">
                {combination.agents.map((agentName) => (
                  <span key={agentName} className="text-xs bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 px-2 py-1 rounded">
                    {agentName}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex space-x-2">
              <button
                onClick={() => executeCombination(combination.name)}
                className="flex items-center space-x-1 px-3 py-1.5 bg-green-100 hover:bg-green-200 dark:bg-green-900 dark:hover:bg-green-800 text-green-700 dark:text-green-300 rounded-md text-sm font-medium transition-colors"
              >
                <Play className="w-4 h-4" />
                <span>Execute</span>
              </button>
              
              <button className="flex items-center space-x-1 px-3 py-1.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-md text-sm font-medium transition-colors">
                <Settings className="w-4 h-4" />
                <span>Config</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Create New Combination
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Name
                </label>
                <input
                  type="text"
                  value={newCombination.name}
                  onChange={(e) => setNewCombination({...newCombination, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Description
                </label>
                <textarea
                  value={newCombination.description}
                  onChange={(e) => setNewCombination({...newCombination, description: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  rows={3}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Select Agents
                </label>
                <div className="max-h-40 overflow-y-auto border border-gray-300 dark:border-gray-600 rounded-md p-2">
                  {agents.map((agent) => (
                    <label key={agent.name} className="flex items-center space-x-2 p-1">
                      <input
                        type="checkbox"
                        checked={newCombination.agents.includes(agent.name)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setNewCombination({
                              ...newCombination,
                              agents: [...newCombination.agents, agent.name]
                            })
                          } else {
                            setNewCombination({
                              ...newCombination,
                              agents: newCombination.agents.filter(a => a !== agent.name)
                            })
                          }
                        }}
                        className="rounded"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">{agent.name}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="flex space-x-3 mt-6">
              <button
                onClick={createCombination}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors"
              >
                Create
              </button>
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded-md font-medium transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}