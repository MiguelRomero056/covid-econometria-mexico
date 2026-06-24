# Fase 13 - Modelo de ajuste parcial

## Modelo

```text
defunciones_t = beta0 + gamma defunciones_t-1 + rezagos de casos y hospitalizaciones + u_t
```

## Coeficientes

| modelo | robusto | variable | coeficiente | error_std | p_value | ci_95_inf | ci_95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ajuste parcial | 0 | const | 2.2575 | 1.7203 | 0.1896 | -1.1160 | 5.6310 |
| Ajuste parcial | 0 | defunciones_lag_1 | 0.9952 | 0.0459 | 0.0000 | 0.9051 | 1.0853 |
| Ajuste parcial | 0 | casos_confirmados_lag_1 | 0.0016 | 0.0008 | 0.0404 | 0.0001 | 0.0031 |
| Ajuste parcial | 0 | casos_confirmados_lag_7 | 0.0049 | 0.0012 | 0.0001 | 0.0025 | 0.0072 |
| Ajuste parcial | 0 | casos_confirmados_lag_14 | -0.0063 | 0.0007 | 0.0000 | -0.0077 | -0.0049 |
| Ajuste parcial | 0 | hospitalizaciones_lag_1 | -0.2677 | 0.0274 | 0.0000 | -0.3215 | -0.2139 |
| Ajuste parcial | 0 | hospitalizaciones_lag_7 | 0.1983 | 0.0129 | 0.0000 | 0.1730 | 0.2235 |
| Ajuste parcial | 0 | hospitalizaciones_lag_14 | 0.0633 | 0.0106 | 0.0000 | 0.0425 | 0.0841 |
| Ajuste parcial | 1 | const | 2.2575 | 1.3801 | 0.1020 | -0.4488 | 4.9638 |
| Ajuste parcial | 1 | defunciones_lag_1 | 0.9952 | 0.1494 | 0.0000 | 0.7023 | 1.2881 |
| Ajuste parcial | 1 | casos_confirmados_lag_1 | 0.0016 | 0.0014 | 0.2685 | -0.0012 | 0.0044 |
| Ajuste parcial | 1 | casos_confirmados_lag_7 | 0.0049 | 0.0015 | 0.0015 | 0.0019 | 0.0079 |
| Ajuste parcial | 1 | casos_confirmados_lag_14 | -0.0063 | 0.0011 | 0.0000 | -0.0084 | -0.0042 |
| Ajuste parcial | 1 | hospitalizaciones_lag_1 | -0.2677 | 0.0906 | 0.0032 | -0.4453 | -0.0901 |
| Ajuste parcial | 1 | hospitalizaciones_lag_7 | 0.1983 | 0.0263 | 0.0000 | 0.1466 | 0.2499 |
| Ajuste parcial | 1 | hospitalizaciones_lag_14 | 0.0633 | 0.0285 | 0.0263 | 0.0075 | 0.1192 |

## Metricas

| modelo | nobs | r2 | r2_ajustado | aic | bic | rmse | mae |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ajuste parcial | 2,277.0000 | 0.9440 | 0.9438 | 25,509.9180 | 25,555.7629 | 65.3135 | 26.4551 |

## Persistencia

Coeficiente de `defunciones_lag_1`: `0.9952`. Velocidad de ajuste aproximada `1 - gamma`: `0.0048`.

## Interpretacion

Un coeficiente positivo y alto de `defunciones_lag_1` apoya H3: las defunciones diarias presentan persistencia temporal.
