# Handoff de sesion - Proyecto COVID-19

Fecha de handoff: 2026-06-08

## Estado actual

El proyecto quedo completado hasta la **fase 5**.

Se trabajo con datos oficiales de COVID-19 Mexico, periodo 2020-2026, usando como muestra principal los casos confirmados con clasificacion COVID 1, 2 o 3. El dataset procesado contiene **7,735,170 registros confirmados** y se guardo en:

`data/processed/covid_mexico_confirmados_2020_2026.parquet`

La serie diaria disponible cubre del **2020-02-19 al 2026-05-28**.

## Pregunta definitiva

**En que medida los casos confirmados y hospitalizaciones permiten explicar y pronosticar las defunciones por COVID-19 en Mexico entre 2020 y 2026?**

## Hipotesis definitivas

1. **H1:** Los casos confirmados tienen un efecto positivo y rezagado sobre las defunciones diarias.
2. **H2:** Las hospitalizaciones son un predictor mas cercano de las defunciones que los casos confirmados.
3. **H3:** Las defunciones diarias presentan autocorrelacion y persistencia temporal.
4. **H4:** Los modelos ARIMA permiten generar pronosticos razonables de corto plazo para horizontes de 7, 14 y 30 dias.

## Artefactos ya listos

### Notebooks

- `notebooks/01_data_loading_cleaning.ipynb`
- `notebooks/02_descriptive_analysis.ipynb`

### Documentacion por fase

- `reports/tables/fase_01_datos_raw.md`
- `reports/tables/fase_02_diccionario_variables.md`
- `reports/tables/fase_03_limpieza_preparacion.md`
- `reports/tables/fase_04_pregunta_hipotesis.md`
- `reports/tables/fase_05_estadistica_descriptiva.md`

### Tablas clave

- `reports/tables/fase_03_resumen_procesamiento.csv`
- `reports/tables/fase_03_validaciones.csv`
- `reports/tables/fase_04_viabilidad_series_rezagos.csv`
- `reports/tables/fase_05_estadisticos_descriptivos.csv`
- `reports/tables/fase_05_frecuencias_binarias.csv`
- `reports/tables/fase_05_matriz_correlacion.csv`
- `reports/tables/fase_05_series_diarias.csv`

### Graficas fase 5

- `reports/figures/histograma_edad.png`
- `reports/figures/histograma_dias_sintomas_ingreso.png`
- `reports/figures/histograma_defuncion.png`
- `reports/figures/histograma_hospitalizacion.png`
- `reports/figures/histograma_neumonia_dummy.png`
- `reports/figures/boxplot_edad_por_hospitalizacion.png`
- `reports/figures/boxplot_edad_por_defuncion.png`
- `reports/figures/scatter_edad_dias_defuncion.png`
- `reports/figures/scatter_edad_dias_hospitalizacion.png`
- `reports/figures/matriz_correlacion.png`

## Evidencia de viabilidad para la nueva pregunta

La tabla `fase_04_viabilidad_series_rezagos.csv` confirma que el giro hacia series de tiempo es viable:

- Serie diaria continua: **2,291 dias**.
- Correlacion casos-defunciones sin rezago: **0.5148**.
- Correlacion casos rezagados 7 dias-defunciones: **0.5107**.
- Correlacion hospitalizaciones-defunciones sin rezago: **0.9866**.
- Correlacion hospitalizaciones rezagadas 7 dias-defunciones: **0.9435**.
- Autocorrelacion de defunciones a 1 dia: **0.9609**.
- Autocorrelacion de defunciones a 7 dias: **0.9551**.

## Desde donde continuar

La siguiente sesion debe continuar desde la **fase 6**.

Como la pregunta definitiva ahora esta centrada en defunciones diarias, rezagos y pronostico, conviene reorganizar las fases restantes asi:

