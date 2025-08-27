"""
FastAPI Web API for the Master Agent Menu System
Provides REST endpoints for the web interface
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import logging
from datetime import datetime
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import our existing components
from agent_launcher import AgentLauncher, AgentProcess
from agent_registry import AgentRegistry, AgentInfo, AgentCombination
from config_manager import ConfigurationManager, AgentConfig
from status_monitor import StatusMonitor
from combination_engine import CombinationEngine

logger = logging.getLogger(__name__)

# Pydantic models for API
class AgentInfoResponse(BaseModel):
    name: str
    category: str
    description: str
    main_file: str
    config_files: List[str]
    requirements_file: Optional[str]
    readme_file: Optional[str]
    dependencies: List[str]
    api_keys_required: List[str]
    supported_models: List[str]
    last_modified: datetime

class AgentConfigRequest(BaseModel):
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 300
    env_vars: Dict[str, str] = {}

class AgentLaunchRequest(BaseModel):
    agent_name: str
    config: Optional[AgentConfigRequest] = None
    background: bool = True

class AgentStatusResponse(BaseModel):
    agent_name: str
    status: str
    uptime_seconds: Optional[int] = None
    cpu_percent: Optional[float] = None
    memory_mb: Optional[float] = None
    requests_count: Optional[int] = None
    errors_count: Optional[int] = None
    last_activity: Optional[datetime] = None

class CombinationRequest(BaseModel):
    name: str
    agents: List[str]
    workflow_type: str = "sequential"
    description: Optional[str] = None

class DeploymentRequest(BaseModel):
    provider: str  # "ollama", "localai", "openrouter"
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None

# Global instances
launcher: Optional[AgentLauncher] = None
registry: Optional[AgentRegistry] = None
config_manager: Optional[ConfigurationManager] = None
status_monitor: Optional[StatusMonitor] = None
combination_engine: Optional[CombinationEngine] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup for the FastAPI app"""
    global launcher, registry, config_manager, status_monitor, combination_engine
    
    # Initialize components
    try:
        launcher = AgentLauncher()
        registry = launcher.registry
        config_manager = launcher.config_manager
        status_monitor = launcher.status_monitor
        combination_engine = launcher.combination_engine
        
        logger.info("Web API initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize Web API: {e}")
        raise
    finally:
        # Cleanup
        if launcher:
            # Stop all running agents
            for agent_name in list(launcher.running_agents.keys()):
                try:
                    launcher.stop_agent(agent_name)
                except Exception as e:
                    logger.error(f"Error stopping agent {agent_name}: {e}")
        logger.info("Web API shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Master Agent Menu API",
    description="REST API for managing AI agents",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Master Agent Menu API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "components": {
            "registry": registry is not None,
            "launcher": launcher is not None,
            "config_manager": config_manager is not None,
            "status_monitor": status_monitor is not None,
            "combination_engine": combination_engine is not None,
        }
    }

# Agent Registry Endpoints
@app.get("/api/agents", response_model=List[AgentInfoResponse])
async def get_agents():
    """Get all discovered agents"""
    if not registry:
        raise HTTPException(status_code=500, detail="Registry not initialized")
    
    agents = []
    for agent_info in registry.agents.values():
        agents.append(AgentInfoResponse(
            name=agent_info.name,
            category=agent_info.category,
            description=agent_info.description,
            main_file=agent_info.main_file,
            config_files=agent_info.config_files,
            requirements_file=agent_info.requirements_file,
            readme_file=agent_info.readme_file,
            dependencies=agent_info.dependencies,
            api_keys_required=agent_info.api_keys_required,
            supported_models=agent_info.supported_models,
            last_modified=agent_info.last_modified
        ))
    
    return agents

@app.get("/api/agents/{agent_name}", response_model=AgentInfoResponse)
async def get_agent(agent_name: str):
    """Get specific agent information"""
    if not registry:
        raise HTTPException(status_code=500, detail="Registry not initialized")
    
    if agent_name not in registry.agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    agent_info = registry.agents[agent_name]
    return AgentInfoResponse(
        name=agent_info.name,
        category=agent_info.category,
        description=agent_info.description,
        main_file=agent_info.main_file,
        config_files=agent_info.config_files,
        requirements_file=agent_info.requirements_file,
        readme_file=agent_info.readme_file,
        dependencies=agent_info.dependencies,
        api_keys_required=agent_info.api_keys_required,
        supported_models=agent_info.supported_models,
        last_modified=agent_info.last_modified
    )

