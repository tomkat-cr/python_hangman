# File: decorator_execution_time.py
# 2022-07-02 | CR

from datetime import datetime

def execution_time(func):
    # OJO el * es el 'operador de desesructuracion' de Python.
    # args = parametros NO nombrados, o sea que importa su posicion en la llamada
    # kwargs = parametros nombrados, o sea que no importa su posicion, se pasan con el nombre del parametro
    def wrapper(*args, **kwargs):
        initial_time = datetime.now()
        response = func(*args, **kwargs)
        final_time = datetime.now()
        time_elapsed = final_time - initial_time
        print(f'Pasaron {time_elapsed.total_seconds()} segundos')
        return response
    return wrapper
