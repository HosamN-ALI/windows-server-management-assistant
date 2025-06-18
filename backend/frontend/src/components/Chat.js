import React, { useState, useEffect, useRef } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  IconButton,
  Alert,
  Chip,
  CircularProgress
} from '@mui/material';
import {
  Send,
  Mic,
  MicOff,
  VolumeUp,
  Chat as ChatIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

function Chat() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const wsRef = useRef(null);
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectWebSocket = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/chat/ws/${user?.username || 'anonymous'}`;
    
    wsRef.current = new WebSocket(wsUrl);
    
    wsRef.current.onopen = () => {
      setIsConnected(true);
      setError(null);
      console.log('WebSocket connected');
    };
    
    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      addMessage(data);
      setIsLoading(false);
    };
    
    wsRef.current.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
      // Attempt to reconnect after 3 seconds
      setTimeout(connectWebSocket, 3000);
    };
    
    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('Connection error. Attempting to reconnect...');
    };
  };

  const addMessage = (messageData) => {
    const message = {
      id: Date.now(),
      type: messageData.type || 'text',
      content: messageData.message || messageData.content,
      timestamp: new Date(),
      interpretation: messageData.interpretation,
      result: messageData.result
    };
    
    setMessages(prev => [...prev, message]);
  };

  const sendMessage = () => {
    if (!inputMessage.trim() || !isConnected) return;
    
    // Add user message to chat
    addMessage({
      type: 'user',
      message: inputMessage,
    });
    
    // Send to WebSocket
    const messageData = {
      type: 'text',
      content: inputMessage,
      context: {
        username: user?.username,
        timestamp: new Date().toISOString()
      }
    };
    
    wsRef.current.send(JSON.stringify(messageData));
    setInputMessage('');
    setIsLoading(true);
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        sendVoiceMessage(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      setError('Microphone access denied or not available');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const sendVoiceMessage = async (audioBlob) => {
    if (!isConnected) return;
    
    // Convert blob to base64
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64Audio = reader.result.split(',')[1];
      
      const messageData = {
        type: 'voice',
        content: base64Audio,
        context: {
          username: user?.username,
          timestamp: new Date().toISOString()
        }
      };
      
      wsRef.current.send(JSON.stringify(messageData));
      setIsLoading(true);
    };
    reader.readAsDataURL(audioBlob);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const renderMessage = (message) => {
    const isUser = message.type === 'user';
    const isSystem = message.type === 'system';
    const isError = message.type === 'error';
    
    return (
      <Box
        key={message.id}
        className={`message ${message.type}`}
        sx={{
          mb: 1,
          p: 1.5,
          borderRadius: 2,
          maxWidth: '80%',
          alignSelf: isUser ? 'flex-end' : 'flex-start',
          bgcolor: isUser ? 'primary.main' : isError ? 'error.main' : isSystem ? 'success.main' : 'grey.800',
          color: 'white'
        }}
      >
        <Typography variant="body1">
          {message.content}
        </Typography>
        
        {message.interpretation && (
          <Box sx={{ mt: 1 }}>
            <Chip
              label={`Intent: ${message.interpretation.intent}`}
              size="small"
              sx={{ mr: 1, mb: 0.5 }}
            />
            <Chip
              label={`Confidence: ${(message.interpretation.confidence * 100).toFixed(0)}%`}
              size="small"
              color={message.interpretation.confidence > 0.8 ? 'success' : 'warning'}
            />
          </Box>
        )}
        
        <Typography variant="caption" sx={{ display: 'block', mt: 0.5, opacity: 0.7 }}>
          {message.timestamp.toLocaleTimeString()}
        </Typography>
      </Box>
    );
  };

  return (
    <Container maxWidth="md" sx={{ height: '100vh', display: 'flex', flexDirection: 'column', py: 2 }}>
      <Typography variant="h4" gutterBottom>
        <ChatIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        AI Assistant
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Chip
          label={isConnected ? 'Connected' : 'Disconnected'}
          color={isConnected ? 'success' : 'error'}
          size="small"
        />
        {isLoading && (
          <Box sx={{ ml: 2, display: 'flex', alignItems: 'center' }}>
            <CircularProgress size={16} sx={{ mr: 1 }} />
            <Typography variant="caption">Processing...</Typography>
          </Box>
        )}
      </Box>
      
      <Paper sx={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <Box
          sx={{
            flex: 1,
            overflow: 'auto',
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            gap: 1
          }}
        >
          {messages.length === 0 && (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="body1" color="textSecondary">
                Welcome! Ask me anything about your Windows server or request system operations.
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                Examples: "Show system info", "Install Chrome", "Run a security scan"
              </Typography>
            </Box>
          )}
          
          {messages.map(renderMessage)}
          <div ref={messagesEndRef} />
        </Box>
        
        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              multiline
              maxRows={4}
              placeholder="Type your message or use voice input..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={!isConnected}
            />
            
            <IconButton
              color={isRecording ? 'error' : 'primary'}
              onClick={isRecording ? stopRecording : startRecording}
              disabled={!isConnected}
              className={isRecording ? 'recording' : ''}
            >
              {isRecording ? <MicOff /> : <Mic />}
            </IconButton>
            
            <Button
              variant="contained"
              onClick={sendMessage}
              disabled={!inputMessage.trim() || !isConnected}
              endIcon={<Send />}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

export default Chat;
