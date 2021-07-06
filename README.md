# DIAGantt #
Sistema de gestión de diagramas de Gantt  

by [Martincholp](mailto:martincholp@hotmail.com)  

El diagrama de Gantt es una herramienta gráfica cuyo objetivo es exponer el tiempo de dedicación previsto para diferentes tareas o actividades a lo largo de un tiempo total determinado.

* * *

### Elementos que definen un diagrama de Gantt: ###

- **Hitos:**
Son los hechos de importancia para una tarea o grupo de tareas (por ejemplo el inicio o el final).
Tienen una variable booleana que indica si el hito ya ha ocurrido o aún no.
Tienen también un tiempo planificado (t_plan) que es el momento en que el hito debería ocurrir, y un tiempo de ocurrencia (t_ocur) que es el momento en que realmente se produjo. La diferencia entre ellos indica la desviación temporal (t_desv) en la planificación (t_desv = t_plan - t_ocur ). Si t_desv es negativa estoy retrasado, y si es positiva estoy adelantado.
Otra característica importante es el valor de progreso que define que porcentaje de la tarea o grupo de tareas debe estar completo para que el hito ocurra. Hay una excepción a este comportamiento y es cuando el progreso es 0%, ya que en este punto puede que el hito aún no haya ocurrido tal como sucede con el hito de inicio de una tarea. En este caso, la ocurrencia debe realizarse manualmente o sincronizarce mediante la lista de precedentes.
La ocurrencia de un hito puede estar condicionada por la ocurrencia de uno o mas hitos y no solo por el progreso. Esto se logra con una lista de precedentes, que es una lista con los hitos que ya deben haber ocurrido para que pueda ocurrir el hito actual. De esta forma, por ejemplo, puede sincronizarse el inicio de una tarea con la finalización de otra. Para la sincronizacion de acciones se dispone de triggers que se utilizan para disparar alguna función cuando el hito ocurra.

- **Tareas:**
Son los procesos a realizar en un proyecto. Tienen un hito de inicio, uno de finalización, y un valor de progreso que es el que se debe actualizar indicando el porcentaje de completado de la tarea. Cuando el porcentaje de progreso de la tarea es igual o mayor al porcentaje de progreso de un hito de la tarea, entonces ese hito ocurre y se guarda el tiempo en que ocurrió en t_ocur del hito en cuestión. La diferencia entre el t_plan del final y del inicio es la duración planificada de la tarea, y la diferencia entre el t_ocur del final y del inicio es la duración ocurrida.
Otra propiedad de las tareas es su variable estado, que indica la situación actual de la tarea. Los estados posibles son:

  * *'esperando'*  --> La tarea no está iniciada pero aún está a término, 
  * *'demorado'*   --> La tarea no está iniciada y está retrasada (el tiempo global es mayor que el t_plan de su inicio)
  * *'ejecutando'* --> La tarea comenzó y se está ejecutando
  * *'pausado'*    --> La tarea comenzó, pero se ha establecido una pausa en su ejecución
  * *'cancelado'*  --> La tarea fué cancelada
  * *'finalizado'* --> La tarea llegó al final de su ejecución

Por último también se pueden agregar hitos manualmente, pudiendo definir hitos de usuario que ocurren en algún momento deseado del progreso de la tarea.

- **Grupos:**
Son elementos contenedores de hitos, tareas y otros grupos. Tienen un hito de inicio, que es el hito con el menor t_plan de sus hijos y el hito de finalizacion que es el hito con mayor t_plan de sus hijos, y al igual que con las tareas se puede calcular la duración planificada y la duración ocurrida.
El valor de progreso se calcula según el progreso de sus hijos.
Hay una diferencia importante con la propiedad de estado del grupo y es que además de poder tomar los mismos valores que en las tareas, también se agrega un valor mas que es el estado *indeterminado*. Este estado se produce cuando entre sus hijos hay distintos estados no pudiendo establecer un estado general para el grupo.

- **Diagrama:**
Es un grupo particular que comprende la totalidad de los grupos, hitos y tareas que componen el diagrama de Gantt.

### La clase base "Elemento" ###

Todos los elementos definidos anteriormente derivan de la clase "Elemento", la cual contiene propiedades como nombre, tipo, id, padre, etc. y que son comunes a todos los elementos.

### La clase "Proyecto" ###

Es el mayor de los elementos en la jerarquía del documento, y agrupa a todos los diagramas definidos en el mismo. Tiene propiedades globales, como el tiempo transcurrido desde el inicio del proyecto (se debe actualizar manualmente) o las unidades empleadas para medir el tiempo (horas, días, semanas, meses). También es el que cuenta con los métodos correspondientes para guardar y cargar los diagramas realizados, o para exportarlos como imagen, etc. Entre las funciones auxiliares está la que provee de ids válidos, para asegurar que cada elemento tenga un id que lo identifique de forma unívoca dentro del proyecto, para poder referenciarlo cuando sea necesario.

