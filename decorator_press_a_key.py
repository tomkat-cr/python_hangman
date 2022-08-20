# decorator_press_a_key.py
# 2022-06-02 | CR

# Este es un ejemplo de decorador al que se pasa un parámetro nombrado, en este caso 'msg'

# La llamada al decorador puede ser:
# @press_a_key(msg='Presionar ENTER para jugar de nuevo, o "T" para terminar: ')
#            o
# @press_a_key() # Si no se va a pasar el parámetro, se debe obligatoriamente poner los paréntesis.

# Fuente de referencia:
# venv/lib/python3.9/site-packages/flask_cors/decorator.py

from functools import update_wrapper


# A diferencia del decorador sin parámetros, este no puede recibir únicamente la función 'f'
# en el nivel superior, mas bien debe recibir los parámetros *args y **kwargs,
# luego el primer closure 'decorator(f)' es el que recibe a la función 'f'
# A continuacion hay un sub-closure wrapped_function() que vuelve a recibir los parámetros *args y **kwargs
# En el decorator() se debe suprimir los parámetros que le corresponden al decorador,
# en este caso el parámetro 'msg', de tal forma que la función final no los reciba,
# sobre todo si dicha función 'f' no tiene ningún parámetro, de lo contrario dara error:
# TypeError: f() takes 0 positional arguments but 1 was given

def press_a_key(*args, **kwargs):
    def decorator(f):
        # El parámetro se debe leer antes de llamar al 2do nivel de 'Closure'
        # O sea por fuera de wrapped_function()
        # De lo contrario no lo reconocerá
        # y tomará el valor por defecto.
        if 'msg' in kwargs:
            msg = kwargs['msg']
            del(kwargs['msg'])
        else:    
            msg = 'Press ENTER to continue...'

        def wrapped_function(*args, **kwargs):
            response_func = f(*args, *kwargs)
            print()
            key_pressed = input(msg)
            print()
            # Devuelve una tupla con el valor ingresado por el
    	    #  usuario y la eventual respuesta de la función 'f'
            return (key_pressed, response_func)

        # OJO si no se le pone la llamada a update_wrapper(),
        # ejecutará la función "f" antes de pasar por el 
        # flujo normal que comienza con 
    	# "if __name__ == '__main__':"
        return update_wrapper(wrapped_function, f)

    return decorator
