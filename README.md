## Trabajo-Aplicado

# 

### Sistema de planificación de estudio y prevención de procrastinación y sobreexigencia.

# 

Lola Fanti, Clara Henestrosa, Ela Iturriaga, Olivia Muller.





### Objetivo:



El objetivo de este proyecto es desarrollar un sistema de planificación de estudio que permita organizar de manera automática las actividades de estudio de un usuario en función de su disponibilidad horaria, las fechas de examen, la dificultad de los temas y el conocimiento previo sobre cada uno de ellos. Además, el sistema busca favorecer una mejor administración del tiempo, evitando situaciones de procrastinación y sobrecarga de estudio mediante el seguimiento del progreso realizado.



El sistema comienza solicitando al usuario información sobre su disponibilidad semanal, las materias que desea preparar, las fechas de los exámenes y los temas correspondientes a cada materia. Para cada tema se registra un nivel de dificultad y un nivel de conocimiento previo.



A partir de estos datos, el programa calcula una prioridad para cada tema considerando su dificultad, el conocimiento previo del usuario y la cercanía del examen. Luego estima la cantidad de horas de estudio necesarias y genera automáticamente un plan de estudio distribuyendo las actividades en los días disponibles antes de cada examen.



El plan generado se almacena en archivos CSV para que pueda ser recuperado posteriormente. El usuario puede consultar el calendario visual de estudio y registrar periódicamente el progreso realizado. En función de este progreso, el sistema detecta posibles situaciones de procrastinación o sobreexigencia y reorganiza automáticamente las horas pendientes en los días futuros considerando la disponibilidad del usuario. Si no es posible reubicar todas las horas faltantes, el sistema informa al usuario que debería aumentar su tiempo disponible para el estudio.





### **Distribución de tareas entre los integrantes**



Para organizar el desarrollo del proyecto, decidimos dividir las tareas en grupos de a dos, ya que nos pareció la forma más eficiente de avanzar con las distintas partes del sistema. Sin embargo, a medida que fuimos perfeccionando el programa, todas participamos en la revisión, corrección y mejora de las distintas funciones. Por este motivo, los commits del repositorio no reflejan de manera completamente exacta la división inicial de tareas, ya que en varias ocasiones trabajamos de a parejas en una misma computadora o realizamos modificaciones conjuntas sobre partes del código que originalmente habían sido asignadas a otro grupo. De esta manera, aunque hubo una organización inicial por áreas, el trabajo final fue revisado y mejorado de forma colaborativa por todas las integrantes.



#### **Lola**

Desarrollo del módulo de recolección de información (recoleccion\_info.py).

Desarrollo del módulo de planificación (planificador.py).

Diagramas de flujo del código general y función registrar\_progreso(), generar\_nuevo\_plan() y participación en el testing.

Descripción en el README.



#### **Ela**

Desarrollo del módulo gráfico (graficos.py).

Desarrollo del módulo de almacenamiento (almacenamiento.py).

Diagrama de flujo de las funciones: ver\_calendario(), y participación en el testing.

Descripción en el README.

Creación de docstrings de main y recolección info.

#### 

#### **Olivia**

Desarrollo del módulo gráfico (graficos.py).

Desarrollo del módulo de seguimiento (seguimiento.py).

Elaboración de la presentación del proyecto.

Creacion de docstring de los modulos planificador y verificacion.





#### **Clara**

Corrección de errores (verificación.py).

Desarrollo del módulo de planificación (planificador.py).

Elaboración de la presentación del proyecto.

Creacion de docstring de los modulos graficos, seguimientos y almacenamiento.





### **Trabajo realizado en conjunto**



Diseño general del sistema.

Elaboración del documento de diseño a partir de las ideas y aportes de todas las integrantes.

Integración de los distintos módulos mediante el archivo principal (main.py).

Arreglos y perfeccionamiento de los distintos archivos y funciones.

##### 

### **Descripción de la fuente de datos**



