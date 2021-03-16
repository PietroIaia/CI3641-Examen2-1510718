import sys
import math
import itertools

# Diccionarios con los tipos atómicos, registros y registros variantes
# Cada diccionario esta definido de la siguiente manera:
# atoms == {key : (representación, alineación)}
# structs == {key : [alineación, tipo1, tipo2, ...]}
# unions == {key : [alineación, tipo1, tipo2, ...]}
atoms, structs, unions = {}, {}, {}
# Revisa si nombre es un tipo atómico
def in_atoms(nombre):
  global atoms
  if nombre in atoms.keys():
    return True
  return False
# Revisa si nombre es un registro
def in_structs(nombre):
  global structs
  if nombre in structs.keys():
    return True
  return False
# Revisa si nombre es un registro variante
def in_unions(nombre):
  global unions
  if nombre in unions.keys():
    return True
  return False

# Funcion para hallar el Maximo Comun Divisor 
def mcd(num1, num2):
    a = max(num1, num2)
    b = min(num1, num2)
    while b!=0:
        mcd = b
        b = a%b
        a = mcd
    return mcd
# Funcion para hallar el Minimo Comun Multiplo
def mcm(num1, num2):
    a = max(num1, num2)
    b = min(num1, num2)
    mcm = (a / mcd(a, b)) * b
    return mcm


# Define un nuevo tipo atómico de nombre <nombre>, cuya representación ocupa
# <representación> bytes y debe estar alineado a <alineación> bytes
def def_atomico(nombre, representacion, alineacion):
  global atoms
  try:
    representacion = int(representacion)
    alineacion = int(alineacion)
    if (representacion < 0) or (alineacion < 0):
      raise Exception
  except:
    print("La representacion y la alineacion ingresada debe ser de tipo entero positivo.")
    return
  # Si el nombre no ha sido definido, lo añadimos al diccionario de tipos atómicos con sus datos relevantes. 
  # Si ya se ha definido, imprimimos un mensaje de error.
  if in_atoms(nombre) or in_structs(nombre) or in_unions(nombre):
    print(nombre + " ya corresponde a algún tipo creado en el programa.")
  else:
    atoms[nombre] = (representacion, alineacion)


# Define un nuevo registro de nombre <nombre>. La definición de los campos del
# registro viene dada por la lista en [<tipo>].
def def_struct(nombre, tipos):
  global atoms, structs, unions

  # Si el nombre no ha sido definido, lo añadimos al diccionario de registros con sus datos relevantes. 
  # Si ya se ha definido, imprimimos un mensaje de error.
  if in_atoms(nombre) or in_structs(nombre) or in_unions(nombre):
    print(nombre + " ya corresponde a algún tipo creado en el programa.")
  else:
    # Calculamos la alineación del registro, que será la alineación de su primer campo.
    # Aparte, verificamos si en la lista de tipos todos estan definidos. Si alguno no lo está, imprimimos un mensaje de error.
    fst = True
    for t in tipos:
      if not in_atoms(t) and not in_structs(t) and not in_unions(t):
        print("Alguno de los tipos ingresados no han sido definidos.")
        return
      # Obtenemos el primer campo del registro
      if fst:
        fst_t = t
        fst = False

    structs[nombre] = tipos
    # Definimos la alineación del registro
    if in_atoms(fst_t):
      structs[nombre].insert(0, atoms[fst_t][1])  
    elif in_structs(fst_t):
      structs[nombre].insert(0, structs[fst_t][0]) 
    elif in_unions(fst_t):
      structs[nombre].insert(0, unions[fst_t][0])


# Define un nuevo registro variante de nombre <nombre>. La definición de los campos 
# del registro variante viene dada por la lista en [<tipo>].
def def_union(nombre, tipos):
  global atoms, structs, unions

  # Si el nombre no ha sido definido, lo añadimos al diccionario de registros variantes con sus datos relevantes. 
  # Si ya se ha definido, imprimimos un mensaje de error.
  if in_atoms(nombre) or in_structs(nombre) or in_unions(nombre):
    print(nombre + " ya corresponde a algún tipo creado en el programa.")
  else:
    # Aparte, verificamos si en la lista de tipos todos estan definidos. Si alguno no lo está, imprimimos un mensaje de error.
    for t in tipos:
      if not in_atoms(t) and not in_structs(t) and not in_unions(t):
        print("Alguno de los tipos ingresados no han sido definidos.")
        return

    unions[nombre] = tipos
    # Calculamos la alineación del registro variante, que será el mínimo común múltiplo de las alineaciones de sus campos.
    alineacion = 1
    for t in tipos:
      if in_atoms(t):
        alineacion = mcm(alineacion, atoms[t][1])
      if in_structs(t):
        alineacion = mcm(alineacion, structs[t][0])
      if in_unions(t):
        alineacion = mcm(alineacion, unions[t][0])
    unions[nombre].insert(0, int(alineacion))



