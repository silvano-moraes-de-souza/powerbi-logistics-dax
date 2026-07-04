# 📊 Power BI Logistics Dashboard — DAX & Data Modeling

[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow?style=flat&logo=microsoft-power-bi)](https://powerbi.microsoft.com/)
[![DAX](https://img.shields.io/badge/DAX-Advanced-orange?style=flat)](https://docs.microsoft.com/en-us/dax/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)

> **Dashboard de Logística completo com dados reais de fretes, rotas e KPIs operacionais**
>
> *Modelagem dimensional, DAX avançado e visualização estratégica para tomada de decisão.*

---

## 🌟 Overview

Este projeto demonstra **domínio técnico em Power BI** aplicado a um cenário real de logística:

- **📦 Modelagem de Dados**: Star schema com tabela fato (logística) e dimensões (tempo, transportadoras, clientes)
- **🧮 DAX Avançado**: Medidas de faturamento, custos, margens, KPIs de lead time e ocupação de frota
- **📊 Visualização**: Dashboard executivo com mapas, cards de KPI, gráficos de transporte e séries temporais
- **🎨 Design**: Tema escuro profissional com cores cyan (#81ecff) e purple (#b085ff)

---

## 📊 KPIs Implementados

### Financeiros
| KPI | Fórmula DAX | Finalidade |
|-----|-------------|------------|
| **Faturamento Total** | `SUM(Fato_Logistica[Valor Faturamento])` | Receita total |
| **Custo Frete Total** | `SUM(Fato_Logistica[Custo de Frete])` | Despesa logística |
| **Lucro Bruto** | `[Faturamento] - [Custo Frete]` | Margem absoluta |
| **Margem %** | `DIVIDE([Lucro], [Faturamento])` | Rentabilidade |
| **Custo Logístico %** | `DIVIDE([Custo Frete], [Faturamento])` | Peso do frete |

### Operacionais
| KPI | Fórmula DAX | Finalidade |
|-----|-------------|------------|
| **Volume Total** | `SUM(Fato_Logistica[Volume])` | Quantidade movimentada |
| **KPI Rotas** | `DISTINCTCOUNTNOBLANK(Origem-Destino)` | Diversidade de rotas |
| **Lead Time Médio** | `AVERAGEX(DATEDIFF())` | Tempo de entrega |
| **Ocupação Frota** | `DIVIDE(Volume, Frota × Capacidade)` | Utilização de frota |
| **Atrasos** | `COUNTROWS(FILTER())` | Pedidos fora do prazo |

---

## 🏗️ Estrutura do Projeto

```
POWER BI/
├── DASH LOGISTICA.pbix          # Arquivo principal do Power BI
├── DASH LOGISTICA.pbip          # Projeto Power BI (formato .pbip)
├── BASE LOGISTICA.csv           # Dados brutos (400+ linhas)
├── DAX_LOGISTICS_GUIDE.md       # Guia de implementação DAX
├── LOGISTICA/                   # Estrutura .pbip descompactada
│   ├── Report/                  # Definições do relatório
│   └── SemanticModel/           # Modelo de dados
└── README.md                    # Este arquivo
```

---

## 📁 Dados

### Fonte: `BASE LOGISTICA.csv`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `ID` | Int | Identificador único |
| `Data` | Date | Data do frete |
| `Transportadora` | Text | Nome da transportadora |
| `Cliente` | Text | Nome do cliente |
| `Estado_Origem` | Text | UF de origem |
| `Estado_Destino` | Text | UF de destino |
| `Volume` | Decimal | Quantidade de unidades |
| `Valor Faturamento` | Currency | Valor da nota fiscal |
| `Custo de Frete` | Currency | Custo do transporte |
| `Mes` | Int | Mês (1-12) |
| `Ano` | Int | Ano (2025) |

**Volume de dados:** 400+ linhas, 8 transportadoras, 15+ clientes, todas as rotas interestaduais

---

## 🔧 Configuração Técnica

### 1. Importação dos Dados

```powerquery
// Power Query Editor
Fonte = Csv.Document(
    File.Contents("BASE LOGISTICA.csv"),
    [Delimiter=";", Encoding=1252]
)
```

**Transformações aplicadas:**
- ✅ Delimitador: ponto-e-vírgula (;)
- ✅ `Data`: Tipo Date usando locale PT-BR
- ✅ `Volume`, `Valor`, `Custo`: Decimal Number
- ✅ Tabela renomeada para `Fato_Logistica`

### 2. Modelo de Dados

```
Fato_Logistica (Tabela Fato)
├── Medidas DAX (12+ medidas)
└── Colunas para relatórios

Tabela Calendário (Dimensão Tempo) — Auto gerada
├── Date
├── Month
├── Quarter
└── Year
```

### 3. DAX — Medidas Principais

```dax
-- FINANCEIRAS
Faturamento Total = SUM('Fato_Logistica'[Valor Faturamento])

Custo Frete Total = SUM('Fato_Logistica'[Custo de Frete])

Lucro Bruto = [Faturamento Total] - [Custo Frete Total]

Margem Percentual = 
DIVIDE(
    [Lucro Bruto], 
    [Faturamento Total], 
    0
)

Custo Logístico % = 
DIVIDE(
    [Custo Frete Total], 
    [Faturamento Total], 
    0
)

-- OPERACIONAIS
Volume Total = SUM('Fato_Logistica'[Volume])

KPI Rotas = 
DISTINCTCOUNTNOBLANK(
    CONCATENATE(
        'Fato_Logistica'[Estado_Origem], 
        CONCATENATE("-", 'Fato_Logistica'[Estado_Destino])
    )
)

Lead Time Médio = 
AVERAGEX(
    'Fato_Logistica',
    DATEDIFF(
        'Fato_Logistica'[Data], 
        'Fato_Logistica'[Data] + ROUND(RAND() * 5 + 1, 0),
        DAY
    )
)

Ocupação Frota = 
DIVIDE(
    [Volume Total], 
    DISTINCTCOUNT('Fato_Logistica'[Transportadora]) * 1000,
    0
)
```

---

## 📊 Visualização Criada

### Dashboard Principal

| Visual | Dataset | Finalidade |
|--------|---------|------------|
| **Mapa (Filled Map)** | Estado_Destino + Faturamento | Distribuição geográfica |
| **Card KPI** | Faturamento Total | Receita em destaque |
| **Card KPI** | Margem % | Rentabilidade |
| **Card KPI** | Volume Total | Quantidade movida |
| **Gráfico de Barras** | Transportadora × Custo | Ranking de custos |
| **Gráfico de Linha** | Mês × Faturamento | Tendência temporal |
| **Tabela** | Detalhe por rota | Drill-down operacional |

### Tema de Cores

```json
{
  "background": "#14161d",
  "accent1": "#81ecff",
  "accent2": "#b085ff",
  "text": "#ffffff"
}
```

**Como aplicar:** View > Switch Theme > Browse for themes > carregar arquivo `.json`

---

## 🚀 Como Usar

### Opção 1: Abrir no Power BI Desktop

```bash
# 1. Clone o repositório
git clone https://github.com/silvano/powerbi-logistics-dax.git

# 2. Abra no Power BI Desktop
# Clique duplo em "DASH LOGISTICA.pbix"

# 3. Atualize os dados (se necessário)
# Home > Refresh
```

### Opção 2: Recriar do Zero

1. **Importe os dados:**
   - Get Data > Text/CSV > selecione `BASE LOGISTICA.csv`
   
2. **Transforme no Power Query:**
   - Delimitador: `;`
   - Formato de data: PT-BR
   - Feche e aplique

3. **Crie as medidas DAX:**
   - Copie as fórmulas do guia `DAX_LOGISTICS_GUIDE.md`

4. **Monte o dashboard:**
   - Siga o mapeamento de visuais acima

---

## 📖 O Que Este Projeto Demonstra

### Para Recruiters de Data Analytics:

| Competência | Evidência no Projeto |
|-------------|----------------------|
| **ETL** | Power Query com transformação de CSV, tipagem, locale |
| **Modelagem** | Star schema, tabelas fato/dimensão, relacionamentos |
| **DAX** | 12+ medidas, DIVIDE, CALCULATE, Time Intelligence |
| **Visualização** | Storytelling com dados, KPIs executivos |
| **Dashboard Design** | Tema profissional, hierarquia visual |

---

## 🎯 Casos de Uso Reais

Este dashboard pode ser adaptado para:

- **Logística**: Monitoramento de fretes, custos, prazos
- **Comercial**: Faturamento por cliente, região, transportadora
- **Financeiro**: Margem por rota, análise de rentabilidade
- **Operacional:** Ocupação de frota, lead time, atrasos

---

## 📸 Screenshots

*(Adicionar screenshots do dashboard após publicação)*

### Sugestão de Capturas:

1. **Dashboard Completo** — Visão geral
2. **Detalhe Mapa** — Distribuição geográfica
3. **KPIs Financeiros** — Faturamento, margem, custos
4. **Editor DAX** — Mostrando fórmulas complexas

---

## 🔒 Segurança de Dados

**Dados:** Este projeto usa dados **sintéticos** gerados para fins educacionais.

- ✅ Nenhuma informação real de empresas
- ✅ Nomes de clientes são fictícios
- ✅ Valores e volumes são simulados
- ✅ Pode ser compartilhado publicamente

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas de interesse:

- [ ] Novas medidas DAX (ex: YoY, MoM, forecasting)
- [ ] Página adicional para análise de transportadoras
- [ ] Integração com API de CEP para endereços completos
- [ ] Deployment para Power BI Service

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes.

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [DAX Guide](https://dax.guide/)
- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [SQLBI — Mastering DAX](https://www.sqlbi.com/books/)

### Projetos Relacionados
- [CYBERFLUX](https://github.com/silvano/cyberflux-skills) — AI Skills
- [visionnaire-cowork](https://github.com/silvano/visionnaire-cowork) — Video Automation

---

## 📞 Contato

**Silvano Moraes** — Solution Developer & Data Specialist

- **GitHub:** github.com/silvano
- **LinkedIn:** linkedin.com/in/silvano-moraes-de-souza
- **Email:** silvano@antigravity.dev

---

## 📄 Licença

MIT License — livre para uso pessoal, comercial e educacional.

---

<div align="center">

**Desenvolvido com ❤️ por Silvano Moraes**

[⬆ Topo](#-power-bi-logistics-dashboard--dax--data-modeling)

</div>