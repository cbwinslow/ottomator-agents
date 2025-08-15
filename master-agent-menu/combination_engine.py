"""
Combination Engine - Creates and manages agent combinations for hybrid functionality
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import uuid

from agent_registry import AgentRegistry, AgentInfo, AgentCombination
from config_manager import ConfigurationManager

logger = logging.getLogger(__name__)

@dataclass
class CombinationStep:
    """A step in an agent combination workflow"""
    step_id: str
    agent_name: str
    action: str
    inputs: Dict[str, Any]
    outputs: List[str]
    conditions: Dict[str, Any] = None
    timeout: int = 300
    retry_count: int = 3

@dataclass
class CombinationResult:
    """Result of executing an agent combination"""
    combination_name: str
    execution_id: str
    status: str  # success, failure, partial
    steps_completed: int
    total_steps: int
    results: Dict[str, Any]
    errors: List[str]
    execution_time: float
    timestamp: datetime

class CombinationEngine:
    """Engine for creating and executing agent combinations"""
    
    def __init__(self, registry: AgentRegistry, config_manager: ConfigurationManager):
        self.registry = registry
        self.config_manager = config_manager
        self.combinations_dir = Path(__file__).parent / "combinations"
        self.combinations_dir.mkdir(exist_ok=True)
        
        # Track running combinations
        self.running_combinations: Dict[str, Dict[str, Any]] = {}
        
        # Load existing combinations
        self._load_custom_combinations()
    
    def create_combination(self, name: str, agent_names: List[str], 
                          workflow: Dict[str, Any] = None, **kwargs) -> bool:
        """Create a new agent combination"""
        try:
            # Validate that all agents exist
            missing_agents = []
            for agent_name in agent_names:
                if not self.registry.get_agent(agent_name):
                    missing_agents.append(agent_name)
            
            if missing_agents:
                logger.error(f"Cannot create combination {name}: missing agents {missing_agents}")
                return False
            
            # Create default workflow if none provided
            if workflow is None:
                workflow = self._create_default_workflow(agent_names)
            
            # Create combination object
            combination = AgentCombination(
                name=name,
                description=kwargs.get("description", f"Combination of {', '.join(agent_names)}"),
                component_agents=agent_names,
                workflow=workflow,
                benefits=kwargs.get("benefits", []),
                use_cases=kwargs.get("use_cases", [])
            )
            
            # Save to registry
            self.registry.combinations[name] = combination
            
            # Save to file
            self._save_combination(combination)
            
            logger.info(f"Created combination: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create combination {name}: {e}")
            return False
    
    def _create_default_workflow(self, agent_names: List[str]) -> Dict[str, Any]:
        """Create a default sequential workflow for agents"""
        workflow = {
            "type": "sequential",
            "steps": []
        }
        
        for i, agent_name in enumerate(agent_names):
            agent_info = self.registry.get_agent(agent_name)
            
            step = {
                "step_id": f"step_{i+1}",
                "agent_name": agent_name,
                "action": "process",
                "description": f"Execute {agent_info.description[:50]}...",
                "inputs": {"query": "${input}" if i == 0 else "${previous_result}"},
                "outputs": ["result"],
                "timeout": 300
            }
            
            workflow["steps"].append(step)
        
        return workflow
    
    def launch_combination(self, combination_name: str, input_data: Any = None, **kwargs) -> str:
        """Launch an agent combination and return execution ID"""
        combination = self.registry.combinations.get(combination_name)
        if not combination:
            logger.error(f"Combination {combination_name} not found")
            return None
        
        execution_id = str(uuid.uuid4())
        
        # Start execution in background
        asyncio.create_task(self._execute_combination_async(
            combination, execution_id, input_data, **kwargs
        ))
        
        return execution_id
    
    async def _execute_combination_async(self, combination: AgentCombination, 
                                       execution_id: str, input_data: Any = None, **kwargs):
        """Execute a combination asynchronously"""
        start_time = datetime.now()
        
        # Initialize execution tracking
        execution_context = {
            "combination_name": combination.name,
            "execution_id": execution_id,
            "status": "running",
            "steps_completed": 0,
            "total_steps": len(combination.workflow.get("steps", [])),
            "results": {},
            "errors": [],
            "start_time": start_time,
            "current_step": None
        }
        
        self.running_combinations[execution_id] = execution_context
        
        try:
            result = await self._execute_workflow(combination.workflow, input_data, execution_context)
            
            execution_context["status"] = "completed"
            execution_context["final_result"] = result
            
        except Exception as e:
            logger.error(f"Error executing combination {combination.name}: {e}")
            execution_context["status"] = "failed"
            execution_context["errors"].append(str(e))
        
        finally:
            execution_context["end_time"] = datetime.now()
            execution_context["execution_time"] = (execution_context["end_time"] - start_time).total_seconds()
            
            # Save execution log
            self._save_execution_log(execution_context)
    
    async def _execute_workflow(self, workflow: Dict[str, Any], input_data: Any, 
                              execution_context: Dict[str, Any]) -> Any:
        """Execute a workflow"""
        workflow_type = workflow.get("type", "sequential")
        steps = workflow.get("steps", [])
        
        if workflow_type == "sequential":
            return await self._execute_sequential_workflow(steps, input_data, execution_context)
        elif workflow_type == "parallel":
            return await self._execute_parallel_workflow(steps, input_data, execution_context)
        elif workflow_type == "conditional":
            return await self._execute_conditional_workflow(steps, input_data, execution_context)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
    
    async def _execute_sequential_workflow(self, steps: List[Dict[str, Any]], 
                                         input_data: Any, execution_context: Dict[str, Any]) -> Any:
        """Execute steps sequentially"""
        current_data = input_data
        
        for i, step in enumerate(steps):
            execution_context["current_step"] = step["step_id"]
            execution_context["steps_completed"] = i
            
            try:
                logger.info(f"Executing step {step['step_id']}: {step.get('description', '')}")
                
                # Process inputs
                step_inputs = self._process_step_inputs(step.get("inputs", {}), current_data, execution_context)
                
                # Execute step
                step_result = await self._execute_step(step, step_inputs, execution_context)
                
                # Store result
                execution_context["results"][step["step_id"]] = step_result
                current_data = step_result
                
                logger.info(f"Completed step {step['step_id']}")
                
            except Exception as e:
                error_msg = f"Error in step {step['step_id']}: {str(e)}"
                logger.error(error_msg)
                execution_context["errors"].append(error_msg)
                raise
        
        execution_context["steps_completed"] = len(steps)
        return current_data
    
    async def _execute_parallel_workflow(self, steps: List[Dict[str, Any]], 
                                       input_data: Any, execution_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute steps in parallel"""
        tasks = []
        
        for step in steps:
            step_inputs = self._process_step_inputs(step.get("inputs", {}), input_data, execution_context)
            task = asyncio.create_task(self._execute_step(step, step_inputs, execution_context))
            tasks.append((step["step_id"], task))
        
        results = {}
        completed = 0
        
        for step_id, task in tasks:
            try:
                result = await task
                results[step_id] = result
                completed += 1
                execution_context["steps_completed"] = completed
                logger.info(f"Completed parallel step {step_id}")
            except Exception as e:
                error_msg = f"Error in parallel step {step_id}: {str(e)}"
                logger.error(error_msg)
                execution_context["errors"].append(error_msg)
                results[step_id] = {"error": str(e)}
        
        return results
    
    async def _execute_conditional_workflow(self, steps: List[Dict[str, Any]], 
                                          input_data: Any, execution_context: Dict[str, Any]) -> Any:
        """Execute steps with conditional logic"""
        current_data = input_data
        
        for step in steps:
            # Check conditions
            conditions = step.get("conditions", {})
            if not self._evaluate_conditions(conditions, current_data, execution_context):
                logger.info(f"Skipping step {step['step_id']} due to conditions")
                continue
            
            execution_context["current_step"] = step["step_id"]
            
            try:
                step_inputs = self._process_step_inputs(step.get("inputs", {}), current_data, execution_context)
                step_result = await self._execute_step(step, step_inputs, execution_context)
                
                execution_context["results"][step["step_id"]] = step_result
                current_data = step_result
                execution_context["steps_completed"] += 1
                
            except Exception as e:
                error_msg = f"Error in conditional step {step['step_id']}: {str(e)}"
                logger.error(error_msg)
                execution_context["errors"].append(error_msg)
                
                # Check if we should continue on error
                if not step.get("continue_on_error", False):
                    raise
        
        return current_data
    
    def _process_step_inputs(self, inputs: Dict[str, Any], current_data: Any, 
                           execution_context: Dict[str, Any]) -> Dict[str, Any]:
        """Process step inputs, resolving variables"""
        processed_inputs = {}
        
        for key, value in inputs.items():
            if isinstance(value, str):
                # Replace variables
                if value == "${input}":
                    processed_inputs[key] = current_data
                elif value == "${previous_result}":
                    processed_inputs[key] = current_data
                elif value.startswith("${") and value.endswith("}"):
                    # Extract variable name
                    var_name = value[2:-1]
                    if var_name in execution_context["results"]:
                        processed_inputs[key] = execution_context["results"][var_name]
                    else:
                        processed_inputs[key] = value  # Keep as is if not found
                else:
                    processed_inputs[key] = value
            else:
                processed_inputs[key] = value
        
        return processed_inputs
    
    def _evaluate_conditions(self, conditions: Dict[str, Any], current_data: Any, 
                           execution_context: Dict[str, Any]) -> bool:
        """Evaluate step conditions"""
        if not conditions:
            return True
        
        # Simple condition evaluation
        for condition_type, condition_value in conditions.items():
            if condition_type == "has_data":
                if not current_data:
                    return False
            elif condition_type == "data_contains":
                if isinstance(current_data, str) and condition_value not in current_data:
                    return False
            elif condition_type == "previous_step_success":
                if execution_context["errors"]:
                    return False
            # Add more condition types as needed
        
        return True
    
    async def _execute_step(self, step: Dict[str, Any], inputs: Dict[str, Any], 
                          execution_context: Dict[str, Any]) -> Any:
        """Execute a single step"""
        agent_name = step["agent_name"]
        action = step.get("action", "process")
        timeout = step.get("timeout", 300)
        
        # For now, simulate agent execution
        # In a real implementation, this would call the actual agent
        logger.info(f"Simulating execution of {agent_name} with action {action}")
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Create mock result based on agent category
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            raise ValueError(f"Agent {agent_name} not found")
        
        mock_result = self._create_mock_result(agent_info, action, inputs)
        
        return mock_result
    
    def _create_mock_result(self, agent_info: AgentInfo, action: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Create a mock result for testing purposes"""
        category = agent_info.category
        
        base_result = {
            "agent": agent_info.name,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        if category == "research":
            base_result["data"] = {
                "sources": ["source1.com", "source2.com", "source3.com"],
                "summary": f"Research results for: {inputs.get('query', 'unknown query')}",
                "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
                "confidence": 0.85
            }
        elif category == "content":
            base_result["data"] = {
                "content": f"Generated content based on: {inputs.get('query', 'input data')}",
                "format": "markdown",
                "word_count": 500,
                "readability_score": 8.5
            }
        elif category == "business":
            base_result["data"] = {
                "analysis": f"Business analysis for: {inputs.get('query', 'business domain')}",
                "recommendations": ["Recommendation 1", "Recommendation 2"],
                "metrics": {"roi": 15.5, "market_size": "1.2B"},
                "risk_level": "medium"
            }
        else:
            base_result["data"] = {
                "result": f"Processed: {inputs.get('query', 'input data')}",
                "details": f"Executed {action} action on {agent_info.name}"
            }
        
        return base_result
    
    def get_combination_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a running combination"""
        return self.running_combinations.get(execution_id)
    
    def stop_combination(self, execution_id: str) -> bool:
        """Stop a running combination"""
        if execution_id in self.running_combinations:
            execution_context = self.running_combinations[execution_id]
            execution_context["status"] = "stopped"
            execution_context["end_time"] = datetime.now()
            
            # Save execution log
            self._save_execution_log(execution_context)
            
            del self.running_combinations[execution_id]
            return True
        
        return False
    
    def list_running_combinations(self) -> List[Dict[str, Any]]:
        """List all running combinations"""
        return [
            {
                "execution_id": exec_id,
                "combination_name": context["combination_name"],
                "status": context["status"],
                "steps_completed": context["steps_completed"],
                "total_steps": context["total_steps"],
                "start_time": context["start_time"].isoformat(),
                "current_step": context.get("current_step")
            }
            for exec_id, context in self.running_combinations.items()
        ]
    
    def create_predefined_combinations(self):
        """Create some predefined useful combinations"""
        combinations = [
            {
                "name": "content-research-pipeline",
                "agents": ["advanced-web-researcher", "foundational-rag-agent", "linkedin-x-blog-content-creator"],
                "description": "Research topic, gather knowledge, and create content",
                "workflow": {
                    "type": "sequential",
                    "steps": [
                        {
                            "step_id": "research",
                            "agent_name": "advanced-web-researcher",
                            "action": "search",
                            "description": "Research the topic on the web",
                            "inputs": {"query": "${input}"},
                            "timeout": 300
                        },
                        {
                            "step_id": "knowledge",
                            "agent_name": "foundational-rag-agent",
                            "action": "retrieve",
                            "description": "Retrieve relevant knowledge",
                            "inputs": {"query": "${input}", "web_results": "${research}"},
                            "timeout": 200
                        },
                        {
                            "step_id": "content",
                            "agent_name": "linkedin-x-blog-content-creator",
                            "action": "create",
                            "description": "Create professional content",
                            "inputs": {"topic": "${input}", "research": "${research}", "knowledge": "${knowledge}"},
                            "timeout": 400
                        }
                    ]
                }
            },
            {
                "name": "social-media-analyzer",
                "agents": ["ask-reddit-agent", "youtube-summary-agent", "tweet-generator-agent"],
                "description": "Analyze social media trends and create content",
                "workflow": {
                    "type": "parallel",
                    "steps": [
                        {
                            "step_id": "reddit_analysis",
                            "agent_name": "ask-reddit-agent",
                            "action": "analyze",
                            "description": "Analyze Reddit discussions",
                            "inputs": {"query": "${input}"},
                            "timeout": 300
                        },
                        {
                            "step_id": "youtube_analysis",
                            "agent_name": "youtube-summary-agent",
                            "action": "analyze",
                            "description": "Analyze YouTube content",
                            "inputs": {"query": "${input}"},
                            "timeout": 300
                        }
                    ]
                }
            },
            {
                "name": "business-intelligence-suite",
                "agents": ["small-business-researcher", "advanced-web-researcher", "genericsuite-app-maker-agent"],
                "description": "Comprehensive business research and analysis",
                "workflow": {
                    "type": "sequential",
                    "steps": [
                        {
                            "step_id": "market_research",
                            "agent_name": "small-business-researcher",
                            "action": "research",
                            "description": "Research business market",
                            "inputs": {"domain": "${input}"},
                            "timeout": 400
                        },
                        {
                            "step_id": "competitive_analysis",
                            "agent_name": "advanced-web-researcher",
                            "action": "search",
                            "description": "Analyze competitors",
                            "inputs": {"query": "${input} competitors analysis"},
                            "timeout": 300
                        },
                        {
                            "step_id": "business_plan",
                            "agent_name": "genericsuite-app-maker-agent",
                            "action": "generate",
                            "description": "Generate business documentation",
                            "inputs": {"market_data": "${market_research}", "competitive_data": "${competitive_analysis}"},
                            "timeout": 500
                        }
                    ]
                }
            }
        ]
        
        for combo_def in combinations:
            self.create_combination(
                combo_def["name"],
                combo_def["agents"],
                combo_def["workflow"],
                description=combo_def["description"]
            )
    
    def _save_combination(self, combination: AgentCombination):
        """Save combination to file"""
        filepath = self.combinations_dir / f"{combination.name}.json"
        with open(filepath, 'w') as f:
            json.dump(asdict(combination), f, indent=2, default=str)
    
    def _load_custom_combinations(self):
        """Load custom combinations from files"""
        for combo_file in self.combinations_dir.glob("*.json"):
            try:
                with open(combo_file, 'r') as f:
                    data = json.load(f)
                
                combination = AgentCombination(**data)
                self.registry.combinations[combination.name] = combination
                
            except Exception as e:
                logger.error(f"Error loading combination from {combo_file}: {e}")
    
    def _save_execution_log(self, execution_context: Dict[str, Any]):
        """Save execution log for analysis"""
        logs_dir = self.combinations_dir / "execution_logs"
        logs_dir.mkdir(exist_ok=True)
        
        log_file = logs_dir / f"{execution_context['execution_id']}.json"
        
        # Prepare log data (convert datetime objects)
        log_data = execution_context.copy()
        for key, value in log_data.items():
            if isinstance(value, datetime):
                log_data[key] = value.isoformat()
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2, default=str)

if __name__ == "__main__":
    # Test the combination engine
    from agent_registry import AgentRegistry
    from config_manager import ConfigurationManager
    
    registry = AgentRegistry()
    registry.discover_agents()
    
    config_manager = ConfigurationManager()
    engine = CombinationEngine(registry, config_manager)
    
    # Create predefined combinations
    engine.create_predefined_combinations()
    
    print(f"Created {len(registry.combinations)} combinations:")
    for name, combo in registry.combinations.items():
        print(f"- {name}: {combo.description}")
        print(f"  Components: {', '.join(combo.component_agents)}")
        print()