# Función recursiva utilizada para imprimir la información correspondiente al tipo ingresado 
# si el lenguaje guarda registros y registros viariantes sin empaquetar o empaquetados.
# Si el tipo ingresado es un registro o registro variante, se llamará recursivamente la función 
# con cada uno de sus campos para imprimir la información correspondiente a cada uno.
# Si el tipo ingresado es un tipo atómico, se imprime su información nada mas.
# Usaremos un contador de espacios en bytes (curr_byte) para saber donde asignar los tipos en la memoria.
def describir(nombre, curr_byte, bytes_des, sin_empaquetar, nivel=0):
  global atoms, structs, unions

  # Si el tipo es un tipo atómico
  if in_atoms(nombre):
    # Si el lenguaje no empaqueta, se calcula la posición inicial del tipo tomando en cuenta su alineación
    # y se modifica el contador de espacio desperdiciado.
    if sin_empaquetar:
      if curr_byte % atoms[nombre][1] != 0:
        tmp = atoms[nombre][1] - (curr_byte % atoms[nombre][1])
        bytes_des += tmp
        curr_byte += tmp
    # Imprimimos la información
    print(("\t"*nivel) + "Tipo atómico " + nombre + "\n" +
    ("\t"*nivel) + "posición inicial: byte " + str(curr_byte) + "\n" +
    ("\t"*nivel) + "tamaño: " + str(atoms[nombre][0]))
    # Si el lenguaje no empaqueta, imprimimos la información referente a la alineación del tipo
    if sin_empaquetar:
      print(("\t"*nivel) + "alineación: " + str(atoms[nombre][1]))
    print()
    # Aumentamos el contador con el tamaño del tipo atómico
    curr_byte += atoms[nombre][0]
    return curr_byte, bytes_des

  # Si el tipo es un registro
  elif in_structs(nombre):
    print(("\t"*nivel) + "Registro " + nombre + " ->")
    # Si el lenguaje no empaqueta, se calcula la posición inicial del registro tomando en cuenta su alineación
    # y se guarda la cantidad de espacio desperdiciado para luego modificar el contador de espacio desperdiciado.
    if sin_empaquetar:
      init_des = 0
      if curr_byte % structs[nombre][0] != 0:
        init_des = structs[nombre][0] - (curr_byte % structs[nombre][0])
        curr_byte += init_des
    # Posición inicial del registro
    init_byte = curr_byte
    # Llamamos recursivamente a la función para imprimir la información de cada uno de sus campos
    for reg in structs[nombre][1:]:
      curr_byte, bytes_des = describir(reg, curr_byte, bytes_des, sin_empaquetar, nivel+1)
    # Calculamos el tamaño total del registro
    size = curr_byte - init_byte
    # Imprimimos la información
    print(("\t"*nivel) + "posición inicial: byte " + str(init_byte) + "\n" +
    ("\t"*nivel) + "tamaño: " + str(size) + "\n" +
    ("\t"*nivel) + "desperdicio de bytes: " + str(bytes_des))
    # Si el lenguaje no empaqueta, imprimimos la información referente a la alineación del registro
    # y se modifica el contador de espacio desperdiciado.
    if sin_empaquetar:
      print(("\t"*nivel) + "alineación: " + str(structs[nombre][0]))
      bytes_des += init_des
    print()
    return curr_byte, bytes_des
  
  # Si el tipo es un registro variante
  elif in_unions(nombre):
    print(("\t"*nivel) + "Registro variable " + nombre + " ->")
    # Si el lenguaje no empaqueta, se calcula la posición inicial del registro variante tomando en cuenta su alineación
    # y se guarda la cantidad de espacio desperdiciado para luego modificar el contador de espacio desperdiciado.
    if sin_empaquetar:
      init_des = 0
      if curr_byte % unions[nombre][0] != 0:
        init_des = unions[nombre][0] - (curr_byte % unions[nombre][0])
        curr_byte += init_des
    # Posición inicial del registro variante
    init_byte = curr_byte
    # Tamaño del registro variante
    max_size = 0
    # Desperdicio en bytes del registro variante
    min_des = 99999
    # Llamamos recursivamente a la función para imprimir la información de cada uno de sus campos.
    # Ademas, calculamos el tamaño del registro variante, que será el tamaño máximo de los tamaños de sus campos.
    for reg in unions[nombre][1:]:
      tmp_byte, tmp_des = describir(reg, curr_byte, bytes_des, sin_empaquetar, nivel+1)
      max_size = max(max_size, tmp_byte - init_byte)
      # Aqui encontramos el minimo valor calculado, ya que esto será sumado al final para encontrar el desperdicio de bytes
      min_des = min(min_des, tmp_des - tmp_byte)
    # Una vez encontrado el tamaño de la union, podemos calcular el desperdicio de la union.
    # En esta operación, le restamos el tamaño del campo con menor desperdicio de bytes al tamaño total de la Union, y luego  
    # le sumamos los bytes desperdiciados por este campo, asi obtenemos el mínimo entre los desperdicios de cada una de sus 
    # campos, es decir, ((tam. Union) - (tam. Campo)) + (desp. bytes). En la parte izquierda de la suma obtenemos los bytes 
    # desperdiciados al final del campo, y en la parte derecha obtenemos los bytes desperdiciados dentro del campo.
    min_des = max_size + init_byte + min_des
    # Imprimimos la información
    print(("\t"*nivel) + "posición inicial: byte " + str(init_byte) + "\n" +
    ("\t"*nivel) + "tamaño: " + str(max_size) + "\n" +
    ("\t"*nivel) + "desperdicio de bytes: " + str(min_des))
    # Aumentamos el contador con el tamaño del registro variante
    curr_byte += max_size
    # Si el lenguaje no empaqueta, imprimimos la información referente a la alineación del registro variante
    # y se modifica el contador de espacio desperdiciado.
    if sin_empaquetar:
      print(("\t"*nivel) + "alineación: " + str(unions[nombre][0]))
      bytes_des += init_des + min_des
    print()
    return curr_byte, bytes_des
    
  else:
    print("El nombre ingresado no corresponde a ningún registro.")

  

