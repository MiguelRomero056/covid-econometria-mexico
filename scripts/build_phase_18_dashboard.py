"""Construye el dashboard ejecutivo de la fase 18."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "reports" / "tables"
FIGURES = ROOT / "reports" / "figures"
DASHBOARD = ROOT / "reports" / "dashboard"
NOTEBOOKS = ROOT / "notebooks"


def fmt_int(value: float | int) -> str:
    return f"{int(round(float(value))):,}"


def fmt_pct(value: float | int) -> str:
    return f"{float(value) * 100:.2f}%"


def fmt_num(value: float | int, digits: int = 4) -> str:
    return f"{float(value):,.{digits}f}"


def read_csv(name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(TABLES / name, **kwargs)


def metric_card(label: str, value: str, note: str = "") -> str:
    note_html = f"<span>{note}</span>" if note else ""
    return f"""
    <article class="metric-card">
      <p>{label}</p>
      <strong>{value}</strong>
      {note_html}
    </article>
    """


def image_panel(title: str, filename: str, alt: str) -> str:
    path = f"../figures/{filename}"
    return f"""
    <article class="visual-panel">
      <h3>{title}</h3>
      <img src="{path}" alt="{alt}">
    </article>
    """


def table_html(data: pd.DataFrame, columns: list[str] | None = None, max_rows: int | None = None) -> str:
    frame = data.copy()
    if columns is not None:
        frame = frame[columns]
    if max_rows is not None:
        frame = frame.head(max_rows)
    return frame.to_html(index=False, classes="data-table", border=0, escape=False)


def create_notebook(path: Path) -> None:
    cells = [
        (
            "markdown",
            "# 05 - Resultados finales y dashboard\n\n"
            "Notebook de integracion para revisar los resultados principales y regenerar el dashboard de fase 18.",
        ),
        (
            "code",
            "from pathlib import Path\n"
            "import pandas as pd\n\n"
            "ROOT = Path('..').resolve()\n"
            "TABLES = ROOT / 'reports' / 'tables'\n"
            "DASHBOARD = ROOT / 'reports' / 'dashboard' / 'fase_18_dashboard.html'\n",
        ),
        (
            "markdown",
            "## Regenerar dashboard\n\n"
            "Ejecuta este bloque si cambian las tablas o graficas de fases 1 a 15.",
        ),
        ("code", "%run ../scripts/build_phase_18_dashboard.py"),
        ("markdown", "## Indicadores ejecutivos"),
        (
            "code",
            "display(pd.read_csv(TABLES / 'fase_18_dashboard_kpis.csv'))\n"
            "display(pd.read_csv(TABLES / 'fase_06_15_contraste_hipotesis.csv'))",
        ),
        ("markdown", "## Modelos y pronosticos"),
        (
            "code",
            "display(pd.read_csv(TABLES / 'fase_12_metricas_rezagos_distribuidos.csv'))\n"
            "display(pd.read_csv(TABLES / 'fase_15_errores_pronostico.csv'))\n"
            "print(f'Dashboard HTML: {DASHBOARD}')",
        ),
    ]
    notebook_cells = []
    for cell_type, source in cells:
        cell = {
            "cell_type": cell_type,
            "metadata": {},
            "source": source.splitlines(keepends=True),
        }
        if cell_type == "code":
            cell.update({"execution_count": None, "outputs": []})
        notebook_cells.append(cell)
    notebook = {
        "cells": notebook_cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    DASHBOARD.mkdir(parents=True, exist_ok=True)

    daily = read_csv("fase_06_15_series_diarias_continuas.csv", parse_dates=["fecha_sintomas"])
    freq = read_csv("fase_05_frecuencias_binarias.csv")
    lag_metrics = read_csv("fase_12_metricas_rezagos_distribuidos.csv")
    arima_errors = read_csv("fase_15_errores_pronostico.csv")
    hypotheses = read_csv("fase_06_15_contraste_hipotesis.csv")
    forecast = read_csv("fase_15_pronosticos_7_14_30.csv", parse_dates=["fecha"])

    def count_for(variable: str) -> int:
        return int(freq.loc[freq["variable"].eq(variable), "casos_1"].iloc[0])

    total_cases = int(freq["observaciones_validas"].max())
    total_deaths = count_for("defuncion")
    total_hosp = count_for("hospitalizacion")
    fatality_rate = total_deaths / total_cases
    hosp_rate = total_hosp / total_cases
    date_min = daily["fecha_sintomas"].min().date().isoformat()
    date_max = daily["fecha_sintomas"].max().date().isoformat()
    forecast_min = forecast["fecha"].min().date().isoformat()
    forecast_max = forecast["fecha"].max().date().isoformat()

    best_lag = lag_metrics.sort_values("r2", ascending=False).iloc[0]
    rmse_30 = float(arima_errors.loc[arima_errors["horizonte"].eq(30), "rmse"].iloc[0])
    rmse_7 = float(arima_errors.loc[arima_errors["horizonte"].eq(7), "rmse"].iloc[0])

    kpis = pd.DataFrame(
        [
            {"indicador": "Casos confirmados analizados", "valor": total_cases},
            {"indicador": "Defunciones", "valor": total_deaths},
            {"indicador": "Hospitalizaciones", "valor": total_hosp},
            {"indicador": "Tasa de letalidad observada", "valor": fatality_rate},
            {"indicador": "Tasa de hospitalizacion observada", "valor": hosp_rate},
            {"indicador": "Dias en serie continua", "valor": len(daily)},
            {"indicador": "R2 mejor modelo de rezagos", "valor": float(best_lag["r2"])},
            {"indicador": "RMSE ARIMA 7 dias", "valor": rmse_7},
            {"indicador": "RMSE ARIMA 30 dias", "valor": rmse_30},
        ]
    )
    kpis.to_csv(TABLES / "fase_18_dashboard_kpis.csv", index=False, encoding="utf-8-sig")

    cards = "\n".join(
        [
            metric_card("Casos analizados", fmt_int(total_cases), f"{date_min} a {date_max}"),
            metric_card("Defunciones", fmt_int(total_deaths), fmt_pct(fatality_rate)),
            metric_card("Hospitalizaciones", fmt_int(total_hosp), fmt_pct(hosp_rate)),
            metric_card("Serie diaria", fmt_int(len(daily)), "dias continuos"),
            metric_card("Mejor R2 de rezagos", fmt_num(best_lag["r2"]), str(best_lag["modelo"])),
            metric_card("RMSE ARIMA 30d", fmt_num(rmse_30), f"{forecast_min} a {forecast_max}"),
        ]
    )

    hypothesis_view = hypotheses.copy()
    hypothesis_view["evidencia"] = hypothesis_view["evidencia"].str.replace(";", "<br>", regex=False)

    comorbidities = freq[
        freq["variable"].isin(
            [
                "neumonia_dummy",
                "diabetes_dummy",
                "hipertension_dummy",
                "obesidad_dummy",
                "inmunosupresion_dummy",
                "epoc_dummy",
                "asma_dummy",
                "tabaquismo_dummy",
            ]
        )
    ].copy()
    comorbidities["prevalencia"] = comorbidities["proporcion_1"].map(lambda value: fmt_pct(value))
    comorbidities = comorbidities.sort_values("proporcion_1", ascending=False)

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dashboard fase 18 - COVID-19 Mexico</title>
  <style>
    :root {{
      color-scheme: light;
      --text: #172033;
      --muted: #667085;
      --line: #d9e2ec;
      --panel: #ffffff;
      --soft: #f5f7fb;
      --brand: #1d4ed8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--text);
      background: var(--soft);
    }}
    header {{
      padding: 28px clamp(18px, 4vw, 56px);
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }}
    header h1 {{
      margin: 0 0 8px;
      font-size: clamp(26px, 4vw, 42px);
      line-height: 1.1;
      letter-spacing: 0;
    }}
    header p {{
      margin: 0;
      max-width: 980px;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.5;
    }}
    main {{
      width: min(1220px, calc(100% - 32px));
      margin: 22px auto 42px;
    }}
    section {{
      margin-top: 22px;
      padding: 20px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    h2 {{
      margin: 0 0 14px;
      font-size: 20px;
      letter-spacing: 0;
    }}
    h3 {{
      margin: 0 0 10px;
      font-size: 16px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 12px;
      margin-top: 18px;
    }}
    .metric-card {{
      min-height: 118px;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #ffffff;
    }}
    .metric-card p {{
      margin: 0 0 10px;
      color: var(--muted);
      font-size: 13px;
    }}
    .metric-card strong {{
      display: block;
      font-size: 24px;
      line-height: 1.2;
    }}
    .metric-card span {{
      display: block;
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 18px;
    }}
    .visual-panel {{
      min-width: 0;
    }}
    .visual-panel img {{
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    .data-table th,
    .data-table td {{
      padding: 10px 8px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }}
    .data-table th {{
      color: #344054;
      background: #f8fafc;
    }}
    footer {{
      width: min(1220px, calc(100% - 32px));
      margin: 0 auto 28px;
      color: var(--muted);
      font-size: 13px;
    }}
    @media (max-width: 980px) {{
      .metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 560px) {{
      .metrics {{ grid-template-columns: 1fr; }}
      section {{ padding: 14px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Dashboard ejecutivo COVID-19 Mexico</h1>
    <p>Fase 18 del proyecto econometrico. Resume la muestra confirmada, tendencias temporales, comorbilidades, resultados de modelos con rezagos y pronosticos ARIMA.</p>
    <div class="metrics">{cards}</div>
  </header>
  <main>
    <section>
      <h2>Series temporales y pronostico</h2>
      <div class="grid-2">
        {image_panel("Casos, hospitalizaciones y defunciones", "fase_11_series_temporales.png", "Series temporales COVID-19")}
        {image_panel("Pronostico ARIMA", "fase_15_arima_pronostico.png", "Pronostico ARIMA de defunciones")}
      </div>
    </section>
    <section>
      <h2>Exploracion descriptiva</h2>
      <div class="grid-2">
        {image_panel("Distribucion de edad", "histograma_edad.png", "Histograma de edad")}
        {image_panel("Matriz de correlacion", "matriz_correlacion.png", "Matriz de correlacion")}
      </div>
    </section>
    <section>
      <h2>Modelos dinamicos</h2>
      <div class="grid-2">
        {image_panel("Rezagos combinados", "fase_12_rezagos_observado_estimado.png", "Modelo de rezagos observado contra estimado")}
        {image_panel("Ajuste parcial", "fase_13_ajuste_parcial.png", "Modelo de ajuste parcial")}
      </div>
    </section>
    <section>
      <h2>Metricas de rezagos</h2>
      {table_html(lag_metrics)}
    </section>
    <section>
      <h2>Comorbilidades principales</h2>
      {table_html(comorbidities, ["variable", "casos_1", "observaciones_validas", "prevalencia"])}
    </section>
    <section>
      <h2>Contraste de hipotesis</h2>
      {table_html(hypothesis_view)}
    </section>
    <section>
      <h2>Errores de pronostico ARIMA</h2>
      {table_html(arima_errors)}
    </section>
  </main>
  <footer>
    Generado con <code>scripts/build_phase_18_dashboard.py</code>. Fuentes internas: tablas y graficas de fases 5 a 15.
  </footer>
</body>
</html>
"""

    dashboard_path = DASHBOARD / "fase_18_dashboard.html"
    dashboard_path.write_text(html, encoding="utf-8")

    summary = f"""
# Fase 18 - Dashboard resumen

## Artefacto generado

- Dashboard HTML: `reports/dashboard/fase_18_dashboard.html`
- KPIs exportados: `reports/tables/fase_18_dashboard_kpis.csv`
- Script reproducible: `scripts/build_phase_18_dashboard.py`

## Contenido incluido

- Total de casos confirmados analizados: {fmt_int(total_cases)}.
- Total de defunciones: {fmt_int(total_deaths)}.
- Total de hospitalizaciones: {fmt_int(total_hosp)}.
- Serie diaria continua de {date_min} a {date_max}.
- Principales comorbilidades.
- Tendencias temporales de casos, hospitalizaciones y defunciones.
- Comparacion de modelos con rezagos.
- Pronostico ARIMA final y errores de validacion.
- Contraste sintetico de hipotesis.

## Estado

La fase 18 queda implementada como dashboard estatico en HTML. La revision conceptual y estetica final queda pendiente para la auditoria guiada.
"""
    (TABLES / "fase_18_dashboard_resumen.md").write_text(summary.strip() + "\n", encoding="utf-8")
    create_notebook(NOTEBOOKS / "05_final_results.ipynb")

    print(f"Dashboard generado: {dashboard_path}")
    print(f"KPIs generados: {TABLES / 'fase_18_dashboard_kpis.csv'}")


if __name__ == "__main__":
    main()
