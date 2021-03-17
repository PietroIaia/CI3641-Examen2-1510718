import sys
import re

# Diccionario de nombres que guardará un diccionario por cada nombre, que a su vez guardará:
# 1- El árbol que representa el tipo del nombre
# 2- Un diccionario que guardará las variables de tipo, presentes en él, con sus valores reales.
nombres = {}

# Función utilizada para eliminar caracteres innecesarios del input que se le pasará al árbol.
def r_innecesario(arr):
  while ('' in arr): arr.remove('')
  while (' ' in arr): arr.remove(' ')
  while ('-' in arr): arr.remove('-')
  while ('>' in arr): arr.remove('>')
  return arr

# Función utilizada para verificar si todos los elementos del input son nombres previamente definidos.
def rev_nombre(input):
  for elem in input:
    if (elem != "(") and (elem != ")") and (not elem in nombres.keys()):
      return False, elem
  return True, None

def original_dict(nombre):
  for k in nombres[nombre]:
    if k == "arbol_tipo":
      continue
    if not k[0].isupper():
      nombres[nombre][k] = "var"


# Árbol utilizado para representar el tipo de un nombre definido
# Si definimos un nombre de la siguiente forma: DEF test a -> (b -> b) -> a, el árbol resultante será de la siguiente forma:
#                         a
#                          \
#                         None
#                        /   \
#                       b     a
#                        \
#                         b
# El Árbol se construye de manera recursiva, es decir, primero se define el nodo raíz y luego se define la rama izquierda y\o 
# derecha (de tenerlas) desde el nodo raíz, y seguimos hasta completar el árbol.
class ArbolTipo:
  # Inicializamos el Nodo del arbol
  def __init__(self, nombre, input):
    self.nombre = nombre
    self.val = None
    self.hijoIzquierda = None
    self.hijoDerecha = None
    self.__crearArbol(input)
  
  # Creamos el arbol del tipo a partir del input dado.
  def __crearArbol(self, input):
    # Si aún queda input por procesar.
    if input:
      j = 1
      # Revisamos si el primer elemento del input es un paréntesis abierto.
      # Esto quiere decir que debemos crear una rama izquierda desde el nodo actual.
      # La rama izquierda será creada utilizando el sub-input que está entre paréntesis.
      # Una vez creada la rama izquierda, debemos encontrar en el input cuando se cierra 
      # este paréntesis para proseguir con la creación del arbol por la rama derecha,
      # utilizando el sub-input que se encuentra luego de los paréntesis.
      if input[0] == "(":
        # Creamos la rama izquierda.
        self.hijoIzquierda = ArbolTipo(self.nombre, input[1:])
        # Encontramos cuando se cierra este paréntesis.
        num_paren = 1
        while j < len(input):
          if num_paren == 0: break
          if input[j] == "(": num_paren += 1
          elif input[j] == ")": num_paren -= 1
          j += 1
      # Si el primer elemento del input no es un paréntesis, entonces es una
      # variable de tipo o una constante de tipo.
      elif input[0] != "(" and input[0] != ")":
        # Si es una constante de tipo, colocamos el valor del nodo y definimos
        # su verdadero tipo que será él mismo.
        if input[0][0].isupper():
          self.val = input[0]
          nombres[self.nombre][self.val] = input[0]
        # Si es una variable de tipo, colocamos el valor del nodo y definimos su
        # verdadero tipo con la palabra "var" que representa a las variables de tipo.
        else:
          self.val = input[0]
          nombres[self.nombre][self.val] = "var"
      # Si aun queda input por procesar, entonces la creación del árbol aun no ha finalizado,
      # por lo que seguimos su creación por la rama derecha.
      if input[j:]:
        if input[j] != ")": self.hijoDerecha = ArbolTipo(self.nombre, input[j:])
  
  # Representación en String del árbol.
  def __str__(self):
    if self.hijoIzquierda and self.hijoDerecha:
      return "(" + self.hijoIzquierda.__str__() + ")->" + self.hijoDerecha.__str__()
    elif self.hijoIzquierda and not self.hijoDerecha:
      return self.hijoIzquierda.__str__()
    elif not self.hijoIzquierda and self.hijoDerecha:
      if nombres[self.nombre][self.val] != "var":
        if "->" in nombres[self.nombre][self.val]:
          return "(" + nombres[self.nombre][self.val] + ")->" + self.hijoDerecha.__str__()
        else:
          return nombres[self.nombre][self.val] + "->" + self.hijoDerecha.__str__()
      return self.val + "->" + self.hijoDerecha.__str__()
    else:
      if nombres[self.nombre][self.val] != "var":
        return nombres[self.nombre][self.val]
      return self.val
  
  # Devuelve True si el nodo es una hoja del árbol, devuelve False si no lo es.
  def es_hoja(self):
    if not self.hijoIzquierda and not self.hijoDerecha and self.val:
      return True
    return False
  

  # ||| Where the real MAGIC happens (o eso se trata) |||
  # Método utilizado para consultar el tipo de la expresión pasada en input.
  # Se definió como método del arbol ya que podemos realizar la construcción del tipo resultante de
  # manera recursiva, iterando entre los nodos del árbol y revisando si el input y el tipo son compatibles.
  def revisar_tipo(self, input, num_paren):
    # Si ya no queda input por procesar, quiere decir que completamos la revisión de compatibilidad
    # entre el tipo y el input, por lo que devolvemos el tipo resultante de la expresión.
    if not input:
      return self.__str__()
    # Si el primer elemento del input es un paréntesis abierto, aumentamos el contador de paréntesis abiertos
    # y seguimos con la revisión.
    if input[0] == "(":
      return self.revisar_tipo(input[1:], num_paren+1)
    # Si el primer elemento del input es un paréntesis cerrado, decrementamos el contador de paréntesis abiertos
    # y seguimos con la revisión.
    elif input[0] == ")":
      return self.revisar_tipo(input[1:], num_paren-1)
    # Si el primer elemento del input no es un paréntesis.
    elif self.val and input[0] != "(" and input[0] != ")":
      # Si el primer elemento del input es un nombre con un árbol de tipo que consiste solo en una hoja.
      if nombres[input[0]]["arbol_tipo"].es_hoja():
        # Verificamos si el valor del nodo actual es una variable. 
        # Si lo es, actualizamos su valor real.
        if nombres[self.nombre][self.val] == "var":
          nombres[self.nombre][self.val] = nombres[input[0]]["arbol_tipo"].val
        # Si el nodo no es una variable, verificamos si sus tipos son iguales, y si no lo son devolvemos 
        # un error de unificación.
        else:
          if nombres[self.nombre][self.val] != nombres[input[0]]["arbol_tipo"].val:
            return False, "ERROR, no se pudo unificar " + nombres[self.nombre][self.val] + " con " + nombres[input[0]]["arbol_tipo"].val
        # Si aun no hemos terminado de revisar el tipo, seguimos.
        if self.hijoDerecha:
          return self.hijoDerecha.revisar_tipo(input[1:], num_paren)
        # Si ya no queda más input por revisar, pero en el input hay mas parámetros, devolvemos un error.
        else:
          return False, "ERROR, ingresó más parametros en la función " + self.nombre + " de los que debería."

      # Si el primer elemento del input es un nombre con un árbol de tipo mas complejo, debemos obtener el tipo
      # resultante de este (su imagen).
      else:
        j, tmp = 1, num_paren
        # Si el nombre es una función entre paréntesis (con parámetros), debemos encontrar
        # cuando se cierra este paréntesis.
        if num_paren > 0:
          while j < len(input):
            if input[j] == "(": tmp += 1
            elif input[j] == ")": tmp -= 1
            if tmp == 0: break
            j += 1
        # Una vez que sabemos cuando se cierra el paréntesis, podemos verificar el tipo de la sub-expresión
        # en el árbol de tipo del nombre que estaba en el input, y así obtener el tipo resultante de esta 
        # sub-expresión, que se utilizará para seguir construyendo el tipo final de la expresión.
        tipo_result = nombres[input[0]]["arbol_tipo"].revisar_tipo(input[1:j], 0)
        original_dict(input[0])
        # Si tipo_result regresó un tipo y no un error.
        if type(tipo_result) == str:
          # Verificamos si el valor del nodo actual es una variable. 
          # Si lo es, actualizamos su valor real.
          if nombres[self.nombre][self.val] == "var":
            nombres[self.nombre][self.val] = tipo_result
          # Si el nodo no es una variable, verificamos si sus tipos son iguales, y si no lo son devolvemos 
          # un error de unificación.
          elif nombres[self.nombre][self.val] != "var":
            if nombres[self.nombre][self.val] != tipo_result:
              return False, "ERROR, no se pudo unificar " + nombres[self.nombre][self.val] + " con " + tipo_result
        # Si tipo_result regresó un error, se devuelve este error.
        else:
          return tipo_result
        # Si aun no hemos terminado de revisar el tipo, seguimos.
        if self.hijoDerecha:
          return self.hijoDerecha.revisar_tipo(input[j:], num_paren)
        # Si ya no queda más input por revisar, pero en el input hay mas parámetros, devolvemos un error.
        else:
          return False, "ERROR, ingresó más parametros en la función " + self.nombre + " de los que debería."



