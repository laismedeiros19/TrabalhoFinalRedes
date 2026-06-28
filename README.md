# 🌐 NetWatch — Plataforma de Monitoramento de Rede e Resposta a Incidentes

**Contexto Acadêmico:** Instituto de Desenvolvimento e Pesquisa (IDP)
**Disciplina:** Redes de Computadores
**Orientadora:** Prof.ª Lorena Borges
**Alunas:** Lais Medeiros e Gabriela Suares
**Ano:** 2026

---

## 📝 Descrição do Projeto

O **NetWatch** é um ecossistema de telemetria e monitoramento de infraestrutura distribuída em tempo real. O sistema foi projetado para coletar, persistir e renderizar métricas vitais de quatro serviços essenciais de rede (Web Server, Banco de Dados, DNS e SMTP), além de atuar ativamente na auditoria de segurança e resposta automatizada a incidentes (NOC/SOC Alerting) via simulação de envelopes de rede do protocolo SMTP.

---

## 🏗️ Arquitetura e Engenharia do Sistema

O projeto é dividido em três camadas principais operando de forma assíncrona:

1. **Backend (API REST):** Desenvolvido em **FastAPI (Python)** e estruturado com persistência em banco de dados relacional **SQLite**. Ele expõe endpoints para recebimento de métricas (`/api/metrics`) e logs de segurança (`/api/security`), processando regras de limiares operacionais (*thresholds*).
2. **Frontend (Dashboard):** Uma interface rica de visualização construída com **HTML5 estrutural, CSS3 (variáveis modernas) e JavaScript Vanilla**. Utiliza a biblioteca **Chart.js** para renderização de gráficos temporais de linhas com eixos dinâmicos reativos.
3. **Agente (Controlador de Incidentes):** Um script em Python responsável por injetar cargas de telemetria e simular anomalias de redes complexas para validação do ecossistema.

---

## 🚨 Cenários de Redes e Segurança Simulados

O painel interativo permite injetar 5 estados distintos para avaliar o comportamento do monitoramento:

### [1] Estado Normal (Baseline)

- **Comportamento:** Todos os ativos operando nos níveis ideais de SLA. O dashboard renderiza cartões em verde e status `OK`.
- **Métricas:** Latência Web estável (~45ms), tráfego balanceado e zero falhas.

### [2] Ataque DDoS de Camada 7 (Web Server Flood)

- **Comportamento:** Simulação de um bombardeio volumétrico de requisições maliciosas.
- **Métricas:** O tráfego de **RPS (Requisições por Segundo)** explode para mais de 95.000, a **Latência** vai ao teto (~4500ms) e a disponibilidade cai para 0, alterando o status do painel para `CRÍTICO`.
- **Segurança:** Injeta um log de auditoria isolando o IP do atacante.

### [3] Ataque de Força Bruta e Pane Seca (Database Downtime)

- **Comportamento:** Simulação de um ataque *Brute-force* contra o usuário `root` na porta padrão `3306`. O estouro de conexões simultâneas esgota os recursos, derrubando o banco.
- **Métricas:** **QPS (Consultas por Segundo)** e **Uso de CPU** despencam verticalmente para `0.0`.
- **Gatilho de Alerta:** O backend detecta a violação do limiar e gera no console o log técnico estruturado do **envelope do protocolo SMTP (RFC 5322)**, simulando a notificação imediata da equipe de suporte.

### [4] Exaustão Criptográfica DNS (CVE-2023-50387 - KeyTrap)

- **Comportamento:** Exploração de uma vulnerabilidade lógica real no protocolo **DNSSEC** dentro do servidor **BIND9**. O envio de assinaturas inválidas cruzadas coloca o processador do servidor em loop infinito.
- **Métricas:** O tempo de resposta estoura para 5200ms e o gráfico de **Falhas/s** dá um salto vertical na tela.

### [5] Inundação SMTP (Email Bombing / Spam)

- **Comportamento:** Ataque de negação de serviço direcionado ao Mail Transfer Agent (MTA).
- **Métricas:** A fila de mensagens (*Queue Length*) acumula milhares de e-mails presos, a taxa de entrega legítima cai para `18.5%` e o volume por minuto vai ao topo.

---

## ⚙️ Como Executar o Projeto (Guia de Implantação)

Para rodar o ecossistema, certifique-se de ter as dependências instaladas (`pip install fastapi uvicorn requests`) e abra **três terminais separados** no seu ambiente de desenvolvimento:

### Terminal 1 — Servidor de API (Backend)

```bash
uvicorn backend.app.main:app --reload --port 8000
```

> **Nota:** Se estiver utilizando o GitHub Codespaces, altere a visibilidade da porta 8000 para "Pública" na aba **Ports**.

### Terminal 2 — Servidor Web Estático (Frontend)

```bash
python3 -m http.server 3000 --directory frontend
```

### Terminal 3 — Orquestrador de Ataques (Agente)

```bash
python3 agents/controlador.py
```

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologias |
|---|---|
| **Linguagens** | Python 3.12, JavaScript (ES6+), HTML5, CSS3 |
| **Frameworks / Libs** | FastAPI, Uvicorn, Chart.js (v4) |
| **Banco de Dados** | SQLite (com SQLAlchemy / Driver Nativo) |
| **Protocolos** | HTTP/HTTPS, SMTP (Transmissão de Alertas), DNS/DNSSEC (Validação de Chaves) |