def describir_reordenado(nombre, curr_byte, bytes_des, nivel=0):
  global atoms, structs, unions

  # Si el tipo es un tipo atómico
  if in_atoms(nombre):

    if curr_byte % atoms[nombre][1] != 0:
      tmp = atoms[nombre][1] - (curr_byte % atoms[nombre][1])
      bytes_des += tmp
      curr_byte += tmp
    
    info = ("\t"*nivel) + "Tipo atómico " + nombre + "\n" + \
    ("\t"*nivel) + "posición inicial: byte " + str(curr_byte) + "\n" + \
    ("\t"*nivel) + "tamaño: " + str(atoms[nombre][0]) + "\n" + \
    ("\t"*nivel) + "alineación: " + str(atoms[nombre][1]) + "\n\n"

    curr_byte += atoms[nombre][0]
    return curr_byte, bytes_des, info, atoms[nombre][1]

  # Si el tipo es un registro
  elif in_structs(nombre):
    op_size = 999999999
    info = None
    final_curr_byte = None
    final_bytes_des = None
    original_cur_byte = curr_byte
    original_bytes_des = bytes_des

    for perm in list(itertools.permutations(structs[nombre][1:])):
      curr_byte = original_cur_byte
      bytes_des = original_bytes_des
      info_campos = ""
      fst = True
      alineacion = None

      init_des = 0
      if curr_byte % structs[nombre][0] != 0:
        init_des = structs[nombre][0] - (curr_byte % structs[nombre][0])
        curr_byte += init_des
      
      init_byte = curr_byte
      for reg in perm:
        curr_byte, bytes_des, tmp_info_campos, tmp_alineacion = describir_reordenado(reg, curr_byte, bytes_des, nivel+1)
        info_campos += tmp_info_campos
        if fst:
          alineacion = tmp_alineacion
          fst = False
      
      size = curr_byte - init_byte
      if size < op_size:
        op_size = size
        final_curr_byte = curr_byte
        final_bytes_des = bytes_des + init_des
        info = ("\t"*nivel) + "Registro " + nombre + " ->\n" + info_campos + \
        ("\t"*nivel) + "posición inicial: byte " + str(init_byte) + "\n" + \
        ("\t"*nivel) + "tamaño: " + str(size) + "\n" + \
        ("\t"*nivel) + "desperdicio de bytes: " + str(bytes_des) + "\n" + \
        ("\t"*nivel) + "alineación: " + str(alineacion) + "\n\n"
    return final_curr_byte, final_bytes_des, info, alineacion
  
  # Si el tipo es un registro variante
  elif in_unions(nombre):
    
    alineacion = 1
    for reg in unions[nombre][1:]:
      alineacion = mcm(alineacion, describir_reordenado(reg, curr_byte, bytes_des, nivel+1)[3])
    alineacion = int(alineacion)
    
    info_campos = ""
    init_des = 0
    if curr_byte % alineacion != 0:
      init_des = alineacion - (curr_byte % alineacion)
      curr_byte += init_des
    
    init_byte = curr_byte
    max_size = 0
    min_des = 9999999
    for reg in unions[nombre][1:]:
      tmp_byte, tmp_des, tmp_info_campos, tmp_alineacion = describir_reordenado(reg, curr_byte, bytes_des, nivel+1)
      info_campos += tmp_info_campos
      max_size = max(max_size, tmp_byte - init_byte)
      min_des = min(min_des, tmp_des - tmp_byte)

    min_des = max_size + init_byte + min_des

    info = ("\t"*nivel) + "Registro variable " + nombre + " ->\n" + info_campos + \
    ("\t"*nivel) + "posición inicial: byte " + str(init_byte) + "\n" + \
    ("\t"*nivel) + "tamaño: " + str(max_size) + "\n" + \
    ("\t"*nivel) + "desperdicio de bytes: " + str(min_des) + "\n" + \
    ("\t"*nivel) + "alineación: " + str(alineacion) + "\n\n"

    curr_byte += max_size
    bytes_des += init_des + min_des
    return curr_byte, bytes_des, info, alineacion
    
  else:
    print("El nombre ingresado no corresponde a ningún registro.")


