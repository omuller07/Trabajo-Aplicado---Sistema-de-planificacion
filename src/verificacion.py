def verificar_disponibilidad(df_disponibilidad):
    '''
    Verifica si el usuario tiene horas disponibles cada dia.

    Parameters
    ----------
    df_disponibilidad : DataFrame
        Contiene los datos de la disponibilidad semanal del usuario

    Returns
    -------
    bool
        False si hay horas negativas o no hay horas disponibles
        para estudiar.
        True si hay horas disponible.

    '''

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
    '''
    Verifica que la fecha de examen de cada materia sea posterior
    a su fecha de inicio.

    Parameters
    ----------
    df_materias : DataFrame
        Contiene los datos de cada materia (temas, fecha de examen, fecha de inicio).

    Returns
    -------
    bool
        False si la fecha del examen es antes de la fecha de inicio.
        True si la fecha de examen es despues de la fecha de inicio.

    '''

    for indice, fila in df_materias.iterrows():

        if fila["fecha_examen"] <= fila["fecha_inicio"]:
            print("Error: la fecha del examen de",fila["materia"],"debe ser posterior a la fecha de inicio.")
            return False

    return True


def verificar_nombres_materias(df_materias):
    '''
    Verifica que cada materia tenga un nombre asociado. 

    Parameters
    ----------
    df_materias : DataFrame
        Contiene los datos de cada materia (temas, fecha de examen, fecha de inicio).

    Returns
    -------
    bool
        True si todas las materias tienen nombre.
        False si existe al menos una materia con nombre vacío.

    '''

    for indice, fila in df_materias.iterrows():

        if fila["materia"] == "":
            print("Error: hay una materia sin nombre.")
            return False

    return True


def verificar_nombres_temas(df_temas):
    '''
    Verfica que cada tema tenga un nombre asociado.

    Parameters
    ----------
    df_temas : DataFrame
        Contiene la informacion de cada tema dentro de cada materia (la dificultad, conocimiento previo, urgencia).

    Returns
    -------
    bool
        False si hay un tema sin nombre.
        True si todos los temas tienen nombre.
    '''

    for indice, fila in df_temas.iterrows():

        if fila["tema"] == "":
            print("Error: hay un tema sin nombre.")
            return False

    return True



