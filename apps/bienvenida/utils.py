
def get_total_votos(v_resultado):
    if v_resultado:
        return sum([int(x) for x in v_resultado])
    else:
        return 0


def get_porcentaje(parcial, total):
    return str(int(parcial)//total)


def get_escrutinio(boletas, v_res, total_votos):
    escrutinio = [(b.candidato, v_res[b.indice], get_porcentaje(
        v_res[b.indice])//total_votos) for b in boletas]
    # ORDENAR
    escrutinio.append(('En Blanco', v_res[0], get_porcentaje(v_res[0]//total_votos))
    # sort by second element of tuple
    escrutinio.sort(reverse=True, key=lambda x: x[1])  # index 1 means second element
    return escrutinio