* * *

## Propiedades y funciones de módulo ##

### Estado de ejecución de una tarea, grupo, diagrama o proyecto   ###

  + Estado_indeterminado = 0
  + Estado_esperando     = 1
  + Estado_demorado      = 2
  + Estado_ejecutando    = 3
  + Estado_pausado       = 4
  + Estado_cancelado     = 5
  + Estado_finalizado    = 6

### Tipos de elementos ###

  + Tipo_proyecto    = 0
  + Tipo_hito        = 1
  + Tipo_tarea       = 2
  + Tipo_grupo       = 3
  + Tipo_diagrama    = 4

### Funciones ###

  + estados_string(estado(int))  **(str)**
  + tipos_string(tipo(int))  **(str)**

* * *

## Estructura de clases ##

clase Elemento(Object)
* propiedades:
    + nombre    **(str)**
    + id        **(int)** *(solo lectura)*
    + tipo      **(int)** *(solo lectura)*
    + padre     **(Diagrama|Grupo|Tarea|None)** *(solo lectura)*
    + proyecto  **(Proyecto|None)** *(Solo lectura)*
* metodos:
    + \_\_init\_\_(nombre(str), padre(Diagrama|Grupo|Tarea|None), tipo(int))
    + \_\_str\_\_()  **(str)**
    + t_global()     **(int)**

clase Hito(Elemento)
* propiedades:
    + ocurrido              **(bool)** *(solo lectura)*
    + t_plan                **(int)** *(solo lectura)*
    + t_ocur                **(int)** *(solo lectura)*
    + t_desv                **(int)** *(solo lectura)*
    + progreso              **(int)** *(solo lectura)*
* propiedades heredadas:
    + nombre                **(str)** *(Elemento)*
    + id                    **(int)** *(solo lectura) (Elemento)*
    + tipo                  **(int)** *(solo lectura) (Elemento)*
    + padre                 **(Diagrama|Grupo|Tarea|None)** *(solo lectura) (Elemento)*
    + proyecto              **(Proyecto|None)** *(Solo lectura) (Elemento)*
* metodos:
    + \_\_init\_\_(nombre(str), t_plan(int), progreso(int), padre(Diagrama|Grupo|Tarea|None))
    + actualizar()                        **(bool)**
    + set_ocurrido(estado(bool))          **(bool)**
    + add_precedente(precedente(hito))        
    + rem_precedente(id(int))             **(Hito)**
    + get_precedente(id(int))             **(Hito)**
    + lista_precedentes()                 **(tuple(Hito))**    
    + lista_trigger_ocur()                **(tuple(func))**
    + add_trigger_ocur(trigger(func))         
    + rem_trigger_ocur(trigger(func))         
    + lista_trigger_no_ocur()             **(tuple(func))**
    + add_trigger_no_ocur(trigger(func))      
    + rem_trigger_no_ocur(trigger(func))
* metodos heredados:
    + \_\_str\_\_()  **(str)**

clase Tarea(Elemento)
* propiedades:
    + inicio         **(Hito)** *(solo lectura)*
    + fin            **(Hito)** *(solo lectura)*
    + progreso       **(int)**
    + duracion_plan  **(int)** *(solo lectura)*
    + duracion_ocur  **(int)** *(solo lectura)*
    + estado         **(int)** *(solo lectura)*
* propiedades heredadas:
    + nombre         **(str)** *(Elemento)*
    + id             **(int)** *(solo lectura) (Elemento)*
    + tipo           **(int)** *(solo lectura) (Elemento)*
    + padre          **(Diagrama|Grupo|None)** *(solo lectura) (Elemento)*
    + proyecto       **(Proyecto|None)** *(Solo lectura) (Elemento)*
* metodos:
    + \_\_init\_\_(nombre(str), inicio(int), duracion(int), padre(Diagrama|Grupo|None))
    + crear_hito(nombre(str), t_plan(int), progreso(int))  **(Hito)**
    + add_hijo(hito(Hito))   
    + rem_hijo(index(int))                                 **(Hito)**
    + get_hijo(index(int))                                 **(Hito)**
    + lista_hijos()                                        **(tuple(Hito))**    
    + set_estado(int)    
    + t_transcurrido()                                     **(int)** 
* metodos heredados:
    + \_\_str\_\_()  **(str)** *(Elemento)*


