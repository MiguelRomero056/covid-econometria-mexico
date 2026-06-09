# Fase 3 - Limpieza y preparacion de datos

## Dataset procesado

Archivo generado:

`data/processed/covid_mexico_confirmados_2020_2026.parquet`

Resumen:

| Indicador | Valor |
|---|---:|
| Registros raw leidos | 20,772,901 |
| Casos confirmados conservados | 7,735,170 |
| Columnas procesadas | 36 |
| Fecha minima de sintomas | 2020-02-19 |
| Fecha maxima de sintomas | 2026-05-28 |

## Reglas aplicadas

- Se leyeron solo columnas necesarias para reducir uso de memoria.
- Se filtraron casos confirmados con clasificacion COVID en 1, 2 o 3.
- Se normalizo `CLASIFICACION_FINAL` y `CLASIFICACION_FINAL_COVID` como `clasificacion_final_covid`.
- Se convirtieron fechas a formato datetime.
- `FECHA_DEF = 9999-99-99` se trato como ausencia de defuncion.
- Codigos 97, 98 y 99 en variables SI/NO se trataron como valores no informativos.
- El analisis se conserva a nivel nacional, manteniendo entidad y municipio para fases posteriores.

## Variables derivadas

| Variable | Definicion |
|---|---|
| `defuncion` | 1 si `FECHA_DEF` contiene una fecha valida, 0 si es `9999-99-99` |
| `hospitalizacion` | 1 si `TIPO_PACIENTE = 2`, 0 si `TIPO_PACIENTE = 1` |
| `sexo_hombre` | 1 si `SEXO = 2`, 0 si `SEXO = 1` |
| `*_dummy` | 1 si el diagnostico es si, 0 si es no, NA si es 97/98/99 |
| `dias_sintomas_ingreso` | Diferencia en dias entre `FECHA_INGRESO` y `FECHA_SINTOMAS` |
| `anio_sintomas`, `mes_sintomas`, `semana_sintomas` | Componentes temporales derivados de `FECHA_SINTOMAS` |

## Validaciones

| Prueba | Resultado |
|---|---|
| Codigos confirmados presentes | `[1, 2, 3]` |
| Valores de `defuncion` | `[0, 1]` |
| Valores de `hospitalizacion` | `[0, 1]` |
| Archivos procesados | 6 de 6 |
| Tabla de procesamiento | `reports/tables/fase_03_resumen_procesamiento.csv` |
| Tabla de validaciones | `reports/tables/fase_03_validaciones.csv` |
