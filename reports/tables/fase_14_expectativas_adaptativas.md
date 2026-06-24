# Fase 14 - Expectativas adaptativas

Se construyeron expectativas adaptativas con promedios exponenciales de 7 dias rezagados un dia.

## Coeficientes

| modelo | robusto | variable | coeficiente | error_std | p_value | ci_95_inf | ci_95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Expectativas adaptativas | 0 | const | 1.7987 | 1.6302 | 0.2700 | -1.3981 | 4.9954 |
| Expectativas adaptativas | 0 | casos_confirmados_ema7_lag1 | 0.0015 | 0.0004 | 0.0000 | 0.0008 | 0.0022 |
| Expectativas adaptativas | 0 | hospitalizaciones_ema7_lag1 | -0.0733 | 0.0254 | 0.0039 | -0.1231 | -0.0235 |
| Expectativas adaptativas | 0 | defunciones_ema7_lag1 | 1.1151 | 0.0455 | 0.0000 | 1.0259 | 1.2043 |
| Expectativas adaptativas | 1 | const | 1.7987 | 1.6828 | 0.2852 | -1.5013 | 5.0987 |
| Expectativas adaptativas | 1 | casos_confirmados_ema7_lag1 | 0.0015 | 0.0011 | 0.1619 | -0.0006 | 0.0036 |
| Expectativas adaptativas | 1 | hospitalizaciones_ema7_lag1 | -0.0733 | 0.0928 | 0.4298 | -0.2552 | 0.1087 |
| Expectativas adaptativas | 1 | defunciones_ema7_lag1 | 1.1151 | 0.1790 | 0.0000 | 0.7641 | 1.4661 |

## Comparacion con modelos dinamicos

| modelo | nobs | r2 | r2_ajustado | aic | bic | rmse | mae | bloque |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rezagos casos | 2,277.0000 | 0.2774 | 0.2765 | 31,326.1538 | 31,349.0763 | 234.6574 | 150.9432 | Rezagos |
| Rezagos hospitalizaciones | 2,277.0000 | 0.9186 | 0.9185 | 26,354.5109 | 26,377.4333 | 78.7610 | 38.2506 | Rezagos |
| Rezagos combinados | 2,277.0000 | 0.9324 | 0.9323 | 25,935.8758 | 25,975.9901 | 71.7489 | 31.4141 | Rezagos |
| Ajuste parcial | 2,277.0000 | 0.9440 | 0.9438 | 25,509.9180 | 25,555.7629 | 65.3135 | 26.4551 | Ajuste parcial |
| Expectativas adaptativas | 2,290.0000 | 0.9496 | 0.9495 | 25,398.1137 | 25,421.0590 | 61.8526 | 23.9269 | Expectativas |

## Interpretacion

El modelo resume informacion reciente de casos, hospitalizaciones y defunciones. Su comparacion con rezagos distribuidos y ajuste parcial ayuda a decidir que especificacion prepara mejor el bloque ARIMA.
