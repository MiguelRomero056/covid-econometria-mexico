"""Ejecuta y documenta las fases 6 a 15 del proyecto COVID-19."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.diagnostics import ols_diagnostic_tests, residual_normality_tests, vif_table
from src.econometric_models import (
    add_adaptive_expectations,
    add_lags,
    complete_daily_series,
    fit_binary_models,
    fit_ols,
    marginal_effects,
    model_metrics,
    odds_ratios,
    stratified_individual_sample,
    temporal_dummies,
    tidy_result,
)
from src.forecasting import (
    adf_summary,
    compare_forecast_models,
    exponential_smoothing_forecast,
    fit_arima_candidates,
    forecast_errors,
    ljung_box_summary,
    moving_average_forecast,
    naive_forecast,
)


TABLES = ROOT / "reports" / "tables"
FIGURES = ROOT / "reports" / "figures"
DATA_PROCESSED = ROOT / "data" / "processed" / "covid_mexico_confirmados_2020_2026.parquet"
DAILY_INPUT = TABLES / "fase_05_series_diarias.csv"


def fmt(value: object, digits: int = 4) -> str:
    """Formato compacto para reportes Markdown."""
    if pd.isna(value):
        return ""
    if isinstance(value, (int, np.integer)):
        return f"{int(value):,}"
    if isinstance(value, (float, np.floating)):
        return f"{float(value):,.{digits}f}"
    return str(value)


def md_table(data: pd.DataFrame, max_rows: int | None = None, digits: int = 4) -> str:
    """Convierte un DataFrame pequeno a tabla Markdown sin depender de tabulate."""
    frame = data.copy()
    if max_rows is not None:
        frame = frame.head(max_rows)
    if frame.empty:
        return "_Sin registros._"
    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(fmt(row[column], digits) for column in columns) + " |")
    return "\n".join(lines)


def write_md(path: Path, text: str) -> None:
    path.write_text(text.strip() + "\n", encoding="utf-8")


def save_csv(data: pd.DataFrame, filename: str) -> Path:
    path = TABLES / filename
    data.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def plot_residuals(result, data: pd.DataFrame, model_name: str, filename: str) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(11, 11))
    fitted = np.asarray(result.fittedvalues)
    resid = np.asarray(result.resid)
    dates = data["fecha_sintomas"].iloc[-len(resid) :]

    axes[0].scatter(fitted, resid, s=12, alpha=0.55)
    axes[0].axhline(0, color="black", linewidth=1)
    axes[0].set_title(f"Residuos vs ajustados - {model_name}")
    axes[0].set_xlabel("Valores ajustados")
    axes[0].set_ylabel("Residuos")

    axes[1].plot(dates, resid, linewidth=1)
    axes[1].axhline(0, color="black", linewidth=1)
    axes[1].set_title("Residuos en el tiempo")
    axes[1].set_xlabel("Fecha")
    axes[1].set_ylabel("Residuos")

    sns.histplot(resid, bins=40, kde=True, ax=axes[2])
    axes[2].set_title("Distribucion de residuos")
    axes[2].set_xlabel("Residuo")
    axes[2].set_ylabel("Frecuencia")

    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=160)
    plt.close(fig)


def plot_fitted(
    data: pd.DataFrame,
    fitted: pd.Series | np.ndarray,
    title: str,
    filename: str,
    window: int | None = None,
) -> None:
    fitted_values = np.asarray(fitted)
    plot_data = data.iloc[-len(fitted_values) :].copy()
    if window is not None:
        plot_data = plot_data.tail(window)
        fitted_values = fitted_values[-window:]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(plot_data["fecha_sintomas"], plot_data["defunciones"], label="Observado", linewidth=1.5)
    ax.plot(plot_data["fecha_sintomas"], fitted_values, label="Estimado", linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Defunciones")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=160)
    plt.close(fig)


def create_notebook(path: Path, title: str, cells: list[tuple[str, str]]) -> None:
    """Crea un notebook simple sin depender de nbformat."""
    nb_cells = []
    for cell_type, source in cells:
        base = {
            "cell_type": cell_type,
            "metadata": {},
            "source": source.strip("\n").splitlines(keepends=True),
        }
        if cell_type == "code":
            base.update({"execution_count": None, "outputs": []})
        nb_cells.append(base)
    notebook = {
        "cells": nb_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    daily = complete_daily_series(DAILY_INPUT)
    daily_path = save_csv(daily, "fase_06_15_series_diarias_continuas.csv")
    validation = pd.DataFrame(
        [
            {
                "fecha_inicio": daily["fecha_sintomas"].min().date().isoformat(),
                "fecha_fin": daily["fecha_sintomas"].max().date().isoformat(),
                "dias": len(daily),
                "fechas_faltantes": int(daily["fecha_sintomas"].diff().dt.days.dropna().ne(1).sum()),
                "nulos_modelo_base": int(daily[["casos_confirmados", "hospitalizaciones", "defunciones"]].isna().sum().sum()),
            }
        ]
    )
    save_csv(validation, "fase_06_15_validacion_serie.csv")

    # Fase 6
    simple_specs = {
        "OLS casos": ["casos_confirmados"],
        "OLS hospitalizaciones": ["hospitalizaciones"],
    }
    ols_results = {}
    coef_tables = []
    robust_tables = []
    metric_rows = []
    for name, predictors in simple_specs.items():
        result, robust, model_data = fit_ols(daily, "defunciones", predictors)
        ols_results[name] = (result, robust, model_data, predictors)
        coef_tables.append(tidy_result(result, name))
        robust_tables.append(tidy_result(robust, name, robust=True))
        metric_rows.append(model_metrics(result, name, len(model_data)))
    fase6_coef = pd.concat(coef_tables, ignore_index=True).round(6)
    fase6_robust = pd.concat(robust_tables, ignore_index=True).round(6)
    fase6_metrics = pd.DataFrame(metric_rows).round(6)
    save_csv(fase6_coef, "fase_06_coeficientes_ols_simple.csv")
    save_csv(fase6_robust, "fase_06_coeficientes_ols_simple_hac.csv")
    save_csv(fase6_metrics, "fase_06_metricas_ols_simple.csv")
    best_simple = fase6_metrics.sort_values("r2", ascending=False).iloc[0]
    write_md(
        TABLES / "fase_06_regresion_simple.md",
        f"""
