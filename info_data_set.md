# Individual Household Electric Power Consumption Dataset

## Visão Geral

Este dataset contém medições de consumo de energia elétrica em uma residência individual com taxa de amostragem de um minuto, coletadas ao longo de quase 4 anos. Diferentes quantidades elétricas e alguns valores de sub-medição estão disponíveis.

**Doado em:** 29/08/2012  
**Período de coleta:** Dezembro 2006 - Novembro 2010 (47 meses)  
**Localização:** Sceaux (7km de Paris, França)

## Características do Dataset

- **Tipo:** Multivariado, Série Temporal
- **Área:** Física e Química
- **Tarefas associadas:** Regressão, Clustering
- **Tipo de features:** Real
- **Número de instâncias:** 2.075.259 medições
- **Número de features:** 9
- **Valores faltantes:** Sim (~1,25% das linhas)

## Variáveis

### 1. date
- **Formato:** dd/mm/yyyy
- **Descrição:** Date in format dd/mm/yyyy

### 2. time
- **Formato:** hh:mm:ss
- **Descrição:** time in format hh:mm:ss

### 3. global_active_power
- **Unidade:** kilowatt
- **Descrição:** household global minute-averaged active power (in kilowatt)

### 4. global_reactive_power
- **Unidade:** kilowatt
- **Descrição:** household global minute-averaged reactive power (in kilowatt)

### 5. voltage
- **Unidade:** volt
- **Descrição:** minute-averaged voltage (in volt)

### 6. global_intensity
- **Unidade:** ampere
- **Descrição:** household global minute-averaged current intensity (in ampere)

### 7. sub_metering_1
- **Unidade:** watt-hour of active energy
- **Descrição:** energy sub-metering No. 1 (in watt-hour of active energy)
- **Contexto:** It corresponds to the kitchen, containing mainly a dishwasher, an oven and a microwave (hot plates are not electric but gas powered)

### 8. sub_metering_2
- **Unidade:** watt-hour of active energy
- **Descrição:** energy sub-metering No. 2 (in watt-hour of active energy)
- **Contexto:** It corresponds to the laundry room, containing a washing-machine, a tumble-drier, a refrigerator and a light

### 9. sub_metering_3
- **Unidade:** watt-hour of active energy
- **Descrição:** energy sub-metering No. 3 (in watt-hour of active energy)
- **Contexto:** It corresponds to an electric water-heater and an air-conditioner

## Informações Importantes

```
(global_active_power * 1000/60 - sub_metering_1 - sub_metering_2 - sub_metering_3)
```

### Valores Faltantes

- O dataset contém aproximadamente **1,25% de valores faltantes**
- Todos os timestamps de calendário estão presentes no dataset
- Para alguns timestamps, os valores de medição estão faltando
- Um valor faltante é representado pela **ausência de valor entre dois separadores de ponto-e-vírgula consecutivos**
- **Exemplo:** O dataset mostra valores faltantes em 28 de abril de 2007

### Formato do Arquivo

- **Nome do arquivo:** `household_power_consumption.txt`
- **Tamanho:** 126.8 MB
- **Separador:** Ponto-e-vírgula

## Citação

Hebrail, G. & Berard, A. (2006). Individual Household Electric Power Consumption [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C58K54.

## Licença

Creative Commons Attribution 4.0 International (CC BY 4.0)

Este dataset permite o compartilhamento e adaptação para qualquer propósito, desde que o crédito apropriado seja dado.

## Uso com Python

## Guia para uso do arquivo local

O arquivo `household_power_consumption.txt` pode ser carregado diretamente com pandas:

### Exemplo de leitura do arquivo local
```python
import pandas as pd

# Carregar o arquivo
df = pd.read_csv('household_power_consumption.txt', sep=';', na_values=['?'])

# Visualizar as primeiras linhas
print(df.head())

# Verificar valores faltantes
print(df.isnull().sum())
```

**Dicas:**
- O separador é ponto-e-vírgula (`;`).
- Valores faltantes podem aparecer como campos vazios ou `?`.
- As colunas de data e hora podem ser combinadas para facilitar a análise temporal.

## Aplicações e Citações

Este dataset é amplamente utilizado em pesquisas de:
- **Deep Learning para previsão de séries temporais**
- **Normalizing Flows**
- **Aprendizado não supervisionado de representações para séries temporais multivariadas**
- **Análise de consumo de energia**

**Total de citações:** 29 publicações  
**Total de visualizações:** 160.579

## Keywords

- power consumption
- time series
- energy monitoring
- household electricity
- smart meters
1