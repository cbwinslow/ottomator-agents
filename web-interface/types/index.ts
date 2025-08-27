export interface AgentInfo {
  name: string;
  category: string;
  description: string;
  main_file: string;
  config_files: string[];
  requirements_file?: string;
  readme_file?: string;
  dependencies: string[];
  api_keys_required: string[];
  supported_models: string[];
  last_modified: string;
}

export interface AgentStatus {
  status: string;
  uptime?: number;
  metrics?: {
    cpu_percent: number;
    memory_mb: number;
    requests_count: number;
    errors_count: number;
    last_activity?: string;
  };
}

export interface SystemStats {
  total_agents: number;
  total_combinations: number;
  agents_by_category: Record<string, number>;
  categories: string[];
  api_keys_required: string[];
  common_dependencies: string[];
  running_agents?: number;
  running_combinations?: number;
}

export interface AgentConfig {
  model: string;
  temperature: number;
  max_tokens: number;
  timeout: number;
  env_vars: Record<string, string>;
}

export interface Combination {
  name: string;
  agents: string[];
  workflow: any;
  description?: string;
  created: string;
}

export interface DeploymentConfig {
  provider: 'ollama' | 'localai' | 'openrouter';
  model: string;
  api_key?: string;
  base_url?: string;
}