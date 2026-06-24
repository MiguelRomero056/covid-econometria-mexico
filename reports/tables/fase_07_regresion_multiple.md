# Fase 7 - Regresion lineal multiple

## Modelo

```text
defunciones_t = beta0 + beta1 casos_confirmados_t + beta2 hospitalizaciones_t + u_t
```

## Coeficientes OLS y HAC

| modelo | robusto | variable | coeficiente | error_std | p_value | ci_95_inf | ci_95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OLS multiple | 0 | const | -12.4044 | 0.7508 | 0.0000 | -13.8768 | -10.9321 |
| OLS multiple | 0 | casos_confirmados | -0.0060 | 0.0001 | 0.0000 | -0.0063 | -0.0058 |
| OLS multiple | 0 | hospitalizaciones | 0.5531 | 0.0015 | 0.0000 | 0.5501 | 0.5560 |
| OLS multiple | 1 | const | -12.4044 | 2.0273 | 0.0000 | -16.3799 | -8.4290 |
| OLS multiple | 1 | casos_confirmados | -0.0060 | 0.0007 | 0.0000 | -0.0073 | -0.0047 |
| OLS multiple | 1 | hospitalizaciones | 0.5531 | 0.0143 | 0.0000 | 0.5250 | 0.5812 |

## Metricas

| modelo | nobs | r2 | r2_ajustado | aic | bic | rmse | mae |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OLS multiple | 2,291.0000 | 0.9877 | 0.9877 | 22,171.9248 | 22,189.1350 | 30.5288 | 17.9658 |

## Interpretacion

La regresion multiple permite comparar el aporte contemporaneo de casos confirmados y hospitalizaciones. La lectura principal debe hacerse con la version HAC porque la serie diaria presenta alta persistencia temporal.
