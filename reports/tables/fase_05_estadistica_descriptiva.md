# Fase 5 - Estadistica descriptiva

## Muestra analizada

La estadistica descriptiva se realizo sobre `7,735,170` casos confirmados de COVID-19 en Mexico, con fecha de sintomas entre `2020-02-19` y `2026-05-28`.

## Tablas generadas

| Archivo | Contenido |
|---|---|
| `fase_05_estadisticos_descriptivos.csv` | Media, mediana, moda, varianza, desviacion estandar, coeficiente de variacion, asimetria y curtosis |
| `fase_05_frecuencias_binarias.csv` | Frecuencias y proporciones de variables binarias |
| `fase_05_matriz_correlacion.csv` | Matriz de correlacion entre variables principales |
| `fase_05_series_diarias.csv` | Casos confirmados, hospitalizaciones y defunciones por fecha de sintomas |

## Graficas generadas

| Tipo | Archivos |
|---|---|
| Histogramas | `histograma_edad.png`, `histograma_dias_sintomas_ingreso.png`, `histograma_defuncion.png`, `histograma_hospitalizacion.png`, `histograma_neumonia_dummy.png` |
| Diagramas de caja | `boxplot_edad_por_hospitalizacion.png`, `boxplot_edad_por_defuncion.png` |
| Diagramas de dispersion | `scatter_edad_dias_defuncion.png`, `scatter_edad_dias_hospitalizacion.png` |
| Matriz de correlacion | `matriz_correlacion.png` |

## Resultados descriptivos principales

| Indicador | Resultado |
|---|---:|
| Edad media | 40.03 anos |
| Edad mediana | 38 anos |
| Tasa de defuncion | 4.35% |
| Tasa de hospitalizacion | 9.62% |
| Proporcion de hombres | 46.25% |
| Neumonia registrada | 6.95% |
| Diabetes registrada | 8.78% |
| Hipertension registrada | 11.96% |
| Obesidad registrada | 9.61% |
| Inmunosupresion registrada | 0.59% |

## Hallazgos temporales

| Serie | Maximo diario | Fecha |
|---|---:|---|
| Casos confirmados | 80,705 | 2022-01-10 |
| Hospitalizaciones | 3,705 | 2021-01-01 |
| Defunciones | 2,202 | 2021-01-01 |

La serie diaria contiene 2,270 fechas con registros entre 2020 y 2026. Los picos descriptivos sugieren que la mayor carga de casos confirmados aparece en 2022, mientras que hospitalizaciones y defunciones alcanzan su maximo al inicio de 2021.

## Correlaciones relevantes

- `defuncion` tiene correlacion positiva con `hospitalizacion` (0.6237), `neumonia_dummy` (0.5421), `edad` (0.2943), `hipertension_dummy` (0.2133) y `diabetes_dummy` (0.2115).
- `hospitalizacion` tiene correlacion positiva con `neumonia_dummy` (0.6917), `defuncion` (0.6237), `edad` (0.3201), `diabetes_dummy` (0.2536) e `hipertension_dummy` (0.2455).
- Estas correlaciones individuales no prueban causalidad, pero sirven como caracterizacion clinica secundaria de la muestra.

## Viabilidad para rezagos y pronostico

La serie diaria construida en esta fase permite reformular el eje del proyecto hacia defunciones diarias. La tabla `fase_04_viabilidad_series_rezagos.csv` muestra que:

- los casos confirmados tienen relacion positiva con defunciones contemporaneas y rezagadas;
- las hospitalizaciones tienen una relacion mas cercana con defunciones que los casos confirmados;
- las defunciones presentan autocorrelacion alta incluso a 7 y 14 dias;
- por lo anterior, los modelos con rezagos, ajuste parcial y ARIMA son metodologicamente viables.

## Cierre de hipotesis para avanzar

Las hipotesis quedan cerradas como marco definitivo del proyecto:

1. **H1:** Los casos confirmados tienen un efecto positivo y rezagado sobre las defunciones diarias.
2. **H2:** Las hospitalizaciones son un predictor mas cercano de las defunciones que los casos confirmados.
3. **H3:** Las defunciones diarias presentan autocorrelacion y persistencia temporal.
4. **H4:** Los modelos ARIMA permiten generar pronosticos razonables de corto plazo para horizontes de 7, 14 y 30 dias.

Con esta fase, el proyecto queda listo para avanzar a regresion con rezagos, ajuste parcial, expectativas adaptativas, AR, MA, ARMA, ARIMA y pronosticos. Las regresiones lineales y modelos Logit/Probit pueden mantenerse como componentes complementarios si el curso los exige, pero ya no son la narrativa central.
