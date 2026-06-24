# Fase 6 - Regresion lineal simple

Se estimaron dos modelos OLS con la serie diaria continua guardada en `reports\tables\fase_06_15_series_diarias_continuas.csv`.

## Modelos

```text
defunciones_t = beta0 + beta1 casos_confirmados_t + u_t
defunciones_t = beta0 + beta1 hospitalizaciones_t + u_t
```

## Coeficientes

| modelo | robusto | variable | coeficiente | error_std | p_value | ci_95_inf | ci_95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OLS casos | 0 | const | 78.2146 | 5.4830 | 0.0000 | 67.4623 | 88.9668 |
| OLS casos | 0 | casos_confirmados | 0.0203 | 0.0007 | 0.0000 | 0.0189 | 0.0217 |
| OLS hospitalizaciones | 0 | const | -17.0867 | 1.0987 | 0.0000 | -19.2412 | -14.9322 |
| OLS hospitalizaciones | 0 | hospitalizaciones | 0.5048 | 0.0017 | 0.0000 | 0.5014 | 0.5083 |

## Metricas

| modelo | nobs | r2 | r2_ajustado | aic | bic | rmse | mae |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OLS casos | 2,291.0000 | 0.2650 | 0.2647 | 31,543.5200 | 31,554.9935 | 236.1374 | 153.2445 |
| OLS hospitalizaciones | 2,291.0000 | 0.9733 | 0.9733 | 23,948.6910 | 23,960.1645 | 45.0097 | 25.6613 |

## Interpretacion

El modelo simple con mayor R2 fue `OLS hospitalizaciones`. Esto deja una primera evidencia descriptiva de que las hospitalizaciones y los casos estan asociados positivamente con las defunciones diarias, aunque OLS simple no controla rezagos, persistencia temporal ni autocorrelacion.
