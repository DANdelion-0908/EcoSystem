MANDATORY_POSITIONS = [
    "Piccolo",
    "Tiple",
    "Centro",
    "Bajo",
    "Piccolo segundo",
    "Tiple segundo", 
    "Bajo tenor",
    "Batería"]

# Datos de prueba
# Llena los puestos obligatorios y algunos substitutos
test = {"1": {"member": "Dan", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Tiple", "member_positions": None}, 
        "2": {"member": "André", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Piccolo", "member_positions": None},
        "3": {"member": "Tiffany", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Centro", "member_positions": None},
        "4": {"member": "Pallais", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Bajo", "member_positions": None},
        "5": {"member": "Kilary", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Piccolo segundo", "member_positions": None},
        "6": {"member": "Lourdes", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Tiple segundo", "member_positions": None},
        "7": {"member": "Minely", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Bajo tenor", "member_positions": None},
        "8": {"member": "Christian", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Batería", "member_positions": None},
        "9": {"member": "Jefferson", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Tiple segundo", "member_positions": None},
        "10": {"member": "Daniela", "melody": "Verónica", "instrument": "Marimba 4/4", "main": "Tiple", "member_positions": None}}

def recommend_member_for_position(available_members: dict, filled_positions: dict) -> dict:
    """Recomienda un integrante disponible para un puesto obligatorio en una melodía específica.
    
    Args:
        available_members (dict): Todos los miembros disponibles.
        filled_positions (dict): Puestos obligatorios ya ocupados en la melodía.

    Returns:
        dict: Diccionario con la recomendación del integrante para el puesto obligatorio.
    """
    recommendations = filled_positions.copy()

    for details in available_members.values():
        if details["member"] not in recommendations[details["main"]] and len(recommendations[details["main"]]) <= 1:
            print(f"- Se sugiere agregar a {details["member"]} al puesto {details["main"]}\n")
            recommendations[details["main"]].append(details["member"])

        elif details["member"] not in recommendations[details["main"]] and len(recommendations[details["main"]]) >= 1:
            print(f"El puesto {details["main"]} ya posee varias personas. Buscando otro...")
            
            for key, value in recommendations.items():
                if not value:
                    print(f"- Se sugiere agregar a {details["member"]} al puesto {key}\n")
                    recommendations[key].append(details["member"])
                    break

                elif len(value) == 1:
                    print(f"- Se sugiere agregar a {details["member"]} al puesto {key}\n")
                    recommendations[key].append(details["member"])
                    break

                else:
                    print(f"Todos los puestos poseen al menos un substituto")
                    break

    return recommendations

def check_mandatory_positions_filled(members_in_melody: dict) -> dict:
    """Verifica si todos los puestos obligatorios han sido llenados para una melodía específica.

    Args:
        members_in_melody (dict): Miembros asignados a la melodía.

    Returns:
        dict: Diccionario con los puestos obligatorios, su estado (True si está llenado, False si no lo está) y quién lo ocupa.
    """
    filled_positions: dict = {position: [] for position in MANDATORY_POSITIONS}

    for member in members_in_melody.values():
        if member["member_positions"]:
            positions = str(member["member_positions"]).split(",")

            for position in positions:
                if position.strip() in MANDATORY_POSITIONS:
                    filled_positions[position.strip()].append(member["member"])

    return filled_positions
