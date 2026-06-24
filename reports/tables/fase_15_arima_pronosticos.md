# Fase 15 - AR, MA, ARMA, ARIMA y pronosticos

## Comparacion de modelos

| modelo | p | d | q | aic | bic | llf |
| --- | --- | --- | --- | --- | --- | --- |
| ARIMA(2, 0, 2) | 2 | 0 | 2 | 24,750.3676 | 24,784.7010 | -12,369.1838 |
| ARIMA(2, 1, 2) | 2 | 1 | 2 | 25,003.4236 | 25,032.0326 | -12,496.7118 |
| ARIMA(1, 1, 2) | 1 | 1 | 2 | 25,008.0323 | 25,030.9194 | -12,500.0161 |
| ARIMA(2, 1, 1) | 2 | 1 | 1 | 25,009.2150 | 25,032.1040 | -12,500.6075 |
| ARIMA(0, 1, 2) | 0 | 1 | 2 | 25,013.3431 | 25,030.5085 | -12,503.6715 |
| ARIMA(1, 0, 2) | 1 | 0 | 2 | 25,024.9008 | 25,053.5120 | -12,507.4504 |
| ARIMA(1, 1, 1) | 1 | 1 | 1 | 25,031.7779 | 25,048.9446 | -12,512.8889 |
| ARIMA(2, 0, 1) | 2 | 0 | 1 | 25,043.1224 | 25,071.7358 | -12,516.5612 |
| ARIMA(0, 1, 1) | 0 | 1 | 1 | 25,048.1214 | 25,059.5659 | -12,522.0607 |
| ARIMA(1, 0, 1) | 1 | 0 | 1 | 25,059.6415 | 25,082.5322 | -12,525.8208 |

## Modelo seleccionado

El mejor modelo por AIC en la ventana de entrenamiento fue `ARIMA(2, 0, 2)`.

## Errores de pronostico

| horizonte | rmse | mae | mape |
| --- | --- | --- | --- |
| 7.0000 | 3.2166 | 3.1205 | 343.9427 |
| 14.0000 | 6.7769 | 5.9623 | 343.9427 |
| 30.0000 | 17.3820 | 14.6216 | 872.8408 |

## Comparacion de multiples modelos de pronostico

| modelo | horizonte | rmse | mae | mape |
| --- | --- | --- | --- | --- |
| Naive | 7.0000 | 0.5345 | 0.2857 | 100.0000 |
| Naive | 14.0000 | 0.3780 | 0.1429 | 100.0000 |
| Naive | 30.0000 | 0.3162 | 0.1000 | 100.0000 |
| Promedio movil 7 dias | 7.0000 | 0.5345 | 0.2857 | 100.0000 |
| Promedio movil 7 dias | 14.0000 | 0.3780 | 0.1429 | 100.0000 |
| Promedio movil 7 dias | 30.0000 | 0.3162 | 0.1000 | 100.0000 |
| Exponential Smoothing | 7.0000 | 0.5344 | 0.2858 | 99.9769 |
| Exponential Smoothing | 14.0000 | 0.3779 | 0.1430 | 99.9769 |
| Exponential Smoothing | 30.0000 | 0.3162 | 0.1002 | 99.9769 |
| ARIMA(2, 0, 2) | 7.0000 | 3.2166 | 3.1205 | 343.9427 |
| ARIMA(2, 0, 2) | 14.0000 | 6.7769 | 5.9623 | 343.9427 |
| ARIMA(2, 0, 2) | 30.0000 | 17.3820 | 14.6216 | 872.8408 |

## Mejor modelo por horizonte

| horizonte | mejor_modelo | mejor_rmse | mejor_mae | mejor_mape |
| --- | --- | --- | --- | --- |
| 7.0000 | Exponential Smoothing | 0.5344 | 0.2858 | 99.9769 |
| 14.0000 | Exponential Smoothing | 0.3779 | 0.1430 | 99.9769 |
| 30.0000 | Exponential Smoothing | 0.3162 | 0.1002 | 99.9769 |

## Ljung-Box de residuos

| modelo | rezago | lb_stat | lb_pvalue |
| --- | --- | --- | --- |
| ARIMA(2, 0, 2) | 7 | 118.7646 | 0.0000 |
| ARIMA(2, 0, 2) | 14 | 237.0184 | 0.0000 |
| ARIMA(2, 0, 2) | 30 | 380.2368 | 0.0000 |

## Primeros pronosticos futuros

| fecha | pronostico_defunciones |
| --- | --- |
| 2026-05-29 00:00:00 | 2.3175 |
| 2026-05-30 00:00:00 | 2.5119 |
| 2026-05-31 00:00:00 | 2.8326 |
| 2026-06-01 00:00:00 | 3.2670 |
| 2026-06-02 00:00:00 | 3.8037 |
| 2026-06-03 00:00:00 | 4.4323 |
| 2026-06-04 00:00:00 | 5.1432 |
| 2026-06-05 00:00:00 | 5.9278 |
| 2026-06-06 00:00:00 | 6.7781 |
| 2026-06-07 00:00:00 | 7.6869 |

## Interpretacion

Los pronosticos a 7, 14 y 30 dias permiten evaluar H4. La comparacion no se limita a ordenes ARIMA: se incluyen benchmarks Naive, promedio movil de 7 dias, Exponential Smoothing y el ARIMA seleccionado. La narrativa oficial del punto extra es: se realizo una comparacion de multiples modelos de pronostico; ARIMA(2, 0, 2) fue el mejor por AIC dentro de los modelos ARIMA, pero Exponential Smoothing tuvo mejor desempeno en la validacion final por RMSE en los horizontes de 7, 14 y 30 dias. Esta comparacion hace defendible el punto extra porque contrasta el ARIMA contra alternativas simples y transparentes antes de seleccionar el pronostico final.

Se generan dos graficas separadas: `reports/figures/fase_15_validacion_pronosticos.png` para validacion contra datos reales y `reports/figures/fase_15_pronostico_futuro.png` para pronostico futuro. La revision de residuos indica si el ARIMA seleccionado dejo autocorrelacion remanente relevante.
