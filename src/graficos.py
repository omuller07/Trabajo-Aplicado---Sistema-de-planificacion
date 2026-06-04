import matplotlib.pyplot as plt
import calendar


def convertir_plan_a_texto(plan):
    plan_por_dia = {}

    for fecha, actividades in plan.items():
        textos = []

        for actividad in actividades:
            texto = (actividad["actividad"]+ "\n" + actividad["materia"] + "\n"
                     + actividad["tema"] + "\n" + str(actividad["horas"]) + " hs")

            textos.append(texto)

        plan_por_dia[fecha.day] = "\n\n".join(textos)
            # fecha.day = obtiene el número del día del mes
            # "\n\n".join(textos) = une todos los textos de la lista usando dos saltos de línea entre ellos.

    return plan_por_dia


def obtener_meses_del_plan(plan, df_materias):
    meses = []

    for fecha in plan.keys():
        mes_anio = (fecha.year, fecha.month)
        # Extrae año y mes

        if mes_anio not in meses:
            meses.append(mes_anio)

    for indice, fila in df_materias.iterrows():
        fecha_examen = fila["fecha_examen"]
        mes_anio = (fecha_examen.year, fecha_examen.month)
        # Extrae año y mes

        if mes_anio not in meses:
            meses.append(mes_anio)

    return meses

