# 🚀 Ottomator Agents Web Interface

A comprehensive web-based management system for the Ottomator Agents ecosystem. This Next.js application provides a modern, intuitive interface to deploy, configure, monitor, and orchestrate AI agents with support for local AI models.

## ✨ Features

### 🎛️ **Agent Management**
- **Discover & Launch**: Automatically discover and launch 55+ AI agents
- **Real-time Monitoring**: Live status, performance metrics, and health monitoring
- **Configuration Management**: Easy-to-use forms for agent configuration
- **Batch Operations**: Start/stop multiple agents simultaneously

### 🔧 **Multi-Agent Orchestration**
- **Combination Builder**: Create custom multi-agent workflows
- **Sequential & Parallel Execution**: Flexible workflow patterns
- **Visual Workflow Designer**: Drag-and-drop interface for complex orchestrations
- **Template Library**: Pre-built combinations for common use cases

### 🏠 **Local AI Deployment**
- **Ollama Integration**: Full support for local Ollama models
- **LocalAI Support**: OpenAI-compatible local server integration
- **OpenRouter Integration**: Access to cloud-based models
- **Model Management**: Download, configure, and switch between models

### 📊 **Analytics & Monitoring**
- **System Overview**: Real-time dashboard with key metrics
- **Performance Analytics**: CPU, memory, and request tracking
- **Agent Health**: Status monitoring and error reporting
- **Usage Statistics**: Detailed insights into agent utilization

### 🎨 **Modern UI/UX**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Mode**: Automatic theme switching
- **Real-time Updates**: Live data refresh every 30 seconds
- **Intuitive Navigation**: Clean, organized interface

## 🛠️ Technology Stack

- **Frontend**: Next.js 15, React 18, TypeScript
- **Styling**: Tailwind CSS, Lucide Icons
- **Backend**: FastAPI (Python), REST API
- **State Management**: React Hooks
- **Build Tool**: Turbopack (Next.js)
- **Agent Management**: Python-based orchestrator

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Git

### 1. Installation

Clone the repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/cbwinslow/ottomator-agents.git
cd ottomator-agents

# Run the automated deployment script
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 2. Manual Setup (Alternative)

If the automated script doesn't work in your environment:

```bash
# Install web interface dependencies
cd web-interface
npm install
npm run build

# Install Python dependencies
cd ../master-agent-menu
pip install --user fastapi uvicorn rich pydantic psutil python-dotenv pyyaml

# Create environment file
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Services

```bash
# Terminal 1: Start the Python API
cd master-agent-menu
python web_api.py

# Terminal 2: Start the web interface
cd web-interface
npm run dev
```

### 4. Access the Interface

Open your browser and navigate to:
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

## 📱 Interface Overview

### Dashboard
- System overview with key metrics
- Running agents status
- Resource utilization charts
- Quick action buttons

### Agents Page
- Grid view of all discovered agents
- Filter by category and search
- Individual agent controls (start/stop/configure)
- Real-time status indicators

### Combinations Page
- Create multi-agent workflows
- Execute predefined combinations
- Monitor combination status
- Workflow templates

### Deployment Page
- Configure local AI providers
- Model management
- Provider selection (Ollama/LocalAI/OpenRouter)
- Connection testing

### Monitoring Page
- Real-time performance metrics
- Agent health monitoring
- System resource usage
- Historical data (coming soon)

### Settings Page
- Global configuration
- API key management
- Theme preferences
- System preferences

## 🤖 Local AI Setup

### Using Ollama (Recommended)

1. **Install Ollama**:
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Start Ollama Service**:
   ```bash
   ollama serve
   ```

3. **Pull Models**:
   ```bash
   ollama pull llama3.2
   ollama pull codellama
   ollama pull mistral
   ```

4. **Configure in Web Interface**:
   - Go to Deployment → Ollama
   - Set Base URL: `http://localhost:11434`
   - Select your model
   - Click "Deploy Configuration"

### Using LocalAI

1. **Download LocalAI**:
   ```bash
   wget https://github.com/go-skynet/LocalAI/releases/download/v2.20.1/local-ai-Linux-x86_64
   chmod +x local-ai-Linux-x86_64
   ```

2. **Create Models Directory**:
   ```bash
   mkdir models
   # Download your models to this directory
   ```

