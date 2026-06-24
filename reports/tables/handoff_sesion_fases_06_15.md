# Handoff de sesion - Fases 6 a 15

Fecha de handoff: 2026-06-15

## Estado actual

El proyecto quedo implementado hasta la **fase 15**. Se mantuvo como eje principal la pregunta:

**En que medida los casos confirmados y hospitalizaciones permiten explicar y pronosticar las defunciones por COVID-19 en Mexico entre 2020 y 2026?**

La serie diaria continua cubre del **2020-02-19 al 2026-05-28**, con **2,291 dias**, sin fechas faltantes y sin nulos en las variables principales.

## Artefactos principales

- `notebooks/03_econometric_models.ipynb`
- `notebooks/04_time_series_forecasting.ipynb`
- `scripts/run_phases_06_15.py`
- `reports/tables/fase_06_15_series_diarias_continuas.csv`
- `reports/tables/fase_06_15_contraste_hipotesis.md`
- `reports/tables/fase_15_arima_pronosticos.md`

## Hallazgos principales

- H1 recibe apoyo parcial: 2 de 3 rezagos de casos tienen signo positivo.
- H2 queda apoyada: los rezagos de hospitalizaciones explican mejor las defunciones que los rezagos de casos.
- H3 queda apoyada: existe alta persistencia temporal en defunciones.
- H4 recibe apoyo inicial: el ARIMA seleccionado genera pronosticos para 7, 14 y 30 dias.

## Resultados clave

| Resultado | Valor |
|---|---:|
| R2 rezagos de casos | 0.2774 |
| R2 rezagos de hospitalizaciones | 0.9186 |
| R2 rezagos combinados | 0.9324 |
| Coeficiente defunciones_t-1 | 0.9952 |
| Mejor ARIMA por AIC | ARIMA(2, 0, 2) |
| RMSE pronostico 7 dias | 3.2166 |
| RMSE pronostico 30 dias | 17.3820 |

## Desde donde continuar

La siguiente sesion puede iniciar en la **fase 16**:

1. Investigacion bibliografica.
2. Interpretacion economica y de politica publica.
3. Dashboard resumen.
4. Reporte tecnico final.
5. Presentacion y video.

