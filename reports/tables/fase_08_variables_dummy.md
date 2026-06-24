# Fase 8 - Variables dummy

Se agregaron dummies temporales de dia de semana, mes y anio para controlar patrones calendario en la serie diaria.

## Variables agregadas

| grupo | dummies |
| --- | --- |
| dia_semana | 6 |
| mes | 11 |
| anio | 6 |

## Coeficientes principales

| modelo | robusto | variable | coeficiente | error_std | p_value | ci_95_inf | ci_95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OLS dummies temporales | 0 | const | -31.3451 | 3.9038 | 0.0000 | -39.0005 | -23.6897 |
| OLS dummies temporales | 0 | casos_confirmados | -0.0064 | 0.0001 | 0.0000 | -0.0067 | -0.0062 |
| OLS dummies temporales | 0 | hospitalizaciones | 0.5793 | 0.0021 | 0.0000 | 0.5752 | 0.5834 |
| OLS dummies temporales | 1 | const | -31.3451 | 15.3690 | 0.0415 | -61.4839 | -1.2063 |
| OLS dummies temporales | 1 | casos_confirmados | -0.0064 | 0.0007 | 0.0000 | -0.0078 | -0.0051 |
| OLS dummies temporales | 1 | hospitalizaciones | 0.5793 | 0.0181 | 0.0000 | 0.5439 | 0.6147 |

## Metricas

| modelo | nobs | r2 | r2_ajustado | aic | bic | rmse | mae |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OLS dummies temporales | 2,291.0000 | 0.9910 | 0.9909 | 21,509.4658 | 21,658.6212 | 26.1553 | 16.6925 |

## Interpretacion

Las dummies temporales no sustituyen modelos dinamicos, pero ayudan a controlar diferencias sistematicas por calendario antes de pasar a rezagos y ARIMA.