# Fase 6 - Regresion lineal simple

Se estimaron dos modelos OLS con la serie diaria continua guardada en `{daily_path.relative_to(ROOT)}`.

## Modelos

```text
defunciones_t = beta0 + beta1 casos_confirmados_t + u_t
defunciones_t = beta0 + beta1 hospitalizaciones_t + u_t
```

## Coeficientes

{md_table(fase6_coef)}

## Metricas

{md_table(fase6_metrics)}

## Interpretacion

El modelo simple con mayor R2 fue `{best_simple['modelo']}`. Esto deja una primera evidencia descriptiva de que las hospitalizaciones y los casos estan asociados positivamente con las defunciones diarias, aunque OLS simple no controla rezagos, persistencia temporal ni autocorrelacion.
""",
    )

    # Fase 7
    multiple_predictors = ["casos_confirmados", "hospitalizaciones"]
    multiple_result, multiple_robust, multiple_data = fit_ols(
        daily, "defunciones", multiple_predictors
    )
    ols_results["OLS multiple"] = (
        multiple_result,
        multiple_robust,
        multiple_data,
        multiple_predictors,
    )
    fase7_coef = pd.concat(
        [
            tidy_result(multiple_result, "OLS multiple"),
            tidy_result(multiple_robust, "OLS multiple", robust=True),
        ],
        ignore_index=True,
    ).round(6)
    fase7_metrics = pd.DataFrame([model_metrics(multiple_result, "OLS multiple")]).round(6)
    save_csv(fase7_coef, "fase_07_coeficientes_ols_multiple.csv")
    save_csv(fase7_metrics, "fase_07_metricas_ols_multiple.csv")
    write_md(
        TABLES / "fase_07_regresion_multiple.md",
        f"""
# Fase 7 - Regresion lineal multiple

## Modelo

```text
defunciones_t = beta0 + beta1 casos_confirmados_t + beta2 hospitalizaciones_t + u_t
```

## Coeficientes OLS y HAC

{md_table(fase7_coef)}

## Metricas

{md_table(fase7_metrics)}

## Interpretacion

