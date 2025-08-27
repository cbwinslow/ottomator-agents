#!/bin/bash

# Master deployment script for Ottomator Agents
# This script sets up the entire agent ecosystem with local AI providers

set -e

echo "🚀 Ottomator Agents Master Deployment Script"
echo "=============================================="

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="$(dirname "$SCRIPT_DIR")"
WEB_INTERFACE_DIR="$AGENTS_DIR/web-interface"
MASTER_MENU_DIR="$AGENTS_DIR/master-agent-menu"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is open
port_open() {
    nc -z localhost "$1" 2>/dev/null
}

# Function to wait for service to be ready
wait_for_service() {
    local url="$1"
    local service_name="$2"
    local max_attempts=30
    local attempt=1
    
    log_info "Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            log_success "$service_name is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    log_error "$service_name failed to start within timeout"
    return 1
}

# Function to install Ollama
install_ollama() {
    log_info "Installing Ollama..."
    
    if command_exists ollama; then
        log_success "Ollama is already installed"
        return 0
    fi
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command_exists brew; then
            brew install ollama
        else
            log_error "Please install Homebrew first or download Ollama manually"
            return 1
        fi
    else
        log_error "Unsupported OS. Please install Ollama manually from https://ollama.ai"
        return 1
    fi
    
    log_success "Ollama installed successfully"
}

# Function to start Ollama
start_ollama() {
    log_info "Starting Ollama service..."
    
    if port_open 11434; then
        log_success "Ollama is already running"
        return 0
    fi
    
    # Start Ollama in background
    if [[ "$OSTYPE" == "darwin"* ]]; then
        ollama serve &
    else
        systemctl start ollama || (ollama serve &)
    fi
    
    # Wait for Ollama to be ready
    wait_for_service "http://localhost:11434" "Ollama"
}

# Function to pull Ollama models
pull_ollama_models() {
    log_info "Pulling Ollama models..."
    
    local models=("llama3.2" "llama3.2:1b" "codellama" "mistral")
    
    for model in "${models[@]}"; do
        log_info "Pulling model: $model"
        if ollama pull "$model"; then
            log_success "Successfully pulled $model"
        else
            log_warning "Failed to pull $model, continuing..."
        fi
    done
}

# Function to install Node.js dependencies
install_web_dependencies() {
    log_info "Installing web interface dependencies..."
    
    if [ ! -d "$WEB_INTERFACE_DIR" ]; then
        log_error "Web interface directory not found: $WEB_INTERFACE_DIR"
        return 1
    fi
    
    cd "$WEB_INTERFACE_DIR"
    
    if [ ! -f "package.json" ]; then
        log_error "package.json not found in web interface directory"
        return 1
    fi
    
    npm install
    log_success "Web interface dependencies installed"
}

# Function to install Python dependencies
install_python_dependencies() {
    log_info "Installing Python dependencies..."
    
    cd "$MASTER_MENU_DIR"
    
    # Install dependencies directly (skip venv for sandboxed environment)
    if [ -f "requirements.txt" ]; then
        pip install --user -r requirements.txt
        log_success "Python dependencies installed"
    else
        # Install basic dependencies
        pip install --user fastapi uvicorn rich pydantic psutil python-dotenv pyyaml
        log_success "Basic Python dependencies installed"
    fi
}

# Function to start the web API
start_web_api() {
    log_info "Starting web API..."
    
    cd "$MASTER_MENU_DIR"
    
    # Start web API in background
    python web_api.py &
    WEB_API_PID=$!
    echo $WEB_API_PID > web_api.pid
    
    # Wait for API to be ready
    wait_for_service "http://localhost:8000/health" "Web API"
}

# Function to start the web interface
start_web_interface() {
    log_info "Starting web interface..."
    
    cd "$WEB_INTERFACE_DIR"
    
    # Build and start Next.js
    npm run build
    npm run start &
    WEB_INTERFACE_PID=$!
    echo $WEB_INTERFACE_PID > web_interface.pid
    
    # Wait for web interface to be ready
    wait_for_service "http://localhost:3000" "Web Interface"
}

# Function to setup environment
setup_environment() {
    log_info "Setting up environment..."
    
    # Create .env file for master agent menu if it doesn't exist
    cd "$MASTER_MENU_DIR"
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Ottomator Agents Environment Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Local AI Configuration
OLLAMA_BASE_URL=http://localhost:11434
LOCALAI_BASE_URL=http://localhost:8080

# Default Model Configuration
DEFAULT_MODEL=llama3.2
DEFAULT_PROVIDER=ollama

# Web Interface Configuration
WEB_API_PORT=8000
WEB_INTERFACE_PORT=3000
EOF
        log_success "Environment file created"
    fi
}

# Function to display final information
display_final_info() {
    echo
    echo "🎉 Deployment Complete!"
    echo "======================"
    echo
    echo "Services are running on:"
    echo "  📱 Web Interface: http://localhost:3000"
    echo "  🔧 Web API:       http://localhost:8000"
    echo "  🤖 Ollama:        http://localhost:11434"
    echo
    echo "Available models:"
    ollama list 2>/dev/null || echo "  Run 'ollama list' to see available models"
    echo
    echo "To stop services:"
    echo "  ./scripts/stop_services.sh"
    echo
    echo "To manage individual agents:"
    echo "  cd master-agent-menu && python main.py"
    echo
}

# Function to create stop script
create_stop_script() {
    cat > "$SCRIPT_DIR/stop_services.sh" << 'EOF'
#!/bin/bash

echo "🛑 Stopping Ottomator Agents services..."

# Stop web interface
if [ -f "web-interface/web_interface.pid" ]; then
    kill $(cat web-interface/web_interface.pid) 2>/dev/null || true
    rm -f web-interface/web_interface.pid
fi

# Stop web API
if [ -f "master-agent-menu/web_api.pid" ]; then
    kill $(cat master-agent-menu/web_api.pid) 2>/dev/null || true
    rm -f master-agent-menu/web_api.pid
fi

# Stop any running agents
pkill -f "python.*agent" 2>/dev/null || true

echo "✅ Services stopped"
EOF
    chmod +x "$SCRIPT_DIR/stop_services.sh"
}

# Main deployment function
main() {
    echo "Starting deployment process..."
    echo
    
    # Check prerequisites
    log_info "Checking prerequisites..."
    
    if ! command_exists python3; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi
    
    if ! command_exists node; then
        log_error "Node.js is required but not installed"
        exit 1
    fi
    
    if ! command_exists npm; then
        log_error "npm is required but not installed"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
    
    # Run deployment steps
    setup_environment
    install_python_dependencies
    install_web_dependencies
    
    log_success "Deployment setup complete!"
    log_info "To start services, run: python master-agent-menu/web_api.py & npm run dev --prefix web-interface"
}

# Handle script interruption
trap 'log_error "Deployment interrupted"; exit 1' INT TERM

# Run main function
main "$@"