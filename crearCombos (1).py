# Función para convertir una dirección IP en un entero
def ip_to_int(ip):
    octetos = ip.split('.')
    return (int(octetos[0]) << 24) + (int(octetos[1]) << 16) + (int(octetos[2]) << 8) + int(octetos[3])

# Función para convertir un entero en una dirección IP
def int_to_ip(ip_int):
    return f'{(ip_int >> 24) & 255}.{(ip_int >> 16) & 255}.{(ip_int >> 8) & 255}.{ip_int & 255}'

# Función para convertir una longitud de máscara en su formato decimal
def mask_to_decimal(mask_length):
    mask = (0xFFFFFFFF >> (32 - mask_length)) << (32 - mask_length)
    return int_to_ip(mask)

# Función para calcular el rango de una subred dado un IP base y una máscara
def calcular_rango_subred(base_ip, mask, subredes_ocupadas):
    base_ip_int = ip_to_int(base_ip)
    mask_bits = (2 ** (32 - mask))  # Cantidad de direcciones en la subred

    # Buscar la primera subred que no esté ocupada
    for i in range(1, 1000):  # Intentamos hasta un límite (por ejemplo 1000 redes)
        subnet_start = base_ip_int + i * mask_bits
        subnet_end = subnet_start + mask_bits - 1

        # Verificar si esta subred se solapa con las ocupadas
        rango_ocupado = False
        for ocupada in subredes_ocupadas:
            ocupada_inicio, ocupada_fin = ocupada
            if not (subnet_end < ocupada_inicio or subnet_start > ocupada_fin):
                rango_ocupado = True
                break
        
        if not rango_ocupado:
            subredes_ocupadas.append((subnet_start, subnet_end))
            return (int_to_ip(subnet_start), int_to_ip(subnet_end))
    
    return None

# Función para configurar las redes entre routers (/30)
def configurar_redes_entre_routers(num_redes, base_ip, subredes_ocupadas):
    print(f"\nConfigurando {num_redes} redes entre routers (máscara /30):")
    redes_routers = []
    for i in range(num_redes):
        combo = calcular_rango_subred(base_ip, 30, subredes_ocupadas)
        if combo:
            redes_routers.append(combo)
            print(f"Router {i + 1}: {combo[0]} - {combo[1]} (máscara {mask_to_decimal(30)})")
        else:
            print("No hay más espacio para redes entre routers.")
            break
    return redes_routers

# Función para configurar combos de VLANs
def configurar_vlans(num_vlans, base_ip, subredes_ocupadas):
    vlans = []
    
    for i in range(num_vlans):
        mask_vlan = int(input(f'Introduce la máscara para la VLAN {i+2} (e.g., 22, 23, etc.): '))
        num_combos = int(input(f'¿Cuántos combos necesitas para la VLAN {i+2}?: '))
        
        combos = []
        for _ in range(num_combos):
            combo = calcular_rango_subred(base_ip, mask_vlan, subredes_ocupadas)
            if combo:
                combos.append(combo)
            else:
                print(f"No hay más espacio para combos en la VLAN {i+2}.")
                break
        
        vlans.append((mask_vlan, combos))
    
    return vlans

# Función para imprimir los resultados
def imprimir_resultados(vlans, redes_routers):
    print("\nRedes entre routers (/30):")
    for idx, rango in enumerate(redes_routers):
        print(f'Router {idx+1}: {rango[0]} - {rango[1]} (máscara {mask_to_decimal(30)})')
    
    print("\nCombos generados para cada VLAN:")
    for idx, vlan in enumerate(vlans):
        print(f'\nVLAN {idx+2} (máscara {mask_to_decimal(vlan[0])}):')
        for rango in vlan[1]:
            print(f'{rango[0]} - {rango[1]}')

    print("\nComandos ip route generados:")
    for idx, rango in enumerate(redes_routers):
        print(f'ip route {rango[0]} {mask_to_decimal(30)}')
    for idx, vlan in enumerate(vlans):
        for rango in vlan[1]:
            print(f'ip route {rango[0]} {mask_to_decimal(vlan[0])}')

# Función principal
def main():
    base_ip = input("Introduce la IP base (se usará para todo): ")
    num_redes_routers = int(input("Introduce cuántas redes entre routers necesitas (máscara /30): "))
    num_vlans = int(input("Introduce el número de VLANs: "))
    
    subredes_ocupadas = []  # Para llevar el control de las subredes ya asignadas
    
    # Configurar redes entre routers primero
    redes_routers = configurar_redes_entre_routers(num_redes_routers, base_ip, subredes_ocupadas)
    
    # Configurar VLANs y generar combos
    vlans = configurar_vlans(num_vlans, base_ip, subredes_ocupadas)
    
    # Imprimir los resultados
    imprimir_resultados(vlans, redes_routers)

if __name__ == "__main__":
    main()