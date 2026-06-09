# Fase 2 - Diccionario de variables y cierre inicial de investigacion

## Diccionarios revisados

- `data_dictionary/240708 Descriptores_.xlsx`
- `data_dictionary/240708 Catalogos.xlsx`

## Codigos relevantes

| Variable/catalogo | Codigos usados | Interpretacion |
|---|---|---|
| Sexo | 1, 2, 99 | 1 = mujer, 2 = hombre, 99 = no especificado |
| Tipo de paciente | 1, 2, 99 | 1 = ambulatorio, 2 = hospitalizado, 99 = no especificado |
| Variables SI/NO | 1, 2, 97, 98, 99 | 1 = si, 2 = no, 97 = no aplica, 98 = se ignora, 99 = no especificado |
| Clasificacion COVID | 1, 2, 3 | Casos confirmados por asociacion, dictaminacion o prueba |
| Clasificacion COVID | 4, 5, 6, 7 | Invalido, no realizado, sospechoso o negativo; se excluyen del analisis principal |
| Fecha de defuncion | `9999-99-99` | El paciente no fallecio en el registro |

## Variables seleccionadas

| Grupo | Variables | Uso en el proyecto |
|---|---|---|
| Identificacion | `ID_REGISTRO`, archivo de origen | Trazabilidad y conteo de registros |
| Demograficas | `EDAD`, `SEXO`, `ENTIDAD_RES`, `MUNICIPIO_RES`, `NACIONALIDAD` | Caracterizacion secundaria de pacientes |
| Temporales | `FECHA_ACTUALIZACION`, `FECHA_INGRESO`, `FECHA_SINTOMAS`, `FECHA_DEF` | Series temporales, rezagos, defunciones y tiempos clinicos |
| Resultados | `TIPO_PACIENTE`, `FECHA_DEF` | Hospitalizaciones y defunciones diarias |
| Clinicas | `NEUMONIA`, `DIABETES`, `EPOC`, `ASMA`, `INMUSUPR`, `HIPERTENSION`, `CARDIOVASCULAR`, `OBESIDAD`, `RENAL_CRONICA`, `TABAQUISMO`, `UCI`, `INTUBADO` | Dummies de comorbilidad y severidad |
| Confirmacion COVID | `CLASIFICACION_FINAL` / `CLASIFICACION_FINAL_COVID` | Filtro de casos confirmados |

## Nota sobre nombres historicos

Los archivos 2020-2023 usan `CLASIFICACION_FINAL`; los archivos 2024-2026 usan `CLASIFICACION_FINAL_COVID`. En la limpieza ambas columnas se normalizan como `clasificacion_final_covid`.

## Pregunta de investigacion al cierre de fase 2

**En que medida los casos confirmados y hospitalizaciones permiten explicar y pronosticar las defunciones por COVID-19 en Mexico entre 2020 y 2026?**

## Hipotesis iniciales al cierre de fase 2

1. **H1:** Los casos confirmados tienen un efecto positivo y rezagado sobre las defunciones diarias.
2. **H2:** Las hospitalizaciones son un predictor mas cercano de las defunciones que los casos confirmados.
3. **H3:** Las defunciones diarias presentan autocorrelacion y persistencia temporal.
4. **H4:** Los modelos ARIMA permiten generar pronosticos razonables de corto plazo para horizontes de 7, 14 y 30 dias.
