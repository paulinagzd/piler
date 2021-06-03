![Piler Logo](/icon.png)
# Piler (the compiler)
## Welcome to πler!
 - Proyecto final - Diseño de compiladores
 - Febrero - Junio 2021
 - Equipo Obj 12

## README Index

 - [Quick Reference Manual](#quick-reference-manual)
   - [Español :es:](#español)
   - [English :gb:](#english)
 - [Instalación](#instalación)
 - [Equipo](#equipo)
---
# Manual de usuario
### Español
### Iniciar un programa

> Para iniciar un programa en πler, se necesita declarar la palabra ‘program’ seguida de su nombre y terminación en punto y coma.
`programa nombrePrograma;`
---
### Declaración de variables
Estas deben de ser declaradas en 3 lugares importantes:
1. Después de la línea de inicio de cada programa
2. Después de la declaración de una función o main (SIEMPRE al inicio del bloque)
3. En clases, después de la palabra clave de *att:*

La sintaxis está compuesta de la palabra clave *var* seguida del *tipo* y *ID* de la variable y finalizada con punto y coma. Ejemplo:
`var int nombreVariable;`

Para arreglos y matrices, se declara el tipo en _plural_ con sus respectivas dimensiones _declaradas_. Ejemplo:
*Arreglos:* `var ints nombreArr[5] = {1,2,3,4,5}`
*Matrices:* `var ints nombreMat[2][2] = {{0,0},{0,0}}`

> Los tipos de datos pueden ser: `int, flt, boo, cha y str` (con sus plurales)
---
### Función main
Un programa siempre debe de tener una función main. Esta se declara con la siguiente sintaxis:
```
int main () {
  /* Aqui va el cuerpo de la función */
}
```

Con una función main puede funcionar el código, sin embargo, si se desean agregar más funciones, serían _antes de la función main_.

### Funciones 
La declaración de las funciones es únicamente de tipos _simples_ (es decir, sin arreglos ni matrices) o de tipo *void*.

Las funciones de tipo simple deben de tener su respectivo valor de retorno al igual que su declaración.
```
func int nombreFunc (int param1, flt param2) {
  /* Aqui va el cuerpo de la función */
return valorInt
}
```

Las funciones de tipo *void* no pueden tener valor de retorno, de lo contrario habría un error.
```
func void nombreFunc (int param1, flt param2) {
  /* Aqui va el cuerpo de la función */
}
```
---
### Contenido de funciones o main

#### Tipos de expresiones y operaciones aritméticas
Operadores binarios aritméticos: `+, -, *, /`
Operadores binarios booleanos: `>, >=, <, <=, ==, !=`

#### Asignación
`nombreVariable = expresion`

#### Condicionales
Las condicionales pueden tener un flujo alterno o no, un ejemplo de implementación es el de un solo *if*.
```
if (expresionBooleana) then {
	/* Aqui va el cuerpo de la condicional */
}; /* No olvidar este punto y coma*/
```
Si se desea un flujo alterno, simplemente agregar antes del punto y coma lo siguiente:
```
else {
  /* Aqui va el cuerpo de la condicional */
}; /* Mover aqui el punto y coma */
```

Si se desea tener una condicional de flujo alterno en una sola línea, se pueden usar expresiones *ternarias*.
`expresionBooleana ? opcion1 : opcion2 ;`

👀 *OJO* : a las expresiones ternarias no se les pueden poner valores de retorno ni ciclos anidados, simplemente estatutos de _una_ línea.

#### Lectura y escritura
Para leer:
`read(variable)`

Para escribir:
`print(expresion)`

#### Ciclos
Existen dos tipos, el *while* y el *do-while*. Se componen de la siguiente sintaxis
```
while (expresionbooleana) then {
  /* Aqui va el cuerpo del ciclo */
};
```

```
do {
  /* Aqui va el cuerpo del ciclo */
} while (expresionbooleana);
```
---
### Llamadas
#### A variables
Llamarla por su identificador. En caso de ser arreglo o matriz, por su identificador seguido del índice deseado.
```
nombreVariable            /* llamada a tipo simple */
nombreMatriz[2][3]        /* llamada a tipo multiple */
```

#### A funciones
Cuando una función es llamada, se deberá de poner su declaración con sus parámetros encasillada entre {} corchetes. Ejemplo:
`{nombreFuncion(param1, param2)}`

Hay excepciones a esta regla. Si la llamada será lo ÚNICO que hay en la línea, entonces no necesitaría estos corchetes. De lo contrario, si es parte de alguna expresión o asignación, sí debe usarlos. 

Ejemplos de código
```
nombreFuncion(param1)            /* llamada simple */
a = {nombreFuncion(param1)} * a  /* llamada con expresiones */
```
---
###  Clases y objetos
Ya que Piler es un lenguaje orientado a objetos, se pueden declarar _clases_ con la siguiente sintaxis.
```
class nombreClase: {
  att:
		/* aqui se declaran las variables de la clase */
  met:
		/* aqui se declaran las funciones de la clase */
};
```

Las clases son _super secretas_ pero afortunadamente tienen una contraseña sencilla: cada que se quiera acceder a algo dentro de esa clase (incluso estando en la misma clase), se necesita llamar por su clase primero.
```
nombreClase.variableDeClase		          /* a atributos */
nombreClase.funcionDeClase(params)      /* a métodos */
```
---
### Ejemplo sencillo de un programa en Piler
```
program aritmetica;
var int a, b;
int main() {
    a = 8 * (7 - 4) + 5
    b = 9
    if (a == 2) then {
        print(2+2, a)
    } else {
        print(b)
    };
    print(a)
}
```
---
### English
### Starting a program

> To start a program in πler, you need to declare the word 'program' followed by its name and ending in a semicolon.
`program programName;`
---
### Declaration of variables
These must be declared in 3 important places:
1. After the start line of each program
2. After the declaration of a function or main (ALWAYS at the beginning of the block)
3. In classes, after the *att* keyword:

The syntax is composed of the keyword *var* followed by the *type* and *ID* of the variable and ended with a semicolon. Example:
`var int variableName;`

For arrays and arrays, the type is declared in _plural_ with its respective _declared_ dimensions. Example:
*Arrays:* `var ints arrName[5] = {1,2,3,4,5}`
*Matrices:* `var ints matName[2][2] = {{0,0},{0,0}}`

> Data types can be: `int, flt, boo, cha y str` (with their plurals)
---
### Main function
A program must always have a main function. This is declared with the following syntax:
```
int main () {
   /* Body of the function goes here */
}
```

With a main function the code can work, however, if you want to add more functions, they would be _before the main_ function.

### Functions
The declaration of functions is only of _simple_ types (that is, no arrays or matrices) or of type *void*.

Simple type functions must have their respective return value as well as their declaration.
```
func int funcName(int param1, flt param2) {
   /* Body of the function goes here */
return intValue
}
```
Functions of type *void* cannot have a return value, otherwise there would be an error.
```
func void funcname (int param1, flt param2) {
  /* Body of the function goes here */
}
```
---
### Content of functions or main

#### Types of expressions and arithmetic operations
Arithmetic binary operators: `+, -, *, /`
Boolean binary operators: `>,> =, <, <=, ==,! =`

#### Assignment
`variableName = expression`

#### Conditionals
Conditionals may also have an alternative flow, an example of an implementation is that of a single *if*.
```
if (booleanExpression) then {
/* Body of the conditional goes here */
}; /* Don't forget this semicolon */
```
If an alternate flow is desired, simply add the following before the semicolon:
```
else {
  /* Body of the conditional goes here */
}; /* Move the semicolon here */
```

If you want to have an alternating flow conditional on a single line, you can use *ternary* expressions.
`Boolean expression? option1: option2;`

👀 *WARNING*: you cannot put return values or nested loops to ternary expressions, just _one_ line statutes.
#### Reading and writing
To read:
`read (variable)`

To write:
`print (expression)`

#### Loops
There are two types, the *while* and the *do-while*. They consist of the following syntax
```
while (booleanExpression) then {
  /* Body of the loop goes here */
};
```

```
do {
  /* Body of the loop goes here */
} while (booleanExpression);
```
---
### Calls
#### To variables
Call it by its identifier. In case of being an array or matrix, by its identifier followed by the desired index.
```
variableName /* simple type call */
arrayName [2][3] /* call to multiple type */
```

#### To functions
When a function is called, its declaration with its parameters must be enclosed in {} brackets. Example:
`{FunctionName (param1, param2)}`

There are exceptions to this rule. If the call will be the ONLY thing on the line, then you would not need these brackets. Otherwise, if it's part of some expression or assignment, you must use them.

Code examples
```
functionName (param1)            /* simple call */
a = {functionName(param1)} * a   /* called with expressions */
```
---
### Classes and objects
Since Piler is an object-oriented language, _classes_ can be declared with the following syntax.
```
class className: {
  att:
/* here the class variables are declared */
  met:
/* here the functions of the class are declared */
};
```

The classes are _super secret_ but fortunately they have a simple password: every time you want to access something inside that class (even being in the same class), you need to call by its class first.
```
classname.classVariable          /* for attributes */
className.classFunction(params)  /* for methods */
```
---
### Simple example of a Piler program
```
program arithmetic;
var int a, b;
int main() {
    a = 8 * (7 - 4) + 5
    b = 9
    if (a == 2) then {
        print(2+2, a)
    } else {
        print(b)
    };
    print(a)
}
```
---
## Instalación
Para instalar este lenguaje es necesario tener Python3 instalado. Esto se puede verificar con el comando `python3` en la terminal.

Para instalar Piler, se debe correr el siguiente comando:
```
git clone https://github.com/paulinagzd/piler.git
```
Con este paso listo, se puede correr:
```
python3 piler.py
```
Esto dará acceso a ingresar el nombre de cualquiera de los archivos de prueba (los de la extensión .pi) para poder usar Piler.

# Haπ Comπling!
---
## Equipo
|  **Paulina González Dávalos** | **Luis Felipe Miranda Icazbalceta** |
| :---: |:---:|
| ![Paulina](https://avatars.githubusercontent.com/u/31547357?v=4) | ![Luis Felipe](https://avatars.githubusercontent.com/u/21185878?v=4) |
|  A01194111 |  A00820799 |