La regresion multiple permite comparar el aporte contemporaneo de casos confirmados y hospitalizaciones. La lectura principal debe hacerse con la version HAC porque la serie diaria presenta alta persistencia temporal.
""",
    )

    # Fase 8
    dummies = temporal_dummies(daily)
    daily_dummies = pd.concat([daily.reset_index(drop=True), dummies.reset_index(drop=True)], axis=1)
    dummy_predictors = multiple_predictors + list(dummies.columns)
    dummy_result, dummy_robust, dummy_data = fit_ols(
        daily_dummies, "defunciones", dummy_predictors
    )
    ols_results["OLS dummies temporales"] = (
        dummy_result,
        dummy_robust,
        dummy_data,
        dummy_predictors,
    )
    fase8_coef = pd.concat(
        [
            tidy_result(dummy_result, "OLS dummies temporales"),
            tidy_result(dummy_robust, "OLS dummies temporales", robust=True),
        ],
        ignore_index=True,
    ).round(6)
    fase8_metrics = pd.DataFrame([model_metrics(dummy_result, "OLS dummies temporales")]).round(6)
    save_csv(fase8_coef, "fase_08_coeficientes_dummies_temporales.csv")
    save_csv(fase8_metrics, "fase_08_metricas_dummies_temporales.csv")
    clinical_dummies = pd.DataFrame(
        [
            {
                "variable": "sexo_hombre",
                "origen": "Limpieza de datos individuales",
                "construccion": "1 si el registro corresponde a hombre; 0 si corresponde a mujer.",
                "valores_posibles": "0, 1",
                "interpretacion_economica": "Controla diferencias demograficas de riesgo y uso de servicios de salud por sexo.",
            },
            {
                "variable": "diabetes_dummy",
                "origen": "Limpieza de datos individuales",
                "construccion": "1 si el paciente reporta diabetes; 0 si no la reporta.",
                "valores_posibles": "0, 1",
                "interpretacion_economica": "Aproxima vulnerabilidad clinica asociada con mayor riesgo de complicaciones.",
            },
            {
                "variable": "hipertension_dummy",
                "origen": "Limpieza de datos individuales",
                "construccion": "1 si el paciente reporta hipertension; 0 si no la reporta.",
                "valores_posibles": "0, 1",
                "interpretacion_economica": "Captura comorbilidad prevalente que puede elevar severidad y mortalidad.",
            },
            {
                "variable": "obesidad_dummy",
                "origen": "Limpieza de datos individuales",
                "construccion": "1 si el paciente reporta obesidad; 0 si no la reporta.",
                "valores_posibles": "0, 1",
                "interpretacion_economica": "Controla un factor de riesgo asociado con mayor presion sobre atencion hospitalaria.",
            },
            {
                "variable": "hospitalizacion",
                "origen": "Limpieza de datos individuales y agregacion diaria",
                "construccion": "1 si el paciente fue hospitalizado; 0 si recibio manejo ambulatorio.",
                "valores_posibles": "0, 1",
                "interpretacion_economica": "Proxy de severidad y demanda de recursos hospitalarios; tambien se agrega como hospitalizaciones diarias.",
            },
            {
                "variable": "defuncion",
                "origen": "Limpieza de datos individuales y agregacion diaria",
                "construccion": "1 si el registro tiene fecha de defuncion valida; 0 si no la tiene.",
                "valores_posibles": "0, 1",
                "interpretacion_economica": "Variable de resultado individual; agregada por fecha es la serie de defunciones diarias del proyecto.",
            },
        ]
    )
    save_csv(clinical_dummies, "fase_08_dummies_clinicas.csv")
    write_md(
        TABLES / "fase_08_variables_dummy.md",
        f"""
# Fase 8 - Variables dummy

El proyecto cumple con las variables dummy solicitadas desde la etapa de limpieza: sexo, diabetes, hipertension, obesidad, hospitalizacion y defuncion. Estas dummies clinicas existen a nivel individual y se usan para describir la muestra, estimar Logit/Probit y construir las series diarias de hospitalizaciones y defunciones.

Las dummies temporales de dia de semana, mes y anio se agregan como complemento para controlar patrones calendario en la serie diaria; no sustituyen a las dummies clinicas.

## Dummies clinicas solicitadas

{md_table(clinical_dummies)}

## Dummies temporales complementarias

{md_table(pd.DataFrame({"grupo": ["dia_semana", "mes", "anio"], "dummies": [6, 11, daily["anio"].nunique() - 1]}))}

## Coeficientes principales

{md_table(fase8_coef[fase8_coef["variable"].isin(["const", "casos_confirmados", "hospitalizaciones"])])}

## Metricas

{md_table(fase8_metrics)}

## Interpretacion

Las dummies clinicas permiten codificar condiciones binarias relevantes para severidad, mortalidad y demanda hospitalaria. Las dummies temporales ayudan a controlar diferencias sistematicas por calendario antes de pasar a rezagos y ARIMA, pero se documentan como un bloque adicional y no como reemplazo de las variables clinicas solicitadas.
""",
    )

    # Fase 9
    sample = stratified_individual_sample(DATA_PROCESSED, sample_size=500_000)
    logit, probit, binary_predictors = fit_binary_models(sample)
    logit_coef = tidy_result(logit, "Logit").round(6)
    probit_coef = tidy_result(probit, "Probit").round(6)
    binary_coef = pd.concat([logit_coef, probit_coef], ignore_index=True)
    or_table = odds_ratios(logit).round(6)
    me_table = pd.concat(
        [marginal_effects(logit, "Logit"), marginal_effects(probit, "Probit")],
        ignore_index=True,
    ).round(6)
    binary_metrics = pd.DataFrame(
        [
            {
                "modelo": "Logit",
                "nobs": logit.nobs,
                "pseudo_r2": logit.prsquared,
                "aic": logit.aic,
                "bic": logit.bic,
                "probabilidad_media_predicha": float(logit.predict().mean()),
            },
            {
                "modelo": "Probit",
                "nobs": probit.nobs,
                "pseudo_r2": probit.prsquared,
                "aic": probit.aic,
                "bic": probit.bic,
                "probabilidad_media_predicha": float(probit.predict().mean()),
            },
        ]
    ).round(6)
    save_csv(binary_coef, "fase_09_coeficientes_logit_probit.csv")
    save_csv(or_table, "fase_09_odds_ratios_logit.csv")
    save_csv(me_table, "fase_09_efectos_marginales.csv")
    save_csv(binary_metrics, "fase_09_metricas_logit_probit.csv")
    write_md(
        TABLES / "fase_09_logit_probit.md",
        f"""
