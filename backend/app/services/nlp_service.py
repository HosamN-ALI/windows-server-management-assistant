import asyncio
from typing import Dict, List, Optional, Any
import openai
import json
from loguru import logger

from app.core.config import Settings
from app.core.logging import log_security_event

class NLPService:
    """Natural Language Processing service for command interpretation"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.openai_client = None
        self.deepseek_client = None
        
        # Initialize OpenAI client if API key is available
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai
            logger.info("OpenAI client initialized")
        
        # TODO: Initialize DeepSeek client when available
        if settings.DEEPSEEK_API_KEY:
            logger.info("DeepSeek API key found, but client not implemented yet")
    
    async def interpret_command(self, user_input: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Interpret user command and extract intent, parameters, and safety level
        
        Args:
            user_input: Raw user input text
            user_context: Additional context about the user and session
            
        Returns:
            Dictionary containing:
            - intent: The identified intent/action
            - parameters: Extracted parameters
            - confidence: Confidence score (0-1)
            - safety_level: Safety classification (safe, caution, dangerous)
            - requires_confirmation: Whether the command needs user confirmation
            - suggested_command: The actual system command to execute
        """
        try:
            if not self.openai_client:
                return self._fallback_interpretation(user_input)
            
            # Create system prompt for command interpretation
            system_prompt = self._create_system_prompt()
            
            # Create user prompt with context
            user_prompt = self._create_user_prompt(user_input, user_context)
            
            # Call OpenAI API
            response = await self._call_openai_api(system_prompt, user_prompt)
            
            # Parse and validate response
            interpretation = self._parse_api_response(response)
            
            # Log the interpretation for audit
            logger.info(f"Command interpreted: {user_input} -> {interpretation['intent']}")
            
            # Check for potentially dangerous operations
            if interpretation.get('safety_level') == 'dangerous':
                log_security_event(
                    "DANGEROUS_COMMAND_DETECTED",
                    user_context.get('username', 'unknown') if user_context else 'unknown',
                    f"Command: {user_input}, Intent: {interpretation['intent']}"
                )
            
            return interpretation
            
        except Exception as e:
            logger.error(f"Error interpreting command: {str(e)}")
            return self._fallback_interpretation(user_input)
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for the AI model"""
        return """You are an intelligent assistant for Windows Server management and penetration testing.
        
Your task is to interpret user commands and provide structured responses in JSON format.

For each user input, analyze and return:
{
    "intent": "primary action/intent (e.g., 'install_software', 'run_pentest', 'system_info')",
    "parameters": {
        "key": "value pairs of extracted parameters"
    },
    "confidence": 0.95,
    "safety_level": "safe|caution|dangerous",
    "requires_confirmation": true/false,
    "suggested_command": "actual command to execute",
    "explanation": "brief explanation of what will be done"
}

Safety levels:
- safe: Regular operations like viewing information, basic queries
- caution: Operations that modify system state but are reversible
- dangerous: Operations that could cause system damage or security risks

Always require confirmation for:
- System modifications
- Network operations
- Penetration testing activities
- Package installations/removals
- Registry modifications
- Service management

Supported intents include:
- system_info: Get system information
- install_software: Install software via Chocolatey/Winget
- uninstall_software: Remove software
- run_pentest: Execute penetration testing tools
- manage_services: Start/stop/restart services
- file_operations: File system operations
- network_operations: Network-related tasks
- docker_operations: Container management
- powershell_script: Execute PowerShell commands
"""

    def _create_user_prompt(self, user_input: str, user_context: Dict[str, Any] = None) -> str:
        """Create user prompt with context"""
        context_info = ""
        if user_context:
            context_info = f"\nUser context: {json.dumps(user_context, indent=2)}"
        
        return f"User command: {user_input}{context_info}\n\nProvide your interpretation in JSON format:"

    async def _call_openai_api(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    self.openai_client.ChatCompletion.create,
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=500,
                    temperature=0.1
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"OpenAI API attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

    def _parse_api_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate API response"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                interpretation = json.loads(json_str)
                
                # Validate required fields
                required_fields = ['intent', 'confidence', 'safety_level', 'requires_confirmation']
                for field in required_fields:
                    if field not in interpretation:
                        interpretation[field] = self._get_default_value(field)
                
                # Ensure confidence is between 0 and 1
                interpretation['confidence'] = max(0, min(1, interpretation.get('confidence', 0.5)))
                
                return interpretation
            else:
                raise ValueError("No JSON found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse API response: {str(e)}")
            return self._fallback_interpretation(response)

    def _get_default_value(self, field: str) -> Any:
        """Get default value for missing fields"""
        defaults = {
            'intent': 'unknown',
            'parameters': {},
            'confidence': 0.5,
            'safety_level': 'caution',
            'requires_confirmation': True,
            'suggested_command': '',
            'explanation': 'Unable to interpret command'
        }
        return defaults.get(field, None)

    def _fallback_interpretation(self, user_input: str) -> Dict[str, Any]:
        """Fallback interpretation when AI services are unavailable"""
        # Simple keyword-based interpretation
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['install', 'choco', 'winget']):
            intent = 'install_software'
            safety_level = 'caution'
        elif any(word in user_lower for word in ['uninstall', 'remove']):
            intent = 'uninstall_software'
            safety_level = 'caution'
        elif any(word in user_lower for word in ['system', 'info', 'status']):
            intent = 'system_info'
            safety_level = 'safe'
        elif any(word in user_lower for word in ['pentest', 'scan', 'zap', 'burp']):
            intent = 'run_pentest'
            safety_level = 'dangerous'
        else:
            intent = 'unknown'
            safety_level = 'caution'
        
        return {
            'intent': intent,
            'parameters': {'raw_input': user_input},
            'confidence': 0.3,
            'safety_level': safety_level,
            'requires_confirmation': safety_level != 'safe',
            'suggested_command': '',
            'explanation': f'Fallback interpretation: {intent}'
        }

    async def generate_response(self, interpretation: Dict[str, Any], execution_result: Dict[str, Any] = None) -> str:
        """Generate a natural language response based on interpretation and execution results"""
        try:
            if not self.openai_client:
                return self._fallback_response(interpretation, execution_result)
            
            # Create context for response generation
            context = {
                'interpretation': interpretation,
                'execution_result': execution_result
            }
            
            system_prompt = """You are a helpful Windows Server assistant. Generate a clear, concise response to the user based on the command interpretation and execution results. Be professional and informative."""
            
            user_prompt = f"Context: {json.dumps(context, indent=2)}\n\nGenerate a helpful response to the user:"
            
            response = await self._call_openai_api(system_prompt, user_prompt)
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return self._fallback_response(interpretation, execution_result)

    def _fallback_response(self, interpretation: Dict[str, Any], execution_result: Dict[str, Any] = None) -> str:
        """Generate fallback response when AI is unavailable"""
        intent = interpretation.get('intent', 'unknown')
        
        if execution_result:
            if execution_result.get('success'):
                return f"Successfully executed {intent} operation."
            else:
                return f"Failed to execute {intent} operation: {execution_result.get('error', 'Unknown error')}"
        else:
            return f"I understand you want to perform: {intent}. Please confirm to proceed."
