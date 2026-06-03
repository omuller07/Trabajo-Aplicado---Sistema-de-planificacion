def verificar_disponibilidad(df_disponibilidad):

    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

    for dia in dias:
        if df_disponibilidad[dia][0] < 0:
                #el 0 es porque es la fila que tiene el dia, es una sola fila asi que te devuelve la hora.
            print(f"Error: las horas de {dia} no pueden ser negativas.")
            return False

    if df_disponibilidad[dias].sum(axis=1)[0] == 0:
            #axis = 1, es que suma el eje horizontal.
        print("Error: no hay ninguna hora disponible para estudiar.")
        return False

    return True


def verificar_fechas_materias(df_materias):

    for indice, fila in df_materias.iterrows():

        if fila["fecha_examen"] <= fila["fecha_inicio"]:
            print("Error: la fecha del examen de",fila["materia"],"debe ser posterior a la fecha de inicio.")
            return False

    return True


def verificar_nombres_materias(df_materias):

    for indice, fila in df_materias.iterrows():

        if fila["materia"] == "":
            print("Error: hay una materia sin nombre.")
            return False

    return True


def verificar_nombres_temas(df_temas):

    for indice, fila in df_temas.iterrows():

        if fila["tema"] == "":
            print("Error: hay un tema sin nombre.")
            return False

    return True



