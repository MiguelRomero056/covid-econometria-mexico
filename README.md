# Proyecto Modelos Econometricos - COVID 19

Analisis econometrico de la evolucion temporal, hospitalizacion y defunciones por COVID-19 en Mexico, usando datos oficiales de la Secretaria de Salud.

## Pregunta guia

En que medida los casos confirmados y hospitalizaciones permiten explicar y pronosticar las defunciones por COVID-19 en Mexico entre 2020 y 2026?

## Fuente principal de datos

Portal oficial de Datos Abiertos COVID-19 de la Secretaria de Salud de Mexico:

https://www.gob.mx/salud/documentos/datos-abiertos-152127

## Estructura del proyecto

```text
Proyecto Modelos Econometricos - COVID 19/
|-- data/
|   |-- raw/          # Datos originales sin modificar
|   |-- processed/    # Datos limpios o transformados
|   `-- outputs/      # Archivos intermedios generados por notebooks/scripts
|-- notebooks/        # Notebooks de analisis
|-- src/              # Funciones reutilizables de Python
|-- reports/
|   |-- figures/      # Graficas finales
|   `-- tables/       # Tablas finales
|-- presentation/     # Material de exposicion
|-- contexto_y_fases_proyecto_modelos_econometricos.md
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Flujo recomendado

1. Descargar la base oficial y el diccionario de datos en `data/raw/`.
2. Revisar codigos y variables en el diccionario.
3. Crear base procesada en `data/processed/`.
4. Generar estadistica descriptiva y visualizaciones.
5. Estimar modelos lineales, Logit, Probit y diagnosticos.
6. Construir series temporales, rezagos y pronosticos.
7. Integrar resultados en reporte, dashboard, presentacion y video.

## Estado actual del proyecto

Avance completado hasta la fase 15 con datos 2020-2026:

- Fase 1: datos raw documentados y validados en `reports/tables/fase_01_datos_raw.md`.
- Fase 2: diccionario, variables seleccionadas, pregunta e hipotesis iniciales en `reports/tables/fase_02_diccionario_variables.md`.
- Fase 3: dataset procesado en `data/processed/covid_mexico_confirmados_2020_2026.parquet`.
- Fase 4: pregunta e hipotesis formales en `reports/tables/fase_04_pregunta_hipotesis.md`.
- Fase 5: estadistica descriptiva, tablas, graficas e interpretacion en `reports/tables/fase_05_estadistica_descriptiva.md`.
- Fases 6-10: modelos OLS, dummies, Logit/Probit complementario y diagnostico en `notebooks/03_econometric_models.ipynb`.
- Fases 11-15: series temporales, rezagos, ajuste parcial, expectativas adaptativas y ARIMA en `notebooks/04_time_series_forecasting.ipynb`.
- Fase 18: dashboard ejecutivo reproducible en `reports/dashboard/fase_18_dashboard.html`.

Muestra principal: casos confirmados con clasificacion COVID 1, 2 o 3. El dataset procesado contiene 7,735,170 registros confirmados, con `FECHA_SINTOMAS` entre 2020-02-19 y 2026-05-28.
La serie diaria continua generada para modelos temporales contiene 2,291 dias entre 2020-02-19 y 2026-05-28.

## Resultados econometricos principales

- Las hospitalizaciones explican mejor las defunciones diarias que los casos confirmados en modelos con rezagos: R2 de 0.9186 contra 0.2774.
- El modelo con rezagos combinados mejora el ajuste: R2 de 0.9324.
- El modelo de ajuste parcial muestra persistencia fuerte: coeficiente de `defunciones_t-1` de 0.9952.
- El mejor candidato dentro de los modelos ARIMA por AIC fue ARIMA(2, 0, 2); en la comparacion final de pronosticos por RMSE, Exponential Smoothing tuvo el mejor desempeno en los horizontes de 7, 14 y 30 dias.
- La fase de dummies documenta explicitamente sexo, diabetes, hipertension, obesidad, hospitalizacion y defuncion, ademas de dummies temporales complementarias.
- El diagnostico incluye heterocedasticidad, autocorrelacion, VIF y normalidad de residuos con Jarque-Bera y Shapiro-Wilk.
- La fase de pronostico compara Naive, promedio movil, Exponential Smoothing y ARIMA para horizontes de 7, 14 y 30 dias como punto extra.
- El contraste de hipotesis esta disponible en `reports/tables/fase_06_15_contraste_hipotesis.md`.
- El dashboard resumen estatico se genera con `scripts/build_phase_18_dashboard.py`.

## Pregunta e hipotesis definitivas

Pregunta:

**En que medida los casos confirmados y hospitalizaciones permiten explicar y pronosticar las defunciones por COVID-19 en Mexico entre 2020 y 2026?**

Hipotesis:

1. Los casos confirmados tienen un efecto positivo y rezagado sobre las defunciones diarias.
2. Las hospitalizaciones son un predictor mas cercano de las defunciones que los casos confirmados.
3. Las defunciones diarias presentan autocorrelacion y persistencia temporal.
4. Los modelos ARIMA permiten generar pronosticos razonables de corto plazo para horizontes de 7, 14 y 30 dias.

## Decisiones pendientes

- Muestra decidida: casos confirmados.
- Enfoque decidido: defunciones diarias explicadas por casos confirmados, hospitalizaciones y dinamica temporal.
- Rango temporal decidido: 2020-2026.
- Alcance geografico principal decidido: nacional.
- Dashboard decidido: HTML estatico para fase 18.
