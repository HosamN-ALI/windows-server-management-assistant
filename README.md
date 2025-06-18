# Windows Server Management and Penetration Testing Assistant

A comprehensive AI-powered assistant for Windows Server management and penetration testing, built with FastAPI backend and React frontend.

## Features

### 🤖 AI Assistant
- Natural language processing for command interpretation
- Voice-to-text and text-to-speech capabilities
- Real-time chat interface with WebSocket support
- Context-aware responses and command execution

### 🖥️ System Management
- Real-time system monitoring (CPU, memory, disk usage)
- Windows service management (start, stop, restart)
- Software package management (install/uninstall via Chocolatey/Winget)
- PowerShell script execution with security controls
- System information gathering and reporting

### 🔒 Penetration Testing
- Integration with popular security tools:
  - OWASP ZAP for web application scanning
  - Burp Suite for advanced security testing
  - SQLMap for SQL injection testing
  - Acunetix for comprehensive vulnerability scanning
  - SonarQube for code quality analysis
- Docker container management for security tools
- Automated scan scheduling and reporting
- Vulnerability assessment and reporting

### 🛡️ Security Features
- JWT-based authentication and authorization
- Role-based access control (RBAC)
- Audit logging for all system operations
- Security event monitoring
- Configurable security policies

## Architecture

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality (config, security, logging)
│   │   ├── services/       # Business logic services
│   │   └── main.py         # Application entry point
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   └── App.js          # Main application
├── requirements.txt        # Python dependencies
└── project_plan.md        # Detailed project documentation
```

## Prerequisites

### System Requirements
- Windows Server 2016+ or Windows 10/11
- Python 3.8+
- Node.js 16+
- Docker Desktop (optional, for containerized security tools)

### Required Software
- PowerShell 5.1+
- Chocolatey package manager
- Windows Package Manager (winget)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd windows-server-assistant
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the backend directory:
```env
# Application Settings
DEBUG=true
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-secret-key-here

# Authentication
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Security Settings
REQUIRE_CONFIRMATION_FOR_PRIVILEGED=true
POWERSHELL_EXECUTION_POLICY=RemoteSigned
MAX_COMMAND_TIMEOUT=300

# External Services (Optional)
OPENAI_API_KEY=your-openai-key
AZURE_SPEECH_KEY=your-azure-speech-key
AZURE_SPEECH_REGION=your-azure-region

# Tool Configurations
CHOCOLATEY_PATH=choco
WINGET_PATH=winget
DOCKER_HOST=tcp://localhost:2375

# Penetration Testing Tools
ACUNETIX_URL=http://localhost:3443
SONARQUBE_URL=http://localhost:9000
```

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Build for Production (Optional)
```bash
npm run build
```

## Usage

### Starting the Application

#### Development Mode
```bash
# Terminal 1: Start Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend (if running separately)
cd frontend
npm start
```

#### Production Mode
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000 (dev) or http://localhost:8000 (prod)
- API Documentation: http://localhost:8000/docs

### Default Credentials
- Username: `admin`
- Password: `admin123`

**⚠️ Change default credentials in production!**

## API Endpoints

### Authentication
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user information
- `POST /auth/logout` - Logout user

### System Management
- `GET /system/info` - Get system information
- `POST /system/powershell` - Execute PowerShell script
- `POST /system/software/install` - Install software package
- `POST /system/software/uninstall` - Uninstall software package
- `POST /system/service` - Manage Windows services

### Penetration Testing
- `POST /pentest/zap/scan` - Start OWASP ZAP scan
- `POST /pentest/burp/scan` - Start Burp Suite scan
- `POST /pentest/sqlmap/scan` - Start SQLMap scan
- `POST /pentest/acunetix/scan` - Start Acunetix scan
- `GET /pentest/containers` - List security tool containers
- `POST /pentest/containers/{tool}/start` - Start tool container

### Chat Interface
- `WebSocket /chat/ws/{client_id}` - Real-time chat communication

## Configuration

### Security Configuration
The application includes several security features that can be configured:

1. **Authentication**: JWT-based with configurable expiration
2. **Authorization**: Role-based access control
3. **Command Execution**: Configurable confirmation requirements
4. **Audit Logging**: All operations are logged with user context

### NLP Configuration
The NLP service supports multiple backends:
- OpenAI GPT models (requires API key)
- Local transformer models
- Rule-based intent recognition

### Voice Processing
Voice features require Azure Cognitive Services:
- Speech-to-text conversion
- Text-to-speech synthesis
- Multiple language support

## Docker Integration

### Security Tools
The application can manage Docker containers for security tools:

```bash
# Start OWASP ZAP container
docker run -d -p 8080:8080 owasp/zap2docker-stable

# Start Burp Suite container
docker run -d -p 8090:8090 portswigger/burp-rest-api
```

## Development

### Code Structure
- **Backend**: FastAPI with async/await patterns
- **Frontend**: React with Material-UI components
- **State Management**: React Context API
- **Communication**: REST API + WebSocket for real-time features

### Adding New Features
1. Create service in `backend/app/services/`
2. Add API endpoints in `backend/app/api/`
3. Create React components in `frontend/src/components/`
4. Update routing and navigation

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Security Considerations

### Production Deployment
1. Change default credentials
2. Use HTTPS/WSS protocols
3. Configure proper CORS origins
4. Set up proper firewall rules
5. Enable audit logging
6. Regular security updates

### Penetration Testing
- Only test systems you own or have permission to test
- Follow responsible disclosure practices
- Comply with local laws and regulations
- Use appropriate scan intensity for production systems

## Troubleshooting

### Common Issues

#### Backend Won't Start
- Check Python version (3.8+ required)
- Verify all dependencies are installed
- Check port availability (8000)
- Review environment variables

#### Frontend Build Fails
- Check Node.js version (16+ required)
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall

#### WebSocket Connection Issues
- Verify backend is running
- Check firewall settings
- Ensure WebSocket support in proxy/load balancer

#### Permission Errors
- Run as Administrator for system operations
- Check PowerShell execution policy
- Verify user permissions for target operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation in `project_plan.md`
- Review API documentation at `/docs` endpoint

## Roadmap

See `project_plan.md` for detailed development phases and future features.
