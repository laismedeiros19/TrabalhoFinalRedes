import requests
import time
import random

URL_METRICAS = "http://localhost:8000/api/metrics"
URL_SEGURANCA = "http://localhost:8000/api/security"

def enviar_metricas_api(dados_infra):
    """Garante o envio desmembrado respeitando as chaves exatas do dashboard.js"""
    for servico, metricas in dados_infra.items():
        for nome_metrica, valor in metricas.items():
            payload = {
                "service": servico,
                "metric_name": nome_metrica,
                "value": float(valor)
            }
            try:
                requests.post(URL_METRICAS, json=payload)
            except Exception as e:
                pass

def menu():
    print("\n" + "="*40)
    print("      NETWATCH - PAINEL DE INCIDENTES      ")
    print("="*40)
    print("[1] ESTADO NORMAL (Todos os servidores UP)")
    print("[2] SIMULAR ATAQUE DoS (Web Server cai / Gráfico zerado)")
    print("[3] DERRUBAR BANCO DE DADOS (Queda total / Alerta SMTP)")
    print("[4] INJETAR VULNERABILIDADE (DNS KeyTrap)")
    print("[5] SIMULAR INUNDAÇÃO SMTP (Spam / Email Bombing)") 
    print("[0] Sair")
    print("="*40)