| Bloque | Fases | Objetivo |
|---|---|---|
| Modelos base | Fases 6-8 | Cumplir regresion simple, multiple y dummies, pero adaptadas a series diarias |
| Modelos probabilisticos complementarios | Fase 9 | Mantener Logit/Probit como apendice individual si el curso lo exige |
| Diagnostico | Fase 10 | Diagnosticar residuos, autocorrelacion, heterocedasticidad y multicolinealidad |
| Series temporales | Fases 11-15 | Bloque central: series, rezagos, ajuste parcial, expectativas adaptativas, ARIMA y pronosticos |
| Cierre academico | Fases 16-20 | Bibliografia, interpretacion, dashboard, reporte, presentacion y video |

## Plan recomendado para la siguiente sesion

### Continuar de fase 6 a fase 15 primero

Prioridad tecnica:

1. **Fase 6:** Regresion lineal simple en serie diaria.
   - Modelo sugerido: `defunciones_t = beta0 + beta1 casos_confirmados_t + u_t`.
   - Variante: `defunciones_t = beta0 + beta1 hospitalizaciones_t + u_t`.

2. **Fase 7:** Regresion lineal multiple.
   - Modelo sugerido: `defunciones_t = beta0 + beta1 casos_confirmados_t + beta2 hospitalizaciones_t + u_t`.
   - Comparar poder explicativo entre casos y hospitalizaciones.

3. **Fase 8:** Variables dummy.
   - Crear dummies temporales utiles: dia de semana, mes, ano, periodos de ola si se decide.
   - Las dummies clinicas individuales pueden quedar como caracterizacion secundaria.

4. **Fase 9:** Logit/Probit complementario.
   - Si se mantiene, usar nivel individual con `defuncion` como dependiente.
   - Marcarlo como complemento, no como eje central.

5. **Fase 10:** Diagnostico econometrico.
   - VIF para modelos multiples.
   - Breusch-Pagan/White para heterocedasticidad.
   - Durbin-Watson/Breusch-Godfrey para autocorrelacion.
   - Graficas de residuos.

6. **Fase 11:** Construccion formal de series temporales.
   - Consolidar `casos_confirmados`, `hospitalizaciones`, `defunciones`.
   - Asegurar frecuencia diaria continua.
   - Crear promedios moviles si se decide.

7. **Fase 12:** Rezagos distribuidos.
   - Incluir rezagos de casos y hospitalizaciones en 1, 7 y 14 dias.
   - Evaluar H1 y H2.

8. **Fase 13:** Ajuste parcial.
   - Incluir `defunciones_t-1`.
   - Evaluar persistencia y velocidad de ajuste.

9. **Fase 14:** Expectativas adaptativas.
   - Usar informacion pasada para aproximar expectativas de defunciones o casos.
   - Comparar errores de prediccion.

10. **Fase 15:** AR, MA, ARMA, ARIMA y pronosticos.
    - Probar estacionariedad con ADF.
    - Comparar AIC/BIC.
    - Generar pronosticos a 7, 14 y 30 dias.
    - Evaluar H3 y H4.

### Despues continuar de fase 16 a fase 20

Una vez cerrado el bloque tecnico 6-15, avanzar a:

- **Fase 16:** Investigacion bibliografica.
- **Fase 17:** Interpretacion economica y de politica publica.
- **Fase 18:** Dashboard resumen.
- **Fase 19:** Reporte tecnico.
- **Fase 20:** Presentacion y video.

## Recomendacion para iniciar la siguiente sesion

Arrancar con una planeacion detallada de las **fases 6 a 15**, porque son el nucleo econometrico que responde directamente la pregunta nueva. Las fases 16 a 20 deben planearse despues, usando los resultados que salgan de los modelos.

Primer entregable sugerido de la siguiente sesion:

`reports/tables/plan_fases_06_15_modelos_temporales.md`

Segundo entregable sugerido:

`notebooks/03_econometric_models.ipynb` actualizado para modelos base, diagnosticos y rezagos.

Tercer entregable sugerido:

`notebooks/04_time_series_forecasting.ipynb` actualizado para ARIMA y pronosticos.
