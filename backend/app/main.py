from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime

# ==============================================================================
# 1. CONFIGURAÇÃO DO BANCO DE DADOS
# ==============================================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./devops_monitor.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==============================================================================
# 2. MODELOS DO BANCO DE DADOS
# ==============================================================================
class MetricLog(Base):
    __tablename__ = "metric_logs"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, index=True)       
    metric_name = Column(String, index=True)  
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)   # ddos, brute, config, vuln
    severity = Column(String)                 # CRIT, WARN, INFO
    service = Column(String)                  # Web Server, Banco de Dados, etc.
    description = Column(String)
    source_ip = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ==============================================================================
# 3. MOTOR DE ALERTAS — LOGS SMTP
# ==============================================================================
def send_email_notification(level: str, service: str, metric: str, value: str, rule: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "═"*80)
    print(f"✉️  [SMTP NOTIFICAÇÃO DISPARADA] - {level} - {timestamp}")
    print(f"De: monitoramento@idp-devops.internal")
    print(f"Para: equipe-suporte@idp.edu.br")
    print(f"Assunto: ALERT: Alerta de rede detectado no serviço [{service.upper()}]")
    print("─"*80)
    print(f"Atenção Engenheiros,\n")
    print(f"O motor de monitoramento detectou uma quebra de limiar de rede:")
    print(f"  - Serviço: {service.upper()}")
    print(f"  - Métrica Violada: {metric}")
    print(f"  - Valor Registrado: {value}")
    print(f"  - Diagnóstico: {rule}")
    print(f"\nStatus da Notificação: E-mail enviado com sucesso via servidor SMTP fictício.")
    print("═"*80 + "\n")

def check_alert_rules(service: str, metric_name: str, value: float):
    if metric_name == "availability" and value == 0.0:
        send_email_notification("CRÍTICO - NÍVEL 3", service, metric_name, "DOWN (0)", "A disponibilidade do serviço caiu para zero.")
        return

    if metric_name in ["latency", "latency_ms", "response_ms"] and value > 200.0:
        send_email_notification("ATENÇÃO - NÍVEL 2", service, metric_name, f"{value:.2f} ms", "Tempo de resposta acima de 200ms.")
    
    elif metric_name in ["error_rate", "error_rate_pct"] and value > 2.0:
        send_email_notification("ATENÇÃO - NÍVEL 2", service, metric_name, f"{value:.2f} %", "Taxa de erros acima de 2%.")

# ==============================================================================
# 4. ROTAS DA API
# ==============================================================================
class MetricCreate(BaseModel):
    service: str
    metric_name: str
    value: float

class SecurityCreate(BaseModel):
    event_type: str
    severity: str
    service: str
    description: str
    source_ip: str

app = FastAPI(title="Plataforma de Monitoramento DevOps - IDP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "API Online"}

@app.post("/api/metrics")
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    db_metric = MetricLog(service=metric.service.lower(), metric_name=metric.metric_name.lower(), value=metric.value)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    check_alert_rules(db_metric.service, db_metric.metric_name, db_metric.value)
    return {"status": "Métrica processada"}

# Rota POST para o Agente registrar anomalias de segurança
@app.post("/api/security")
def create_security_event(event: SecurityCreate, db: Session = Depends(get_db)):
    db_event = SecurityEvent(
        event_type=event.event_type.lower(), severity=event.severity.upper(),
        service=event.service, description=event.description, source_ip=event.source_ip
    )
    db.add(db_event)
    db.commit()
    return {"status": "Evento de segurança registrado"}

@app.get("/api/metrics/latest")
def get_latest_metrics(db: Session = Depends(get_db)):
    return db.query(MetricLog).order_by(MetricLog.timestamp.desc()).limit(100).all()

# NOVA ROTA: Retorna os eventos de segurança salvos no SQLite
@app.get("/api/security")
def get_security_events(db: Session = Depends(get_db)):
    return db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(30).all()