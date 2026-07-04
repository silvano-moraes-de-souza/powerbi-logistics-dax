# Logistics Dashboard - Power BI Implementation Guide

Follow these steps to complete your `DASH LOGISTICA.pbix` file using the `BASE LOGISTICA.csv` data.

## 1. Data Import (Power Query)
1. Open Power BI Desktop.
2. Click **Get Data** > **Text/CSV**.
3. Select `BASE LOGISTICA.csv`.
4. In the preview, ensure the delimiter is set to **Semicolon (;)**.
5. Click **Transform Data**.
6. **Rename Table:** Change the table name to `Fato_Logistica`.
7. **Format Date:**
   - Right-click the `Data` column > **Change Type** > **Using Locale...**.
   - Data Type: **Date**.
   - Locale: **Portuguese (Brazil)**.
8. **Format Numbers:**
   - Ensure `Volume`, `Valor Faturamento`, and `Custo de Frete` are set to **Decimal Number**.
9. Click **Close & Apply**.

## 2. DAX Measures
Create a new table for measures or add these to your `Fato_Logistica` table:

```dax
-- FINANCIALS
Faturamento Total = SUM('Fato_Logistica'[Valor Faturamento])

Custo Frete Total = SUM('Fato_Logistica'[Custo de Frete])

Lucro Bruto = [Faturamento Total] - [Custo Frete Total]

Margem Percentual = DIVIDE([Lucro Bruto], [Faturamento Total], 0)

Custo Logístico % = DIVIDE([Custo Frete Total], [Faturamento Total], 0)

-- LOGISTICS KPIs
Volume Total = SUM('Fato_Logistica'[Volume])

KPI Rotas = 
DISTINCTCOUNTNOBLANK(
    CONCATENATE('Fato_Logistica'[Estado_Origem], 
    CONCATENATE("-", 'Fato_Logistica'[Estado_Destino]))
)

-- SIMULATED KPIs (Based on available data)
Lead Time Médio = 
AVERAGEX(
    'Fato_Logistica',
    DATEDIFF(
        'Fato_Logistica'[Data], 
        'Fato_Logistica'[Data] + ROUND(RAND() * 5 + 1, 0), -- Simulated delivery logic
        DAY
    )
)

Ocupação Frota = 
DIVIDE(
    [Volume Total], 
    DISTINCTCOUNT('Fato_Logistica'[Transportadora]) * 1000, -- Assuming 1000 unit capacity per carrier
    0
)

Atrasos = 
COUNTROWS(
    FILTER(
        'Fato_Logistica',
        'Fato_Logistica'[Volume] > 400 -- Simple logic: large volumes tend to delay
    )
)
```

## 3. Visualization Mapping
- **Map:** Use the "Filled Map" or "Azure Map". Use `Estado_Destino` as Location. Use `Faturamento Total` as Tooltip.
- **KPI Cards:** Use `Faturamento Total`, `Margem Percentual`, `Volume Total`, and `Lead Time Médio`.
- **Bar Chart:** `Transportadora` vs `Custo Frete Total`.
- **Line Chart:** `Mes` vs `Faturamento Total` (ensure a Calendar table is connected for time intelligence).

## 4. Theme Configuration
- Go to the **View** tab > Click the dropdown > **Browse for themes**.
- Use the **Dark** theme or create a custom one with:
  - Background: `#14161d`
  - Accent 1: `#81ecff` (Cyan)
  - Accent 2: `#b085ff` (Purple)
