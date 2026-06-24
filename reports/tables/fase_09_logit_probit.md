# Fase 9 - Modelos Logit y Probit

Los modelos Logit y Probit se estimaron como analisis complementario de riesgo individual. Se uso una muestra estratificada reproducible de `500,000` registros tomada del parquet procesado.

## Variables

Dependiente: `defuncion`.

Explicativas: `edad, sexo_hombre, diabetes_dummy, hipertension_dummy, obesidad_dummy, neumonia_dummy, inmunosupresion_dummy`.

## Metricas

| modelo | nobs | pseudo_r2 | aic | bic | probabilidad_media_predicha |
| --- | --- | --- | --- | --- | --- |
| Logit | 500,000 | 0.4710 | 94,681.2207 | 94,770.1996 | 0.0435 |
| Probit | 500,000 | 0.4791 | 93,222.6044 | 93,311.5833 | 0.0431 |

## Odds ratios Logit

| variable | odds_ratio | or_ci_95_inf | or_ci_95_sup |
| --- | --- | --- | --- |
| const | 0.0004 | 0.0004 | 0.0005 |
| edad | 1.0627 | 1.0615 | 1.0639 |
| sexo_hombre | 1.6892 | 1.6296 | 1.7510 |
| diabetes_dummy | 1.6631 | 1.5948 | 1.7343 |
| hipertension_dummy | 1.3633 | 1.3081 | 1.4208 |
| obesidad_dummy | 1.5611 | 1.4907 | 1.6349 |
| neumonia_dummy | 27.1817 | 26.2324 | 28.1653 |
| inmunosupresion_dummy | 1.8868 | 1.6567 | 2.1488 |

## Efectos marginales

| modelo | variable | dy/dx | Std. Err. | z | Pr(>|z|) | Conf. Int. Low | Cont. Int. Hi. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Logit | edad | 0.0006 | 0.0000 | 76.7854 | 0.0000 | 0.0005 | 0.0006 |
| Logit | sexo_hombre | 0.0048 | 0.0002 | 27.8020 | 0.0000 | 0.0045 | 0.0051 |
| Logit | diabetes_dummy | 0.0047 | 0.0002 | 22.8853 | 0.0000 | 0.0043 | 0.0051 |
| Logit | hipertension_dummy | 0.0028 | 0.0002 | 14.4081 | 0.0000 | 0.0025 | 0.0032 |
| Logit | obesidad_dummy | 0.0041 | 0.0002 | 18.8116 | 0.0000 | 0.0037 | 0.0045 |
| Logit | neumonia_dummy | 0.0303 | 0.0004 | 69.8183 | 0.0000 | 0.0294 | 0.0311 |
| Logit | inmunosupresion_dummy | 0.0058 | 0.0006 | 9.5115 | 0.0000 | 0.0046 | 0.0070 |
| Probit | edad | 0.0006 | 0.0000 | 70.2818 | 0.0000 | 0.0006 | 0.0006 |
| Probit | sexo_hombre | 0.0055 | 0.0002 | 27.9202 | 0.0000 | 0.0051 | 0.0058 |
| Probit | diabetes_dummy | 0.0056 | 0.0002 | 23.5066 | 0.0000 | 0.0052 | 0.0061 |
| Probit | hipertension_dummy | 0.0036 | 0.0002 | 15.6477 | 0.0000 | 0.0031 | 0.0040 |
| Probit | obesidad_dummy | 0.0045 | 0.0002 | 18.2761 | 0.0000 | 0.0041 | 0.0050 |
| Probit | neumonia_dummy | 0.0360 | 0.0006 | 60.7741 | 0.0000 | 0.0348 | 0.0371 |
| Probit | inmunosupresion_dummy | 0.0073 | 0.0007 | 10.3217 | 0.0000 | 0.0059 | 0.0087 |

## Interpretacion

Este bloque caracteriza la probabilidad individual de defuncion segun edad, sexo y comorbilidades. Se mantiene como complemento del proyecto porque la pregunta principal se responde con series diarias y pronosticos.
