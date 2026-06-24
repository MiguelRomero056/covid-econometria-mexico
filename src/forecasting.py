"""Funciones para series de tiempo y pronosticos."""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller


def adf_summary(series: pd.Series, name: str) -> dict[str, float | str]:
    """Resume la prueba Dickey-Fuller aumentada."""
    clean = series.dropna().astype(float)
    statistic, pvalue, usedlag, nobs, critical, icbest = adfuller(clean, autolag="AIC")
    return {
        "serie": name,
        "estadistico_adf": float(statistic),
        "p_value": float(pvalue),
        "rezagos_usados": float(usedlag),
        "nobs": float(nobs),
        "valor_critico_1pct": float(critical["1%"]),
        "valor_critico_5pct": float(critical["5%"]),
        "valor_critico_10pct": float(critical["10%"]),
        "icbest": float(icbest),
    }


def forecast_errors(actual: pd.Series, predicted: pd.Series, horizon: int) -> dict[str, float]:
    """Calcula errores de pronostico para un horizonte."""
    actual_h = np.asarray(actual.iloc[:horizon], dtype=float)
    pred_h = np.asarray(predicted.iloc[:horizon], dtype=float)
    error = actual_h - pred_h
    rmse = float(np.sqrt(np.mean(error**2)))
    mae = float(np.mean(np.abs(error)))
    denom = np.where(actual_h == 0, np.nan, actual_h)
    mape = float(np.nanmean(np.abs(error / denom)) * 100)
    return {"horizonte": float(horizon), "rmse": rmse, "mae": mae, "mape": mape}


def naive_forecast(train: pd.Series, steps: int) -> pd.Series:
    """Pronostico naive: repite el ultimo valor observado."""
    value = float(train.dropna().iloc[-1])
    return pd.Series([value] * steps)


def moving_average_forecast(train: pd.Series, steps: int, window: int = 7) -> pd.Series:
    """Pronostico benchmark con promedio movil fijo de los ultimos dias."""
    value = float(train.dropna().tail(window).mean())
    return pd.Series([value] * steps)


def exponential_smoothing_forecast(train: pd.Series, steps: int) -> pd.Series:
    """Pronostico benchmark con suavizamiento exponencial simple."""
    clean = train.dropna().astype(float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = SimpleExpSmoothing(
            clean,
            initialization_method="estimated",
        ).fit(optimized=True)
    forecast = result.forecast(steps)
    return pd.Series(np.asarray(forecast), index=range(steps))


def compare_forecast_models(
    actual: pd.Series,
    forecasts: dict[str, pd.Series],
    horizons: list[int] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compara modelos de pronostico en varios horizontes."""
    horizons = horizons or [7, 14, 30]
    rows = []
    for model_name, predicted in forecasts.items():
        predicted_series = pd.Series(np.asarray(predicted), index=range(len(predicted)))
        for horizon in horizons:
            row = forecast_errors(actual, predicted_series, horizon)
            row["modelo"] = model_name
            rows.append(row)
    comparison = pd.DataFrame(rows)[["modelo", "horizonte", "rmse", "mae", "mape"]]
    best = (
        comparison.sort_values(["horizonte", "rmse", "mae"])
        .groupby("horizonte", as_index=False)
        .first()
        .rename(
            columns={
                "modelo": "mejor_modelo",
                "rmse": "mejor_rmse",
                "mae": "mejor_mae",
                "mape": "mejor_mape",
            }
        )
    )
    return comparison, best


def fit_arima_candidates(
    series: pd.Series,
    orders: list[tuple[int, int, int]],
) -> tuple[pd.DataFrame, dict[tuple[int, int, int], object]]:
    """Estima candidatos ARIMA y devuelve tabla de comparacion."""
    rows = []
    fitted = {}
    clean = series.dropna().astype(float)
    for order in orders:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = ARIMA(
                    clean,
                    order=order,
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                ).fit()
            fitted[order] = result
            rows.append(
                {
                    "modelo": f"ARIMA{order}",
                    "p": order[0],
                    "d": order[1],
                    "q": order[2],
                    "aic": float(result.aic),
                    "bic": float(result.bic),
                    "llf": float(result.llf),
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "modelo": f"ARIMA{order}",
                    "p": order[0],
                    "d": order[1],
                    "q": order[2],
                    "aic": np.nan,
                    "bic": np.nan,
                    "llf": np.nan,
                    "error": str(exc)[:160],
                }
            )
    table = pd.DataFrame(rows).sort_values("aic", na_position="last")
    return table, fitted


def ljung_box_summary(result, model_name: str, lags: list[int] | None = None) -> pd.DataFrame:
    """Aplica Ljung-Box a residuos de ARIMA."""
    lags = lags or [7, 14, 30]
    table = acorr_ljungbox(result.resid.dropna(), lags=lags, return_df=True)
    table = table.reset_index(names="rezago")
    table.insert(0, "modelo", model_name)
    return table