@app.get("/api/agents/categories")
async def get_agent_categories():
    """Get all agent categories"""
    if not registry:
        raise HTTPException(status_code=500, detail="Registry not initialized")
    
    categories = {}
    for agent_info in registry.agents.values():
        if agent_info.category not in categories:
            categories[agent_info.category] = []
        categories[agent_info.category].append({
            "name": agent_info.name,
            "description": agent_info.description[:100] + "..." if len(agent_info.description) > 100 else agent_info.description
        })
    
    return categories

@app.get("/api/statistics")
async def get_statistics():
    """Get system statistics"""
    if not registry:
        raise HTTPException(status_code=500, detail="Registry not initialized")
    
    stats = registry.get_statistics()
    
    # Add runtime statistics
    if launcher:
        stats["running_agents"] = len(launcher.running_agents)
        stats["running_combinations"] = len(combination_engine.running_combinations) if combination_engine else 0
    
    return stats

# Agent Configuration Endpoints
@app.get("/api/agents/{agent_name}/config")
async def get_agent_config(agent_name: str):
    """Get agent configuration"""
    if not config_manager:
        raise HTTPException(status_code=500, detail="Config manager not initialized")
    
    if agent_name not in config_manager.agent_configs:
        # Return default config
        return {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 2000,
            "timeout": 300,
            "env_vars": {}
        }
    
    config = config_manager.agent_configs[agent_name]
    return {
        "model": config.model,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "timeout": config.timeout,
        "env_vars": config.env_vars
    }

@app.post("/api/agents/{agent_name}/config")
async def update_agent_config(agent_name: str, config_request: AgentConfigRequest):
    """Update agent configuration"""
    if not config_manager:
        raise HTTPException(status_code=500, detail="Config manager not initialized")
    
    try:
        config_manager.configure_agent(
            agent_name,
            model=config_request.model,
            temperature=config_request.temperature,
            max_tokens=config_request.max_tokens,
            timeout=config_request.timeout,
            **config_request.env_vars
        )
        return {"message": f"Configuration updated for {agent_name}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Agent Launch/Control Endpoints
@app.post("/api/agents/{agent_name}/launch")
async def launch_agent(agent_name: str, launch_request: Optional[AgentLaunchRequest] = None):
    """Launch an agent"""
    if not launcher:
        raise HTTPException(status_code=500, detail="Launcher not initialized")
    
    if agent_name not in registry.agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    try:
        # Apply configuration if provided
        if launch_request and launch_request.config:
            config_manager.configure_agent(
                agent_name,
                model=launch_request.config.model,
                temperature=launch_request.config.temperature,
                max_tokens=launch_request.config.max_tokens,
                timeout=launch_request.config.timeout,
                **launch_request.config.env_vars
            )
        
        success = launcher.launch_agent(agent_name)
        if success:
            return {"message": f"Agent {agent_name} launched successfully", "status": "running"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to launch agent {agent_name}")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/agents/{agent_name}/stop")
async def stop_agent(agent_name: str):
    """Stop an agent"""
    if not launcher:
        raise HTTPException(status_code=500, detail="Launcher not initialized")
    
    try:
        success = launcher.stop_agent(agent_name)
        if success:
            return {"message": f"Agent {agent_name} stopped successfully", "status": "stopped"}
        else:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} is not running")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/agents/{agent_name}/status", response_model=AgentStatusResponse)
async def get_agent_status(agent_name: str):
    """Get agent status"""
    if not launcher or not status_monitor:
        raise HTTPException(status_code=500, detail="Status monitor not initialized")
    
    # Check if agent is running
    is_running = agent_name in launcher.running_agents
    status = "running" if is_running else "stopped"
    
    response = AgentStatusResponse(
        agent_name=agent_name,
        status=status
    )
    
    # Add metrics if available
    if agent_name in status_monitor.agent_metrics:
        metrics = status_monitor.agent_metrics[agent_name]
        response.uptime_seconds = metrics.uptime_seconds
        response.cpu_percent = metrics.cpu_percent
        response.memory_mb = metrics.memory_mb
        response.requests_count = metrics.requests_count
        response.errors_count = metrics.errors_count
        response.last_activity = metrics.last_activity
    
    return response

