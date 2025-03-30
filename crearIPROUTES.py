def decimal_mask(mask_bits):
    """Convertir una máscara de bits en formato decimal"""
    mask = (0xffffffff >> (32 - mask_bits)) << (32 - mask_bits)
    return (f"{(mask >> 24) & 255}.{(mask >> 16) & 255}.{(mask >> 8) & 255}.{mask & 255}")

def main():
    routers = []
    router_networks = []
    router_interlinks = []
    
    # 1.- Pedir al usuario el número de routers y la red base
    num_routers = int(input("Ingrese el número de routers: "))
    base_network = input("Ingrese la red base (e.g., 15.0.0): ")

    # 2.- Pedir el número de redes para cada router y sus detalles
    for i in range(1, num_routers + 1):
        print(f"\nRouter {i}:")
        num_networks = int(input(f"Ingrese el número de redes para el router {i}: "))
        networks = []
        for j in range(num_networks):
            net_id = input(f"Ingrese el ID de la red {j+1} para el router {i}: ")
            mask = int(input(f"Ingrese la máscara de red (en bits) para la red {j+1}: "))
            networks.append((net_id, mask))
        router_networks.append(networks)

    # 3.- Pedir las redes entre routers
    num_interlinks = int(input("\n¿Cuántas redes entre routers hay?: "))
    for i in range(num_interlinks):
        interlink_id = input(f"Ingrese el ID de la red entre routers {i+1}: ")
        router_interlinks.append(interlink_id)

    # 4.- Generar las rutas para cada router
    for i in range(1, num_routers + 1):
        print(f"\nConfigurando Router {i}:")
        known_networks = router_networks[i - 1]

        # Imprimir rutas a otras redes
        for j in range(1, num_routers + 1):
            if i != j:  # Evitar las redes propias
                print(f"\nRedes del router {j}:")
                gateway = input(f"¿Por dónde conocerá las redes del router {j}? (Ingrese la última parte de la IP): ")

                for net_id, mask in router_networks[j - 1]:
                    mask_decimal = decimal_mask(mask)
                    print(f"ip route {net_id} {mask_decimal} {base_network}.{gateway}")

        # Imprimir rutas para las redes entre routers
        print("\nRedes entre routers:")
        for interlink_id in router_interlinks:
            print(f"ip route {interlink_id} 255.255.255.252 {base_network}.0")  # Asumimos máscara /30 para las redes entre routers


if __name__ == "__main__":
    main()
