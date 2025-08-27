'use client'

import { useState, useEffect } from 'react'
import { Server, Download, Settings, Play, CheckCircle } from 'lucide-react'
import { DeploymentConfig } from '@/types'

interface DeploymentManagerProps {
  onRefresh: () => void
}

export default function DeploymentManager({ onRefresh }: DeploymentManagerProps) {
  const [selectedProvider, setSelectedProvider] = useState<'ollama' | 'localai' | 'openrouter'>('ollama')
  const [deploymentConfig, setDeploymentConfig] = useState<DeploymentConfig>({
    provider: 'ollama',
    model: 'llama3.2',
    base_url: 'http://localhost:11434'
  })
  const [deploymentStatus, setDeploymentStatus] = useState<{
    global_config?: {
      default_model?: string;
      default_provider?: string;
      configured_agents?: number;
      api_keys_configured?: number;
    };
    running_agents?: number;
    available_agents?: number;
  } | null>(null)
  const [isDeploying, setIsDeploying] = useState(false)

  useEffect(() => {
    fetchDeploymentStatus()
  }, [])

  const fetchDeploymentStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/deploy/status')
      const data = await response.json()
      setDeploymentStatus(data)
    } catch (error) {
      console.error('Error fetching deployment status:', error)
    }
  }

  const deployLocalAI = async () => {
    setIsDeploying(true)
    try {
      const response = await fetch('http://localhost:8000/api/deploy/local-ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(deploymentConfig)
      })
      
      if (response.ok) {
        await fetchDeploymentStatus()
        onRefresh()
      }
    } catch (error) {
      console.error('Error deploying local AI:', error)
    } finally {
      setIsDeploying(false)
    }
  }

  const providerConfigs = {
    ollama: {
      name: 'Ollama',
      description: 'Run models locally with Ollama',
      defaultUrl: 'http://localhost:11434',
      models: ['llama3.2', 'llama3.1', 'codellama', 'mistral', 'phi3'],
      setup: [
        'Install Ollama from https://ollama.ai',
        'Run: ollama serve',
        'Pull a model: ollama pull llama3.2'
      ]
    },
    localai: {
      name: 'LocalAI',
      description: 'OpenAI-compatible local AI server',
      defaultUrl: 'http://localhost:8080',
      models: ['gpt-3.5-turbo', 'gpt-4', 'text-embedding-ada-002'],
      setup: [
        'Download LocalAI binary',
        'Run: ./local-ai --models-path ./models',
        'Download models to ./models directory'
      ]
    },
    openrouter: {
      name: 'OpenRouter',
      description: 'Access multiple AI models via API',
      defaultUrl: 'https://openrouter.ai/api/v1',
      models: ['openai/gpt-4o', 'anthropic/claude-3.5-sonnet', 'meta-llama/llama-3.1-405b'],
      setup: [
        'Sign up at openrouter.ai',
        'Get your API key',
        'Add credits to your account'
      ]
    }
  }

  const currentProvider = providerConfigs[selectedProvider]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Deployment Manager
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Deploy and configure local AI providers
          </p>
        </div>
        <button
          onClick={fetchDeploymentStatus}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
        >
          Refresh Status
        </button>
      </div>

      {/* Current Status */}
      {deploymentStatus && (
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Current Deployment Status
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {deploymentStatus.global_config?.default_model || 'Not Set'}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Default Model</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                {deploymentStatus.running_agents || 0}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Running Agents</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {deploymentStatus.global_config?.configured_agents || 0}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Configured</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {deploymentStatus.global_config?.api_keys_configured || 0}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">API Keys</p>
            </div>
          </div>
        </div>
      )}

      {/* Provider Selection */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {(Object.keys(providerConfigs) as Array<keyof typeof providerConfigs>).map((provider) => {
          const config = providerConfigs[provider]
          const isSelected = selectedProvider === provider
          
          return (
            <div
              key={provider}
              className={`border-2 rounded-lg p-6 cursor-pointer transition-all ${
                isSelected
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
              }`}
              onClick={() => {
                setSelectedProvider(provider)
                setDeploymentConfig({
                  ...deploymentConfig,
                  provider,
                  base_url: config.defaultUrl,
                  model: config.models[0]
                })
              }}
            >
              <div className="flex items-center space-x-3 mb-3">
                <Server className={`w-6 h-6 ${isSelected ? 'text-blue-600' : 'text-gray-500'}`} />
                <h3 className={`text-lg font-semibold ${isSelected ? 'text-blue-900 dark:text-blue-300' : 'text-gray-900 dark:text-white'}`}>
                  {config.name}
                </h3>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                {config.description}
              </p>
              <div className="space-y-1">
                <p className="text-xs font-medium text-gray-700 dark:text-gray-300">Setup Steps:</p>
                {config.setup.slice(0, 2).map((step, index) => (
                  <p key={index} className="text-xs text-gray-500 dark:text-gray-400">
                    {index + 1}. {step}
                  </p>
                ))}
              </div>
            </div>
          )
        })}
      </div>

      {/* Configuration Form */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Configure {currentProvider.name}
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Model
            </label>
            <select
              value={deploymentConfig.model}
              onChange={(e) => setDeploymentConfig({...deploymentConfig, model: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              {currentProvider.models.map((model) => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Base URL
            </label>
            <input
              type="text"
              value={deploymentConfig.base_url}
              onChange={(e) => setDeploymentConfig({...deploymentConfig, base_url: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>
          
          {selectedProvider === 'openrouter' && (
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                API Key
              </label>
              <input
                type="password"
                value={deploymentConfig.api_key || ''}
                onChange={(e) => setDeploymentConfig({...deploymentConfig, api_key: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="Your OpenRouter API key"
              />
            </div>
          )}
        </div>
        
        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3">
            Setup Instructions
          </h3>
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <ol className="space-y-2">
              {currentProvider.setup.map((step, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="flex-shrink-0 w-6 h-6 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-xs font-medium">
                    {index + 1}
                  </span>
                  <span className="text-sm text-gray-700 dark:text-gray-300">{step}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
        
        <div className="flex space-x-4 mt-6">
          <button
            onClick={deployLocalAI}
            disabled={isDeploying}
            className="flex items-center space-x-2 px-6 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"
          >
            {isDeploying ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Deploying...</span>
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>Deploy Configuration</span>
              </>
            )}
          </button>
          
          <button className="flex items-center space-x-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
            <Play className="w-4 h-4" />
            <span>Test Connection</span>
          </button>
        </div>
      </div>
    </div>
  )
}