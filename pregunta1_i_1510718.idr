data Arbol a = Hoja a 
             | Rama a (Arbol a) (Arbol a)

esDeBusqueda : (Ord a) => Arbol a -> Bool 
esDeBusqueda (Hoja x) = True
esDeBusqueda (Rama a b1 b2) = listaAsc (inOrder b1 ++ [a] ++ inOrder b2)
    where
        inOrder (Hoja x) = [x]
        inOrder (Rama x t1 t2) = inOrder t1 ++ [x] ++ inOrder t2
        listaAsc [] = True
        listaAsc [x] = True
        listaAsc (x::y::xs) = x <= y && listaAsc (y::xs)

-- Ejemplo de ejecucion
main : IO ()
main = putStr $ show (esDeBusqueda (Rama 4 (Rama 2 (Hoja 1) (Hoja 3)) (Hoja 5)))