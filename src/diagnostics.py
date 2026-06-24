"""Funciones para diagnosticos econometricos."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import shapiro
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan, het_white
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera


def vif_table(model_data: pd.DataFrame, predictors: list[str]) -> pd.DataFrame:
    """Calcula VIF para predictores de un modelo lineal."""
    x = model_data[predictors].dropna().astype(float)
    rows = []
    for idx, column in enumerate(x.columns):
        try:
            vif = variance_inflation_factor(x.values, idx)
        except Exception:
            vif = np.nan
        rows.append({"variable": column, "vif": float(vif)})
    return pd.DataFrame(rows).sort_values("vif", ascending=False)


def ols_diagnostic_tests(result, model_name: str, nlags: int = 14) -> pd.DataFrame:
    """Aplica pruebas basicas de diagnostico a un resultado OLS."""
    residuals = result.resid
    exog = result.model.exog
    bp_lm, bp_lm_pvalue, bp_f, bp_f_pvalue = het_breuschpagan(residuals, exog)
    white_lm, white_lm_pvalue, white_f, white_f_pvalue = het_white(residuals, exog)
    bg_lm, bg_lm_pvalue, bg_f, bg_f_pvalue = acorr_breusch_godfrey(
        result, nlags=nlags
    )
    return pd.DataFrame(
        [
            {
                "modelo": model_name,
                "prueba": "Durbin-Watson",
                "estadistico": float(durbin_watson(residuals)),
                "p_value": np.nan,
            },
            {
                "modelo": model_name,
                "prueba": "Breusch-Pagan LM",
                "estadistico": float(bp_lm),
                "p_value": float(bp_lm_pvalue),
            },
            {
                "modelo": model_name,
                "prueba": "Breusch-Pagan F",
                "estadistico": float(bp_f),
                "p_value": float(bp_f_pvalue),
            },
            {
                "modelo": model_name,
                "prueba": "White LM",
                "estadistico": float(white_lm),
                "p_value": float(white_lm_pvalue),
            },
            {
                "modelo": model_name,
                "prueba": "White F",
                "estadistico": float(white_f),
                "p_value": float(white_f_pvalue),
            },
            {
                "modelo": model_name,
                "prueba": f"Breusch-Godfrey LM({nlags})",
                "estadistico": float(bg_lm),
                "p_value": float(bg_lm_pvalue),
            },
            {
                "modelo": model_name,
                "prueba": f"Breusch-Godfrey F({nlags})",
                "estadistico": float(bg_f),
                "p_value": float(bg_f_pvalue),
            },
        ]
    )


def residual_normality_tests(
    result,
    model_name: str,
    shapiro_sample_size: int = 5_000,
    random_state: int = 19,
) -> pd.DataFrame:
    """Aplica Jarque-Bera y Shapiro-Wilk a residuos OLS."""
    residuals = pd.Series(result.resid).dropna().astype(float)
    jb_stat, jb_pvalue, skewness, kurtosis = jarque_bera(residuals)

    if len(residuals) > shapiro_sample_size:
        shapiro_residuals = residuals.sample(
            shapiro_sample_size, random_state=random_state
        )
        shapiro_note = (
            f"Shapiro-Wilk aplicado a muestra reproducible de {shapiro_sample_size} "
            f"residuos por tamano total n={len(residuals)}."
        )
    else:
        shapiro_residuals = residuals
        shapiro_note = "Shapiro-Wilk aplicado a todos los residuos disponibles."
    shapiro_stat, shapiro_pvalue = shapiro(shapiro_residuals)

    return pd.DataFrame(
        [
            {
                "modelo": model_name,
                "prueba": "Jarque-Bera",
                "estadistico": float(jb_stat),
                "p_value": float(jb_pvalue),
                "n_residuos": int(len(residuals)),
                "muestra_usada": int(len(residuals)),
                "asimetria": float(skewness),
                "curtosis": float(kurtosis),
                "nota": "Prueba basada en asimetria y curtosis de residuos.",
            },
            {
                "modelo": model_name,
                "prueba": "Shapiro-Wilk",
                "estadistico": float(shapiro_stat),
                "p_value": float(shapiro_pvalue),
                "n_residuos": int(len(residuals)),
                "muestra_usada": int(len(shapiro_residuals)),
                "asimetria": np.nan,
                "curtosis": np.nan,
                "nota": shapiro_note,
            },
        ]
    )
