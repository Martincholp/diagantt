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



        