@app.get("/api/agents/status")
async def get_all_agent_status():
    """Get status of all agents"""
    if not launcher:
        raise HTTPException(status_code=500, detail="Launcher not initialized")
    
    statuses = {}
    for agent_name in registry.agents.keys():
        is_running = agent_name in launcher.running_agents
        statuses[agent_name] = {
            "status": "running" if is_running else "stopped",
            "uptime": None,
            "metrics": None
        }
        
        # Add metrics if available
        if status_monitor and agent_name in status_monitor.agent_metrics:
            metrics = status_monitor.agent_metrics[agent_name]
            statuses[agent_name].update({
                "uptime": metrics.uptime_seconds,
                "metrics": {
                    "cpu_percent": metrics.cpu_percent,
                    "memory_mb": metrics.memory_mb,
                    "requests_count": metrics.requests_count,
                    "errors_count": metrics.errors_count,
                    "last_activity": metrics.last_activity
                }
            })
    
    return statuses

# Agent Combinations Endpoints
@app.get("/api/combinations")
async def get_combinations():
    """Get all agent combinations"""
    if not combination_engine:
        raise HTTPException(status_code=500, detail="Combination engine not initialized")
    
    combinations = []
    for combo in registry.combinations.values():
        combinations.append({
            "name": combo.name,
            "agents": combo.agents,
            "workflow": combo.workflow,
            "description": combo.description,
            "created": combo.created
        })
    
    return combinations

@app.post("/api/combinations")
async def create_combination(combination_request: CombinationRequest):
    """Create a new agent combination"""
    if not combination_engine:
        raise HTTPException(status_code=500, detail="Combination engine not initialized")
    
    try:
        # Create basic workflow structure
        workflow = {
            "type": combination_request.workflow_type,
            "steps": [
                {
                    "step_id": f"step_{i}",
                    "agent_name": agent,
                    "action": "execute",
                    "description": f"Execute {agent}",
                    "inputs": {"query": "${input}" if i == 0 else f"${{step_{i-1}}}"},
                    "timeout": 300
                }
                for i, agent in enumerate(combination_request.agents)
            ]
        }
        
        combination_engine.create_combination(
            combination_request.name,
            combination_request.agents,
            workflow,
            description=combination_request.description
        )
        
        return {"message": f"Combination {combination_request.name} created successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/combinations/{combination_name}/execute")
async def execute_combination(combination_name: str, input_data: Dict[str, Any]):
    """Execute an agent combination"""
    if not combination_engine:
        raise HTTPException(status_code=500, detail="Combination engine not initialized")
    
    try:
        result = await combination_engine.execute_combination(combination_name, input_data)
        return {"result": result, "status": "completed"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Deployment Endpoints
@app.post("/api/deploy/local-ai")
async def deploy_local_ai(deployment_request: DeploymentRequest):
    """Deploy agents with local AI providers"""
    try:
        if deployment_request.provider == "ollama":
            # Configure agents to use Ollama
            config_update = {
                "model": deployment_request.model,
                "base_url": deployment_request.base_url or "http://localhost:11434",
                "provider": "ollama"
            }
        elif deployment_request.provider == "localai":
            # Configure agents to use LocalAI
            config_update = {
                "model": deployment_request.model,
                "base_url": deployment_request.base_url or "http://localhost:8080",
                "provider": "localai"
            }
        elif deployment_request.provider == "openrouter":
            # Configure agents to use OpenRouter
            config_update = {
                "model": deployment_request.model,
                "base_url": "https://openrouter.ai/api/v1",
                "provider": "openrouter",
                "api_key": deployment_request.api_key
            }
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {deployment_request.provider}")
        
        # Update global configuration
        config_manager.global_config.default_model = deployment_request.model
        config_manager.global_config.default_provider = deployment_request.provider
        
        # Save configuration
        config_manager.save_global_config()
        
        return {
            "message": f"Local AI deployment configured for {deployment_request.provider}",
            "provider": deployment_request.provider,
            "model": deployment_request.model,
            "base_url": config_update.get("base_url")
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/deploy/status")
async def get_deployment_status():
    """Get deployment status"""
    try:
        return {
            "global_config": {
                "default_model": config_manager.global_config.default_model,
                "default_provider": getattr(config_manager.global_config, 'default_provider', 'openai'),
                "configured_agents": len(config_manager.agent_configs),
                "api_keys_configured": len(config_manager._get_configured_api_keys())
            },
            "running_agents": len(launcher.running_agents) if launcher else 0,
            "available_agents": len(registry.agents) if registry else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the web API
    uvicorn.run(
        "web_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )