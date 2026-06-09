# Fase 1 - Obtencion y validacion de datos raw

Fecha de trabajo: 2026-06-08

## Fuente oficial

Los datos provienen del portal oficial de Datos Abiertos COVID-19 de la Secretaria de Salud de Mexico:

https://www.gob.mx/salud/documentos/datos-abiertos-152127

## Archivos disponibles

| Archivo | Registros raw | Registros confirmados | Tamano aprox. MB | Periodo esperado |
|---|---:|---:|---:|---|
| `COVID19MEXICO2020.csv` | 3,868,396 | 1,563,135 | 598.14 | 2020 |
| `COVID19MEXICO2021.csv` | 8,830,345 | 2,526,649 | 1,366.11 | 2021 |
| `COVID19MEXICO2022.csv` | 6,451,944 | 3,195,409 | 1,000.48 | 2022 |
| `COVID19MEXICO2023.csv` | 1,222,219 | 428,212 | 189.51 | 2023 |
| `COVID19MEXICO2024.csv` | 177,618 | 14,131 | 28.50 | 2024 |
| `COVID19MEXICO20252026.csv` | 222,379 | 7,634 | 35.59 | 2025-2026 |

## Validacion metodologica

- Se conservaron los archivos originales en `data/raw/` sin modificarlos.
- La validacion previa de `reports/tables/validacion_archivos_raw.md` confirma que `FECHA_SINTOMAS` identifica correctamente el ano epidemiologico.
- Para 2020-2024, `FECHA_SINTOMAS` cae dentro del ano indicado por el nombre del archivo.
- Para 2025-2026, `FECHA_SINTOMAS` cubre del 2025-01-01 al 2026-05-31 en la base raw.
- `FECHA_INGRESO` y `FECHA_DEF` pueden extenderse al ano siguiente por la secuencia clinica del caso; por eso no se usan para validar el ano del archivo.

## Decision de fase

El proyecto trabajara el periodo 2020-2026 con los seis CSV disponibles. La muestra principal se limita a casos confirmados de COVID-19 con clasificacion 1, 2 o 3.