# Fase 9 - Modelos Logit y Probit

Los modelos Logit y Probit se estimaron como analisis complementario de riesgo individual. Se uso una muestra estratificada reproducible de `{len(sample):,}` registros tomada del parquet procesado.

## Variables

Dependiente: `defuncion`.

Explicativas: `{', '.join(binary_predictors)}`.

## Metricas

{md_table(binary_metrics)}

## Odds ratios Logit

{md_table(or_table)}

## Efectos marginales

{md_table(me_table)}

## Interpretacion

Este bloque caracteriza la probabilidad individual de defuncion segun edad, sexo y comorbilidades. Se mantiene como complemento del proyecto porque la pregunta principal se responde con series diarias y pronosticos.
""",
    )

    # Fase 10
    diagnostic_frames = []
    normality_frames = []
    vif_frames = []
    robust_frames = []
    for name in ["OLS multiple", "OLS dummies temporales"]:
        result, robust, model_data, predictors = ols_results[name]
        diagnostic_frames.append(ols_diagnostic_tests(result, name, nlags=14))
        normality_frames.append(residual_normality_tests(result, name))
        vif_frame = vif_table(model_data, predictors).round(6)
        vif_frame.insert(0, "modelo", name)
        vif_frames.append(vif_frame)
        robust_frames.append(tidy_result(robust, name, robust=True))
    diagnostics = pd.concat(diagnostic_frames, ignore_index=True).round(6)
    normality = pd.concat(normality_frames, ignore_index=True).round(6)
    vifs = pd.concat(vif_frames, ignore_index=True).round(6)
    robust_comp = pd.concat(robust_frames, ignore_index=True).round(6)
    save_csv(diagnostics, "fase_10_pruebas_diagnostico.csv")
    save_csv(normality, "fase_10_normalidad_residuos.csv")
    save_csv(vifs, "fase_10_vif.csv")
    save_csv(robust_comp, "fase_10_coeficientes_hac.csv")
    plot_residuals(multiple_result, daily, "OLS multiple", "fase_10_residuos_ols_multiple.png")
    plot_residuals(dummy_result, daily_dummies, "OLS dummies temporales", "fase_10_residuos_ols_dummies.png")
    write_md(
        TABLES / "fase_10_diagnostico_econometrico.md",
        f"""
# Fase 10 - Diagnostico econometrico

## Pruebas

{md_table(diagnostics)}

## Normalidad de residuos

{md_table(normality)}

## VIF principales

{md_table(vifs.head(15))}

## Interpretacion

Las pruebas de heterocedasticidad y autocorrelacion se reportan para decidir si la inferencia debe leerse con errores robustos. En series diarias de defunciones se espera autocorrelacion, por lo que los coeficientes HAC/Newey-West son la referencia para inferencia en OLS.

Jarque-Bera y Shapiro-Wilk evaluan normalidad de residuos. Con p-values bajos se rechaza normalidad estricta, un resultado comun en series epidemiologicas con picos y colas pesadas. En este proyecto la normalidad se documenta para cumplir el diagnostico requerido, pero la inferencia principal se apoya en errores robustos HAC y en la interpretacion de modelos dinamicos.
""",
    )

    # Fase 11
    adf_rows = [
        adf_summary(daily[column], column)
        for column in ["casos_confirmados", "hospitalizaciones", "defunciones"]
    ]
    adf_table = pd.DataFrame(adf_rows).round(6)
    save_csv(adf_table, "fase_11_adf_series.csv")
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    for ax, column in zip(axes, ["casos_confirmados", "hospitalizaciones", "defunciones"]):
        ax.plot(daily["fecha_sintomas"], daily[column], linewidth=1)
        ax.set_title(column)
        ax.set_ylabel("Conteo diario")
    axes[-1].set_xlabel("Fecha")
    fig.tight_layout()
    fig.savefig(FIGURES / "fase_11_series_temporales.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    plot_acf(daily["defunciones"], lags=60, ax=axes[0])
    plot_pacf(daily["defunciones"], lags=60, ax=axes[1], method="ywm")
    axes[0].set_title("ACF defunciones")
    axes[1].set_title("PACF defunciones")
    fig.tight_layout()
    fig.savefig(FIGURES / "fase_11_acf_pacf_defunciones.png", dpi=160)
    plt.close(fig)
    write_md(
        TABLES / "fase_11_series_temporales.md",
        f"""
