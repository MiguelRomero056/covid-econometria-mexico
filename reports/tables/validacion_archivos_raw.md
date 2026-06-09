# Validacion de archivos CSV en data/raw

Fecha de validacion: 2026-06-08

## Criterio usado

Para validar que cada CSV corresponde al anio indicado en su nombre se revisaron las columnas:

- `FECHA_SINTOMAS`: criterio principal recomendado para separar los archivos anuales, porque coincide exactamente con el anio del archivo en 2020-2024.
- `FECHA_INGRESO`: criterio secundario; presenta algunos registros del anio siguiente en los archivos 2020-2024.
- `FECHA_DEF`: criterio complementario; puede extenderse al anio siguiente porque una defuncion puede ocurrir despues del inicio de sintomas o ingreso.
- `FECHA_ACTUALIZACION`: no se usa para validar el anio epidemiologico del archivo, porque corresponde a la fecha de corte/actualizacion del dataset.

## Resultado

| Archivo | Registros | Anios esperados | Rango FECHA_SINTOMAS | Anios FECHA_SINTOMAS | Fuera de anio por sintomas | Rango FECHA_INGRESO | Fuera de anio por ingreso | Estado recomendado |
|---|---:|---|---|---|---:|---|---:|---|
| COVID19MEXICO2020.csv | 3,868,396 | 2020 | 2020-01-01 a 2020-12-31 | 2020: 3,868,396 | 0 | 2020-01-01 a 2021-09-06 | 77,268 | Valido por sintomas |
| COVID19MEXICO2021.csv | 8,830,345 | 2021 | 2021-01-01 a 2021-12-31 | 2021: 8,830,345 | 0 | 2021-01-01 a 2022-03-02 | 64,547 | Valido por sintomas |
| COVID19MEXICO2022.csv | 6,451,944 | 2022 | 2022-01-01 a 2022-12-31 | 2022: 6,451,944 | 0 | 2022-01-01 a 2023-04-03 | 17,852 | Valido por sintomas |
| COVID19MEXICO2023.csv | 1,222,219 | 2023 | 2023-01-01 a 2023-12-31 | 2023: 1,222,219 | 0 | 2023-01-01 a 2024-04-19 | 1,288 | Valido por sintomas |
| COVID19MEXICO2024.csv | 177,618 | 2024 | 2024-01-01 a 2024-12-31 | 2024: 177,618 | 0 | 2024-01-01 a 2025-01-23 | 1,000 | Valido por sintomas |
| COVID19MEXICO20252026.csv | 222,379 | 2025, 2026 | 2025-01-01 a 2026-05-31 | 2025: 159,771; 2026: 62,608 | 0 | 2025-01-01 a 2026-05-31 | 0 | Valido por sintomas e ingreso |

## Observaciones

1. Los archivos 2020 a 2024 corresponden correctamente a su anio si se toma `FECHA_SINTOMAS` como criterio de anio epidemiologico.
2. Los registros de `FECHA_INGRESO` en el anio siguiente no invalidan los archivos: reflejan pacientes cuyo inicio de sintomas fue en el anio del archivo, pero cuyo ingreso ocurrio despues.
3. `FECHA_DEF` tambien puede extenderse al anio siguiente por la misma razon temporal.
4. El archivo `COVID19MEXICO20252026.csv` corresponde correctamente al periodo combinado 2025-2026.

## Decision metodologica sugerida

Para construir muestras anuales o series temporales, usar `FECHA_SINTOMAS` como fecha principal. Usar `FECHA_INGRESO` para variables relacionadas con hospitalizacion/atencion y `FECHA_DEF` solo para eventos de defuncion.

