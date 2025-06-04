const {contextBridge, ipcRenderer} = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    runTest: () => ipcRenderer.invoke('run-speedtest')
});