while True:
    menu()
    opcao = input("Escolha o cenário para apresentar: ")

    if opcao == "1":
        print("\n🟢 Restaurando infraestrutura para a normalidade...")
        infra_normal = {
            "web": {
                "availability": 1.0, 
                "latency": 45.0, 
                "rps": random.randint(110, 135), 
                "error_rate": 0.0, 
                "open_connections": 25.0
            },
            "database": {
                "availability": 1.0, 
                "qps": 90.0, 
                "cpu_usage": 15.5, 
                "slow_queries": 0.0, 
                "open_connections": 12.0, 
                "db_size": 12.450, 
                "error_rate": 0.0
            },
            "dns": {
                "availability": 1.0, 
                "latency": 12.0, 
                "qps": 18.0, 
                "failed_resolutions": 0.0
            },
            "smtp": {
                "availability": 1.0, 
                "latency": 95.0, 
                "delivery_rate": 100.0, 
                "queue_length": 0.0, 
                "error_rate": 0.0
            }
        }
        enviar_metricas_api(infra_normal)
        print("✅ Sistema Operando em Nível 1 - OK.")

    elif opcao == "2":
        print("\n⚔️ [ATAQUE] Disparando bombardeio DDoS contra o Web Server...")
        infra_dos = {
            "web": {
                "availability": 0.0, 
                "latency": 4500.0, 
                "rps": random.randint(95000, 105000), 
                "error_rate": 98.5, 
                "open_connections": 1200.0
            },
            "database": {
                "availability": 1.0, 
                "qps": 45.0, 
                "cpu_usage": 88.0, 
                "slow_queries": 12.0, 
                "open_connections": 45.0, 
                "db_size": 12.450, 
                "error_rate": 0.0
            },
            "dns": {
                "availability": 1.0, 
                "latency": 15.0, 
                "qps": 35.0, 
                "failed_resolutions": 0.0
            },
            "smtp": {
                "availability": 1.0, 
                "latency": 98.0, 
                "delivery_rate": 100.0, 
                "queue_length": 0.0, 
                "error_rate": 0.0
            }
        }
        enviar_metricas_api(infra_dos)
        requests.post(URL_SEGURANCA, json={
            "event_type": "ddos",
            "severity": "CRIT",
            "service": "Web Server",
            "description": "Pico anômalo volumétrico detectado. Mitigação via Firewall ativada.",
            "source_ip": "185.220.101.44"
        })
        print("💥 Ataque injetado com sucesso!")

    elif opcao == "3":
        print("\n🚨 [PANE] Desligando o servidor de Banco de Dados relacional...")
        infra_db_down = {
            "web": {
                "availability": 1.0, 
                "latency": 50.0, 
                "rps": 80.0, 
                "error_rate": 5.0, 
                "open_connections": 15.0
            },
            "database": {
                "availability": 0.0, 
                "qps": 0.0, 
                "cpu_usage": 0.0, 
                "slow_queries": 0.0, 
                "open_connections": 0.0, 
                "db_size": 12.450, 
                "error_rate": 0.0
            },
            "dns": {
                "availability": 1.0, 
                "latency": 12.0, 
                "qps": 15.0, 
                "failed_resolutions": 0.0
            },
            "smtp": {
                "availability": 1.0, 
                "latency": 110.0, 
                "delivery_rate": 95.0, 
                "queue_length": 5.0, 
                "error_rate": 2.0
            }
        }
        enviar_metricas_api(infra_db_down)
        requests.post(URL_SEGURANCA, json={
            "event_type": "brute",
            "severity": "WARN",
            "service": "Database",
            "description": "Múltiplas falhas de autenticação do usuário root. Banco indisponível.",
            "source_ip": "92.118.160.55"
        })
        print("🛑 Banco offline! Verifique os alertas SMTP no terminal do backend.")

    elif opcao == "4":
        print("\n🔍 [VULNERABILIDADE] Simulando ataque KeyTrap e esgotamento do servidor DNS...")
        infra_dns_attack = {
            "web": {"availability": 1.0, "latency": 45.0, "rps": 120.0, "error_rate": 0.0, "open_connections": 25.0},
            "database": {"availability": 1.0, "qps": 90.0, "cpu_usage": 15.5, "slow_queries": 0.0, "open_connections": 12.0, "db_size": 12.450, "error_rate": 0.0},
            "dns": {
                "availability": 0.0,            # Card do DNS fica vermelho (Crítico)
                "latency": 5200.0,             # Tempo de Resposta (ms) explode verticalmente
                "qps": 5.0,                    # Consultas aceitas despencam porque ele está travado
                "failed_resolutions": 150.0    # Gráfico de Falhas/s dá um salto gigante para o topo
            },
            "smtp": {"availability": 1.0, "latency": 95.0, "delivery_rate": 100.0, "queue_length": 0.0, "error_rate": 0.0}
        }
        enviar_metricas_api(infra_dns_attack)
        requests.post(URL_SEGURANCA, json={
            "event_type": "vuln",
            "severity": "CRIT",                # Mudamos para CRIT para combinar com o card vermelho!
            "service": "DNS (BIND9)",
            "description": "Exploitation da CVE-2023-50387 (KeyTrap) detectada. CPU em 100% por exaustão criptográfica DNSSEC.",
            "source_ip": "198.51.100.77"
        })
        print("💥 Ataque de exaustão DNS injetado com sucesso! Verifique o painel.")

    elif opcao == "5":
        print("\n📨 [SMTP FLOOD] Iniciando surto massivo de Email Bombing (Mass Mailing Spam)...")
        infra_smtp_flood = {
            "web": {"availability": 1.0, "latency": 45.0, "rps": 120.0, "error_rate": 0.0, "open_connections": 25.0},
            "database": {"availability": 1.0, "qps": 90.0, "cpu_usage": 15.5, "slow_queries": 0.0, "open_connections": 12.0, "db_size": 12.450, "error_rate": 0.0},
            "dns": {"availability": 1.0, "latency": 12.0, "qps": 28.0, "failed_resolutions": 0.0},
            "smtp": {
                "availability": 0.0,        
                "latency": 3800.0,         
                "delivery_rate": 18.5,     
                "queue_length": 4850.0,    
                "error_rate": 78.2,        
                "volume_per_minute": 950.0 
            }
        }
        enviar_metricas_api(infra_smtp_flood)
        requests.post(URL_SEGURANCA, json={
            "event_type": "ddos",
            "severity": "CRIT",
            "service": "SMTP Server",
            "description": "Ataque de Email Bombing em massa detectado. Fila de mensagens congestionada (MTA Mail Queue Overload).",
            "source_ip": "46.138.200.11"
        })
        print("🔥 Inundação SMTP injetada com sucesso! Veja os gráficos do e-mail reagirem.")

    elif opcao == "0":
        break