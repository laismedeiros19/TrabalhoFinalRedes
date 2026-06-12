import time
import random
import requests
import psutil
import dns.resolver

API_URL = "http://localhost:8000/api/metrics"
SEC_URL = "http://localhost:8000/api/security"
DNS_SERVER = "8.8.8.8"
TARGET_URL = "https://www.google.com"

def send_metric(service, metric_name, value):
    payload = {"service": service, "metric_name": metric_name, "value": float(value)}
    try: requests.post(API_URL, json=payload, timeout=2)
    except Exception: pass

def monitor_web():
    try:
        start_time = time.time()
        response = requests.get(TARGET_URL, timeout=3)
        latency = (time.time() - start_time) * 1000
        send_metric("web", "availability", 1.0 if response.status_code == 200 else 0.0)
        send_metric("web", "latency", latency)
    except Exception:
        send_metric("web", "availability", 0.0)
        send_metric("web", "latency", 0.0)
    send_metric("web", "rps", random.uniform(10, 150))
    send_metric("web", "active_connections", random.randint(5, 40))
    send_metric("web", "error_rate", 0.0 if random.random() > 0.05 else random.uniform(1, 5))

db_size_gb = 12.4
def monitor_database():
    global db_size_gb
    send_metric("database", "availability", 1.0)
    send_metric("database", "cpu_usage", psutil.cpu_percent())
    send_metric("database", "memory_usage", psutil.virtual_memory().percent)
    send_metric("database", "qps", random.uniform(50, 400))
    send_metric("database", "open_connections", random.randint(10, 80))
    send_metric("database", "slow_queries", random.randint(0, 3) if random.random() > 0.8 else 0)
    db_size_gb += random.uniform(0.0001, 0.0005)
    send_metric("database", "db_size", db_size_gb)

resolver = dns.resolver.Resolver()
resolver.nameservers = [DNS_SERVER]
def monitor_dns():
    try:
        start_time = time.time()
        resolver.resolve("google.com", "A")
        send_metric("dns", "availability", 1.0)
        send_metric("dns", "latency", (time.time() - start_time) * 1000)
        send_metric("dns", "failed_resolutions", 0.0)
    except Exception:
        send_metric("dns", "availability", 0.0)
        send_metric("dns", "failed_resolutions", 1.0)
    send_metric("dns", "qps", random.uniform(5, 50))

def monitor_smtp():
    send_metric("smtp", "availability", 1.0)
    delivery_rate = random.uniform(98.0, 100.0) if random.random() > 0.05 else random.uniform(85.0, 95.0)
    send_metric("smtp", "delivery_rate", delivery_rate)
    send_metric("smtp", "latency", random.uniform(100, 450))
    send_metric("smtp", "queue_length", random.randint(0, 5) if delivery_rate > 95 else random.randint(15, 45))
    send_metric("smtp", "error_rate", 100.0 - delivery_rate)
    send_metric("smtp", "volume_per_minute", random.randint(20, 120))

# NOVA FUNÇÃO: Dispara anomalias de segurança para a API real
def simulate_security_incidents():
    if random.random() > 0.2: # 20% de chance de gerar um evento de segurança por iteração
        return
    
    incidents = [
        {"event_type": "ddos", "severity": "CRIT", "service": "Web Server", "description": "Pico de tráfego anormal detectado: 45.000 req/s. Assinatura de DDoS volumétrico de Camada 7.", "source_ip": "198.51.100.77"},
        {"event_type": "brute", "severity": "WARN", "service": "Banco de Dados", "description": "Detecção de Brute-force: 150 tentativas de login falhas para usuário 'root'. IP mitigado.", "source_ip": "92.118.160.55"},
        {"event_type": "config", "severity": "WARN", "service": "Web Server", "description": "Alteração de configuração: hash do arquivo nginx.conf modificado fora da janela de manutenção.", "source_ip": "10.0.1.15"},
        {"event_type": "vuln", "severity": "CRIT", "service": "DNS", "description": "Alerta de Vulnerabilidade: CVE-2023-50387 (KeyTrap) detectada na versão do serviço BIND9.", "source_ip": "-"}
    ]
    
    chosen = random.choice(incidents)
    try:
        requests.post(SEC_URL, json=chosen, timeout=2)
        print(f"⚠️ [SEGURANÇA] Anomalia simulada ({chosen['event_type'].upper()}) enviada com sucesso à API.")
    except Exception:
        pass

print("🚀 Super Agente Centralizado Inicializado! Monitorando os 4 serviços + Módulos de Segurança...")

while True:
    monitor_web()
    monitor_database()
    monitor_dns()
    monitor_smtp()
    simulate_security_incidents()
    print(f"[{time.strftime('%H:%M:%S')}] 🔄 Rodada de métricas enviada para a API.")
    time.sleep(5)