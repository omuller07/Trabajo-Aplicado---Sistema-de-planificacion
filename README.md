## Trabajo-Aplicado

# 

### Sistema de planificación de estudio y prevención de procrastinación y sobreexigencia.

# 

Lola Fanti, Clara Henestrosa, Ela Iturriaga, Olivia Muller.



##### Objetivo:



El objetivo de este proyecto es desarrollar un sistema de planificación de estudio que permita organizar de manera automática las actividades de estudio de un usuario en función de su disponibilidad horaria, las fechas de examen, la dificultad de los temas y el conocimiento previo sobre cada uno de ellos. Además, el sistema busca favorecer una mejor administración del tiempo, evitando situaciones de procrastinación y sobrecarga de estudio mediante el seguimiento del progreso realizado.



El sistema comienza solicitando al usuario información sobre su disponibilidad semanal, las materias que desea preparar, las fechas de los exámenes y los temas correspondientes a cada materia. Para cada tema se registra un nivel de dificultad y un nivel de conocimiento previo.



A partir de estos datos, el programa calcula una prioridad para cada tema considerando su dificultad, el conocimiento previo del usuario y la cercanía del examen. Luego estima la cantidad de horas de estudio necesarias y genera automáticamente un plan de estudio distribuyendo las actividades en los días disponibles antes de cada examen.



El plan generado se almacena en archivos CSV para que pueda ser recuperado posteriormente. El usuario puede consultar el calendario visual de estudio y registrar periódicamente el progreso realizado. En función de este progreso, el sistema detecta posibles situaciones de procrastinación o sobreexigencia y reorganiza automáticamente las horas pendientes en los días futuros considerando la disponibilidad del usuario. Si no es posible reubicar todas las horas faltantes, el sistema informa al usuario que debería aumentar su tiempo disponible para el estudio.



##### **Distribución de tareas entre los integrantes**



**Lola**

Desarrollo del módulo de recolección de información (recoleccion\_info.py).

Diagramas de flujo del código general y función registrar\_progreso(), y participación en el testing.



**Ela**

Desarrollo del módulo de planificación (planificador.py).

Diagrama de flujo de las funciones: generar\_nuevo\_plan() y ver\_calendario(), y participación en el testing



**Olivia**

Desarrollo del módulo de almacenamiento (almacenamiento.py).

Elaboración de la presentación del proyecto y corrección de errores (verificación.py).



**Clara**

Desarrollo del módulo gráfico (graficos.py).

Elaboración de la presentación del proyecto y corrección de errores (verificación.py).





**Trabajo realizado en conjunto**



Diseño general del sistema.

Elaboración del documento de diseño a partir de las ideas y aportes de todas las integrantes.

Desarrollo del módulo de seguimiento (seguimiento.py).

Integración de los distintos módulos mediante el archivo principal (main.py).

##### 

##### **Descripción de la fuente de datos**



El sistema no utiliza fuentes de datos externas. Todos los datos son ingresados manualmente por el usuario al momento de ejecutar el programa. Entre ellos se encuentran la disponibilidad semanal de estudio, las materias a preparar, las fechas de examen, los temas correspondientes a cada materia, el nivel de dificultad de cada tema y el conocimiento previo del usuario.



##### **Instrucciones para ejecutar el programa**



Ejecutar el archivo main.py.

Seleccionar la opción deseada desde el menú principal.

Completar la información solicitada por el sistema.

Ingresar progreso.



##### **Librerías utilizadas**



pandas: almacenamiento y manipulación de datos mediante DataFrames.

datetime: manejo de fechas.

math: cálculos matemáticos utilizados en el algoritmo de planificación.

calendar: generación de calendarios mensuales.

matplotlib: visualización gráfica del calendario de estudio.



##### **Estructura del repositorio**



Trabajo-Aplicado/

│

├── main.py

│

├── datos/

│

└── src/

&#x20;   ├── recoleccion\_info.py

&#x20;   ├── verificacion.py

&#x20;   ├── planificador.py

&#x20;   ├── almacenamiento.py

&#x20;   ├── seguimiento.py

&#x20;   └── graficos.py



##### Explicación breve de las funciones principales



**recolectar\_informacion()**

&#x09;Solicita al usuario la información necesaria para generar el plan de estudio.



**generar\_plan()**

&#x09;Calcula las prioridades de los temas, estima las horas necesarias y distribuye las actividades en función de la disponibilidad del usuario.



**crear\_calendario\_visual()**

&#x09;Genera un calendario gráfico que muestra las actividades de estudio y las fechas de examen.



**guardar\_plan()**

&#x09;Almacena el plan generado en archivos CSV para permitir su reutilización posterior.



**registrar\_progreso\_del\_dia()**

&#x09;Permite al usuario registrar el avance realizado en una fecha determinada.



**detectar\_alertas()**

&#x09;Analiza el progreso registrado y detecta posibles situaciones de procrastinación o sobreexigencia.



**reorganizar\_plan\_por\_progreso(**)

&#x09;Redistribuye horas pendientes en fechas futuras cuando el usuario no cumple completamente el plan original.





##### **Resultados, salidas, métricas y funcionalidades generadas**



El sistema genera:



Un plan de estudio personalizado.

Un calendario visual mensual con las actividades programadas.

Un resumen de prioridades de los temas.

Alertas de procrastinación.

Alertas de sobreexigencia.

Reorganización automática del plan cuando existen horas pendientes.

Archivos CSV para almacenar la información del usuario y el progreso realizado.





##### **Declaración de uso de IA**

