"""Funciones de carga, limpieza y preparacion de datos COVID-19."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


CONFIRMED_CODES = {1, 2, 3}
SPECIAL_CODES = {97, 98, 99}

BASE_COLUMNS = [
    "FECHA_ACTUALIZACION",
    "ID_REGISTRO",
    "ORIGEN",
    "SECTOR",
    "ENTIDAD_UM",
    "SEXO",
    "ENTIDAD_RES",
    "MUNICIPIO_RES",
    "TIPO_PACIENTE",
    "FECHA_INGRESO",
    "FECHA_SINTOMAS",
    "FECHA_DEF",
    "INTUBADO",
    "NEUMONIA",
    "EDAD",
    "NACIONALIDAD",
    "DIABETES",
    "EPOC",
    "ASMA",
    "INMUSUPR",
    "HIPERTENSION",
    "OTRA_COM",
    "CARDIOVASCULAR",
    "OBESIDAD",
    "RENAL_CRONICA",
    "TABAQUISMO",
    "UCI",
]

CLASSIFICATION_ALIASES = [
    "CLASIFICACION_FINAL_COVID",
    "CLASIFICACION_FINAL",
]

YES_NO_COLUMNS = [
    "INTUBADO",
    "NEUMONIA",
    "DIABETES",
    "EPOC",
    "ASMA",
    "INMUSUPR",
    "HIPERTENSION",
    "OTRA_COM",
    "CARDIOVASCULAR",
    "OBESIDAD",
    "RENAL_CRONICA",
    "TABAQUISMO",
    "UCI",
]

OUTPUT_COLUMNS = [
    "id_registro",
    "archivo_origen",
    "fecha_actualizacion",
    "fecha_ingreso",
    "fecha_sintomas",
    "fecha_def",
    "anio_sintomas",
    "mes_sintomas",
    "semana_sintomas",
    "dias_sintomas_ingreso",
    "origen",
    "sector",
    "entidad_um",
    "entidad_res",
    "municipio_res",
    "edad",
    "sexo",
    "sexo_hombre",
    "nacionalidad",
    "tipo_paciente",
    "hospitalizacion",
    "defuncion",
    "clasificacion_final_covid",
    "intubado_dummy",
    "neumonia_dummy",
    "diabetes_dummy",
    "epoc_dummy",
    "asma_dummy",
    "inmunosupresion_dummy",
    "hipertension_dummy",
    "otra_com_dummy",
    "cardiovascular_dummy",
    "obesidad_dummy",
    "renal_cronica_dummy",
    "tabaquismo_dummy",
    "uci_dummy",
]


def build_binary_from_yes_no(series: pd.Series) -> pd.Series:
    """Convierte codigos 1/2 del diccionario COVID en variable binaria 1/0."""
    return pd.to_numeric(series, errors="coerce").map({1: 1, 2: 0})


def classification_column(columns: Iterable[str]) -> str:
    """Devuelve el nombre de la columna de clasificacion COVID disponible."""
    available = set(columns)
    for column in CLASSIFICATION_ALIASES:
        if column in available:
            return column
    raise ValueError("No se encontro columna de clasificacion COVID.")


def raw_file_columns(path: Path) -> list[str]:
    """Lee solo el encabezado de un CSV crudo."""
    return pd.read_csv(path, nrows=0).columns.tolist()


def selected_columns_for_file(path: Path) -> list[str]:
    """Obtiene columnas requeridas compatibles con versiones historicas del CSV."""
    columns = raw_file_columns(path)
    selected = [column for column in BASE_COLUMNS if column in columns]
    selected.append(classification_column(columns))
    return selected


def normalize_confirmed_chunk(chunk: pd.DataFrame, source_file: str) -> pd.DataFrame:
    """Filtra casos confirmados y construye variables derivadas del proyecto."""
    class_col = classification_column(chunk.columns)
    chunk = chunk.rename(columns={class_col: "CLASIFICACION_FINAL_COVID"}).copy()

    chunk["CLASIFICACION_FINAL_COVID"] = pd.to_numeric(
        chunk["CLASIFICACION_FINAL_COVID"], errors="coerce"
    )
    chunk = chunk[chunk["CLASIFICACION_FINAL_COVID"].isin(CONFIRMED_CODES)].copy()
    if chunk.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    for column in [
        "ORIGEN",
        "SECTOR",
        "ENTIDAD_UM",
        "SEXO",
        "ENTIDAD_RES",
        "MUNICIPIO_RES",
        "TIPO_PACIENTE",
        "EDAD",
        "NACIONALIDAD",
        "CLASIFICACION_FINAL_COVID",
    ] + YES_NO_COLUMNS:
        if column in chunk.columns:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

    fecha_def_raw = chunk["FECHA_DEF"].astype("string")
    fecha_def_clean = fecha_def_raw.mask(fecha_def_raw.eq("9999-99-99"))

    fecha_actualizacion = pd.to_datetime(chunk["FECHA_ACTUALIZACION"], errors="coerce")
    fecha_ingreso = pd.to_datetime(chunk["FECHA_INGRESO"], errors="coerce")
    fecha_sintomas = pd.to_datetime(chunk["FECHA_SINTOMAS"], errors="coerce")
    fecha_def = pd.to_datetime(fecha_def_clean, errors="coerce")

    output = pd.DataFrame(
        {
            "id_registro": chunk["ID_REGISTRO"].astype("string"),
            "archivo_origen": source_file,
            "fecha_actualizacion": fecha_actualizacion,
            "fecha_ingreso": fecha_ingreso,
            "fecha_sintomas": fecha_sintomas,
            "fecha_def": fecha_def,
            "anio_sintomas": fecha_sintomas.dt.year.astype("Int16"),
            "mes_sintomas": fecha_sintomas.dt.month.astype("Int8"),
            "semana_sintomas": fecha_sintomas.dt.isocalendar().week.astype("Int8"),
            "dias_sintomas_ingreso": (fecha_ingreso - fecha_sintomas).dt.days.astype(
                "Int16"
            ),
            "origen": chunk["ORIGEN"].astype("Int16"),
            "sector": chunk["SECTOR"].astype("Int16"),
            "entidad_um": chunk["ENTIDAD_UM"].astype("Int16"),
            "entidad_res": chunk["ENTIDAD_RES"].astype("Int16"),
            "municipio_res": chunk["MUNICIPIO_RES"].astype("Int32"),
            "edad": chunk["EDAD"].astype("Int16"),
            "sexo": chunk["SEXO"].astype("Int8"),
            "sexo_hombre": chunk["SEXO"].map({1: 0, 2: 1}).astype("Int8"),
            "nacionalidad": chunk["NACIONALIDAD"].astype("Int8"),
            "tipo_paciente": chunk["TIPO_PACIENTE"].astype("Int8"),
            "hospitalizacion": chunk["TIPO_PACIENTE"].map({1: 0, 2: 1}).astype("Int8"),
            "defuncion": fecha_def.notna().astype("int8"),
            "clasificacion_final_covid": chunk["CLASIFICACION_FINAL_COVID"].astype(
                "Int8"
            ),
        }
    )

    dummy_names = {
        "INTUBADO": "intubado_dummy",
        "NEUMONIA": "neumonia_dummy",
        "DIABETES": "diabetes_dummy",
        "EPOC": "epoc_dummy",
        "ASMA": "asma_dummy",
        "INMUSUPR": "inmunosupresion_dummy",
        "HIPERTENSION": "hipertension_dummy",
        "OTRA_COM": "otra_com_dummy",
        "CARDIOVASCULAR": "cardiovascular_dummy",
        "OBESIDAD": "obesidad_dummy",
        "RENAL_CRONICA": "renal_cronica_dummy",
        "TABAQUISMO": "tabaquismo_dummy",
        "UCI": "uci_dummy",
    }
    for source, target in dummy_names.items():
        output[target] = build_binary_from_yes_no(chunk[source]).astype("Int8")

    return output[OUTPUT_COLUMNS]


def build_confirmed_dataset(
    raw_dir: Path,
    output_path: Path,
    chunksize: int = 500_000,
) -> pd.DataFrame:
    """Procesa todos los CSV crudos y guarda un Parquet de casos confirmados."""
    raw_files = sorted(raw_dir.glob("COVID19MEXICO*.csv"))
    if not raw_files:
        raise FileNotFoundError(f"No se encontraron CSV en {raw_dir}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    writer: pq.ParquetWriter | None = None
    summary_rows = []
    try:
        for raw_file in raw_files:
            total_rows = 0
            confirmed_rows = 0
            usecols = selected_columns_for_file(raw_file)
            for chunk in pd.read_csv(raw_file, usecols=usecols, chunksize=chunksize):
                total_rows += len(chunk)
                processed = normalize_confirmed_chunk(chunk, raw_file.name)
                confirmed_rows += len(processed)
                if processed.empty:
                    continue
                table = pa.Table.from_pandas(processed, preserve_index=False)
                if writer is None:
                    writer = pq.ParquetWriter(output_path, table.schema)
                writer.write_table(table)

            summary_rows.append(
                {
                    "archivo": raw_file.name,
                    "registros_raw": total_rows,
                    "registros_confirmados": confirmed_rows,
                }
            )
    finally:
        if writer is not None:
            writer.close()

    return pd.DataFrame(summary_rows)


def validation_summary(processed: pd.DataFrame) -> dict[str, object]:
    """Calcula validaciones basicas de la fase 3."""
    return {
        "registros": len(processed),
        "codigos_confirmados": sorted(
            processed["clasificacion_final_covid"].dropna().unique().tolist()
        ),
        "defuncion_valores": sorted(processed["defuncion"].dropna().unique().tolist()),
        "hospitalizacion_valores": sorted(
            processed["hospitalizacion"].dropna().unique().tolist()
        ),
        "fecha_sintomas_min": processed["fecha_sintomas"].min(),
        "fecha_sintomas_max": processed["fecha_sintomas"].max(),
    }
