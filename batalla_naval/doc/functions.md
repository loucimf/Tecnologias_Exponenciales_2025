

## Utilize varias funciones que no vimos, como por ejemplo: 
 
[funcs]:
- min(int, int2) (opcional arg 2) devuelve el `minimo` entre 2 args

- max(int, int2) (opcional arg 2) devuelve el `maximo` entre 2 args

- range(int) hasta 3 args (start, stop, step) `step` especifica el <incremento> [+-] y progreso de la secuencia, osea cuantos "`salta`"

[listas]:
- remove(arg) `elimina` un objeto de un <array>

- append(arg) `añade` como ultimo elemento un obj a un <array>

- index(arg) retorna el `indice` de un obj en un <array>

- join(arg1, arg2, arg3.....) `concatena` cualquier cantidad de strings que se especifiquen y el [string] que haya llamado el metodo
        se `inserta` en el medio de cada elemento


## Documentacion de las funciones (solo las importantes)


saca el `maximo` y el `minimo` entre las primeras 2 coords y da un rango entre estas dos

[def] get_numbers_between(num1: int, num2: int):
    lower = min(num1, num2)
    upper = max(num1, num2)

    numbers_in_between = list(range(lower + 1, upper))
    return numbers_in_between




Como cuando se instancia el barco, no se definen todas sus `coords`, hago una funcion que en base a `get_numbers_between`,
    añade a un <array> las coordenadas del barco enteras

[def] set_all_coordinates(boat: Ship):

    allCoordinates: list = []
<paso1 
    agarrar las coords de inicio y fin.
>
    startCoord: Coordinate = boat.start_coord
    endCoord: Coordinate = boat.end_coord
<paso2
    añadir la start coord al inicio de allCoordinates, para que este bien ordenado.
>
    allCoordinates.append(startCoord)

<paso3
    definir si esta vertical, para trabajar en el axis adecuado
    - en el caso de eje Y (numeros crudos) es mas facil
    - en el caso de eje X (letras abstractas) hay que conseguir la posicion en la matriz
>
    if (not isVertical(boat)): 
        # get the missing numbers in the Y axis (number axis)
        missingCoords: list = get_numbers_between(startCoord.number, endCoord.number)
        for yCoords in missingCoords: 
            coordinate: Coordinate = Coordinate(startCoord.letter, yCoords)
            allCoordinates.append(coordinate)
        allCoordinates.append(endCoord)

    else: 

<paso4
    ya lo documente, pero es lo mismo pero con coords crudas
>
        # get raw coords for alphabet identification
        raw_start_coords: list = startCoord.getMatrixPosition()
        raw_end_coords: list = endCoord.getMatrixPosition()
    
        # get the missing numbers in the X axis (letter axis)
        missingCoords: list = get_numbers_between(raw_start_coords[0], raw_end_coords[0])
        for xCoords in missingCoords: 
            coordinate: Coordinate = Coordinate(ALPHABET[xCoords], startCoord.number)
            # append the coords (abstract) to allCoordinates 
            allCoordinates.append(coordinate)

        allCoordinates.append(endCoord)
    # set the coordinates to the boat
    boat.coords = allCoordinates