El sistema no utiliza fuentes de datos externas. Todos los datos son ingresados manualmente por el usuario al momento de ejecutar el programa. Entre ellos se encuentran la disponibilidad semanal de estudio, las materias a preparar, las fechas de examen, los temas correspondientes a cada materia, el nivel de dificultad de cada tema y el conocimiento previo del usuario.





### **Instrucciones para ejecutar el programa**



Ejecutar el archivo main.py.

Seleccionar la opción deseada desde el menú principal.

Completar la información solicitada por el sistema.

Opcional: Ingresar progreso.





### **Librerías utilizadas**



pandas: almacenamiento y manipulación de datos mediante DataFrames.

datetime: manejo de fechas.

math: cálculos matemáticos utilizados en el algoritmo de planificación.

calendar: generación de calendarios mensuales.

matplotlib: visualización gráfica del calendario de estudio.





### **Estructura del repositorio**



Trabajo-Aplicado---Sistema-de-planificación/

├── datos/

├── docs/

├── src/

│   ├── almacenamiento.py

│   ├── graficos.py

│   ├── planificador.py

│   ├── recoleccion\_info.py

│   ├── seguimiento.py

│   └── verificacion.py

├── main.py

└── README.md





### **Explicación breve de las funciones principales**



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





### 

### **Resultados, salidas, métricas y funcionalidades generadas**



El sistema genera:



Un plan de estudio personalizado.

Un calendario visual mensual con las actividades programadas.

Alertas de procrastinación.

Alertas de sobreexigencia.

Reorganización automática del plan cuando existen horas pendientes.

Archivos CSV para almacenar la información del usuario y el progreso realizado.



### 

### **Declaración de uso de IA**



Durante el desarrollo del proyecto utilizamos herramientas de inteligencia artificial como apoyo complementario en distintas etapas del trabajo. En primer lugar, nos ayudó en la lluvia de ideas inicial, para pensar posibles enfoques del sistema y organizar mejor los objetivos del proyecto. También la utilizamos para ordenar nuestras ideas al momento de redactar los párrafos del documento de diseño y del README. En relación con el código, la IA nos sirvió para obtener una idea general sobre cómo estructurar algunas funciones, que luego fueron revisadas, modificadas y perfeccionadas por nosotras según las necesidades específicas del programa. Además, la usamos para conocer librerías útiles para la creación del calendario, resolver dudas puntuales, corregir errores y pensar posibles soluciones cuando alguna parte del código no funcionaba correctamente. De todos modos, las decisiones finales, la adaptación del código y la integración del sistema fueron realizadas por el grupo.

#### 

#### **Algunos prompts utilizados:** 



* "¿Cómo se asignan los temas a cada día? es una pregunta que no se como responder, bajo que criterios decís que se asignan los temas"



* "Necesitamos implementar un calendario visual para un planificador de estudio desarrollado en Python. El calendario debe permitir mostrar actividades de estudio dentro de cada día del mes, indicar fechas de examen y diferenciar visualmente distintos tipos de actividades mediante colores. ¿Qué librería recomendás utilizar para esto?"



* "Con todo esto que hablamos y el documento con la información brindada del trabajo y las librerías pandas, calendar, matplotlib, e imagiando que sos un programador experto, que funciones podrían ser útiles para la creación del calendario visual, utilizando data frames con la información brindada por el usuario."



* "Necesito que en el archivo de grafico, hagas que el texto de cada tarea este en un linea en vez de uno arriba del otro, ya que esto genera problemas visuales si hay demasiadas tareas. NO CAMBIES NADA MAS."



* "En nuestro proyecto de planificación de estudio estamos almacenando la disponibilidad, las materias y los temas utilizando varios diccionarios y DataFrames. Sin embargo, la disponibilidad semanal es la misma para todas las materias y cada materia agrupa temas que comparten la misma fecha de examen. ¿La estructura actual está generando información redundante? ¿Se podría simplificar el modelo de datos para evitar almacenar información repetida y mantener una organización más eficiente y fácil de mantener? Proponé una alternativa y explicá qué cambios habría que realizar en los módulos del sistema."



* "¿Encontrás algún error en este código?"