# Menu principal del programa
def Menu():
  global atoms, structs, unions 
  while(True):
    # Obtenemos el input
    print("\n\nPosibles acciones:\n\tATOMICO <nombre> <representación> <alineación>\n\tSTRUCT <nombre> [<tipo>]\n\tUNION <nombre> [<tipo>]\n\tDESCRIBIR <nombre>\n\tSALIR")
    accion = input("Ingrese una acción para proceder: ").split(" ")
    while '' in accion: accion.remove('')
    # Si no se ingresó ningun tipo de acción, devolvemos un error
    if not accion:
      print("\nNo se ingresó ninguna acción.")
      continue
    print()

    # Aplicamos la acción correspondiente
    # Se define un nuevo tipo atómico
    if len(accion) == 4 and accion[0] == "ATOMICO":
      def_atomico(accion[1], accion[2], accion[3])
    # Se define un nuevo registro
    elif len(accion) > 1 and accion[0] == "STRUCT":
      def_struct(accion[1], accion[2:])
    # Se define un nuevo registro variante
    elif len(accion) > 1 and accion[0] == "UNION":
      def_union(accion[1], accion[2:])
    # Se imprime la información correspondiente al tipo ingresado.
    elif len(accion) == 2 and accion[0] == "DESCRIBIR":
      print("Si el lenguaje guarda registros y registros variantes sin empaquetar:")
      describir(accion[1], 0, 0, True)
      print("Si el lenguaje guarda registros y registros variantes empaquetados:")
      describir(accion[1], 0, 0, False)
      print("El lenguaje guarda registros y registros viariantes reordenando los campos de manera óptima:")
      print(describir_reordenado(accion[1], 0, 0)[2])
    # Se sale del programa
    elif len(accion) == 1 and accion[0] == "SALIR":
      break
    else:
      print("\nLa acción que ingresó no existe, intente de nuevo.")



# Hacemos esto para poder aplicar al script las pruebas unitarias
if __name__ == "__main__":
  Menu()