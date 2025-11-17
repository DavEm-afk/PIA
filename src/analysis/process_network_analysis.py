import json
from pathlib import Path

def load_priorities(config_dir):
    # Carga priorities.json
    prio_path = Path(config_dir) / "priorities.json"

    if not prio_path.exists():
        raise FileNotFoundError(f"No se encontró {prio_path}")

    with open(prio_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    suspicious_ports = data.get("suspicious_ports", [])
    internal_ranges = data.get("internal_ip_ranges", [])

    return suspicious_ports, internal_ranges

def parse_address(addr):
    """Convierte 'IP:PORT' en (IP, PORT) o (None, None)."""
    if not addr:
        return None, None
    try:
        ip, port = addr.rsplit(":", 1)
        return ip, int(port)
    except:
        return None, None

def is_internal_ip(ip, internal_ranges):
    """Evalúa si la IP pertenece a rangos internos declarados."""
    if not ip:
        return False
    return any(ip.startswith(prefix) for prefix in internal_ranges)

def analyze_process_connections(connections, process_info, suspicious_ports, internal_ranges):
    # Analisis a conexiones de un PID
    total = len(connections)
    listen_ports = []
    remote_connections = []
    suspicious = False
    notes = []

    for conn in connections:
        local_ip, local_port = parse_address(conn.get("laddr"))
        remote_ip, remote_port = parse_address(conn.get("raddr"))
        status = conn.get("status")
        sock_type = "TCP" if conn.get("type") == "1" else "UDP"

        if status == "LISTEN" and local_port:
            listen_ports.append(f"{local_ip}:{local_port}")

            if local_port in suspicious_ports:
                suspicious = True
                notes.append(f"Puerto LISTEN sospechoso: {local_port}")

        if remote_ip:
            remote_connections.append({
                "remote_ip": remote_ip,
                "remote_port": remote_port,
                "type": sock_type,
                "status": status
            })

            # Conexión a IP fuera de red interna dado en priorities.json
            if not is_internal_ip(remote_ip, internal_ranges):
                suspicious = True
                notes.append(f"Conexión a IP externa: {remote_ip}")

            # Conexión a puerto remoto sospechoso dado en priorities.json
            if remote_port in suspicious_ports:
                suspicious = True
                notes.append(f"Puerto remoto sospechoso: {remote_port}")

    pid = connections[0]["pid"]
    pname = process_info.get(str(pid), f"PID {pid}")

    return pname, {
        "connections": total,
        "listen_ports": listen_ports,
        "remote_connections": remote_connections,
        "suspicious": suspicious,
        "notes": notes
    }

def perform_network_analysis(net_file, process_file, config_dir="./config"):
    """Función principal"""
    # Cargar desde priorities
    suspicious_ports, internal_ranges = load_priorities(config_dir)

    # net_connections.json
    with open(net_file, "r", encoding="utf-8-sig") as f:
        net_data = json.load(f)

    # process_list.json
    with open(process_file, "r", encoding="utf-8-sig") as f:
        process_list = json.load(f)

    process_list = process_list.get("Procesos", [])
    process_info = {str(p.get("ID")): p.get("Nombre") for p in process_list}

    # Agrupar conexiones por PID
    per_pid = {}
    for conn in net_data:
        pid = conn.get("pid")
        if pid is not None:
            per_pid.setdefault(pid, []).append(conn)

    results = {}
    suspicious_count = 0

    for pid, conns in per_pid.items():
        pname, analysis = analyze_process_connections(
            conns,
            process_info,
            suspicious_ports,
            internal_ranges
        )
        results[f"{pname} (PID {pid})"] = analysis

        if analysis["suspicious"]:
            suspicious_count += 1

    summary = {
        "total_connections": len(net_data),
        "processes_with_listen_ports": sum(
            1 for v in results.values() if v["listen_ports"]
        ),
        "suspicious_processes": suspicious_count
    }

    return {
        "network_analysis": {
            "per_process": results,
            "summary": summary
        }
    }
