# Proyecto Final — Modelos Econométricos

## Análisis Econométrico Integral de la Evolución, Mortalidad y Hospitalización por COVID-19 en México

### Contexto inicial del proyecto

Este proyecto corresponde al curso de **Modelos Econométricos** y tiene como propósito desarrollar un análisis econométrico completo utilizando datos oficiales sobre COVID-19 en México.

La pandemia de COVID-19 generó uno de los conjuntos de datos epidemiológicos más relevantes de los últimos años. A partir de esta información, el proyecto busca estudiar relaciones entre variables demográficas, clínicas y temporales mediante técnicas econométricas vistas durante el curso.

El análisis debe enfocarse en explicar, analizar y predecir fenómenos asociados con la pandemia, principalmente:

- Mortalidad por COVID-19.
- Hospitalización de pacientes.
- Evolución temporal de casos, hospitalizaciones o defunciones.
- Relación entre características clínicas/demográficas y resultados epidemiológicos.
- Comportamiento dinámico de variables a través del tiempo.

La fuente obligatoria de datos será el portal oficial de **Datos Abiertos COVID-19 de la Secretaría de Salud de México**:

https://www.gob.mx/salud/documentos/datos-abiertos-152127

El proyecto debe desarrollarse como una investigación aplicada, con pregunta de investigación, hipótesis, metodología, modelos econométricos, pruebas de diagnóstico, interpretación económica y presentación de resultados.

---

## Objetivo general del proyecto

Aplicar técnicas econométricas estáticas, dinámicas y predictivas para analizar los factores asociados a la mortalidad, hospitalización y evolución temporal del COVID-19 en México utilizando datos abiertos oficiales.

---

## Enfoque recomendado para el proyecto

Para mantener el proyecto ordenado y evitar dispersión, se recomienda trabajar con una línea central de análisis:

### Pregunta guía sugerida

**¿En qué medida los casos confirmados y hospitalizaciones permiten explicar y pronosticar las defunciones por COVID-19 en México entre 2020 y 2026?**

Esta pregunta permite cubrir prácticamente todas las etapas solicitadas por el profesor, ya que permite trabajar con:

- Casos confirmados diarios.
- Hospitalizaciones diarias.
- Defunciones diarias.
- Rezagos de 1, 7 y 14 días.
- Ajuste parcial.
- Expectativas adaptativas.
- Modelos AR, MA, ARMA y ARIMA.
- Pronósticos de 7, 14 y 30 días.
- Variables clínicas y demográficas como caracterización complementaria.

---

## Variables sugeridas

### Variables dependientes principales

1. **Defunción**
   - Variable binaria.
   - 1 si el paciente falleció.
   - 0 si el paciente no falleció.

2. **Hospitalización**
   - Variable binaria.
   - 1 si el paciente fue hospitalizado.
   - 0 si el paciente fue ambulatorio.

### Variables explicativas sugeridas

- Edad.
- Sexo.
- Diabetes.
- Hipertensión.
- Obesidad.
- Neumonía.
- Inmunosupresión.
- EPOC.
- Asma.
- Tabaquismo.
- Entidad federativa.
- Fecha de ingreso.
- Fecha de síntomas.
- Fecha de defunción.
- Resultado COVID.
- Tipo de paciente.

### Variables temporales sugeridas

- Casos diarios.
- Defunciones diarias.
- Hospitalizaciones diarias.
- Casos rezagados 1 día.
- Casos rezagados 7 días.
- Casos rezagados 14 días.
- Hospitalizaciones rezagadas.
- Defunciones rezagadas.

---

# Fases de trabajo recomendadas

## Fase 0. Preparación inicial del repositorio

### Objetivo

Crear la estructura base del proyecto para trabajar de forma ordenada desde el inicio.

### Tareas

- Crear repositorio en GitHub.
- Crear estructura de carpetas.
- Crear archivo `README.md`.
- Crear notebook principal.
- Crear archivo de requerimientos.
- Definir convenciones de nombres.

### Estructura sugerida