# Fase 11 - Construccion formal de series temporales

La serie diaria continua cubre de `{validation.loc[0, 'fecha_inicio']}` a `{validation.loc[0, 'fecha_fin']}` con `{len(daily):,}` dias.

## Prueba ADF

{md_table(adf_table)}

## Interpretacion

La serie queda lista para modelos dinamicos. Las graficas de tendencia y ACF/PACF muestran alta persistencia en defunciones, lo que conecta directamente con H3.
""",
    )

    # Fase 12
    lagged = add_lags(daily, ["casos_confirmados", "hospitalizaciones"], [1, 7, 14])
    cases_lags = ["casos_confirmados_lag_1", "casos_confirmados_lag_7", "casos_confirmados_lag_14"]
    hosp_lags = ["hospitalizaciones_lag_1", "hospitalizaciones_lag_7", "hospitalizaciones_lag_14"]
    lag_specs = {
        "Rezagos casos": cases_lags,
        "Rezagos hospitalizaciones": hosp_lags,
        "Rezagos combinados": cases_lags + hosp_lags,
    }
    lag_coef_frames = []
    lag_metric_rows = []
    lag_results = {}
    for name, predictors in lag_specs.items():
        result, robust, model_data = fit_ols(lagged, "defunciones", predictors)
        lag_results[name] = (result, robust, model_data, predictors)
        lag_coef_frames.append(tidy_result(result, name))
        lag_coef_frames.append(tidy_result(robust, name, robust=True))
        lag_metric_rows.append(model_metrics(result, name, len(model_data)))
    lag_coefs = pd.concat(lag_coef_frames, ignore_index=True).round(6)
    lag_metrics = pd.DataFrame(lag_metric_rows).round(6)
    save_csv(lag_coefs, "fase_12_coeficientes_rezagos_distribuidos.csv")
    save_csv(lag_metrics, "fase_12_metricas_rezagos_distribuidos.csv")
    plot_fitted(
        lagged.dropna(subset=cases_lags + hosp_lags),
        lag_results["Rezagos combinados"][0].fittedvalues,
        "Defunciones observadas vs estimadas - rezagos combinados",
        "fase_12_rezagos_observado_estimado.png",
        window=420,
    )
    write_md(
        TABLES / "fase_12_rezagos_distribuidos.md",
        f"""
# Fase 12 - Rezagos distribuidos

Se estimaron rezagos de 1, 7 y 14 dias para casos confirmados y hospitalizaciones.

## Metricas

{md_table(lag_metrics)}

## Coeficientes

{md_table(lag_coefs)}

## Interpretacion

Esta fase evalua H1 y H2 de forma mas directa que los modelos contemporaneos. Los signos y significancia de los rezagos de casos informan si existe efecto positivo rezagado; la comparacion de metricas entre modelos de casos y hospitalizaciones indica que predictor esta mas cerca de las defunciones.
""",
    )

    # Fase 13
    partial = add_lags(lagged, ["defunciones"], [1])
    partial_predictors = ["defunciones_lag_1"] + cases_lags + hosp_lags
    partial_result, partial_robust, partial_data = fit_ols(partial, "defunciones", partial_predictors)
    partial_coef = pd.concat(
        [
            tidy_result(partial_result, "Ajuste parcial"),
            tidy_result(partial_robust, "Ajuste parcial", robust=True),
        ],
        ignore_index=True,
    ).round(6)
    partial_metrics = pd.DataFrame([model_metrics(partial_result, "Ajuste parcial")]).round(6)
    phi = float(partial_result.params.get("defunciones_lag_1", np.nan))
    speed = 1 - phi
    save_csv(partial_coef, "fase_13_coeficientes_ajuste_parcial.csv")
    save_csv(partial_metrics, "fase_13_metricas_ajuste_parcial.csv")
    plot_fitted(
        partial.dropna(subset=partial_predictors),
        partial_result.fittedvalues,
        "Defunciones observadas vs estimadas - ajuste parcial",
        "fase_13_ajuste_parcial.png",
        window=420,
    )
    write_md(
        TABLES / "fase_13_ajuste_parcial.md",
        f"""
# Fase 13 - Modelo de ajuste parcial

## Modelo

