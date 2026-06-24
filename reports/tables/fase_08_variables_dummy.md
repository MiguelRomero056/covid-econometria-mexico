# Fase 8 - Variables dummy

El proyecto cumple con las variables dummy solicitadas desde la etapa de limpieza: sexo, diabetes, hipertension, obesidad, hospitalizacion y defuncion. Estas dummies clinicas existen a nivel individual y se usan para describir la muestra, estimar Logit/Probit y construir las series diarias de hospitalizaciones y defunciones.

Las dummies temporales de dia de semana, mes y anio se agregan como complemento para controlar patrones calendario en la serie diaria; no sustituyen a las dummies clinicas.

## Dummies clinicas solicitadas

| variable | origen | construccion | valores_posibles | interpretacion_economica |
| --- | --- | --- | --- | --- |
| sexo_hombre | Limpieza de datos individuales | 1 si el registro corresponde a hombre; 0 si corresponde a mujer. | 0, 1 | Controla diferencias demograficas de riesgo y uso de servicios de salud por sexo. |
| diabetes_dummy | Limpieza de datos individuales | 1 si el paciente reporta diabetes; 0 si no la reporta. | 0, 1 | Aproxima vulnerabilidad clinica asociada con mayor riesgo de complicaciones. |
| hipertension_dummy | Limpieza de datos individuales | 1 si el paciente reporta hipertension; 0 si no la reporta. | 0, 1 | Captura comorbilidad prevalente que puede elevar severidad y mortalidad. |
| obesidad_dummy | Limpieza de datos individuales | 1 si el paciente reporta obesidad; 0 si no la reporta. | 0, 1 | Controla un factor de riesgo asociado con mayor presion sobre atencion hospitalaria. |
| hospitalizacion | Limpieza de datos individuales y agregacion diaria | 1 si el paciente fue hospitalizado; 0 si recibio manejo ambulatorio. | 0, 1 | Proxy de severidad y demanda de recursos hospitalarios; tambien se agrega como hospitalizaciones diarias. |
| defuncion | Limpieza de datos individuales y agregacion diaria | 1 si el registro tiene fecha de defuncion valida; 0 si no la tiene. | 0, 1 | Variable de resultado individual; agregada por fecha es la serie de defunciones diarias del proyecto. |

## Dummies temporales complementarias

| grupo | dummies |
| --- | --- |
| dia_semana | 6 |
| mes | 11 |
| anio | 6 |

## Coeficientes principales

| modelo | robusto | variable | coeficiente | error_std | p_value | ci_95_inf | ci_95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OLS dummies temporales | 0 | const | -31.3451 | 3.9038 | 0.0000 | -39.0005 | -23.6897 |
| OLS dummies temporales | 0 | casos_confirmados | -0.0064 | 0.0001 | 0.0000 | -0.0067 | -0.0062 |
| OLS dummies temporales | 0 | hospitalizaciones | 0.5793 | 0.0021 | 0.0000 | 0.5752 | 0.5834 |
| OLS dummies temporales | 1 | const | -31.3451 | 15.3690 | 0.0415 | -61.4839 | -1.2063 |
| OLS dummies temporales | 1 | casos_confirmados | -0.0064 | 0.0007 | 0.0000 | -0.0078 | -0.0051 |
| OLS dummies temporales | 1 | hospitalizaciones | 0.5793 | 0.0181 | 0.0000 | 0.5439 | 0.6147 |

## Metricas

| modelo | nobs | r2 | r2_ajustado | aic | bic | rmse | mae |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OLS dummies temporales | 2,291.0000 | 0.9910 | 0.9909 | 21,509.4658 | 21,658.6212 | 26.1553 | 16.6925 |

## Interpretacion

Las dummies clinicas permiten codificar condiciones binarias relevantes para severidad, mortalidad y demanda hospitalaria. Las dummies temporales ayudan a controlar diferencias sistematicas por calendario antes de pasar a rezagos y ARIMA, pero se documentan como un bloque adicional y no como reemplazo de las variables clinicas solicitadas.
