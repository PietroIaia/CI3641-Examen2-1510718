%hide show

data Church = Cero 
            | Suc Church

suma : Church -> Church -> Church
suma Cero Cero = Cero
suma (Suc x) Cero = Suc (suma x Cero)
suma Cero (Suc x) = Suc (suma Cero x)
suma (Suc y) (Suc x) = Suc (suma y (Suc x))

multiplicacion : Church -> Church -> Church
multiplicacion _ Cero = Cero
multiplicacion Cero _ = Cero
multiplicacion (Suc Cero) (Suc x) = Suc x
multiplicacion (Suc x) (Suc Cero) = Suc x
multiplicacion (Suc x) (Suc y) = multAux (Suc x) (Suc y) (Suc y)
    where
        multAux : Church -> Church -> Church -> Church
        multAux (Suc Cero) (Suc y) (Suc z) = Suc y
        multAux (Suc x) (Suc y) (Suc z) = multAux x (suma (Suc y) (Suc z)) (Suc z)

show : Church -> String
show Cero = "Cero"
show (Suc x) = "Suc " ++ show x

-- Ejemplo de ejecucion
main : IO ()
main =
    do  
        -- suma 3 + 3 == 6
        putStr $ show (suma (Suc (Suc (Suc Cero))) (Suc (Suc (Suc Cero)))) ++ "\n"
        -- multiplicacion 4 * 3 == 12
        putStr $ show (multiplicacion (Suc (Suc (Suc (Suc Cero)))) (Suc (Suc (Suc Cero))))