```text
covid-econometria-mexico/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
│
├── notebooks/
│   ├── 01_data_loading_cleaning.ipynb
│   ├── 02_descriptive_analysis.ipynb
│   ├── 03_econometric_models.ipynb
│   ├── 04_time_series_forecasting.ipynb
│   └── 05_final_results.ipynb
│
├── src/
│   ├── data_preprocessing.py
│   ├── descriptive_statistics.py
│   ├── econometric_models.py
│   ├── diagnostics.py
│   └── forecasting.py
│
├── reports/
│   ├── figures/
│   ├── tables/
│   └── final_report.pdf
│
├── presentation/
│   └── final_presentation.pptx
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Resultado esperado

Un repositorio listo para comenzar el desarrollo del proyecto.

---

## Fase 1. Obtención de los datos

### Objetivo

Descargar los datos oficiales de COVID-19 desde la Secretaría de Salud de México.

### Tareas

- Entrar al portal oficial de Datos Abiertos COVID-19.
- Descargar la base de datos.
- Descargar el diccionario de datos.
- Guardar los archivos originales en `data/raw/`.
- Documentar la fecha de descarga.
- Revisar el tamaño de los archivos y el formato disponible.

### Resultado esperado

Datos oficiales almacenados sin modificar en la carpeta `data/raw/`.

### Nota importante

Esta debe ser la primera fase real de trabajo, porque todo el proyecto depende de comprender la estructura de la base, las variables disponibles, los códigos del diccionario y el volumen de datos.

---

## Fase 2. Comprensión del diccionario de datos

### Objetivo

Entender qué significa cada variable antes de limpiar o modelar.

### Tareas

- Revisar el diccionario de datos.
- Identificar variables clínicas.
- Identificar variables demográficas.
- Identificar variables temporales.
- Identificar variables de resultado.
- Identificar códigos especiales como:
  - Sí.
  - No.
  - No aplica.
  - Se ignora.
  - No especificado.
- Documentar las variables que se usarán.

### Variables mínimas a revisar

- `FECHA_ACTUALIZACION`
- `ID_REGISTRO`
- `ORIGEN`
- `SECTOR`
- `ENTIDAD_UM`
- `SEXO`
- `ENTIDAD_NAC`
- `ENTIDAD_RES`
- `MUNICIPIO_RES`
- `TIPO_PACIENTE`
- `FECHA_INGRESO`
- `FECHA_SINTOMAS`
- `FECHA_DEF`
- `INTUBADO`
- `NEUMONIA`
- `EDAD`
- `NACIONALIDAD`
- `EMBARAZO`
- `DIABETES`
- `EPOC`
- `ASMA`
- `INMUSUPR`
- `HIPERTENSION`
- `OTRA_COM`
- `CARDIOVASCULAR`
- `OBESIDAD`
- `RENAL_CRONICA`
- `TABAQUISMO`
- `UCI`
- `CLASIFICACION_FINAL`

### Resultado esperado

Una tabla o sección documentada con las variables seleccionadas y su justificación.

---

## Fase 3. Limpieza y preparación de datos

### Objetivo

Construir una base limpia y lista para análisis econométrico.

### Tareas

- Cargar la base en Python o R.
- Filtrar registros relevantes.
- Convertir fechas a formato datetime.
- Crear variable binaria de defunción.
- Crear variable binaria de hospitalización.
- Crear variables dummy de enfermedades.
- Crear variable dummy de sexo.
- Tratar valores faltantes o códigos especiales.
- Filtrar casos confirmados de COVID-19 si se decide trabajar solo con confirmados.
- Guardar base procesada en `data/processed/`.

### Variables derivadas sugeridas

```text
defuncion
hospitalizacion
sexo_hombre
diabetes_dummy
hipertension_dummy
obesidad_dummy
neumonia_dummy
inmunosupresion_dummy
fecha_ingreso_dt
fecha_sintomas_dt
fecha_defuncion_dt
dias_sintomas_ingreso
```

### Resultado esperado

Un dataset limpio y documentado, listo para estadística descriptiva y modelos.

---

## Fase 4. Definición formal de pregunta e hipótesis

### Objetivo

Establecer el marco de investigación del proyecto.

### Pregunta de investigación sugerida

**¿En qué medida los casos confirmados y hospitalizaciones permiten explicar y pronosticar las defunciones por COVID-19 en México entre 2020 y 2026?**

### Hipótesis sugeridas

1. Los casos confirmados tienen un efecto positivo y rezagado sobre las defunciones diarias.
2. Las hospitalizaciones son un predictor más cercano de las defunciones que los casos confirmados.
3. Las defunciones diarias presentan autocorrelación y persistencia temporal.
4. Los modelos ARIMA permiten generar pronósticos razonables de corto plazo para horizontes de 7, 14 y 30 días.

### Resultado esperado

Pregunta e hipótesis listas para incorporarse al reporte técnico.

---

## Fase 5. Estadística descriptiva

### Objetivo

Explorar los datos antes de construir los modelos.

### Tareas

- Calcular media, mediana y moda.
- Calcular varianza, desviación estándar y coeficiente de variación.
- Calcular asimetría y curtosis.
- Generar histogramas.
- Generar diagramas de caja.
- Generar diagramas de dispersión.
- Generar matriz de correlación.
- Interpretar los hallazgos principales.

### Visualizaciones mínimas obligatorias en esta fase

- 5 histogramas.
- 2 diagramas de caja.
- 2 diagramas de dispersión.
- 1 matriz de correlación.

### Resultado esperado

Sección de estadística descriptiva con tablas, gráficas e interpretación.

---

## Fase 6. Regresión lineal simple

### Objetivo

Construir un primer modelo econométrico básico.

### Modelo sugerido

```text
hospitalizacion = β0 + β1 edad + u
```

También puede usarse:

```text
defuncion = β0 + β1 edad + u
```

### Tareas

- Estimar el modelo.
- Interpretar el coeficiente de edad.
- Revisar significancia estadística.
- Calcular intervalo de confianza.
- Reportar R².
- Explicar las limitaciones de usar regresión lineal con una variable dependiente binaria.

### Resultado esperado

Modelo simple estimado e interpretado.

---

## Fase 7. Regresión lineal múltiple

### Objetivo

Evaluar el efecto conjunto de varias variables explicativas.

### Modelo sugerido

```text
hospitalizacion = β0 + β1 edad + β2 diabetes + β3 hipertension + β4 obesidad + β5 neumonia + β6 sexo_hombre + u
```

O bien:

```text
defuncion = β0 + β1 edad + β2 diabetes + β3 hipertension + β4 obesidad + β5 neumonia + β6 sexo_hombre + u
```

### Tareas

- Estimar el modelo multivariable.
- Interpretar coeficientes.
- Comparar signos esperados con signos obtenidos.
- Analizar significancia individual.
- Analizar significancia global.
- Revisar bondad de ajuste.
- Guardar tabla de resultados.

### Resultado esperado

Modelo múltiple estimado, explicado y listo para el reporte.

---

## Fase 8. Variables dummy

### Objetivo

Construir e interpretar variables binarias dentro de los modelos.

### Variables dummy obligatorias

- Sexo.
- Diabetes.
- Hipertensión.
- Obesidad.
- Hospitalización.
- Defunción.

### Tareas

- Crear las variables dummy.
- Verificar codificación.
- Usarlas dentro de modelos lineales, Logit y Probit.
- Interpretar económicamente sus coeficientes.

### Resultado esperado

Variables dummy correctamente construidas y documentadas.

---

## Fase 9. Modelos Logit y Probit

### Objetivo

Modelar formalmente la probabilidad de defunción u hospitalización.

### Variable dependiente recomendada

```text
defuncion
```

### Variables explicativas sugeridas

```text
edad
sexo_hombre
diabetes_dummy
hipertension_dummy
obesidad_dummy
neumonia_dummy
inmunosupresion_dummy
```

### Tareas

- Estimar modelo Logit.
- Estimar modelo Probit.
- Calcular Odds Ratios en Logit.
- Calcular efectos marginales.
- Calcular probabilidades predichas.
- Comparar Logit vs Probit.
- Interpretar resultados con enfoque de salud pública.

### Resultado esperado

Modelos Logit y Probit completos, comparados e interpretados.

---

## Fase 10. Diagnóstico econométrico

### Objetivo

Evaluar si los modelos cumplen supuestos econométricos básicos.

### 10.1 Multicolinealidad

Aplicar:

- Matriz de correlación.
- VIF.

Interpretar si existen variables altamente correlacionadas.

### 10.2 Heterocedasticidad

Aplicar:

- Breusch-Pagan.
- White.

Si existe heterocedasticidad:

- Aplicar errores robustos.
- Comparar resultados con y sin errores robustos.

### 10.3 Autocorrelación

Aplicar:

- Durbin-Watson.
- Breusch-Godfrey.

Especialmente para modelos con datos temporales.

### 10.4 Normalidad

Aplicar:

- Jarque-Bera.
- Shapiro-Wilk.

También analizar gráficamente los residuos.

### Visualizaciones obligatorias relacionadas

- 2 gráficas de residuos.

### Resultado esperado

Sección de diagnóstico con pruebas, resultados, interpretación y correcciones cuando aplique.

---

## Fase 11. Construcción de series temporales

### Objetivo

Preparar series diarias para modelos dinámicos y pronóstico.

### Series sugeridas

- Casos confirmados diarios.
- Defunciones diarias.
- Hospitalizaciones diarias.

### Tareas

- Agrupar datos por fecha.
- Contar casos diarios.
- Contar defunciones diarias.
- Contar hospitalizaciones diarias.
- Ordenar cronológicamente.
- Revisar valores faltantes en fechas.
- Suavizar si es necesario con promedio móvil.
- Guardar serie temporal procesada.

### Resultado esperado

Dataset temporal listo para rezagos, ARIMA y pronósticos.

---

## Fase 12. Modelos con rezagos distribuidos

### Objetivo

Analizar si una variable pasada influye sobre una variable actual.

### Modelo sugerido

```text
defunciones_t = β0 + β1 casos_t + β2 casos_t-1 + β3 casos_t-7 + β4 casos_t-14 + u_t
```

### Rezagos obligatorios

- 1 día.
- 7 días.
- 14 días.

### Tareas

- Crear variables rezagadas.
- Estimar modelo.
- Interpretar efecto contemporáneo.
- Interpretar efecto rezagado.
- Calcular efecto acumulado.
- Calcular multiplicador de largo plazo.

### Resultado esperado

Modelo de rezagos distribuido aplicado a casos, defunciones u hospitalizaciones.

---

## Fase 13. Modelo de ajuste parcial

### Objetivo

Analizar la velocidad con la que una variable se ajusta a su nivel de equilibrio en el tiempo.

### Variable sugerida

- Defunciones diarias.
- Hospitalizaciones diarias.
- Casos diarios.

### Tareas

- Definir variable dependiente temporal.
- Incluir rezago de la variable dependiente.
- Estimar modelo.
- Calcular velocidad de ajuste.
- Interpretar persistencia temporal.
- Interpretar equilibrio de largo plazo.

### Resultado esperado

Modelo dinámico con interpretación de velocidad de ajuste y persistencia.

---

## Fase 14. Modelo de expectativas adaptativas

### Objetivo

Modelar cómo las expectativas actuales dependen de información pasada.

### Variables sugeridas

- Casos diarios.
- Hospitalizaciones diarias.
- Defunciones diarias.

### Tareas

- Construir variable esperada usando información pasada.
- Estimar modelo con expectativas adaptativas.
- Calcular error de predicción.
- Interpretar impacto de expectativas pasadas.
- Explicar cómo se forman las expectativas en el contexto de COVID-19.

### Resultado esperado

Modelo de expectativas adaptativas aplicado e interpretado.

---

## Fase 15. Modelos de series de tiempo y ARIMA

### Objetivo

Modelar y pronosticar una serie temporal epidemiológica.

### Serie recomendada

```text
defunciones_diarias
```

También puede usarse:

```text
casos_diarios
hospitalizaciones_diarias
```

### Tareas

- Aplicar prueba ADF.
- Verificar estacionariedad.
- Diferenciar la serie si es necesario.
- Estimar modelos AR.
- Estimar modelos MA.
- Estimar modelos ARMA.
- Estimar modelos ARIMA.
- Comparar modelos con AIC y BIC.
- Seleccionar mejor modelo.
- Generar pronósticos.

### Horizontes de pronóstico obligatorios

- 7 días.
- 14 días.
- 30 días.

### Visualizaciones obligatorias relacionadas

- 2 gráficas de pronóstico.

### Resultado esperado

Modelo de serie de tiempo seleccionado y pronósticos generados.

---

## Fase 16. Investigación bibliográfica

### Objetivo

Comparar los resultados del proyecto con literatura científica y fuentes oficiales.

### Requisitos

- Al menos 5 artículos científicos indexados.
- Al menos 3 fuentes oficiales.

### Fuentes oficiales sugeridas

- Secretaría de Salud de México.
- INEGI.
- Organización Mundial de la Salud.
- Organización Panamericana de la Salud.
- CONAHCYT.
- Gobierno de México.

### Tareas

- Buscar artículos sobre factores asociados a mortalidad por COVID-19.
- Buscar artículos sobre hospitalización y comorbilidades.
- Buscar referencias oficiales sobre COVID-19 en México.
- Comparar hallazgos propios con los hallazgos de la literatura.
- Redactar sección de discusión bibliográfica.

### Resultado esperado

Sección bibliográfica con comparación real entre resultados del proyecto y fuentes externas.

---

## Fase 17. Interpretación económica y de política pública

### Objetivo

Traducir los resultados estadísticos en conclusiones útiles.

### Preguntas obligatorias a responder

1. ¿Qué variables son más importantes?
2. ¿Cuáles son estadísticamente significativas?
3. ¿Qué implicaciones tienen para políticas públicas?
4. ¿Qué limitaciones tiene el estudio?
5. ¿Qué recomendaciones pueden derivarse de los resultados obtenidos?

### Resultado esperado

Discusión final del proyecto con interpretación clara y no solo técnica.

---

## Fase 18. Dashboard resumen

### Objetivo

Crear una visualización ejecutiva del proyecto.

### Contenido sugerido

- Total de casos analizados.
- Total de defunciones.
- Total de hospitalizaciones.
- Distribución por edad.
- Distribución por sexo.
- Principales comorbilidades.
- Serie temporal de casos o defunciones.
- Resultados principales de modelos.
- Pronóstico final.

### Herramientas posibles

- Python con Plotly/Dash.
- Power BI.
- Tableau.
- Streamlit.
- Excel.

### Resultado esperado

Dashboard resumen obligatorio para presentar resultados de forma visual.

---

## Fase 19. Redacción del reporte técnico

### Objetivo

Integrar todo el proyecto en un documento formal de 20 a 30 páginas.

### Estructura obligatoria

1. Portada.
2. Resumen.
3. Introducción.
4. Marco teórico.
5. Pregunta de investigación.
6. Hipótesis.
7. Descripción de los datos.
8. Metodología.
9. Estadística descriptiva.
10. Modelos econométricos.
11. Diagnósticos.
12. Pronósticos.
13. Discusión.
14. Conclusiones.
15. Referencias.

### Resultado esperado

Reporte técnico completo en PDF.

---

## Fase 20. Presentación y video

### Objetivo

Preparar la exposición final del proyecto.

### Requisitos del video

- Duración de 15 a 20 minutos.
- Participación de todos los integrantes.
- URL activa hasta final de semestre.
- URL colocada en la primera página del reporte técnico.

### Contenido mínimo del video

- Introducción.
- Preparación de datos.
- Explicación de modelos.
- Diagnósticos.
- Resultados.
- Interpretación económica.
- Conclusiones.

### Resultado esperado

Presentación final y video listos para entregar.

---

# Entregables principales

Los entregables obligatorios son:

1. Reporte técnico en PDF.
2. Código fuente.
3. Notebook de Python, R o Gretl.
4. Repositorio GitHub.
5. Presentación final.
6. URL del video de exposición.

---

# Orden recomendado de ejecución

## Prioridad 1

1. Crear repositorio.
2. Descargar datos oficiales.
3. Leer diccionario de datos.
4. Definir variables principales.
5. Limpiar la base.

## Prioridad 2

6. Formular pregunta e hipótesis.
7. Hacer estadística descriptiva.
8. Crear visualizaciones obligatorias.
9. Construir regresión simple.
10. Construir regresión múltiple.

## Prioridad 3

11. Crear variables dummy.
12. Construir Logit y Probit.
13. Calcular Odds Ratios, efectos marginales y probabilidades predichas.
14. Aplicar pruebas de diagnóstico.

## Prioridad 4

15. Construir series temporales.
16. Crear rezagos.
17. Estimar rezagos distribuidos.
18. Estimar ajuste parcial.
19. Estimar expectativas adaptativas.
20. Estimar AR, MA, ARMA y ARIMA.
21. Generar pronósticos.

## Prioridad 5

22. Buscar bibliografía.
23. Redactar interpretación económica.
24. Crear dashboard.
25. Redactar reporte final.
26. Preparar presentación.
27. Grabar video.
28. Subir todo a GitHub.

---

# Primer paso recomendado

El primer paso real del proyecto debe ser:

## Descargar y comprender los datos oficiales

Antes de modelar, graficar o redactar, se debe obtener la base oficial y el diccionario de datos. Esta etapa es fundamental porque permitirá saber:

- Qué variables existen.
- Qué variables sirven para responder la pregunta.
- Cómo están codificadas.
- Qué tan grande es la base.
- Qué limpieza será necesaria.
- Qué modelos son realmente viables.

Una vez descargada la base, el siguiente paso inmediato será construir un notebook de limpieza y exploración inicial.

---

# Decisiones iniciales que debe tomar el equipo

Antes de avanzar demasiado, el equipo debe decidir:

1. Si trabajará con todos los registros o solo con casos confirmados.
2. Si el foco principal será defunción, hospitalización o ambas.
3. Qué rango temporal analizará.
4. Si el análisis será nacional o también por entidad federativa.
5. Qué herramienta principal usará: Python, R, Gretl u otra.
6. Si el dashboard será en Python, Power BI, Tableau o Excel.
7. Cómo se dividirá el trabajo entre integrantes.

---

# Recomendación metodológica

Para este proyecto, se recomienda utilizar **Python** como herramienta principal, porque permite integrar en un solo flujo:

- Limpieza de datos.
- Estadística descriptiva.
- Visualizaciones.
- Regresiones.
- Modelos Logit y Probit.
- Pruebas econométricas.
- Modelos de series de tiempo.
- Pronósticos.
- Exportación de tablas y gráficas.

Librerías sugeridas:

```text
pandas
numpy
matplotlib
seaborn
statsmodels
scipy
sklearn
plotly
pmdarima
jupyter
```

---

# Posible división de trabajo

Si el equipo tiene tres integrantes, se puede dividir así:

## Integrante 1: Datos y descriptiva

- Descarga de datos.
- Limpieza.
- Diccionario de variables.
- Estadística descriptiva.
- Visualizaciones iniciales.

## Integrante 2: Modelos estáticos y diagnóstico

- Regresión lineal simple.
- Regresión lineal múltiple.
- Variables dummy.
- Logit y Probit.
- Multicolinealidad.
- Heterocedasticidad.
- Normalidad.

## Integrante 3: Modelos dinámicos y comunicación

- Series de tiempo.
- Rezagos distribuidos.
- Ajuste parcial.
- Expectativas adaptativas.
- ARIMA.
- Pronósticos.
- Dashboard.
- Presentación y video.

---

# Riesgos del proyecto

## Riesgo 1. Base de datos muy grande

La base de COVID puede ser pesada. Puede requerir optimización de lectura o trabajar con una muestra si la computadora no soporta todo.

### Posible solución

- Leer por chunks.
- Usar columnas seleccionadas.
- Trabajar con formatos comprimidos.
- Guardar versión procesada en Parquet.

## Riesgo 2. Variables mal codificadas

Algunas variables usan códigos especiales como 97, 98 o 99.

### Posible solución

- Revisar cuidadosamente el diccionario.
- Convertir códigos especiales en valores faltantes o categorías separadas.

## Riesgo 3. Variable dependiente binaria usada en regresión lineal

Hospitalización y defunción son binarias, por lo que la regresión lineal tiene limitaciones.

### Posible solución

- Usar regresión lineal solo para cumplir la etapa.
- Usar Logit y Probit como modelos principales para interpretación probabilística.

## Riesgo 4. Series de tiempo con cambios estructurales

La pandemia tuvo olas, cambios de prueba, vacunación y variantes.

### Posible solución

- Reconocerlo como limitación.
- Analizar periodos específicos.
- Usar promedios móviles.
- Incluir interpretación prudente.

## Riesgo 5. Exceso de modelos sin narrativa

El proyecto pide muchas técnicas, pero puede volverse una lista de modelos sin historia.

### Posible solución

Mantener una narrativa central:

**Explicación y pronóstico de defunciones diarias a partir de casos confirmados, hospitalizaciones y dinámica temporal.**

---

# Cierre

Este proyecto debe entenderse como un análisis econométrico integral. No se trata únicamente de correr modelos, sino de construir una historia investigativa completa:

1. Se plantea una pregunta.
2. Se formulan hipótesis.
3. Se preparan datos oficiales.
4. Se exploran los datos.
5. Se estiman modelos.
6. Se validan supuestos.
7. Se hacen pronósticos.
8. Se comparan resultados con literatura.
9. Se interpretan implicaciones económicas y de política pública.
10. Se comunican los hallazgos mediante reporte, presentación y video.
