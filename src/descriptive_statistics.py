"""Funciones para estadistica descriptiva y visualizaciones."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


NUMERIC_VARIABLES = [
    "edad",
    "dias_sintomas_ingreso",
    "defuncion",
    "hospitalizacion",
    "sexo_hombre",
    "neumonia_dummy",
    "diabetes_dummy",
    "hipertension_dummy",
    "obesidad_dummy",
    "inmunosupresion_dummy",
]

HISTOGRAM_VARIABLES = [
    "edad",
    "dias_sintomas_ingreso",
    "defuncion",
    "hospitalizacion",
    "neumonia_dummy",
]

BOXPLOT_SPECS = [
    ("hospitalizacion", "edad", "boxplot_edad_por_hospitalizacion.png"),
    ("defuncion", "edad", "boxplot_edad_por_defuncion.png"),
]

SCATTER_SPECS = [
    ("edad", "dias_sintomas_ingreso", "defuncion", "scatter_edad_dias_defuncion.png"),
    (
        "edad",
        "dias_sintomas_ingreso",
        "hospitalizacion",
        "scatter_edad_dias_hospitalizacion.png",
    ),
]


def descriptive_table(data: pd.DataFrame, variables: list[str] | None = None) -> pd.DataFrame:
    """Genera tabla con estadisticos solicitados en la fase 5."""
    variables = variables or NUMERIC_VARIABLES
    available = [column for column in variables if column in data.columns]
    table = data[available].describe().T
    table["median"] = data[available].median(numeric_only=True)
    table["mode"] = data[available].mode(dropna=True).iloc[0]
    table["variance"] = data[available].var(numeric_only=True)
    table["coef_variation"] = table["std"] / table["mean"].replace(0, pd.NA)
    table["skewness"] = data[available].skew(numeric_only=True)
    table["kurtosis"] = data[available].kurtosis(numeric_only=True)
    ordered = [
        "count",
        "mean",
        "median",
        "mode",
        "std",
        "variance",
        "coef_variation",
        "min",
        "25%",
        "50%",
        "75%",
        "max",
        "skewness",
        "kurtosis",
    ]
    return table[ordered].round(4)


def frequency_table(data: pd.DataFrame) -> pd.DataFrame:
    """Resume tasas y frecuencias de variables binarias clave."""
    binary_columns = [
        "defuncion",
        "hospitalizacion",
        "sexo_hombre",
        "neumonia_dummy",
        "diabetes_dummy",
        "hipertension_dummy",
        "obesidad_dummy",
        "inmunosupresion_dummy",
        "epoc_dummy",
        "asma_dummy",
        "tabaquismo_dummy",
        "uci_dummy",
    ]
    rows = []
    for column in binary_columns:
        if column not in data.columns:
            continue
        valid = data[column].dropna()
        rows.append(
            {
                "variable": column,
                "observaciones_validas": int(valid.count()),
                "casos_1": int((valid == 1).sum()),
                "casos_0": int((valid == 0).sum()),
                "proporcion_1": round(float((valid == 1).mean()), 4),
            }
        )
    return pd.DataFrame(rows)


def temporal_table(data: pd.DataFrame) -> pd.DataFrame:
    """Cuenta casos, hospitalizaciones y defunciones por fecha de sintomas."""
    daily = (
        data.dropna(subset=["fecha_sintomas"])
        .groupby("fecha_sintomas")
        .agg(
            casos_confirmados=("id_registro", "count"),
            hospitalizaciones=("hospitalizacion", "sum"),
            defunciones=("defuncion", "sum"),
        )
        .reset_index()
        .sort_values("fecha_sintomas")
    )
    daily["casos_confirmados_lag_1"] = daily["casos_confirmados"].shift(1)
    daily["casos_confirmados_lag_7"] = daily["casos_confirmados"].shift(7)
    daily["casos_confirmados_lag_14"] = daily["casos_confirmados"].shift(14)
    return daily


def save_phase5_outputs(
    data: pd.DataFrame,
    tables_dir: Path,
    figures_dir: Path,
    sample_size: int = 250_000,
) -> dict[str, Path]:
    """Exporta tablas y visualizaciones minimas obligatorias de fase 5."""
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    outputs: dict[str, Path] = {}
    desc = descriptive_table(data)
    freq = frequency_table(data)
    daily = temporal_table(data)
    corr = data[[column for column in NUMERIC_VARIABLES if column in data.columns]].corr()

    desc_path = tables_dir / "fase_05_estadisticos_descriptivos.csv"
    freq_path = tables_dir / "fase_05_frecuencias_binarias.csv"
    daily_path = tables_dir / "fase_05_series_diarias.csv"
    corr_path = tables_dir / "fase_05_matriz_correlacion.csv"
    desc.to_csv(desc_path, encoding="utf-8-sig")
    freq.to_csv(freq_path, index=False, encoding="utf-8-sig")
    daily.to_csv(daily_path, index=False, encoding="utf-8-sig")
    corr.round(4).to_csv(corr_path, encoding="utf-8-sig")
    outputs.update(
        {
            "descriptive_table": desc_path,
            "frequency_table": freq_path,
            "daily_series": daily_path,
            "correlation_table": corr_path,
        }
    )

    plot_data = data
    if len(plot_data) > sample_size:
        plot_data = plot_data.sample(sample_size, random_state=19)

    for variable in HISTOGRAM_VARIABLES:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(plot_data[variable].dropna(), kde=False, ax=ax)
        ax.set_title(f"Histograma de {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Frecuencia")
        path = figures_dir / f"histograma_{variable}.png"
        fig.tight_layout()
        fig.savefig(path, dpi=160)
        plt.close(fig)
        outputs[f"histogram_{variable}"] = path

    for x_col, y_col, filename in BOXPLOT_SPECS:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=plot_data, x=x_col, y=y_col, ax=ax)
        ax.set_title(f"{y_col} por {x_col}")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        path = figures_dir / filename
        fig.tight_layout()
        fig.savefig(path, dpi=160)
        plt.close(fig)
        outputs[filename] = path

    for x_col, y_col, hue_col, filename in SCATTER_SPECS:
        scatter_data = plot_data[[x_col, y_col, hue_col]].dropna()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(
            data=scatter_data,
            x=x_col,
            y=y_col,
            hue=hue_col,
            alpha=0.25,
            s=10,
            ax=ax,
        )
        ax.set_title(f"{x_col} vs {y_col} por {hue_col}")
        path = figures_dir / filename
        fig.tight_layout()
        fig.savefig(path, dpi=160)
        plt.close(fig)
        outputs[filename] = path

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
    ax.set_title("Matriz de correlacion")
    path = figures_dir / "matriz_correlacion.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    outputs["correlation_heatmap"] = path

    return outputs