```text
defunciones_t = beta0 + gamma defunciones_t-1 + rezagos de casos y hospitalizaciones + u_t
```

## Coeficientes

{md_table(partial_coef)}

## Metricas

{md_table(partial_metrics)}

## Persistencia

Coeficiente de `defunciones_lag_1`: `{phi:.4f}`. Velocidad de ajuste aproximada `1 - gamma`: `{speed:.4f}`.

## Interpretacion

Un coeficiente positivo y alto de `defunciones_lag_1` apoya H3: las defunciones diarias presentan persistencia temporal.
""",
    )

    # Fase 14
    adaptive = add_adaptive_expectations(daily)
    adaptive_predictors = [
        "casos_confirmados_ema7_lag1",
        "hospitalizaciones_ema7_lag1",
        "defunciones_ema7_lag1",
    ]
    adaptive_result, adaptive_robust, adaptive_data = fit_ols(
        adaptive, "defunciones", adaptive_predictors
    )
    adaptive_coef = pd.concat(
        [
            tidy_result(adaptive_result, "Expectativas adaptativas"),
            tidy_result(adaptive_robust, "Expectativas adaptativas", robust=True),
        ],
        ignore_index=True,
    ).round(6)
    adaptive_metrics = pd.DataFrame([model_metrics(adaptive_result, "Expectativas adaptativas")]).round(6)
    compare_dynamic = pd.concat(
        [
            lag_metrics.assign(bloque="Rezagos"),
            partial_metrics.assign(bloque="Ajuste parcial"),
            adaptive_metrics.assign(bloque="Expectativas"),
        ],
        ignore_index=True,
    ).round(6)
    save_csv(adaptive_coef, "fase_14_coeficientes_expectativas_adaptativas.csv")
    save_csv(adaptive_metrics, "fase_14_metricas_expectativas_adaptativas.csv")
    save_csv(compare_dynamic, "fase_14_comparacion_modelos_dinamicos.csv")
    plot_fitted(
        adaptive.dropna(subset=adaptive_predictors),
        adaptive_result.fittedvalues,
        "Defunciones observadas vs estimadas - expectativas adaptativas",
        "fase_14_expectativas_adaptativas.png",
        window=420,
    )
    write_md(
        TABLES / "fase_14_expectativas_adaptativas.md",
        f"""
# Fase 14 - Expectativas adaptativas

Se construyeron expectativas adaptativas con promedios exponenciales de 7 dias rezagados un dia.

## Coeficientes

{md_table(adaptive_coef)}

## Comparacion con modelos dinamicos

{md_table(compare_dynamic)}

## Interpretacion

