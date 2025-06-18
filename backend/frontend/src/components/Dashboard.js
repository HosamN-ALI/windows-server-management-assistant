import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  LinearProgress,
  Alert
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Computer,
  Security,
  Chat,
  CheckCircle,
  Error,
  Warning
} from '@mui/icons-material';
import axios from 'axios';

function Dashboard() {
  const [systemInfo, setSystemInfo] = useState(null);
  const [serviceStatus, setServiceStatus] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch system info
      const systemResponse = await axios.get('/system/info');
      setSystemInfo(systemResponse.data);
      
      // Fetch service status
      const healthResponse = await axios.get('/api/health');
      setServiceStatus(healthResponse.data.services);
      
      setError(null);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusColor = (status) => {
    if (status === true) return 'success';
    if (status === false) return 'error';
    return 'warning';
  };

  const getStatusIcon = (status) => {
    if (status === true) return <CheckCircle />;
    if (status === false) return <Error />;
    return <Warning />;
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ width: '100%' }}>
          <LinearProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={fetchDashboardData}>
            Retry
          </Button>
        }>
          {error}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        <DashboardIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* System Overview */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              <Computer sx={{ mr: 1, verticalAlign: 'middle' }} />
              System Overview
            </Typography>
            
            {systemInfo && (
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Operating System
                    </Typography>
                    <Typography variant="body1">
                      {systemInfo.os?.name} {systemInfo.os?.version}
                    </Typography>
                  </Box>
                  
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Architecture
                    </Typography>
                    <Typography variant="body1">
                      {systemInfo.os?.architecture}
                    </Typography>
                  </Box>
                  
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      CPU Cores
                    </Typography>
                    <Typography variant="body1">
                      {systemInfo.cpu?.count}
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Memory Usage
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={systemInfo.memory?.percent || 0}
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2">
                      {formatBytes(systemInfo.memory?.used)} / {formatBytes(systemInfo.memory?.total)}
                      ({systemInfo.memory?.percent?.toFixed(1)}%)
                    </Typography>
                  </Box>
                  
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      CPU Usage
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={systemInfo.cpu?.percent || 0}
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2">
                      {systemInfo.cpu?.percent?.toFixed(1)}%
                    </Typography>
                  </Box>
                  
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Running Processes
                    </Typography>
                    <Typography variant="body1">
                      {systemInfo.processes}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            )}
          </Paper>
        </Grid>

        {/* Service Status */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Service Status
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {Object.entries(serviceStatus).map(([service, status]) => (
                <Box key={service} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                    {service}
                  </Typography>
                  <Chip
                    icon={getStatusIcon(status)}
                    label={status ? 'Online' : 'Offline'}
                    color={getStatusColor(status)}
                    size="small"
                  />
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Chat color="primary" sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="h6" component="div">
                      Chat Assistant
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Interact with the AI assistant for system management
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small" href="/chat">Open Chat</Button>
                  </CardActions>
                </Card>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Computer color="primary" sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="h6" component="div">
                      System Monitor
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Monitor system performance and manage services
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small" href="/system">View System</Button>
                  </CardActions>
                </Card>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Security color="primary" sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="h6" component="div">
                      Security Scans
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Run penetration tests and security assessments
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small" href="/pentest">View Results</Button>
                  </CardActions>
                </Card>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <DashboardIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="h6" component="div">
                      Refresh Data
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Update dashboard with latest system information
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small" onClick={fetchDashboardData}>Refresh</Button>
                  </CardActions>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;
