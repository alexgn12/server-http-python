data = "hola querido que es lo que tu quiere" \
"mi guapo"

def parsea_get(data):
    linea = data.split('\r\n')
    print(linea)
    divide = linea[0].split(' ')
    saludo, amor, k = divide[0,1,2]
    print(divide)
    print(saludo, amor, k)


parsea_get(data)
