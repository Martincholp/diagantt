#! /usr/bin/env python
#-*- coding: UTF-8 -*-

'''Estructura de excepciones del sistema de gestión de diagramas de Gantt'''


##  EXCEPCIONES  ##
class Error_de_tipo(Exception):
    """Se lanza al utilizar un tipo no válido"""

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return "El tipo " + self.val + " no es válido"


class Nombre_no_valido(Exception):
    """Se lanza al utilizar un nombre no válido"""

    def __init__(self, val=None):
        self.val = val
        self.mensaje = "El nombre no puede ser '" + self.val + "' ni tampoco una cadena vacía"

    def __str__(self):
        return self.mensaje


class Padre_no_valido(Exception):
    """Se lanza al utilizar un padre no válido"""

    def __init__(self, val=None):
        self.val = val
        self.mensaje = "El tipo de elemento del padre no es correcto --> " + str(self.val)

    def __str__(self):
        return self.mensaje


class Nombre_repetido(Exception):
    """Se lanza al utilizar un nombre que ya existe"""

    def __init__(self, val=None):
        self.val = val
        self.mensaje = "El nombre '" + self.val + "' ya existe para la acción que desea realizar"

    def __str__(self):
        return self.mensaje


class Error_de_progreso(Exception):
    """Ocurre al no poder computar u obtener el progreso de un elemento"""

    def __init__(self, elem):
        self.elem = elem

    def __str__(self):
        return "No se puede obtener el progreso del elemento " + elem.nombre


class Progreso_no_valido(Exception):
    """Error al ingresar un valor de progreso que no es correcto para la acción que se intenta realizar"""

    def __init__(self, valor):
        self.valor = valor
        self.mensaje = "El valor " + str(self.valor) + " no es correcto"

    def __str__(self):
        return self.mensaje


class Error_de_agregado(Exception):
    """Error al intentar agregar un elemento que no es apto para tal accion"""

    def __init__(self, valor):
        self.valor = valor
        self.mensaje = "El elemento " + self.valor.nombre + " no se puede agregar."

    def __str__(self):
        return self.mensaje


class Error_de_grupo(Exception):
    """Error general para grupos"""

    def __init__(self, valor):
        self.valor = valor
        self.mensaje = "El grupo debe contener al menos 1 hijo."

    def __str__(self):
        return self.mensaje


class Error_de_momento(Exception):
    """Error general para momentos"""

    def __init__(self, valor):
        self.valor = valor
        self.mensaje = "No se puede determinar el momento indicado en " + self.valor.nombre

    def __str__(self):
        return self.mensaje


class Elemento_huerfano(Exception):
    """Error para elemento huerfano"""

    def __init__(self, elem):
        self.elem = elem
        self.mensaje = "El elemento " + self.elem.nombre + " no tiene un padre asociado"

    def __str__(self):
        return self.mensaje


class Error_de_estado(Exception):
    """Error para estados no válidos"""

    def __init__(self, elem):
        self.elem = elem
        self.mensaje = "El estado no puede tener valor " + str(elem)

    def __str__(self):
        return self.mensaje



