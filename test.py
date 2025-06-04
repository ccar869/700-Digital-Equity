import speedtest
import platform
import psutil
import subprocess
import re

from ping3 import ping
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def ping_host(host):
    # Use 'ping' instead of 'ping.exe' for Linux
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    result = (subprocess.run(command, capture_output=True, text=True))
    return result.stdout

def speedTest():
        
    s = speedtest.Speedtest(secure=True)

    download = s.download()
    upload = s.upload()

    download = format(download/1000000, '.2f')
    upload = format(upload/1000000, '.2f')

    print('Download speed is:', download, 'MB per second')
    print('Upload speed is:', upload, 'MB per second')

    #output = ping_host("www.google.com")
    # Extract packet loss

    count = 4
    lost = 0
    total_ping = 0
    successful_pings = 0
    for _ in range(count):
        result = ping("www.google.com", timeout=2)
        if result is None:
            lost += 1
        else:
            total_ping += result
            successful_pings += 1
    packet_loss = (lost / count) * 100
    ping_time = f"{(total_ping / successful_pings) * 1000:.1f}" if successful_pings > 0 else None

    return [download, upload, packet_loss, ping_time]    

def getHardware():
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")

    # let's print CPU information
    print("="*40, "CPU Info", "="*40)
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

if __name__ == '__main__':
    speedTest()

