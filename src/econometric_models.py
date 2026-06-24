"""Funciones para modelos lineales, Logit y Probit."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


DAILY_COLUMNS = ["casos_confirmados", "hospitalizaciones", "defunciones"]
INDIVIDUAL_MODEL_COLUMNS = [
    "defuncion",
    "edad",
    "sexo_hombre",
    "diabetes_dummy",
    "hipertension_dummy",
    "obesidad_dummy",
    "neumonia_dummy",
    "inmunosupresion_dummy",
]


def complete_daily_series(path: Path | str) -> pd.DataFrame:
    """Carga la serie diaria y completa fechas faltantes con cero."""
    daily = pd.read_csv(path, parse_dates=["fecha_sintomas"])
    daily = daily[["fecha_sintomas", *DAILY_COLUMNS]].copy()
    daily = daily.groupby("fecha_sintomas", as_index=False)[DAILY_COLUMNS].sum()
    full_index = pd.date_range(
        daily["fecha_sintomas"].min(), daily["fecha_sintomas"].max(), freq="D"
    )
    daily = (
        daily.set_index("fecha_sintomas")
        .reindex(full_index)
        .rename_axis("fecha_sintomas")
        .reset_index()
    )
    daily[DAILY_COLUMNS] = daily[DAILY_COLUMNS].fillna(0).astype(int)
    daily["dia_semana"] = daily["fecha_sintomas"].dt.dayofweek
    daily["mes"] = daily["fecha_sintomas"].dt.month
    daily["anio"] = daily["fecha_sintomas"].dt.year
    daily["t"] = np.arange(1, len(daily) + 1)
    return daily


def add_lags(data: pd.DataFrame, columns: list[str], lags: list[int]) -> pd.DataFrame:
    """Agrega rezagos para una lista de columnas."""
    output = data.copy()
    for column in columns:
        for lag in lags:
            output[f"{column}_lag_{lag}"] = output[column].shift(lag)
    return output


def add_adaptive_expectations(data: pd.DataFrame) -> pd.DataFrame:
    """Crea expectativas adaptativas simples con informacion pasada."""
    output = data.copy()
    for column in ["casos_confirmados", "hospitalizaciones", "defunciones"]:
        output[f"{column}_ma7_lag1"] = output[column].rolling(7).mean().shift(1)
        output[f"{column}_ema7_lag1"] = (
            output[column].ewm(span=7, adjust=False).mean().shift(1)
        )
    return output


def temporal_dummies(data: pd.DataFrame) -> pd.DataFrame:
    """Construye dummies calendario para dia de semana, mes y anio."""
    dummy_source = data[["dia_semana", "mes", "anio"]].astype("category")
    return pd.get_dummies(
        dummy_source,
        columns=["dia_semana", "mes", "anio"],
        drop_first=True,
        dtype=int,
        prefix=["dow", "mes", "anio"],
    )


def fit_ols(
    data: pd.DataFrame,
    dependent: str,
    predictors: list[str],
    hac_lags: int | None = 14,
):
    """Estima OLS y opcionalmente una version robusta HAC/Newey-West."""
    model_data = data[[dependent, *predictors]].dropna().copy()
    y = model_data[dependent].astype(float)
    x = sm.add_constant(model_data[predictors].astype(float), has_constant="add")
    result = sm.OLS(y, x).fit()
    robust = None
    if hac_lags is not None:
        robust = result.get_robustcov_results(cov_type="HAC", maxlags=hac_lags)
    return result, robust, model_data


def tidy_result(result, model_name: str, robust: bool = False) -> pd.DataFrame:
    """Convierte un resultado statsmodels en tabla de coeficientes."""
    params = pd.Series(result.params, index=result.model.exog_names)
    bse = pd.Series(result.bse, index=result.model.exog_names)
    pvalues = pd.Series(result.pvalues, index=result.model.exog_names)
    conf = pd.DataFrame(result.conf_int(), index=result.model.exog_names)
    conf.columns = ["ci_low", "ci_high"]
    table = pd.DataFrame(
        {
            "modelo": model_name,
            "robusto": robust,
            "variable": params.index,
            "coeficiente": params.values,
            "error_std": bse.values,
            "p_value": pvalues.values,
            "ci_95_inf": conf["ci_low"].values,
            "ci_95_sup": conf["ci_high"].values,
        }
    )
    return table


def model_metrics(result, model_name: str, nobs: int | None = None) -> dict[str, float]:
    """Extrae metricas comparables de un modelo."""
    y = np.asarray(result.model.endog)
    fitted = np.asarray(result.fittedvalues)
    rmse = float(np.sqrt(np.mean((y - fitted) ** 2)))
    mae = float(np.mean(np.abs(y - fitted)))
    return {
        "modelo": model_name,
        "nobs": float(nobs or result.nobs),
        "r2": float(getattr(result, "rsquared", np.nan)),
        "r2_ajustado": float(getattr(result, "rsquared_adj", np.nan)),
        "aic": float(getattr(result, "aic", np.nan)),
        "bic": float(getattr(result, "bic", np.nan)),
        "rmse": rmse,
        "mae": mae,
    }


def stratified_individual_sample(
    path: Path | str,
    sample_size: int = 500_000,
    random_state: int = 19,
) -> pd.DataFrame:
    """Carga columnas individuales y toma muestra estratificada por defuncion."""
    data = pd.read_parquet(path, columns=INDIVIDUAL_MODEL_COLUMNS)
    data = data.dropna().copy()
    if len(data) <= sample_size:
        return data
    frac = sample_size / len(data)
    sampled = (
        data.groupby("defuncion", group_keys=False)
        .sample(frac=frac, random_state=random_state)
        .reset_index(drop=True)
    )
    return sampled


def fit_binary_models(data: pd.DataFrame):
    """Estima Logit y Probit para defuncion individual."""
    y = data["defuncion"].astype(float)
    predictors = [column for column in INDIVIDUAL_MODEL_COLUMNS if column != "defuncion"]
    x = sm.add_constant(data[predictors].astype(float), has_constant="add")
    logit = sm.Logit(y, x).fit(method="lbfgs", maxiter=200, disp=False)
    probit = sm.Probit(y, x).fit(method="lbfgs", maxiter=200, disp=False)
    return logit, probit, predictors


def odds_ratios(logit_result) -> pd.DataFrame:
    """Calcula odds ratios e intervalos para Logit."""
    params = pd.Series(logit_result.params, index=logit_result.model.exog_names)
    conf = pd.DataFrame(logit_result.conf_int(), index=logit_result.model.exog_names)
    conf.columns = ["ci_low", "ci_high"]
    return pd.DataFrame(
        {
            "variable": params.index,
            "odds_ratio": np.exp(params.values),
            "or_ci_95_inf": np.exp(conf["ci_low"].values),
            "or_ci_95_sup": np.exp(conf["ci_high"].values),
        }
    )


def marginal_effects(binary_result, model_name: str) -> pd.DataFrame:
    """Calcula efectos marginales en la media de las covariables."""
    margeff = binary_result.get_margeff(at="mean")
    frame = margeff.summary_frame().reset_index(names="variable")
    frame.insert(0, "modelo", model_name)
    return frame