3. **Start LocalAI**:
   ```bash
   ./local-ai-Linux-x86_64 --models-path ./models
   ```

4. **Configure in Web Interface**:
   - Go to Deployment → LocalAI
   - Set Base URL: `http://localhost:8080`
   - Configure your models

### Using OpenRouter

1. **Sign up** at [openrouter.ai](https://openrouter.ai)
2. **Get your API key** from the dashboard
3. **Configure in Web Interface**:
   - Go to Deployment → OpenRouter
   - Enter your API key
   - Select models like `openai/gpt-4o` or `anthropic/claude-3.5-sonnet`

## 🔧 Agent Scripts

Individual launch scripts are generated for each agent:

```bash
# Launch specific agents
./scripts/agents/launch_ask-reddit-agent.sh
./scripts/agents/launch_foundational-rag-agent.sh

# Launch all agents
./scripts/agents/launch_all_agents.sh

# Stop all agents
./scripts/agents/stop_all_agents.sh
```

## 🎯 Multi-Agent Combinations

Create powerful workflows by combining agents:

### Example: Content Research Pipeline
1. **Research Agent** → Gather information
2. **RAG Agent** → Process knowledge
3. **Content Agent** → Generate content

### Example: Business Analysis Workflow
1. **Web Scraper** → Collect data
2. **Analysis Agent** → Process insights
3. **Report Generator** → Create deliverables

## 📚 API Reference

### REST API Endpoints

- `GET /api/agents` - List all agents
- `POST /api/agents/{name}/launch` - Launch an agent
- `POST /api/agents/{name}/stop` - Stop an agent
- `GET /api/agents/{name}/status` - Get agent status
- `POST /api/combinations` - Create agent combination
- `POST /api/deploy/local-ai` - Deploy local AI configuration

Full API documentation available at: http://localhost:8000/docs

## 🔒 Environment Variables

Create a `.env` file in the `master-agent-menu` directory:

```env
# API Keys (Optional - for cloud models)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Local AI Configuration
OLLAMA_BASE_URL=http://localhost:11434
LOCALAI_BASE_URL=http://localhost:8080

# Default Configuration
DEFAULT_MODEL=llama3.2
DEFAULT_PROVIDER=ollama

# Server Configuration
WEB_API_PORT=8000
WEB_INTERFACE_PORT=3000
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Kill processes on ports 3000 and 8000
   killall -9 node
   pkill -f "python.*web_api"
   ```

2. **Module not found errors**:
   ```bash
   # Reinstall dependencies
   cd web-interface && npm install
   cd ../master-agent-menu && pip install --user -r requirements.txt
   ```

3. **Ollama connection failed**:
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434
   
   # Restart Ollama
   ollama serve
   ```

4. **Web interface not loading**:
   ```bash
   # Clear Next.js cache
   cd web-interface
   rm -rf .next
   npm run build
   npm run dev
   ```

### Logs and Debugging

- **Web API logs**: Check terminal output or `master-agent-menu/web_api.log`
- **Web interface logs**: Check browser console or terminal output
- **Agent logs**: Individual agent logs in respective directories

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📖 Documentation

- [Master Agent Menu Documentation](../master-agent-menu/docs/)
- [API Reference](http://localhost:8000/docs)
- [Agent Development Guide](../master-agent-menu/docs/development.md)

## 🛣️ Roadmap

### Phase 1 (Current)
- [x] Web interface with agent management
- [x] Local AI provider integration
- [x] Multi-agent combinations
- [x] Real-time monitoring

### Phase 2 (In Progress)
- [ ] Visual workflow designer
- [ ] Advanced analytics dashboard
- [ ] Agent marketplace
- [ ] Plugin system

### Phase 3 (Planned)
- [ ] Cloud deployment options
- [ ] Enterprise features
- [ ] Advanced security
- [ ] Multi-tenant support

## 📄 License

MIT License - see [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- Built on the comprehensive [Master Agent Menu System](../master-agent-menu/)
- Powered by the 55+ agents in the Ottomator ecosystem
- Uses modern web technologies for optimal performance

---

**Ready to orchestrate your AI agents?** 🚀

Start with `./scripts/deploy.sh` and visit http://localhost:3000!
