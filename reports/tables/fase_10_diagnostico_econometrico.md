# Fase 10 - Diagnostico econometrico

## Pruebas

| modelo | prueba | estadistico | p_value |
| --- | --- | --- | --- |
| OLS multiple | Durbin-Watson | 0.2735 |  |
| OLS multiple | Breusch-Pagan LM | 898.9744 | 0.0000 |
| OLS multiple | Breusch-Pagan F | 738.7988 | 0.0000 |
| OLS multiple | White LM | 1,450.6498 | 0.0000 |
| OLS multiple | White F | 788.8937 | 0.0000 |
| OLS multiple | Breusch-Godfrey LM(14) | 1,920.5069 | 0.0000 |
| OLS multiple | Breusch-Godfrey F(14) | 841.9731 | 0.0000 |
| OLS dummies temporales | Durbin-Watson | 0.4036 |  |
| OLS dummies temporales | Breusch-Pagan LM | 963.6523 | 0.0000 |
| OLS dummies temporales | Breusch-Pagan F | 65.7755 | 0.0000 |
| OLS dummies temporales | White LM | 1,602.5187 | 0.0000 |
| OLS dummies temporales | White F | 20.4512 | 0.0000 |
| OLS dummies temporales | Breusch-Godfrey LM(14) | 1,738.7381 | 0.0000 |
| OLS dummies temporales | Breusch-Godfrey F(14) | 506.2168 | 0.0000 |

## Normalidad de residuos

| modelo | prueba | estadistico | p_value | n_residuos | muestra_usada | asimetria | curtosis | nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OLS multiple | Jarque-Bera | 14,347.9243 | 0.0000 | 2,291 | 2,291 | 1.4285 | 14.9224 | Prueba basada en asimetria y curtosis de residuos. |
| OLS multiple | Shapiro-Wilk | 0.7554 | 0.0000 | 2,291 | 2,291 |  |  | Shapiro-Wilk aplicado a todos los residuos disponibles. |
| OLS dummies temporales | Jarque-Bera | 5,754.3306 | 0.0000 | 2,291 | 2,291 | 0.6362 | 10.6591 | Prueba basada en asimetria y curtosis de residuos. |
| OLS dummies temporales | Shapiro-Wilk | 0.8813 | 0.0000 | 2,291 | 2,291 |  |  | Shapiro-Wilk aplicado a todos los residuos disponibles. |

## VIF principales

| modelo | variable | vif |
| --- | --- | --- |
| OLS multiple | hospitalizaciones | 1.9661 |
| OLS multiple | casos_confirmados | 1.9661 |
| OLS dummies temporales | hospitalizaciones | 3.8398 |
| OLS dummies temporales | casos_confirmados | 3.1183 |
| OLS dummies temporales | anio_2022 | 2.7825 |
| OLS dummies temporales | anio_2023 | 2.1935 |
| OLS dummies temporales | anio_2025 | 2.1764 |
| OLS dummies temporales | anio_2024 | 2.1705 |
| OLS dummies temporales | anio_2021 | 1.8982 |
| OLS dummies temporales | dow_4 | 1.8436 |
| OLS dummies temporales | dow_1 | 1.8394 |
| OLS dummies temporales | dow_3 | 1.8388 |
| OLS dummies temporales | dow_2 | 1.8384 |
| OLS dummies temporales | dow_6 | 1.8360 |
| OLS dummies temporales | dow_5 | 1.8297 |

## Interpretacion

Las pruebas de heterocedasticidad y autocorrelacion se reportan para decidir si la inferencia debe leerse con errores robustos. En series diarias de defunciones se espera autocorrelacion, por lo que los coeficientes HAC/Newey-West son la referencia para inferencia en OLS.

Jarque-Bera y Shapiro-Wilk evaluan normalidad de residuos. Con p-values bajos se rechaza normalidad estricta, un resultado comun en series epidemiologicas con picos y colas pesadas. En este proyecto la normalidad se documenta para cumplir el diagnostico requerido, pero la inferencia principal se apoya en errores robustos HAC y en la interpretacion de modelos dinamicos.
