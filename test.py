import speedtest
import subprocess
import re
import platform
import psutil

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

def speedTest():
        
    s = speedtest.Speedtest(secure=True)

    download = s.download()
    upload = s.upload()

    download = format(download/1000000, '.2f')
    upload = format(upload/1000000, '.2f')

    print('Download speed is:', download, 'MB per second')
    print('Upload speed is:', upload, 'MB per second')

    process = subprocess.Popen(["ping.exe","www.google.com"], stdout = subprocess.PIPE)

    output, error = process.communicate()

    # Decode bytes to string
    output = output.decode("utf-8")

    # Extract packet loss
    packet_loss_match = re.search(r"(\d+)% loss", output)
    packet_loss = int(packet_loss_match.group(1)) if packet_loss_match else None

    # Extract average ping (on Unix)
    min_ping_match = re.search(r"Minimum = (\d+)ms", output)
    min_ping = int(min_ping_match.group(1)) if min_ping_match else None

    max_ping_match = re.search(r"Maximum = (\d+)ms", output)
    max_ping = int(max_ping_match.group(1)) if max_ping_match else None

    ping_match = re.search(r"Average = (\d+)ms", output)
    avg_ping = int(ping_match.group(1)) if ping_match else None

    print(f"Packet Loss: {packet_loss}%")
    print(f"Average Ping: {avg_ping} ms")
    print(f"Maximum Ping: {max_ping} ms")
    print(f"Minimum Ping: {min_ping} ms")

    return [download, upload, packet_loss, avg_ping]

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