# Menu principal del programa.
def Menu():
  global nombres
  while(True):
    # Obtenemos el input.
    print("\n\nPosibles acciones:\n\tDEF <nombre> <tipo>\n\tTIPO <expr>\n\tSALIR")
    accion = input("Ingrese una acción para proceder: ").split(" ", 1)
    if accion[0] == "DEF":
      accion = [accion[0]] + accion[1].split(" ", 1)
    # Si no se ingresó ningun tipo de acción, devolvemos un error.
    if not accion:
      print("\nNo se ingresó ninguna acción.")
      continue
    print()

    if len(accion) == 3 and accion[0] == "DEF":
      # El diccionario que guardará el árbol y las variables de tipo.
      nombres[accion[1]] = {}
      # Removemos los caracteres inncesarios del input
      accion[2] = r_innecesario(re.split(r'(\W)', accion[2]))
      # Construimos el árbol que representa el tipo del nombre
      nombres[accion[1]]["arbol_tipo"] = ArbolTipo(accion[1], accion[2])
      print("Se definió ’" + accion[1] + "’ con tipo " + nombres[accion[1]]["arbol_tipo"].__str__())

    elif len(accion) == 2 and accion[0] == "TIPO":
      # Removemos los caracteres inncesarios del input
      accion[1] = r_innecesario(re.split(r'(\W)', accion[1]))
      # Verificamos que todos los elementos del input, aparte de los paréntesis,
      # son nombres previamente definidos.
      todo_def = rev_nombre(accion[1])
      if todo_def[0]:
        # Obtenemos el tipo resultante de la expresión.
        tipo = nombres[accion[1][0]]["arbol_tipo"].revisar_tipo(accion[1][1:], 0)
        original_dict(accion[1][0])
        # Si se generó un error, se imprime.
        if type(tipo) != str:
          print(tipo[1])
          continue
        # Si todo salió bien, imprimimos el tipo resultante
        print(tipo)
      else:
        print("ERROR, el nombre ’" + todo_def[1] + "’ no ha sido definido")
        continue

    elif len(accion) == 1 and accion[0] == "SALIR":
      break
    else:
      print("\nLa acción que ingresó no existe, intente de nuevo.")



# Hacemos esto para poder aplicar al script las pruebas unitarias
if __name__ == "__main__":
  Menu()