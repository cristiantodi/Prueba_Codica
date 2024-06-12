import requests

# Función para obtener tasas de cambio
def tasaCambio(api_key, base_currency='USD'):
    url = f'https://api.freecurrencyapi.com/v1/latest?apikey={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Error: {response.status_code}')
        return None

def menu():
    print("\nMenú:")
    print("1 - Mostrar lista de monedas")
    print("2 - Mostrar tasas de cambio")
    print("3 - Establecer moneda base")
    print("4 - Establecer cantidad a convertir")
    print("5 - Ver historial de conversiones")
    print("6 - Salir")
    return input("Seleccione una opción: ")

# Función para mostrar la lista de monedas
def listaMonedas(tasas):
    print("\nLista de monedas disponibles:")
    monedas = list(tasas['data'].keys())
    for i in range(0, len(monedas), 4):
        fila = monedas[i:i+4]
        while len(fila) < 4:
            fila.append('')
        print("{:<10} {:<10} {:<10} {:<10}".format(*fila))

# Función para mostrar las tasas de cambio
def mostrarCambio(tasas):
    print("\nTasas de cambio:")
    for moneda, valor in tasas['data'].items():
        print(f"{moneda}: {valor}")

# Función para realizar la conversión
def convertirMoneda(tasas, base_currency, cantidad, historial):
    print("\nConvertir moneda:")
    destino = input("Ingrese la moneda de destino: ").upper()
    if destino in tasas['data']:
        tasa = tasas['data'][destino]
        conversion = cantidad * tasa
        historial.append(f"{cantidad} {base_currency} a {destino} = {conversion:.2f} {destino}")
        print(f"Resultado: {conversion:.2f} {destino}")
    else:
        print("Moneda no disponible.")

# Función para ver el historial de conversiones
def ver_historial(historial):
    print("\nHistorial de conversiones:")
    for registro in historial:
        print(registro)

if __name__ == "__main__":
    api_key = 'fca_live_9wvMjR7hq5t34hDq08D27FYazF3OogFlcKZXpjua'  
    base_currency = 'USD'
    cantidad = 0.0
    historial = []
    
    tasas = tasaCambio(api_key, base_currency)
    if tasas is None:
        print("Error al obtener las tasas de cambio.")
        exit()
        
    def tasasCambios(tasas):
        if tasas:
            clave, valor = next(iter(tasas.items()))
            cantidad = len(valor)
            
            tasas_lista = list(valor.items())
            
            for i in range(0, cantidad, 4):
                fila = tasas_lista[i:i+4]
                for moneda, tasa in fila:
                    print(f"{moneda}: {tasa}", end="\t")
    
    tasasCambios(tasas)

    while True:
        opcion = menu()
        
        if opcion == '1':
            listaMonedas(tasas)
        elif opcion == '2':
            # mostrarCambio(tasas)
            tasasCambios(tasas)
        elif opcion == '3':
            base_currency = input("Ingrese la moneda base: ").upper()
            tasas = tasaCambio(api_key, base_currency)
            if tasas is None:
                print("Error al obtener las tasas de cambio.")
                base_currency = 'USD'
                tasas = tasaCambio(api_key, base_currency)
        elif opcion == '4':
            try:
                cantidad = float(input("Ingrese la cantidad a convertir: "))
                convertirMoneda(tasas, base_currency, cantidad, historial)
            except ValueError:
                print("Por favor, ingrese una cantidad válida.")
        elif opcion == '5':
            ver_historial(historial)
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")