"""
def crear_calendario_visual(plan, df_materias):
    meses = obtener_meses_del_plan(plan, df_materias)

    for anio, mes in meses:
        plan_por_dia = {}

        for fecha, actividades in plan.items():
            if fecha.year == anio and fecha.month == mes:
                textos = []

                for actividad in actividades:
                    texto = (actividad["actividad"] + "\n" + actividad["materia"] + "\n"
                             + actividad["tema"] + "\n" + str(actividad["horas"]) + " hs")

                    textos.append(texto)

                plan_por_dia[fecha.day] = "\n\n".join(textos)
                # Hace lo mismo que la funcion convertir_plan_a_texto y lo agrega a diccio plan_por_dia

        for indice, materia in df_materias.iterrows():
            fecha_examen = materia["fecha_examen"]
            # Recorre las filas del dataframe y busca fecha de examen

            if fecha_examen.year == anio and fecha_examen.month == mes:
                if fecha_examen.day in plan_por_dia:
                    plan_por_dia[fecha_examen.day] += ("\n\nEXAMEN\n" + materia["materia"])
                
                else:
                    plan_por_dia[fecha_examen.day] = ("EXAMEN\n" + materia["materia"])
                    

        cal = calendar.monthcalendar(anio, mes)
        # Crea una lista de listas; cada lista representa una semana del mes con fechas.

        fig, ax = plt.subplots(figsize=(14, 8))
        # Crea una figura (fig) y ejes (ax), figsize indica tamaño de figura
        fig.patch.set_facecolor("#F5F5F5")
        # .patch es el rectangulo ue forma el fondo de la figura, facecolor cambia el color
        ax.axis("off")
        # Oculta los ejes

        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        tabla = []
        # Lista de listas de fila

        for semana in cal:
            fila = []
            # Lista de numero de dia + plan por dia

            for dia in semana:
                if dia == 0:
                    fila.append("")

                else:
                    texto = str(dia)

                    if dia in plan_por_dia:
                        texto += "\n\n" + plan_por_dia[dia]

                    fila.append(texto)

            tabla.append(fila)

        calendario = ax.table(
            #Crea una tabla adentro de la figura
            cellText=tabla,
            # Indica el texto por celda, usando la lista tabla
            colLabels=dias_semana,
            # Pone los nombres de dia de la semana arriba de cada columna
            cellLoc="center",
            # Hace que el texto quede centrado
            loc="center"
            # Coloca la tabla en el centro de la figura
            )

        calendario.auto_set_font_size(False)
        calendario.set_fontsize(7)
        # No poner font size default, pone 7
        calendario.scale(1.2, 4.5)
        # Cambia el tamaño de las celdas de la tabla (ensancha las columnas, hace filas mas altas)

        for col in range(7):
            cell = calendario[(0, col)]
            cell.set_facecolor("#1976D2")
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        
        # Modifica la fila de encabezados del calendario

        for (fila, col), cell in calendario.get_celld().items():
            # get_celld() = recorre cada una de las celdas del calendario
            texto = cell.get_text().get_text()
            # get_text() = primero extrae el contenido de cada celda y el segundo lo convierte en un str para poder dependiendo de lo que dice, elegir los colores

            if "EXAMEN" in texto:
                cell.set_facecolor("#FFCDD2")

            elif "Repaso" in texto:
                cell.set_facecolor("#C8E6C9")

            elif "Práctica" in texto:
                cell.set_facecolor("#FFF9C4")

            elif "Estudio" in texto:
                cell.set_facecolor("#BBDEFB")

            cell.set_edgecolor("#BDBDBD")
            # Color del borde
            cell.set_linewidth(1.5)
            # Ancho del borde
            
        # Recorre todas las celdas de la tabla y les cambia el color según el tipo de actividad que contengan

        plt.title(
            f"Planificador de estudio - {mes}/{anio}",
            fontsize=18,
            fontweight="bold",
            pad=20
        )

        plt.show()

"""
def crear_calendario_visual(plan, df_materias):
    meses = obtener_meses_del_plan(plan, df_materias)

    for anio, mes in meses:
        plan_por_dia = {}

        for fecha, actividades in plan.items():
            if fecha.year == anio and fecha.month == mes:
                textos = []

                for actividad in actividades:
                    texto = (
                        actividad["actividad"] + "\n"
                        + actividad["materia"] + " - " + actividad["tema"] + "\n"
                        + str(actividad["horas"]) + " hs"
                    )
                    textos.append(texto)

                plan_por_dia[fecha.day] = "\n\n".join(textos)

        for indice, materia in df_materias.iterrows():
            fecha_examen = materia["fecha_examen"]

            if fecha_examen.year == anio and fecha_examen.month == mes:
                if fecha_examen.day in plan_por_dia:
                    plan_por_dia[fecha_examen.day] += "\n\nEXAMEN\n" + materia["materia"]
                else:
                    plan_por_dia[fecha_examen.day] = "EXAMEN\n" + materia["materia"]

        cal = calendar.monthcalendar(anio, mes)

        fig, ax = plt.subplots(figsize=(16, 10))
        fig.patch.set_facecolor("#FAFAFA")
        ax.axis("off")

        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        tabla = []

        for semana in cal:
            fila = []

            for dia in semana:
                if dia == 0:
                    fila.append("")
                else:
                    texto = str(dia)

                    if dia in plan_por_dia:
                        texto += "\n\n" + plan_por_dia[dia]

                    fila.append(texto)

            tabla.append(fila)

        calendario = ax.table(
            cellText=tabla,
            colLabels=dias_semana,
            cellLoc="center",
            loc="center"
        )

        calendario.auto_set_font_size(False)
        calendario.set_fontsize(6)
        calendario.scale(1.3, 5.5)

        for col in range(7):
            cell = calendario[(0, col)]
            cell.set_facecolor("#1565C0")
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
            cell.set_height(0.08)

        for (fila, col), cell in calendario.get_celld().items():
            texto = cell.get_text().get_text()

            cell.set_edgecolor("#BDBDBD")
            cell.set_linewidth(1)

            if fila == 0:
                continue

            if texto == "":
                cell.set_facecolor("#F5F5F5")

            elif "EXAMEN" in texto:
                cell.set_facecolor("#FFCDD2")
                cell.get_text().set_weight("bold")

            elif "Repaso" in texto:
                cell.set_facecolor("#C8E6C9")

            elif "Práctica" in texto:
                cell.set_facecolor("#FFF9C4")

            elif "Estudio" in texto:
                cell.set_facecolor("#BBDEFB")

            else:
                cell.set_facecolor("white")

        plt.title(
            f"Planificador de estudio - {mes}/{anio}",
            fontsize=20,
            fontweight="bold",
            pad=30
        )

        plt.tight_layout()
        plt.show()