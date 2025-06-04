import React, {useState} from 'react';

export default function App() {

    const [result, setResult] = useState('');

  const runSpeedtest = async () => {
    const {ipcRenderer} = window.require('electron');
    const output = await ipcRenderer.invoke('run-speedtest');
    setResult(output);
    return (
        <div>
        <h1>Electron Speedtest</h1>
        <p>This is a simple speed test application built with Electron.</p>

        <button id="run-speedtest">Run Speedtest</button>
            <div id="result">
                <button onClick={runSpeedtest}>Run Speedtest</button>
            
                <pre>{result}</pre>
            </div>

        </div>
    )
  };
}