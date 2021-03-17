#test_tutorial.py
from pregunta3_1510718 import *
from unittest import TestCase
from io import StringIO
from unittest.mock import patch
import os
import subprocess

# Para correr pruebas de cobertura: pip install coverage

class pregunta3Test(TestCase):

    # Probamos la creación en un Struct
    def test_input_struct(self):
        self.maxDiff = None

        input_ = "ATOMICO int 4 4\nATOMICO char 2 2\nATOMICO bool 1 2\nATOMICO float 8 8\nSTRUCT wtf int char int float bool\nDESCRIBIR wtf\nSALIR\n"

        menu_string = "\n\nPosibles acciones:\n\tATOMICO <nombre> <representación> <alineación>\n\tSTRUCT <nombre> [<tipo>]\n\tUNION <nombre> [<tipo>]\n\tDESCRIBIR <nombre>\n\tSALIR\nIngrese una acción para proceder: "

        with patch('sys.stdin', StringIO(input_)) as mocked_stdin:
            with patch('sys.stdout', new=StringIO()) as mocked_stdout:

                Menu()

                output = mocked_stdout.getvalue()
                expected_output = menu_string + "\n" + menu_string + "\n" + menu_string + "\n" + menu_string + "\n" + menu_string + "\n" + menu_string + \
                "\nSi el lenguaje guarda registros y registros variantes sin empaquetar:\nRegistro wtf ->\n\tTipo atómico int\n\t" + \
                "posición inicial: byte 0\n\ttamaño: 4\n\talineación: 4\n\n\tTipo atómico char\n\tposición inicial: byte 4\n\ttamaño: 2" + \
                "\n\talineación: 2\n\n\tTipo atómico int\n\tposición inicial: byte 8\n\ttamaño: 4\n\talineación: 4\n\n\tTipo atómico float" + \
                "\n\tposición inicial: byte 16\n\ttamaño: 8\n\talineación: 8\n\n\tTipo atómico bool\n\tposición inicial: byte 24\n\t" + \
                "tamaño: 1\n\talineación: 2\n\nposición inicial: byte 0\ntamaño: 25\ndesperdicio de bytes: 6" + \
                "\nalineación: 4\n\nSi el lenguaje guarda registros y registros variantes empaquetados:\nRegistro wtf ->\n\tTipo atómico int" + \
                "\n\tposición inicial: byte 0\n\ttamaño: 4\n\n\tTipo atómico char\n\tposición inicial: byte 4\n\ttamaño: 2\n\n\t" + \
                "Tipo atómico int\n\tposición inicial: byte 6\n\ttamaño: 4\n\n\tTipo atómico float\n\tposición inicial: byte 10\n\t" + \
                "tamaño: 8\n\n\tTipo atómico bool\n\tposición inicial: byte 18\n\ttamaño: 1\n\nposición inicial: byte 0\ntamaño: 19\n" + \
                "desperdicio de bytes: 0\n\nEl lenguaje guarda registros y registros viariantes reordenando los campos de manera óptima:\n" + \
                "Registro wtf ->\n\tTipo atómico int\n\tposición inicial: byte 0\n\ttamaño: 4\n\talineación: 4\n\n\tTipo atómico int\n\t" + \
                "posición inicial: byte 4\n\ttamaño: 4\n\talineación: 4\n\n\tTipo atómico float\n\tposición inicial: byte 8\n\ttamaño: 8" + \
                "\n\talineación: 8\n\n\tTipo atómico char\n\tposición inicial: byte 16\n\ttamaño: 2\n\talineación: 2\n\n\tTipo atómico bool\n\t" + \
                "posición inicial: byte 18\n\ttamaño: 1\n\talineación: 2\n\nposición inicial: byte 0\ntamaño: 19\ndesperdicio de bytes: 0\nalineación: 4\n\n\n" + \
                menu_string + "\n"

                self.assertEqual(output, expected_output)
    
    # Probamos la creación de un Union
    def test_input_union(self):
        self.maxDiff = None

        input_ = "ATOMICO int' 2 2\nATOMICO float' 1 8\nSTRUCT wtf' int' float'\nUNION this wtf' int'\nDESCRIBIR this\nSALIR\n"

        menu_string = "\n\nPosibles acciones:\n\tATOMICO <nombre> <representación> <alineación>\n\tSTRUCT <nombre> [<tipo>]\n\tUNION <nombre> [<tipo>]\n\tDESCRIBIR <nombre>\n\tSALIR\nIngrese una acción para proceder: "

        with patch('sys.stdin', StringIO(input_)) as mocked_stdin:
            with patch('sys.stdout', new=StringIO()) as mocked_stdout:

                Menu()

                output = mocked_stdout.getvalue()
                expected_output = menu_string + "\n" + menu_string + "\n" + menu_string + "\n" + menu_string + "\n" + menu_string + \
                "\nSi el lenguaje guarda registros y registros variantes sin empaquetar:\nRegistro variable this ->\n\tRegistro wtf' ->" + \
                "\n\t\tTipo atómico int'\n\t\tposición inicial: byte 0\n\t\ttamaño: 2\n\t\talineación: 2\n\n\t\tTipo atómico float'\n\t\t" + \
                "posición inicial: byte 8\n\t\ttamaño: 1\n\t\talineación: 8\n\n\tposición inicial: byte 0\n\ttamaño: 9\n\tdesperdicio de bytes: 6" + \
                "\n\talineación: 2\n\n\tTipo atómico int'\n\tposición inicial: byte 0\n\ttamaño: 2\n\talineación: 2\n\nposición inicial: byte 0\ntamaño: 9" + \
                "\ndesperdicio de bytes: 6\nalineación: 2\n\nSi el lenguaje guarda registros y registros variantes empaquetados:\nRegistro variable this ->\n\t" + \
                "Registro wtf' ->\n\t\tTipo atómico int'\n\t\tposición inicial: byte 0\n\t\ttamaño: 2\n\n\t\tTipo atómico float'\n\t\tposición inicial: byte 2\n\t\t" + \
                "tamaño: 1\n\n\tposición inicial: byte 0\n\ttamaño: 3\n\tdesperdicio de bytes: 0\n\n\tTipo atómico int'\n\tposición inicial: byte 0\n\ttamaño: 2\n\n" + \
                "posición inicial: byte 0\ntamaño: 3\ndesperdicio de bytes: 0\n\nEl lenguaje guarda registros y registros viariantes reordenando los campos de manera óptima:\n" + \
                "Registro variable this ->\n\tRegistro wtf' ->\n\t\tTipo atómico float'\n\t\tposición inicial: byte 0\n\t\ttamaño: 1\n\t\talineación: 8\n\n\t\tTipo atómico int'" + \
                "\n\t\tposición inicial: byte 2\n\t\ttamaño: 2\n\t\talineación: 2\n\n\tposición inicial: byte 0\n\ttamaño: 4\n\tdesperdicio de bytes: 1\n\talineación: 8" + \
                "\n\n\tTipo atómico int'\n\tposición inicial: byte 0\n\ttamaño: 2\n\talineación: 2\n\nposición inicial: byte 0\ntamaño: 4\ndesperdicio de bytes: 1\n" + \
                "alineación: 8\n\n\n" + menu_string + "\n"

                self.assertEqual(output, expected_output)
    

    # Probaremos
    # Definir un tipo atómico con nombre ya definido
    # Definir un tipo atómico con representación no entera
    # Definir un struct con nombre ya definido
    # Definir un struct con algún tipo no definido
    # Definir un union con nombre ya definido
    # Definir un union con algún tipo no definido 
    # Describir un nombre no definido
    # Input vacío
    # Input inválido
    def test_input_error(self):
        self.maxDiff = None

        input_ = "ATOMICO hola 1 1\nATOMICO hola 1 2\nATOMICO hola a 1\nSTRUCT hola hola\nSTRUCT wtf float\nUNION hola hola\nUNION wtf2 float\nDESCRIBIR wtf3\n\nATOMICO hola 1 2 3\nSALIR\n"

        menu_string = "\n\nPosibles acciones:\n\tATOMICO <nombre> <representación> <alineación>\n\tSTRUCT <nombre> [<tipo>]\n\tUNION <nombre> [<tipo>]\n\tDESCRIBIR <nombre>\n\tSALIR\nIngrese una acción para proceder: "

        with patch('sys.stdin', StringIO(input_)) as mocked_stdin:
            with patch('sys.stdout', new=StringIO()) as mocked_stdout:

                Menu()

                output = mocked_stdout.getvalue()
                expected_output = menu_string + "\n" + menu_string +"\nhola ya corresponde a algún tipo creado en el programa.\n" + menu_string + "\nLa representacion y la alineacion ingresada debe ser de tipo entero positivo.\n" + menu_string + \
                "\nhola ya corresponde a algún tipo creado en el programa.\n" + menu_string + "\nAlguno de los tipos ingresados no han sido definidos.\n" + menu_string + \
                "\nhola ya corresponde a algún tipo creado en el programa.\n" + menu_string + "\nAlguno de los tipos ingresados no han sido definidos.\n" + menu_string + \
                "\nEl nombre ingresado no corresponde a ningún tipo creado en el programa.\n" + menu_string + "\nNo se ingresó ninguna acción.\n" + menu_string + \
                "\nLa acción que ingresó no existe, intente de nuevo.\n" + menu_string + "\n"

                self.assertEqual(output, expected_output)