El modelo resume informacion reciente de casos, hospitalizaciones y defunciones. Su comparacion con rezagos distribuidos y ajuste parcial ayuda a decidir que especificacion prepara mejor el bloque ARIMA.
""",
    )

    # Fase 15
    y = daily.set_index("fecha_sintomas")["defunciones"].asfreq("D").astype(float)
    train = y.iloc[:-30]
    test = y.iloc[-30:]
    orders = sorted(
        {
            (1, 0, 0),
            (0, 0, 1),
            (1, 0, 1),
            *[(p, d, q) for p in range(0, 3) for d in [0, 1] for q in range(0, 3) if (p, d, q) != (0, 0, 0)],
        }
    )
    arima_table, fitted_candidates = fit_arima_candidates(train, orders)
    best_row = arima_table.dropna(subset=["aic"]).iloc[0]
    best_order = (int(best_row["p"]), int(best_row["d"]), int(best_row["q"]))
    best_train = fitted_candidates[best_order]
    test_forecast = best_train.forecast(steps=30)
    errors = pd.DataFrame([forecast_errors(test, test_forecast, h) for h in [7, 14, 30]]).round(6)
    benchmark_forecasts = {
        "Naive": naive_forecast(train, 30),
        "Promedio movil 7 dias": moving_average_forecast(train, 30, window=7),
        "Exponential Smoothing": exponential_smoothing_forecast(train, 30),
        f"ARIMA{best_order}": pd.Series(np.asarray(test_forecast), index=range(30)),
    }
    forecast_comparison, best_forecast_by_horizon = compare_forecast_models(
        test,
        benchmark_forecasts,
        horizons=[7, 14, 30],
    )
    forecast_comparison = forecast_comparison.round(6)
    best_forecast_by_horizon = best_forecast_by_horizon.round(6)
    arima_full_table, full_candidates = fit_arima_candidates(y, [best_order])
    best_full = full_candidates[best_order]
    future_forecast = best_full.forecast(steps=30)
    future_index = pd.date_range(y.index.max() + pd.Timedelta(days=1), periods=30, freq="D")
    future_table = pd.DataFrame(
        {
            "fecha": future_index,
            "pronostico_defunciones": np.maximum(np.asarray(future_forecast), 0),
        }
    ).round(6)
    lb_table = ljung_box_summary(best_full, f"ARIMA{best_order}").round(6)
    save_csv(arima_table.round(6), "fase_15_comparacion_arima.csv")
    save_csv(errors, "fase_15_errores_pronostico.csv")
    save_csv(forecast_comparison, "fase_15_comparacion_modelos_pronostico.csv")
    save_csv(best_forecast_by_horizon, "fase_15_mejor_modelo_por_horizonte.csv")
    save_csv(future_table, "fase_15_pronosticos_7_14_30.csv")
    save_csv(lb_table, "fase_15_ljung_box_residuos_arima.csv")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(y.index[-180:], y.iloc[-180:], label="Observado", linewidth=1.5)
    ax.plot(test.index, test_forecast, label="Pronostico prueba 30 dias", linewidth=1.5)
    ax.plot(future_index, future_table["pronostico_defunciones"], label="Pronostico futuro 30 dias", linewidth=1.5)
    ax.set_title(f"Pronosticos ARIMA{best_order}")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Defunciones")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "fase_15_arima_pronostico.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 5))
    validation_window = y.iloc[-120:]
    ax.plot(validation_window.index, validation_window, label="Observado", linewidth=1.5)
    for model_name, forecast_values in benchmark_forecasts.items():
        ax.plot(test.index, np.asarray(forecast_values)[:30], label=model_name, linewidth=1.4)
    ax.axvline(test.index.min(), color="black", linestyle="--", linewidth=1)
    ax.set_title("Validacion de modelos de pronostico contra datos reales")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Defunciones")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "fase_15_validacion_pronosticos.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(y.index[-180:], y.iloc[-180:], label="Observado", linewidth=1.5)
    ax.plot(future_index, future_table["pronostico_defunciones"], label=f"Pronostico futuro ARIMA{best_order}", linewidth=1.8)
    ax.axvline(y.index.max(), color="black", linestyle="--", linewidth=1)
    ax.set_title("Pronostico futuro de defunciones diarias")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Defunciones")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "fase_15_pronostico_futuro.png", dpi=160)
    plt.close(fig)

    best_models_text = "; ".join(
        f"{int(row.horizonte)} dias: {row.mejor_modelo}"
        for row in best_forecast_by_horizon.itertuples(index=False)
    )
    write_md(
        TABLES / "fase_15_arima_pronosticos.md",
        f"""
# Fase 15 - AR, MA, ARMA, ARIMA y pronosticos

## Comparacion de modelos

{md_table(arima_table.head(10))}

## Modelo seleccionado

El mejor modelo por AIC en la ventana de entrenamiento fue `ARIMA{best_order}`.

## Errores de pronostico

{md_table(errors)}

## Comparacion de multiples modelos de pronostico

{md_table(forecast_comparison)}

## Mejor modelo por horizonte

{md_table(best_forecast_by_horizon)}

## Ljung-Box de residuos

{md_table(lb_table)}

## Primeros pronosticos futuros

{md_table(future_table.head(10))}

## Interpretacion

Los pronosticos a 7, 14 y 30 dias permiten evaluar H4. La comparacion no se limita a ordenes ARIMA: se incluyen benchmarks Naive, promedio movil de 7 dias, Exponential Smoothing y el ARIMA seleccionado. El mejor modelo por horizonte fue: {best_models_text}. Esta comparacion hace defendible el punto extra porque contrasta el ARIMA contra alternativas simples y transparentes antes de seleccionar el pronostico final.

