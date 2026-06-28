# 🌐 NetWatch — Plataforma de Monitoramento de Rede e Resposta a Incidentes

**Contexto Acadêmico:** Instituto de Desenvolvimento e Pesquisa (IDP)
**Disciplina:** Redes de Computadores e Internet
**Orientadora:** Prof.ª Lorena Borges
**Autor:** Laís Medeiros e Gabriela Suares
**Ano:** 2026

---

## 📝 Descrição do Projeto

O **NetWatch** é um ecossistema de telemetria, auditoria de segurança e monitoramento de infraestrutura distribuída em tempo real. Projetado para coletar, persistir e renderizar métricas de quatro serviços essenciais de rede (Web Server, Banco de Dados, DNS e SMTP), o sistema atua ativamente na detecção de anomalias, análise de vulnerabilidades conhecidas por serviço e resposta automatizada a incidentes (NOC/SOC Alerting) via simulação de logs do protocolo SMTP.

---

## 🏗️ Arquitetura e Engenharia do Sistema

O projeto é estruturado em três camadas assíncronas independentes:

1. **Backend (API REST):** Desenvolvido em **FastAPI (Python)** com persistência de dados em banco relacional **SQLite** (`devops_monitor.db`). É responsável por receber as telemetrias, avaliar os limiares operacionais (*thresholds*) de alerta e disparar gatilhos automáticos.
2. **Frontend (Dashboard):** Uma interface rica em detalhes visuais construída em **HTML5, CSS3 modernos e JavaScript Vanilla**. Utiliza a biblioteca **Chart.js** para plotagem temporal reativa e eixos dinâmicos.
3. **Agente (Controlador de Incidentes):** Um orquestrador em Python (`controlador.py`) encarregado de injetar cargas de rede e simular os ataques cibernéticos e panes para validação do ecossistema.

---

## 🚨 Cenários de Redes e Segurança Simulados

O painel interativo do controlador permite alternar entre **6 cenários distintos** para testar a resiliência do monitoramento:

### [1] Estado Normal (Baseline)

- **Comportamento:** Todos os ativos operando nos níveis ideais de SLA. Os cartões da visão consolidada exibem o status `OK` em verde.
- **Métricas:** Latência Web estável (~45ms), RPS flutuando de forma realista (110–135) e zero falhas de rede.

### [2] Ataque DDoS de Camada 7 (Web Server Flood)

- **Comportamento:** Simulação de um bombardeio volumétrico massivo contra o servidor de aplicação.
- **Métricas:** O tráfego de **RPS (Requisições por Segundo)** explode para a faixa de 95.000 a 105.000, a **Latência** vai ao teto (~4500ms) e a disponibilidade cai para `0%`, alterando o status do painel para `CRÍTICO`.
- **Segurança:** O feed registra a anomalia isolando o IP de origem do atacante.

### [3] Força Bruta e Queda de Serviço (Database Downtime)

- **Comportamento:** Ataque de *Brute-force* contra o usuário `root` na porta padrão `3306`. O esgotamento de recursos força a queda deliberada do banco.
- **Métricas:** As métricas de **QPS (Consultas por Segundo)** e **Uso de CPU** despencam instantaneamente para `0.0`.
- **Notificação SMTP:** O backend detecta a indisponibilidade e renderiza no console o log técnico de transmissão do envelope estruturado do protocolo **SMTP (RFC 5322)**, simulando o alerta imediato enviado ao time de DevOps (NOC).

### [4] Exaustão Criptográfica DNS (CVE-2023-50387 - KeyTrap)

- **Comportamento:** Exploração de uma vulnerabilidade lógica real no protocolo **DNSSEC** dentro do servidor **BIND9**. O envio de pacotes maliciosos com assinaturas cruzadas inválidas trava a CPU do servidor de nomes.
- **Métricas:** O tempo de resposta de resolução salta para `5200ms` e o gráfico de **Falhas/s** dá um pico vertical de `150.0` falhas na tela.

### [5] Inundação SMTP (Email Bombing / Spam Massivo)

- **Comportamento:** Ataque DoS direcionado ao Mail Transfer Agent (MTA) para estrangular o fluxo de saída de e-mails.
- **Métricas:** A fila de mensagens (*Queue Length*) acumula `4.850` e-mails presos no backlog, a taxa de entrega legítima desce para `18.5%` e o volume por minuto atinge o pico anômalo de `950 e-mails/m`.

### [6] Alteração de Configuração (Integridade de Arquivos)

- **Comportamento:** Monitoramento de integridade focado na detecção de mudanças não autorizadas em arquivos críticos de infraestrutura (FIM).
- **Segurança:** O agente simula a quebra de hash criptográfico **MD5** do arquivo `/etc/nginx/nginx.conf`. O painel incrementa o contador global de configurações alteradas para `1` e adiciona um alerta de nível `ATENÇÃO` no feed de auditoria.

---

## ⚙️ Como Executar o Ecossistema (Guia de Implantação)

Para rodar a plataforma localmente ou no GitHub Codespaces, garanta que possui as dependências instaladas (`pip install fastapi uvicorn requests`) e inicie **três terminais separados**:

### Terminal 1 — API REST (Backend)

```bash
uvicorn backend.app.main:app --reload --port 8000
```

> **Nota:** No GitHub Codespaces, lembre-se de alterar a visibilidade da porta 8000 para "Pública" na aba **Ports**.

### Terminal 2 — Dashboard Web (Frontend)

```bash
python3 -m http.server 3000 --directory frontend
```

### Terminal 3 — Injetor de Ataques (Agente)

```bash
python3 agents/controlador.py
```

---

## 🛠️ Tecnologias e Protocolos Utilizados

| Categoria | Detalhes |
|---|---|
| **Linguagens** | Python 3.12, JavaScript (ES6+), HTML5, CSS3 (Custom Properties) |
| **Frameworks e Bibliotecas** | FastAPI (Python), Chart.js v4 (Gráficos), Uvicorn (Servidor ASGI) |
| **Persistência** | SQLite3 com mapeamento relacional |
| **Conceitos de Redes** | HTTP (Chamadas da API), DNSSEC (Validação de chaves), SMTP (Mensageria e envelopes de alerta), Análise de Vulnerabilidades (CVEs) |