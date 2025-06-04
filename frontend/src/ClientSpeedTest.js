const LIBRESPEED_BASE = "https://700-digital-equity-production-c1d4.up.railway.app";


export async function measureLatency(url = `${LIBRESPEED_BASE}/garbage.php?ckSize=10000`) {
  const start = performance.now();
  await fetch(url + "&cachebust=" + Math.random(), { method: "HEAD", cache: "no-store" });
  const end = performance.now();
  return (end - start).toFixed(2); // ms
}

export async function measureDownloadSpeed() {
  const fileSizeBytes = 1*1024*1024;
  const fileUrl = `${LIBRESPEED_BASE}/garbage.php?ckSize=${fileSizeBytes}`;
  
  const start = performance.now();
  const response = await fetch(fileUrl + "&cachebust=" + Math.random(), { cache: "no-store" });
  const reader = response.body.getReader();

  // Read until complete
  while (true) {
    const { done } = await reader.read();
    if (done) break;
  }  const end = performance.now();
  const durationSeconds = (end - start) / 1000;
  return ((fileSizeBytes * 8) / (durationSeconds * 1024 * 1024)).toFixed(2); // Mbps
}

// Add upload test if needed
export async function measureUploadSpeed() {
  const data = new Uint8Array(1 * 1024 * 1024); // 10MB random data
  const start = performance.now();
  const res = await fetch(`${LIBRESPEED_BASE}/empty.php`, {
    method: "POST",
    body: data,
  });

  await res.text();
  const end = performance.now();

  const durationSeconds = (end - start) / 1000;
  const speedMbps = (data.length * 8) / (durationSeconds * 1024 * 1024);
  console.log("Upload speed:", speedMbps.toFixed(2), "Mbps");

  return speedMbps.toFixed(2);
}