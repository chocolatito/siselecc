

def get_escrutinio(boletas, v_resultado):
    escrutinio = [(b.candidato, v_resultado[b.indice]) for b in boletas]
    # ORDENAR
    escrutinio.append(('En Blanco', v_resultado[0],))
    # sort by second element of tuple
    escrutinio.sort(reverse=True, key=lambda x: x[1])  # index 1 means second element
    return escrutinio
