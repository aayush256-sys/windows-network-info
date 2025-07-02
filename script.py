import psutil
import socket
import wmi

def get_dns_servers():
    c = wmi.WMI()
    dns_servers = set()
    for nic in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if nic.DNSServerSearchOrder:
            dns_servers.update(nic.DNSServerSearchOrder)
    return list(dns_servers)

def get_default_gateway():
    gateways = psutil.net_if_addrs()
    gateway_info = {"IPv4": None, "IPv6": None}
    for interface, addrs in gateways.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                gateway_info['IPv4'] = addr.address
            elif addr.family == socket.AF_INET6:
                gateway_info['IPv6'] = addr.address
    return gateway_info

def get_wmi_nic_info():
    c = wmi.WMI()
    nic_info = {}
    for nic in c.Win32_NetworkAdapter():
        if nic.NetConnectionID:
            nic_info[nic.NetConnectionID] = {
                "Description": nic.Description,
                "AdapterType": nic.AdapterType,
                "Speed (WMI)": int(nic.Speed or 0) // 1_000_000 if nic.Speed else "Unknown"
            }
    return nic_info

def audit_windows_interfaces():
    print("=== Enhanced Windows Network Interface Audit ===\n")
    default_gateway = get_default_gateway()
    dns_servers = get_dns_servers()
    wmi_nics = get_wmi_nic_info()
    io_counters = psutil.net_io_counters(pernic=True)

    for interface, addrs in psutil.net_if_addrs().items():
        stats = psutil.net_if_stats().get(interface)
        if not stats or not stats.isup:
            continue

        print(f"Interface       : {interface}")
        if interface in wmi_nics:
            print(f"Description     : {wmi_nics[interface]['Description']}")
            print(f"Adapter Type    : {wmi_nics[interface]['AdapterType']}")
            print(f"Speed (WMI)     : {wmi_nics[interface]['Speed (WMI)']} Mbps")

        mac = next((a.address for a in addrs if a.family == psutil.AF_LINK), "N/A")
        print(f"MAC Address     : {mac}")

        ipv4 = [a.address for a in addrs if a.family == socket.AF_INET]
        ipv6 = [a.address for a in addrs if a.family == socket.AF_INET6]

        print(f"IPv4 Address    : {ipv4[0] if ipv4 else 'Not Assigned'}")
        if ipv6:
            for v6 in ipv6:
                print(f"IPv6 Address    : {v6}")
        else:
            print("IPv6 Address    : Not Assigned")

        print(f"Default Gateway : IPv4: {default_gateway['IPv4']}, IPv6: {default_gateway['IPv6']}")
        print(f"MTU             : {stats.mtu}")
        print(f"Link Speed      : {stats.speed} Mbps")
        print(f"Duplex          : {'Full' if stats.duplex == psutil.NIC_DUPLEX_FULL else 'Half' if stats.duplex == psutil.NIC_DUPLEX_HALF else 'Unknown'}")
        
        ipv6_supported = 'Yes' if any(a.family == socket.AF_INET6 for a in addrs) else 'No'
        print(f"Supports IPv6   : {ipv6_supported}")
        
        print(f"Operational     : {'Up' if stats.isup else 'Down'}")

        if interface in io_counters:
            io = io_counters[interface]
            print(f"Bytes Sent      : {io.bytes_sent:,}")
            print(f"Bytes Received  : {io.bytes_recv:,}")

        print(f"DNS Servers     : {', '.join(dns_servers) if dns_servers else 'Not Found'}")
        print("-" * 50)

if __name__ == "__main__":
    audit_windows_interfaces()
