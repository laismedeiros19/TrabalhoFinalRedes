# NetWatch — Plataforma Integrada de Telemetria, Alertas e Auditoria de Redes

A plataforma **NetWatch** é uma solução completa de monitoramento distribuído focada na análise de performance de ativos corporativos e na auditoria ativa de eventos de segurança cibernética. Este projeto foi desenvolvido como requisito avaliativo prático final para a disciplina de **Redes de Computadores I**, no **Instituto Brasileiro de Ensino, Desenvolvimento e Pesquisa (IDP)** em Brasília.

---

## 🏗️ 1. Arquitetura da Solução e Estrutura de Arquivos

O ecossistema adota o padrão arquitetural de **Sistemas Distribuídos Baseados em Eventos**, operando de forma totalmente desacoplada em três camadas independente:

```text
📂 TrabalhoFinalRedes (Raiz do Repositório)
├── 📂 agents
│   └── 📄 monitor.py             # Agente autônomo de coleta e telemetria de infraestrutura
├── 📂 backend
│   └── 📂 app
│       ├── 📄 database.py        # Configuração do engine e sessão do banco SQLite
│       ├── 📄 main.py            # Endpoints da API FastAPI e Motor de Regras de Alerta
│       └── 📄 models.py          # Modelos relacionais (Métricas e Eventos de Segurança)
├── 📂 frontend
│   ├── 📄 index.html             # Estrutura visual e painéis reativos do Dashboard
│   └── 📂 src
│       ├── 📄 dashboard.js       # Polling assíncrono, Chart.js e manipulação dinâmica do DOM
│       └── 📄 styles.css         # Identidade visual avançada baseada em Dark Mode
├── 📄 .gitignore                 # Filtro de exclusão de binários locais e cache
├── 📄 architecture.md            # Detalhamento técnico estrutural do ecossistema
└── 📄 requirements.txt           # Dependências obrigatórias do ecossistema Python

Divisão de Responsabilidades

    Agente de Coleta (agents/monitor.py): Script independente encarregado de interagir com APIs do sistema operacional e sockets de rede, empacotando telemetrias estruturadas em JSON e despachando-as via requisições HTTP REST (POST).

    Backend Engine (backend/app/): API construída sobre o ecossistema de alta performance FastAPI. Recebe os fluxos de dados, submete as variáveis ao mecanismo interno de avaliação de limites operacionais (thresholds) e persiste os registros em um banco relacional local SQLite via SQLAlchemy ORM.

    Front-end Reativo (frontend/): Interface web construída puramente com linguagens nativas (HTML5, CSS3, JS Vanilla). Consome assincronamente as rotas do backend por meio de requisições estruturadas com a Fetch API em ciclos de polling de 5 segundos, populando dinamicamente gráficos de linhas temporais com a biblioteca Chart.js.

📊 2. Monitoramento de Métricas por Serviço (Seção 3 do PDF)

Em total conformidade com as diretrizes do projeto, o sistema inspeciona ativamente quatro pilares de infraestrutura fundamentais:
3.1 Web Server (HTTP/HTTPS)

    Disponibilidade: Verificação ativa de resposta de sockets de aplicação (HTTP Status Check).

    Requests por Segundo (RPS): Volume total de requisições concorrentes processadas por segundo.

    Latência: Tempo de ida e volta do pacote (Round-Trip Time - RTT) aferido em milissegundos (ms).

    Taxa de Erros: Percentual de respostas de falha na camada de aplicação (famílias HTTP 4xx e 5xx).

    Conexões Ativas: Mapeamento de conexões simultâneas concorrentes ativas estabelecidas no host.

3.2 Banco de Dados (SQL/NoSQL)

    Disponibilidade / QPS: Monitoramento de consultas por segundo processadas pela engine relacional.

    Métricas do Host (CPU e Memória): Coleta em tempo real do consumo de hardware obtidos nativamente via biblioteca psutil.

    Queries Lentas (Slow Queries) / Erros: Rastreamento de transações falhas, rollbacks e timeouts estruturais.

    Armazenamento: Tamanho volumétrico ocupado fisicamente em disco mensurado em Gigabytes (GB).

3.3 Servidor de Nomes (DNS)

    Tempo de Resposta: Tempo gasto para efetuar uma resolução de nomes UDP ativa na porta 53 contra servidores de borda (8.8.8.8).

    Taxa de Falhas: Mapeamento de erros de tradução ou expiração de timeouts de requisição (failed resolutions).

3.4 Serviço de Mensageria (SMTP)

    Taxa de Entrega: Eficiência percentual de despachos de mensagens processados com sucesso.

    Fila de E-mails (Queue Length): Backlog acumulativo de mensagens aguardando liberação nos buffers de saída.

🚦 3. Mecanismo de Alertas e Notificações (Seção 4 do PDF)

O backend possui uma engrenagem de auditoria analítica que intercepta cada payload inserido e classifica os estados do sistema em três níveis rigorosos:

    🟢 Nível 1 — Verde (OK): Operação normal e saudável. Os cards do front-end adotam uma identidade visual padrão estável.

    🟡 Nível 2 — Amarelo (Atenção): Indica flutuação operacional ou degradação parcial (Ex: latência excedendo 200ms ou taxa de erro acima de 2%). O front-end destaca o card do serviço em modo de observação e o backend emite um log estruturado simulando o envio de um e-mail de alerta corporativo via SMTP.

    🔴 Nível 3 — Vermelho (Crítico): Indica falha grave generalizada ou total indisponibilidade do ativo (Disponibilidade em 0%). O card do dashboard pisca em vermelho e o motor de regras gera um disparo prioritário de notificação emergencial no terminal para mobilização imediata dos analistas de infraestrutura.

🛡️ 4. Painel de Segurança e Monitoramento Extra (Seção 5 do PDF)

Além da saúde operacional, o ecossistema embeleza uma camada integrada de monitoramento contra incidentes e anomalias de segurança cibernética:

    Indicadores de DDoS: Monitoramento e correlação de picos súbitos de tráfego volumétrico na camada de aplicação (Camada 7).

    Detecção de Brute-Force: Rastreamento de taxas excessivas de falhas de autenticação de usuários por credenciais ou IPs focados no banco de dados.

    Auditoria de Configurações: Mecanismo de checagem automatizada de integridade estrutural através de cruzamento de hashes criptográficos em arquivos vitais (como o arquivo nginx.conf).

    Vulnerabilidades Conhecidas: Auditoria contínua de CVEs em softwares ativos, incluindo o registro da falha estrutural real CVE-2023-50387 (KeyTrap) no escopo do DNS.

🧭 5. Manual de Execução e Deploy Local
Instalação das Dependências

Para instalar as bibliotecas necessárias declaradas no projeto (fastapi, uvicorn, sqlalchemy, psutil, dnspython), execute:
Bash

pip install -r requirements.txt

Inicialização do Ecossistema em Três Passos

    Passo 1 — API e Banco de Dados (Terminal 1):
    Bash

    uvicorn backend.app.main:app --reload --port 8000

    Passo 2 — Inicialização do Agente Coletor (Terminal 2):
    Bash

    python3 agents/monitor.py

    Passo 3 — Inicialização do Servidor Front-end (Terminal 3):
    Bash

    python3 -m http.server 3000 --directory frontend

    ⚙️ Configuração de Proxy no GitHub Codespaces: Na aba Portas (Ports) da sua IDE, selecione a porta 8000 (backend), clique com o botão direito e altere a visibilidade de Private para Public. Essa etapa é indispensável para que o código JavaScript executado localmente pelo seu navegador web consiga cruzar o proxy seguro e acessar as rotas REST da API.

NetWatch • IDP • 2026
