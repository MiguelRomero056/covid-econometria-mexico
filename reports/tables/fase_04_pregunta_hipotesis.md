# Fase 4 - Pregunta e hipotesis formales

## Pregunta de investigacion definitiva

**En que medida los casos confirmados y hospitalizaciones permiten explicar y pronosticar las defunciones por COVID-19 en Mexico entre 2020 y 2026?**

## Hipotesis definitivas

1. **H1:** Los casos confirmados tienen un efecto positivo y rezagado sobre las defunciones diarias.
2. **H2:** Las hospitalizaciones son un predictor mas cercano de las defunciones que los casos confirmados.
3. **H3:** Las defunciones diarias presentan autocorrelacion y persistencia temporal.
4. **H4:** Los modelos ARIMA permiten generar pronosticos razonables de corto plazo para horizontes de 7, 14 y 30 dias.

## Alcance

- Unidad de analisis principal: serie diaria nacional construida a partir de registros individuales confirmados.
- Poblacion base: casos confirmados de COVID-19 en Mexico, 2020-2026.
- Cobertura geografica: nacional.
- Variable dependiente principal: defunciones diarias.
- Variables explicativas principales: casos confirmados diarios y hospitalizaciones diarias.
- Fecha epidemiologica principal: `FECHA_SINTOMAS`.

## Justificacion metodologica

La pregunta concentra el proyecto en el bloque dinamico del curso. Permite usar rezagos distribuidos, ajuste parcial, expectativas adaptativas, modelos AR, MA, ARMA, ARIMA y pronosticos de 7, 14 y 30 dias. La base individual sigue siendo util para construir las series diarias y, si se requiere, para incluir una seccion complementaria de caracterizacion clinica.

## Viabilidad con los datos disponibles

La tabla `reports/tables/fase_04_viabilidad_series_rezagos.csv` evalua correlaciones simples entre defunciones diarias y predictores rezagados. No sustituye los modelos econometricos, pero confirma que la pregunta es viable.

| Evidencia descriptiva | Resultado |
|---|---:|
| Dias continuos de serie diaria | 2,291 |
| Rango de la serie | 2020-02-19 a 2026-05-28 |
| Correlacion casos-defunciones sin rezago | 0.5148 |
| Correlacion casos rezagados 7 dias-defunciones | 0.5107 |
| Correlacion hospitalizaciones-defunciones sin rezago | 0.9866 |
| Correlacion hospitalizaciones rezagadas 7 dias-defunciones | 0.9435 |
| Autocorrelacion de defunciones a 1 dia | 0.9609 |
| Autocorrelacion de defunciones a 7 dias | 0.9551 |

## Implicacion para fases posteriores

- H1 se probara con modelos de rezagos distribuidos usando casos confirmados en rezagos de 1, 7 y 14 dias.
- H2 se probara comparando modelos con casos confirmados contra modelos con hospitalizaciones.
- H3 se probara con autocorrelacion, rezagos de la variable dependiente y modelos de ajuste parcial.
- H4 se evaluara con ARIMA y errores de pronostico en horizontes de 7, 14 y 30 dias.
