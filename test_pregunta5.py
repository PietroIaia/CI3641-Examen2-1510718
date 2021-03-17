#test_tutorial.py
from pregunta5_1510718 import *
from unittest import TestCase
from io import StringIO
from unittest.mock import patch
import os
import subprocess

# Para correr pruebas de cobertura: pip install coverage

class pregunta3Test(TestCase):


    def test_input_examen(self):
        self.maxDiff = None

        input_ = "DEF 0 Int\nDEF 1 Int\nDEF n Int\nDEF eq a -> a -> Bool\nTIPO eq 0\nTIPO eq 2\nDEF prod Int -> Int -> Int\nDEF dif Int -> Int -> Int\n" + \
                 "DEF if Bool -> a -> a -> a\nTIPO if (eq 0 n) 1 n\nTIPO if (eq 0 n) 1 eq\nTIPO if (eq 0 n) if\nDEF fact t->t\n" + \
                 "TIPO eq (fact n) (if (eq n 0) 1 (prod n (fact (dif n 1))))\nTIPO eq fact (if (eq n 0) 1 (prod n (fact (dif n 1))))\nSALIR\n"

        menu_string = "\n\nPosibles acciones:\n\tDEF <nombre> <tipo>\n\tTIPO <expr>\n\tSALIR\nIngrese una acción para proceder: "

        with patch('sys.stdin', StringIO(input_)) as mocked_stdin:
            with patch('sys.stdout', new=StringIO()) as mocked_stdout:

                Menu()

                output = mocked_stdout.getvalue()
                expected_output = menu_string + "\nSe definió ’0’ con tipo Int\n" + menu_string + "\nSe definió ’1’ con tipo Int\n" + menu_string + \
                "\nSe definió ’n’ con tipo Int\n" + menu_string + "\nSe definió ’eq’ con tipo a->a->Bool\n" + menu_string + \
                "\nInt->Bool\n" + menu_string + "\nERROR, el nombre ’2’ no ha sido definido\n" + menu_string + \
                "\nSe definió ’prod’ con tipo Int->Int->Int\n" + menu_string + "\nSe definió ’dif’ con tipo Int->Int->Int\n" + menu_string + \
                "\nSe definió ’if’ con tipo Bool->a->a->a\n" + menu_string + "\nInt\n" + menu_string + "\nERROR, no se pudo unificar Int con a->a->Bool\n" + menu_string + \
                "\n(Bool->a->a->a)->Bool->a->a->a\n" + menu_string + "\nSe definió ’fact’ con tipo t->t\n" + menu_string + "\nBool\n" + menu_string + "\n" + \
                "ERROR, no se pudo unificar t->t con Int\n" + menu_string + "\n"

                self.assertEqual(output, expected_output)