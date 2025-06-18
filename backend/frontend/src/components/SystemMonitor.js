import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemSecondary,
  IconButton,
  Chip
} from '@mui/material';
import {
  Memory,
  Refresh,
  PlayArrow,
  Stop,
  Delete,
  Warning,
  CheckCircle,
  Error
} from '@mui/icons-material';
import axios from 'axios';

function SystemMonitor() {
  const [systemInfo, setSystemInfo] = useState(null);
  const [services, setServices] = useState([]);
  const [software, setSoftware] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('');
  const [dialogData, setDialogData] = useState({});
  const [refreshInterval, setRefreshInterval] = useState(null);

  useEffect(() => {
    fetchData();
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    setRefreshInterval(interval);
    
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch system info
      const systemResponse = await axios.get('/system/info');
      setSystemInfo(systemResponse.data);
      
      // Fetch installed software
      const softwareResponse = await axios.get('/system/software/installed/chocolatey');
      setSoftware(softwareResponse.data);
      
      setError(null);
    } catch (err) {
      console.error('Error fetching system data:', err);
      setError('Failed to load system information');
    } finally {
      setLoading(false);
    }
  };

  const handleServiceAction = async (serviceName, action) => {
    try {
      setLoading(true);
      await axios.post('/system/service', {
        service_name: serviceName,
        action: action
      });
      await fetchData();
    } catch (err) {
      console.error('Error managing service:', err);
      setError(`Failed to ${action} service ${serviceName}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSoftwareAction = async (packageName, action) => {
    try {
      setLoading(true);
      if (action === 'install') {
        await axios.post('/system/software/install', {
          package_name: packageName,
          manager: 'chocolatey'
        });
      } else {
        await axios.post('/system/software/uninstall', {
          package_name: packageName,
          manager: 'chocolatey'
        });
      }
      await fetchData();
    } catch (err) {
      console.error('Error managing software:', err);
      setError(`Failed to ${action} package ${packageName}`);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (type, data = {}) => {
    setDialogType(type);
    setDialogData(data);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setDialogData({});
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const renderDialog = () => {
    switch (dialogType) {
      case 'install':
        return (
          <Dialog open={openDialog} onClose={handleCloseDialog}>
            <DialogTitle>Install Software</DialogTitle>
            <DialogContent>
              <TextField
                autoFocus
                margin="dense"
                label="Package Name"
                fullWidth
                variant="outlined"
                value={dialogData.packageName || ''}
                onChange={(e) => setDialogData({ ...dialogData, packageName: e.target.value })}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Cancel</Button>
              <Button 
                onClick={() => {
                  handleSoftwareAction(dialogData.packageName, 'install');
                  handleCloseDialog();
                }}
                color="primary"
              >
                Install
              </Button>
            </DialogActions>
          </Dialog>
        );
      default:
        return null;
    }
  };

  if (loading && !systemInfo) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <LinearProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          <Memory sx={{ mr: 1, verticalAlign: 'middle' }} />
          System Monitor
        </Typography>
        <Button
          startIcon={<Refresh />}
          variant="contained"
          onClick={fetchData}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* System Overview */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>System Overview</Typography>
            {systemInfo && (
              <List>
                <ListItem>
                  <ListItemText primary="Operating System" secondary={`${systemInfo.os?.name} ${systemInfo.os?.version}`} />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Architecture" secondary={systemInfo.os?.architecture} />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Memory Usage" 
                    secondary={
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <Box sx={{ flex: 1, mr: 1 }}>
                          <LinearProgress
                            variant="determinate"
                            value={systemInfo.memory?.percent || 0}
                          />
                        </Box>
                        <Typography variant="body2">
                          {formatBytes(systemInfo.memory?.used)} / {formatBytes(systemInfo.memory?.total)}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="CPU Usage" 
                    secondary={
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <Box sx={{ flex: 1, mr: 1 }}>
                          <LinearProgress
                            variant="determinate"
                            value={systemInfo.cpu?.percent || 0}
                          />
                        </Box>
                        <Typography variant="body2">
                          {systemInfo.cpu?.percent?.toFixed(1)}%
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
              </List>
            )}
          </Paper>
        </Grid>

        {/* Installed Software */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Installed Software</Typography>
              <Button
                variant="contained"
                size="small"
                onClick={() => handleOpenDialog('install')}
              >
                Install New
              </Button>
            </Box>
            
            <List>
              {software.map((pkg) => (
                <ListItem
                  key={pkg.name}
                  secondaryAction={
                    <IconButton
                      edge="end"
                      aria-label="uninstall"
                      onClick={() => handleSoftwareAction(pkg.name, 'uninstall')}
                    >
                      <Delete />
                    </IconButton>
                  }
                >
                  <ListItemText
                    primary={pkg.name}
                    secondary={`Version: ${pkg.version}`}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {renderDialog()}
    </Container>
  );
}

export default SystemMonitor;
