"""
Status Monitor - Monitors agent health, performance, and status
"""

import time
import threading
import subprocess
import psutil
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import queue

logger = logging.getLogger(__name__)

@dataclass
class AgentMetrics:
    """Metrics for an agent"""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    uptime_seconds: int = 0
    requests_count: int = 0
    errors_count: int = 0
    last_activity: Optional[datetime] = None
    response_time_avg: float = 0.0
    status: str = "unknown"

class StatusMonitor:
    """Monitors status and performance of running agents"""
    
    def __init__(self, update_interval: int = 30):
        self.update_interval = update_interval
        self.monitoring_threads: Dict[str, threading.Thread] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.stop_events: Dict[str, threading.Event] = {}
        self.process_info: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        
        # Start global monitor thread
        self.global_stop_event = threading.Event()
        self.global_monitor_thread = threading.Thread(target=self._global_monitor_loop, daemon=True)
        self.global_monitor_thread.start()
    
    def start_monitoring(self, agent_name: str, process: subprocess.Popen) -> None:
        """Start monitoring an agent process"""
        with self._lock:
            if agent_name in self.monitoring_threads:
                logger.warning(f"Already monitoring agent {agent_name}")
                return
            
            # Store process info
            self.process_info[agent_name] = {
                "process": process,
                "pid": process.pid,
                "start_time": datetime.now()
            }
            
            # Initialize metrics
            self.agent_metrics[agent_name] = AgentMetrics(
                last_activity=datetime.now(),
                status="starting"
            )
            
            # Create stop event
            stop_event = threading.Event()
            self.stop_events[agent_name] = stop_event
            
            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=self._monitor_agent,
                args=(agent_name, stop_event),
                daemon=True
            )
            monitor_thread.start()
            self.monitoring_threads[agent_name] = monitor_thread
            
            logger.info(f"Started monitoring agent {agent_name} (PID: {process.pid})")
    
    def stop_monitoring(self, agent_name: str) -> None:
        """Stop monitoring an agent"""
        with self._lock:
            if agent_name in self.stop_events:
                self.stop_events[agent_name].set()
                del self.stop_events[agent_name]
            
            if agent_name in self.monitoring_threads:
                thread = self.monitoring_threads[agent_name]
                del self.monitoring_threads[agent_name]
                # Thread will stop naturally due to stop event
            
            if agent_name in self.process_info:
                del self.process_info[agent_name]
            
            if agent_name in self.agent_metrics:
                self.agent_metrics[agent_name].status = "stopped"
            
            logger.info(f"Stopped monitoring agent {agent_name}")
    
    def _monitor_agent(self, agent_name: str, stop_event: threading.Event) -> None:
        """Monitor loop for a specific agent"""
        try:
            while not stop_event.wait(self.update_interval):
                self._update_agent_metrics(agent_name)
        except Exception as e:
            logger.error(f"Error in monitoring thread for {agent_name}: {e}")
        finally:
            logger.debug(f"Monitoring thread for {agent_name} stopped")
    
    def _update_agent_metrics(self, agent_name: str) -> None:
        """Update metrics for a specific agent"""
        try:
            process_info = self.process_info.get(agent_name)
            if not process_info:
                return
            
            process = process_info["process"]
            start_time = process_info["start_time"]
            
            # Check if process is still running
            if process.poll() is not None:
                self.agent_metrics[agent_name].status = "stopped"
                return
            
            # Get process using psutil for detailed metrics
            try:
                ps_process = psutil.Process(process.pid)
                
                # Update metrics
                metrics = self.agent_metrics[agent_name]
                metrics.cpu_percent = ps_process.cpu_percent()
                metrics.memory_mb = ps_process.memory_info().rss / 1024 / 1024
                metrics.uptime_seconds = int((datetime.now() - start_time).total_seconds())
                metrics.last_activity = datetime.now()
                
                # Determine status based on resource usage
                if metrics.cpu_percent > 90 or metrics.memory_mb > 1000:
                    metrics.status = "high_load"
                elif metrics.cpu_percent < 1 and metrics.uptime_seconds > 300:
                    metrics.status = "idle"
                else:
                    metrics.status = "running"
                
            except psutil.NoSuchProcess:
                self.agent_metrics[agent_name].status = "stopped"
            except psutil.AccessDenied:
                # Limited access, just mark as running
                self.agent_metrics[agent_name].status = "running"
                self.agent_metrics[agent_name].last_activity = datetime.now()
                
        except Exception as e:
            logger.error(f"Error updating metrics for {agent_name}: {e}")
            self.agent_metrics[agent_name].status = "error"
    
    def _global_monitor_loop(self) -> None:
        """Global monitoring loop for system-wide checks"""
        while not self.global_stop_event.wait(60):  # Check every minute
            try:
                self._cleanup_dead_processes()
                self._update_system_metrics()
            except Exception as e:
                logger.error(f"Error in global monitor loop: {e}")
    
    def _cleanup_dead_processes(self) -> None:
        """Clean up monitoring for dead processes"""
        dead_agents = []
        
        with self._lock:
            for agent_name, process_info in self.process_info.items():
                process = process_info["process"]
                if process.poll() is not None:
                    dead_agents.append(agent_name)
        
        for agent_name in dead_agents:
            logger.info(f"Cleaning up dead process for agent {agent_name}")
            self.stop_monitoring(agent_name)
    
    def _update_system_metrics(self) -> None:
        """Update system-wide metrics"""
        try:
            # Check system resources
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Log warnings for high resource usage
            if cpu_percent > 80:
                logger.warning(f"High system CPU usage: {cpu_percent}%")
            
            if memory.percent > 80:
                logger.warning(f"High system memory usage: {memory.percent}%")
            
            if disk.percent > 90:
                logger.warning(f"High disk usage: {disk.percent}%")
            
        except Exception as e:
            logger.error(f"Error updating system metrics: {e}")
    
    def get_agent_metrics(self, agent_name: str) -> Dict[str, Any]:
        """Get metrics for a specific agent"""
        metrics = self.agent_metrics.get(agent_name)
        if not metrics:
            return {"error": "Agent not found or not monitored"}
        
        return {
            "cpu_percent": metrics.cpu_percent,
            "memory_mb": round(metrics.memory_mb, 2),
            "uptime_seconds": metrics.uptime_seconds,
            "uptime_formatted": str(timedelta(seconds=metrics.uptime_seconds)),
            "requests_count": metrics.requests_count,
            "errors_count": metrics.errors_count,
            "last_activity": metrics.last_activity.isoformat() if metrics.last_activity else None,
            "response_time_avg": metrics.response_time_avg,
            "status": metrics.status
        }
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics for all monitored agents"""
        return {
            agent_name: self.get_agent_metrics(agent_name)
            for agent_name in self.agent_metrics.keys()
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system-wide metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / 1024 / 1024 / 1024, 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
                "active_agents": len(self.monitoring_threads),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {"error": str(e)}
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get overall health summary"""
        system_metrics = self.get_system_metrics()
        agent_statuses = {}
        
        for agent_name, metrics in self.agent_metrics.items():
            agent_statuses[agent_name] = metrics.status
        
        # Determine overall health
        health_status = "healthy"
        issues = []
        
        if "error" in system_metrics:
            health_status = "error"
            issues.append("System metrics unavailable")
        else:
            if system_metrics["cpu_percent"] > 80:
                health_status = "warning"
                issues.append(f"High CPU usage: {system_metrics['cpu_percent']}%")
            
            if system_metrics["memory_percent"] > 80:
                health_status = "warning"
                issues.append(f"High memory usage: {system_metrics['memory_percent']}%")
            
            if system_metrics["disk_percent"] > 90:
                health_status = "critical"
                issues.append(f"High disk usage: {system_metrics['disk_percent']}%")
        
        # Check agent statuses
        error_agents = [name for name, status in agent_statuses.items() if status == "error"]
        if error_agents:
            health_status = "critical"
            issues.append(f"Agents with errors: {', '.join(error_agents)}")
        
        high_load_agents = [name for name, status in agent_statuses.items() if status == "high_load"]
        if high_load_agents:
            if health_status == "healthy":
                health_status = "warning"
            issues.append(f"Agents with high load: {', '.join(high_load_agents)}")
        
        return {
            "overall_status": health_status,
            "issues": issues,
            "system_metrics": system_metrics,
            "agent_statuses": agent_statuses,
            "total_agents": len(agent_statuses),
            "healthy_agents": len([s for s in agent_statuses.values() if s == "running"]),
            "timestamp": datetime.now().isoformat()
        }
    
    def set_agent_request_count(self, agent_name: str, count: int) -> None:
        """Set request count for an agent (called by agent implementations)"""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].requests_count = count
    
    def increment_agent_errors(self, agent_name: str) -> None:
        """Increment error count for an agent"""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].errors_count += 1
    
    def set_agent_response_time(self, agent_name: str, response_time: float) -> None:
        """Set average response time for an agent"""
        if agent_name in self.agent_metrics:
            current_avg = self.agent_metrics[agent_name].response_time_avg
            if current_avg == 0:
                self.agent_metrics[agent_name].response_time_avg = response_time
            else:
                # Simple moving average
                self.agent_metrics[agent_name].response_time_avg = (current_avg + response_time) / 2
    
    def get_performance_report(self, agent_name: str = None, hours: int = 24) -> Dict[str, Any]:
        """Get a performance report for an agent or all agents"""
        if agent_name:
            metrics = self.get_agent_metrics(agent_name)
            if "error" in metrics:
                return metrics
            
            return {
                "agent": agent_name,
                "current_metrics": metrics,
                "performance_summary": {
                    "avg_cpu": metrics["cpu_percent"],
                    "avg_memory": metrics["memory_mb"],
                    "total_uptime": metrics["uptime_formatted"],
                    "total_requests": metrics["requests_count"],
                    "error_rate": metrics["errors_count"] / max(metrics["requests_count"], 1) * 100,
                    "avg_response_time": metrics["response_time_avg"]
                }
            }
        else:
            all_metrics = self.get_all_metrics()
            total_requests = sum(m.get("requests_count", 0) for m in all_metrics.values())
            total_errors = sum(m.get("errors_count", 0) for m in all_metrics.values())
            
            return {
                "overall_performance": {
                    "total_agents": len(all_metrics),
                    "total_requests": total_requests,
                    "overall_error_rate": total_errors / max(total_requests, 1) * 100,
                    "avg_cpu_across_agents": sum(m.get("cpu_percent", 0) for m in all_metrics.values()) / max(len(all_metrics), 1),
                    "total_memory_mb": sum(m.get("memory_mb", 0) for m in all_metrics.values())
                },
                "agent_metrics": all_metrics,
                "system_metrics": self.get_system_metrics()
            }
    
    def cleanup(self) -> None:
        """Cleanup monitoring resources"""
        logger.info("Cleaning up status monitor...")
        
        # Stop global monitor
        self.global_stop_event.set()
        if self.global_monitor_thread.is_alive():
            self.global_monitor_thread.join(timeout=5)
        
        # Stop all agent monitoring
        agent_names = list(self.monitoring_threads.keys())
        for agent_name in agent_names:
            self.stop_monitoring(agent_name)
        
        # Wait for threads to finish
        for thread in list(self.monitoring_threads.values()):
            if thread.is_alive():
                thread.join(timeout=5)
        
        logger.info("Status monitor cleanup completed")

if __name__ == "__main__":
    # Test the status monitor
    import time
    
    monitor = StatusMonitor(update_interval=5)
    
    # Simulate monitoring a process
    import subprocess
    process = subprocess.Popen(["python", "-c", "import time; time.sleep(30)"])
    
    monitor.start_monitoring("test-agent", process)
    
    # Monitor for a bit
    for i in range(3):
        time.sleep(2)
        metrics = monitor.get_agent_metrics("test-agent")
        print(f"Test agent metrics: {metrics}")
    
    # Get health summary
    health = monitor.get_health_summary()
    print(f"Health summary: {health}")
    
    # Cleanup
    process.terminate()
    monitor.stop_monitoring("test-agent")
    monitor.cleanup()