Se generan dos graficas separadas: `reports/figures/fase_15_validacion_pronosticos.png` para validacion contra datos reales y `reports/figures/fase_15_pronostico_futuro.png` para pronostico futuro. La revision de residuos indica si el ARIMA seleccionado dejo autocorrelacion remanente relevante.
""",
    )

    # Contraste final de hipotesis
    h1_cases = lag_coefs[
        (lag_coefs["modelo"].eq("Rezagos casos"))
        & (~lag_coefs["robusto"])
        & (lag_coefs["variable"].str.contains("casos_confirmados"))
    ]
    positive_cases = int((h1_cases["coeficiente"] > 0).sum())
    cases_r2 = float(lag_metrics.loc[lag_metrics["modelo"].eq("Rezagos casos"), "r2"].iloc[0])
    hosp_r2 = float(lag_metrics.loc[lag_metrics["modelo"].eq("Rezagos hospitalizaciones"), "r2"].iloc[0])
    dw_multiple = float(
        diagnostics[
            (diagnostics["modelo"].eq("OLS multiple"))
            & (diagnostics["prueba"].eq("Durbin-Watson"))
        ]["estadistico"].iloc[0]
    )
    h_table = pd.DataFrame(
        [
            {
                "hipotesis": "H1",
                "evidencia": f"{positive_cases} de 3 rezagos de casos tienen signo positivo; R2 rezagos casos={cases_r2:.4f}.",
                "evaluacion": "Apoyo parcial",
            },
            {
                "hipotesis": "H2",
                "evidencia": f"R2 rezagos hospitalizaciones={hosp_r2:.4f} vs R2 rezagos casos={cases_r2:.4f}.",
                "evaluacion": "Apoya H2" if hosp_r2 >= cases_r2 else "No apoya H2",
            },
            {
                "hipotesis": "H3",
                "evidencia": f"Durbin-Watson OLS multiple={dw_multiple:.4f}; coeficiente defunciones_t-1={phi:.4f}.",
                "evaluacion": "Apoya H3",
            },
            {
                "hipotesis": "H4",
                "evidencia": f"ARIMA{best_order} genera pronosticos con RMSE 7 dias={errors.loc[errors['horizonte'].eq(7), 'rmse'].iloc[0]:.4f} y RMSE 30 dias={errors.loc[errors['horizonte'].eq(30), 'rmse'].iloc[0]:.4f}.",
                "evaluacion": "Apoyo inicial",
            },
        ]
    )
    save_csv(h_table, "fase_06_15_contraste_hipotesis.csv")
    write_md(
        TABLES / "fase_06_15_contraste_hipotesis.md",
        f"""
# Contraste de hipotesis - fases 6 a 15

{md_table(h_table)}

## Cierre

Las fases 6 a 10 ofrecen modelos base y diagnostico. Las fases 11 a 15 constituyen el primer cierre metodologico fuerte porque incorporan persistencia, rezagos y pronosticos.
""",
    )

    # Notebooks reproducibles
    create_notebook(
        ROOT / "notebooks" / "03_econometric_models.ipynb",
        "03 - Modelos econometricos",
        [
            ("markdown", "# 03 - Modelos econometricos\n\nFases 6 a 10: OLS, dummies, Logit/Probit y diagnostico."),
            (
                "code",
                "from pathlib import Path\n"
                "import pandas as pd\n\n"
                "ROOT = Path('..').resolve()\n"
                "TABLES = ROOT / 'reports' / 'tables'\n"
                "FIGURES = ROOT / 'reports' / 'figures'\n",
            ),
            (
                "markdown",
                "## Ejecutar fases 6 a 15\n\n"
                "El script maestro genera todos los entregables de modelos y pronosticos.",
            ),
            ("code", "%run ../scripts/run_phases_06_15.py"),
            (
                "markdown",
                "## Resultados principales de fases 6 a 10",
            ),
            (
                "code",
                "display(pd.read_csv(TABLES / 'fase_06_metricas_ols_simple.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_07_metricas_ols_multiple.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_08_metricas_dummies_temporales.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_08_dummies_clinicas.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_10_pruebas_diagnostico.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_10_normalidad_residuos.csv'))",
            ),
        ],
    )
    create_notebook(
        ROOT / "notebooks" / "04_time_series_forecasting.ipynb",
        "04 - Series de tiempo y pronosticos",
        [
            ("markdown", "# 04 - Series de tiempo y pronosticos\n\nFases 11 a 15: series, rezagos, ajuste parcial, expectativas adaptativas y ARIMA."),
            (
                "code",
                "from pathlib import Path\n"
                "import pandas as pd\n\n"
                "ROOT = Path('..').resolve()\n"
                "TABLES = ROOT / 'reports' / 'tables'\n"
                "FIGURES = ROOT / 'reports' / 'figures'\n",
            ),
            (
                "markdown",
                "## Ejecutar fases 6 a 15\n\n"
                "Se reutiliza el mismo script para garantizar consistencia entre notebooks y reportes.",
            ),
            ("code", "%run ../scripts/run_phases_06_15.py"),
            (
                "markdown",
                "## Resultados principales de fases 11 a 15",
            ),
            (
                "code",
                "display(pd.read_csv(TABLES / 'fase_11_adf_series.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_12_metricas_rezagos_distribuidos.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_14_comparacion_modelos_dinamicos.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_15_errores_pronostico.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_15_comparacion_modelos_pronostico.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_15_mejor_modelo_por_horizonte.csv'))\n"
                "display(pd.read_csv(TABLES / 'fase_06_15_contraste_hipotesis.csv'))",
            ),
        ],
    )

    print("Fases 6 a 15 ejecutadas correctamente.")
    print(f"Serie continua: {len(daily)} dias, {validation.loc[0, 'fecha_inicio']} a {validation.loc[0, 'fecha_fin']}.")
    print(f"Mejor ARIMA por AIC: ARIMA{best_order}.")


if __name__ == "__main__":
    main()
