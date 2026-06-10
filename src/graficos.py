import matplotlib.pyplot as plt
import calendar
from datetime import date


def convertir_plan_a_texto(plan, año, mes):
    """
    Convierte las actividades planificadas de un mes en textos organizados por día.

    Parameters:
    ----------
    plan : dict
        Diccionario donde cada clave es una fecha y cada valor es una lista de actividades planificadas para ese día.

    año : int
        Año del calendario que se desea generar.

    mes : int
        Mes del calendario que se desea generar.

    Returns:
    ----------
    dict
        Diccionario donde la clave es el número de día del mes y el valor es un texto con todas las actividades de ese día.
    """
    plan_por_dia = {}

    for fecha, actividades in plan.items():
        if fecha.year == año and fecha.month == mes:
    
            textos = []
    
            for actividad in actividades:
                texto = (actividad["actividad"] + " | " + actividad["materia"] + " | "
                         + actividad["tema"] + " | " + str(actividad["horas"]) + " hs")
    
                textos.append(texto)
    
            plan_por_dia[fecha.day] = "\n".join(textos)
                # fecha.day --> obtiene el número del día del mes
                # "\n\n".join(textos) --> une todas las actividades del día separándolas mediante dos saltos de línea.
    
    return plan_por_dia


def obtener_meses_del_plan(plan, df_materias):
    """
     • Obtiene los meses y años que deben mostrarse en el calendario.
     • Considera tanto las fechas con actividades planificadas como las fechas de examen de las materias.
    
     Parameters:
     ----------
     plan : dict
         Diccionario que contiene las actividades organizadas por fecha.
    
     df_materias : pandas.DataFrame
         DataFrame con la información de las materias y sus fechas de examen.
    
     Returns:
     ----------
     list
         Lista de tuplas (año, mes) sin repetir.
     """
    meses = []

    for fecha in plan.keys():
        mes_año = (fecha.year, fecha.month)
        # Extrae año y mes

        if mes_año not in meses:
            meses.append(mes_año)

    for indice, fila in df_materias.iterrows():
        fecha_examen = fila["fecha_examen"]
        mes_año = (fecha_examen.year, fecha_examen.month)
        # Extrae año y mes

        if mes_año not in meses:
            meses.append(mes_año)

    return meses


def crear_calendario_visual(plan, df_materias):
    """
    Genera y muestra un calendario visual con las actividades planificadas y las fechas de examen.

    Parameters:
    ----------
    plan : dict
        Diccionario donde cada clave es una fecha y cada valor es una lista de actividades planificadas.

    df_materias : pandas.DataFrame
        DataFrame con la información de las materias y sus fechas de examen.

    Returns:
    ----------
    None
    """
    meses = obtener_meses_del_plan(plan, df_materias)

    for año, mes in meses:
        plan_por_dia = convertir_plan_a_texto( plan, año, mes 
                                              )
        for indice, materia in df_materias.iterrows():
            fecha_examen = materia["fecha_examen"]
            # Recorre las filas del dataframe y busca fecha de examen

            if fecha_examen.year == año and fecha_examen.month == mes:
                if fecha_examen.day in plan_por_dia:
                    plan_por_dia[fecha_examen.day] += "\n\nEXAMEN\n" + materia["materia"]

                else:
                    plan_por_dia[fecha_examen.day] = "EXAMEN\n" + materia["materia"]

        cal = calendar.monthcalendar(año, mes)
        # Crea una lista de listas --> cada lista representa una semana del mes con fechas.

        fig, ax = plt.subplots(figsize=(16, 10))
        # Crea una figura (fig) y ejes (ax). figsize indica tamaño de figura

        fig.patch.set_facecolor("#FAFAFA")
        # .patch es el rectangulo que forma el fondo de la figura, facecolor cambia el color

        ax.axis("off")
        # Oculta los ejes

        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        tabla = []
        # Lista de listas de filas

        for semana in cal:
            fila = []
            # Lista con el número de día y las actividades correspondientes.

            for dia in semana:
                if dia == 0:
                    fila.append("")

                else:
                    texto = str(dia)

                    if dia in plan_por_dia:
                        texto += "\n\n" + plan_por_dia[dia]

                    fila.append(texto)

            tabla.append(fila)

        # Crea una tabla adentro de la figura
        calendario = ax.table(cellText=tabla, # Texto que se mostrará en cada celda 
                              colLabels=dias_semana, # Encabezados con los días de la semana 
                              cellLoc="center", # Centra el texto dentro de cada celda 
                              loc="center" ) # Ubica la tabla en el centro de la figura
                              

        calendario.auto_set_font_size(False)

        calendario.set_fontsize(6) # No pone font size default, pone 6

        # Cambia el tamaño de las celdas de la tabla: ensancha las columnas y hace filas más altas
        calendario.scale(1.3, 7)

        for col in range(7):
            cell = calendario[(0, col)]
            cell.set_facecolor("#1565C0")
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
            cell.set_height(0.08)
        # Modifica la fila de encabezados del calendario

        hoy = date.today()
        # Guarda la fecha de hoy para poder comparar qué días ya pasaron

        for (fila, col), cell in calendario.get_celld().items():
            # get_celld() = recorre cada una de las celdas del calendario

            texto = cell.get_text().get_text()
            # get_text() = extrae el contenido de cada celda y lo convierte en un str
            # para poder elegir los colores según lo que dice

            cell.set_edgecolor("#BDBDBD")
            # Color del borde

            cell.set_linewidth(1)
            # Ancho del borde

            if fila == 0:
                continue
                # Si es la fila de encabezados, no sigue con el resto del código

            if texto == "":
                cell.set_facecolor("#F5F5F5")
                continue
                # Si la celda está vacía, la pinta gris clarito y salta a la siguiente
            
            dia = int(texto.split("\n")[0])
            # Se queda solo con el número del día.
            # Ejemplo: si texto empieza con "12", guarda 12 como número entero
            
            fecha_celda = date(año, mes, dia)
            # Arma una fecha real con el año, mes y día de esa celda
            
            if fecha_celda < hoy:
                cell.set_facecolor("#D6D6D6")
                cell.get_text().set_color("#777777")
                # Si la fecha de la celda ya pasó, la pinta gris
            
            elif "EXAMEN" in texto:
                cell.set_facecolor("#FFCDD2")
                cell.get_text().set_weight("bold")
                # Si es un examen, pinta la celda de rojo claro y pone el texto en negrita
            
            elif "Repaso" in texto:
                cell.set_facecolor("#C8E6C9")
                # Si hay repaso, pinta la celda de verde claro
            
            elif "Práctica" in texto:
                cell.set_facecolor("#FFF9C4")
                # Si hay práctica, pinta la celda de amarillo claro
            
            elif "Estudio" in texto:
                cell.set_facecolor("#BBDEFB")
                # Si hay estudio, pinta la celda de celeste claro
            
            else:
                cell.set_facecolor("white")
                # Si no hay examen ni actividad, deja la celda blanca

        # Recorre todas las celdas de la tabla y les cambia el color según el tipo de actividad o según si el día ya pasó
        meses = ["", "Enero", "Febrero", "Marzo", "Abril","Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        nombre_mes = meses[mes]
        plt.title( f"Planificador de estudio - {nombre_mes}/{año}",
                  fontsize=20, 
                  fontweight="bold", 
                  pad=30)

        plt.tight_layout()
        plt.show()