clase Grupo(Tarea)
* propiedades:
    + progreso       **(int)** *(solo lectura)*
    + estado         **(int)** *(solo lectura)*
* propiedades heredadas:
    + inicio         **(Hito)** *(solo lectura)* *(Tarea)*
    + fin            **(Hito)** *(solo lectura)* *(Tarea)*
    + duracion_plan  **(int)** *(solo lectura)* *(Tarea)*
    + duracion_ocur  **(int)** *(solo lectura)* *(Tarea)*
    + nombre         **(str)** *(Elemento)*
    + id             **(int)** *(solo lectura) (Elemento)*
    + tipo           **(int)** *(solo lectura) (Elemento)*
    + padre          **(Diagrama|Grupo|None)** *(solo lectura) (Elemento)*
    + proyecto       **(Proyecto|None)** *(Solo lectura) (Elemento)*
* metodos:
    + \_\_init\_\_(nombre(str), padre(Diagrama|Grupo|None))
    + crear_hito(nombre(str), t_plan(int), progreso(int))   **(Hito)**
    + crear_tarea(nombre(str), inicio(int), duracion(int))  **(Tarea)**
    + crear_grupo(nombre(str))                              **(Grupo)**
    + add_hijo(hijo(Hito|Tarea|Grupo))   
    + rem_hijo(id(int))                                     **(Hito|Tarea|Grupo)**
    + get_hijo(id(int))                                     **(Hito|Tarea|Grupo)**
    + lista_hijos()                                         **(tuple(Hito|Tarea|Grupo))**
    + set_estado(int)    
* metodos heredados:
    + t_transcurrido()    **(int)** *(Tarea)*
    + \_\_str\_\_()  **(str)** *(Elemento)*

clase Diagrama(Grupo)
* propiedades:
    + proyecto           **(Proyecto|None)**
* propiedades heredadas:
    + progreso       **(int)** *(solo lectura) (Grupo)*
    + estado         **(int)** *(solo lectura) (Grupo)*
    + inicio         **(Hito)** *(solo lectura) (Tarea)*
    + fin            **(Hito)** *(solo lectura) (Tarea)*
    + duracion_plan  **(int)** *(solo lectura) (Tarea)*
    + duracion_ocur  **(int)** *(solo lectura) (Tarea)*
    + nombre         **(str)** *(Elemento)*
    + id             **(int)** *(solo lectura) (Elemento)*
    + padre          **(Proyecto|None)** *(solo lectura) (Elemento)*
    + tipo           **(int)** *(solo lectura) (Elemento)*
* metodos:
    + \_\_init\_\_(nombre(str), proyecto(Proyecto|None))
    + set_proyecto(proyecto(Proyecto|None))
* metodos heredados:
    + crear_hito(nombre(str), t_plan(int), progreso(int))   **(Hito)** *(Grupo)*
    + crear_tarea(nombre(str), inicio(int), duracion(int))  **(Tarea)** *(Grupo)*
    + crear_grupo(nombre(str))                              **(Grupo)** *(Grupo)*
    + add_hijo(hijo(Hito|Tarea|Grupo))                      *(Grupo)*
    + rem_hijo(id(int))                                     **(Hito|Tarea|Grupo)** *(Grupo)*
    + get_hijo(id(int))                                     **(Hito|Tarea|Grupo)** *(Grupo)*
    + lista_hijos()                                         **(tuple(Hito|Tarea|Grupo))** *(Grupo)*
    + set_estado(int)                                       *(Grupo)*
    + t_transcurrido()                                      **(int)** *(Tarea)*
    + \_\_str\_\_()                                         **(str)** *(Elemento)*

clase Proyecto(Object)
* propiedades:
    + nombre                **(str)**
    + unidad_de_tiempo      **(str)**
    + tiempo_global         **(int)**
    + estado                **(int)**
* metodos:
    + \_\_init\_\_()
    + lista_diagramas()                              **(tuple(Diagrama))**
    + add_diagrama(diagrama(Diagrama))               **(Diagrama)**
    + rem_diagrama(diagrama(Diagrama))               **(Diagrama)**
    + buscar_diagrama_por_nombre(nombre(str))        **(Diagrama|None)**
    + buscar_diagrama_por_id(diag_id(int))           **(Diagrama|None)**
    + crear_diagrama(nombre(str))                    **(Diagrama)**
    + get_elem(id_elem(int))                         **(Diagrama|Grupo|Tarea|Hito|None)**
    + set_tiempo(valor(int))
    + set_estado(int)        
    + cargar(url(str))
    + guardar(url(str))
    + crear_id()                                     **(int)** *(metodo de clase)*