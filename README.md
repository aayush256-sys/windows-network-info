# Windows Network Audit Tool

A lightweight Python script that audits and displays detailed network interface information on Windows systems. Ideal for system administrators, network engineers, and cybersecurity analysts who need quick insights into IP configurations, DNS, gateways, traffic stats, and more.

## 🔍 Features

- Lists all active network interfaces  
- Shows:
  - IPv4 and IPv6 addresses  
  - MAC address  
  - Default gateway (IPv4 & IPv6)  
  - MTU  
  - Link speed & duplex mode  
  - DNS servers  
  - Data sent/received  
  - Adapter description & type (via WMI)  
- Checks for IPv6 support

## 🛠️ Requirements

- Python 3.10+  
- Works on **Windows only**

### Python Packages

- `psutil`  
- `wmi`  
- `pywin32` (required by `wmi`)

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aayush256-sys/windows-network-info.git
   cd windows-network-audit
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install psutil wmi pywin32
   ```

## ▶️ Usage

Run the script:

```bash
python script.py
```



