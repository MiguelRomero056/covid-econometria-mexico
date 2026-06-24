# Fase 12 - Rezagos distribuidos

Se estimaron rezagos de 1, 7 y 14 dias para casos confirmados y hospitalizaciones.

## Metricas

| modelo | nobs | r2 | r2_ajustado | aic | bic | rmse | mae |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rezagos casos | 2,277.0000 | 0.2774 | 0.2765 | 31,326.1538 | 31,349.0763 | 234.6574 | 150.9432 |
| Rezagos hospitalizaciones | 2,277.0000 | 0.9186 | 0.9185 | 26,354.5109 | 26,377.4333 | 78.7610 | 38.2506 |
| Rezagos combinados | 2,277.0000 | 0.9324 | 0.9323 | 25,935.8758 | 25,975.9901 | 71.7489 | 31.4141 |

## Coeficientes

| modelo | robusto | variable | coeficiente | error_std | p_value | ci_95_inf | ci_95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rezagos casos | 0 | const | 71.3977 | 5.5834 | 0.0000 | 60.4486 | 82.3468 |
| Rezagos casos | 0 | casos_confirmados_lag_1 | 0.0160 | 0.0022 | 0.0000 | 0.0116 | 0.0204 |
| Rezagos casos | 0 | casos_confirmados_lag_7 | -0.0057 | 0.0037 | 0.1201 | -0.0129 | 0.0015 |
| Rezagos casos | 0 | casos_confirmados_lag_14 | 0.0122 | 0.0022 | 0.0000 | 0.0080 | 0.0165 |
| Rezagos casos | 1 | const | 71.3977 | 15.3383 | 0.0000 | 41.3192 | 101.4761 |
| Rezagos casos | 1 | casos_confirmados_lag_1 | 0.0160 | 0.0092 | 0.0842 | -0.0022 | 0.0341 |
| Rezagos casos | 1 | casos_confirmados_lag_7 | -0.0057 | 0.0131 | 0.6615 | -0.0313 | 0.0199 |
| Rezagos casos | 1 | casos_confirmados_lag_14 | 0.0122 | 0.0093 | 0.1873 | -0.0060 | 0.0304 |
| Rezagos hospitalizaciones | 0 | const | -14.7204 | 1.9430 | 0.0000 | -18.5307 | -10.9102 |
| Rezagos hospitalizaciones | 0 | hospitalizaciones_lag_1 | 0.2757 | 0.0099 | 0.0000 | 0.2563 | 0.2950 |
| Rezagos hospitalizaciones | 0 | hospitalizaciones_lag_7 | 0.2075 | 0.0134 | 0.0000 | 0.1814 | 0.2337 |
| Rezagos hospitalizaciones | 0 | hospitalizaciones_lag_14 | 0.0140 | 0.0103 | 0.1741 | -0.0062 | 0.0343 |
| Rezagos hospitalizaciones | 1 | const | -14.7204 | 3.0139 | 0.0000 | -20.6307 | -8.8102 |
| Rezagos hospitalizaciones | 1 | hospitalizaciones_lag_1 | 0.2757 | 0.0311 | 0.0000 | 0.2147 | 0.3367 |
| Rezagos hospitalizaciones | 1 | hospitalizaciones_lag_7 | 0.2075 | 0.0239 | 0.0000 | 0.1607 | 0.2544 |
| Rezagos hospitalizaciones | 1 | hospitalizaciones_lag_14 | 0.0140 | 0.0308 | 0.6481 | -0.0463 | 0.0744 |
| Rezagos combinados | 0 | const | -9.3358 | 1.7956 | 0.0000 | -12.8570 | -5.8146 |
| Rezagos combinados | 0 | casos_confirmados_lag_1 | -0.0037 | 0.0008 | 0.0000 | -0.0052 | -0.0021 |
| Rezagos combinados | 0 | casos_confirmados_lag_7 | 0.0049 | 0.0013 | 0.0002 | 0.0023 | 0.0075 |
| Rezagos combinados | 0 | casos_confirmados_lag_14 | -0.0076 | 0.0008 | 0.0000 | -0.0092 | -0.0060 |
| Rezagos combinados | 0 | hospitalizaciones_lag_1 | 0.2873 | 0.0108 | 0.0000 | 0.2661 | 0.3085 |
| Rezagos combinados | 0 | hospitalizaciones_lag_7 | 0.2085 | 0.0141 | 0.0000 | 0.1808 | 0.2363 |
| Rezagos combinados | 0 | hospitalizaciones_lag_14 | 0.0515 | 0.0116 | 0.0000 | 0.0287 | 0.0743 |
| Rezagos combinados | 1 | const | -9.3358 | 2.1146 | 0.0000 | -13.4826 | -5.1890 |
| Rezagos combinados | 1 | casos_confirmados_lag_1 | -0.0037 | 0.0010 | 0.0004 | -0.0057 | -0.0016 |
| Rezagos combinados | 1 | casos_confirmados_lag_7 | 0.0049 | 0.0022 | 0.0302 | 0.0005 | 0.0093 |
| Rezagos combinados | 1 | casos_confirmados_lag_14 | -0.0076 | 0.0014 | 0.0000 | -0.0104 | -0.0048 |
| Rezagos combinados | 1 | hospitalizaciones_lag_1 | 0.2873 | 0.0273 | 0.0000 | 0.2338 | 0.3408 |
| Rezagos combinados | 1 | hospitalizaciones_lag_7 | 0.2085 | 0.0241 | 0.0000 | 0.1612 | 0.2559 |
| Rezagos combinados | 1 | hospitalizaciones_lag_14 | 0.0515 | 0.0303 | 0.0894 | -0.0079 | 0.1109 |

## Interpretacion

Esta fase evalua H1 y H2 de forma mas directa que los modelos contemporaneos. Los signos y significancia de los rezagos de casos informan si existe efecto positivo rezagado; la comparacion de metricas entre modelos de casos y hospitalizaciones indica que predictor esta mas cerca de las defunciones.
