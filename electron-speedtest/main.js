const {app , BrowserWindow, ipcMain} = require('electron');
const path = require('path');
const {spawn} = require('child_process');


function createWindow () {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            enableRemoteModule: false,
            contextIsolation: true,
        }
    });
    
     if (process.env.NODE_ENV === 'development') {
        win.loadURL('http://localhost:5173');
    } else {
        win.loadFile(path.join(__dirname, '../frontend/dist/index.html'));
    }
}

app.whenReady().then(createWindow);

app.on('web-contents-created', (event, contents) => {
    contents.session.setPermissionRequestHandler((webContents, permission, callback) => {
        if (permission === 'geolocation') {
            console.log(`Permission request for ${permission} from ${webContents.getURL()}`);
            callback(true); // Automatically grant geolocation permission
        }
        else {
            console.log(`Permission request for ${permission} from ${webContents.getURL()}`);
            callback(false); // Deny other permissions
        }
    }
    );
});

ipcMain.on('run-speedtest', async () => {
    return new Promise((resolve, reject) => {
        const process = spawn('python3', ['electronTests.py']);

        let output = '';
        process.stdout.on('data', (data) => {
            output += data.toString();
        });
        process.stderr.on('data', (data) => {
            console.error(`Error: ${data}`);
        });
        process.on('close', (code) => {
            if (code !== 0) {
                console.error(`Process exited with code ${code}`);
                reject(new Error(`Process exited with code ${code}`));
            } else {
                console.log(`Speedtest output: ${output}`);
                resolve(output);
            }
        });
    })
});

console.log("Hello from Electron!");