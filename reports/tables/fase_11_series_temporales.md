# Fase 11 - Construccion formal de series temporales

La serie diaria continua cubre de `2020-02-19` a `2026-05-28` con `2,291` dias.

## Prueba ADF

| serie | estadistico_adf | p_value | rezagos_usados | nobs | valor_critico_1pct | valor_critico_5pct | valor_critico_10pct | icbest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| casos_confirmados | -5.6897 | 0.0000 | 27.0000 | 2,263.0000 | -3.4332 | -2.8628 | -2.5675 | 37,401.3194 |
| hospitalizaciones | -2.9733 | 0.0375 | 27.0000 | 2,263.0000 | -3.4332 | -2.8628 | -2.5675 | 27,466.6652 |
| defunciones | -3.2879 | 0.0154 | 26.0000 | 2,264.0000 | -3.4332 | -2.8628 | -2.5675 | 24,536.3519 |

## Interpretacion

La serie queda lista para modelos dinamicos. Las graficas de tendencia y ACF/PACF muestran alta persistencia en defunciones, lo que conecta directamente con H3.
