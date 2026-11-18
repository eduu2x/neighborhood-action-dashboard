def porta_and(entrada_a, entrada_b):
    # porta AND
    resultado = entrada_a and entrada_b
    return int(resultado)


def porta_or(entrada_a, entrada_b):
    # porta OR
    resultado = entrada_a or entrada_b
    return int(resultado)


def calcular_alerta_prioridade(risco_imediato, prazo_excedido, reincidencia_registrada):
    # expressao S1
    termo_bc = porta_and(prazo_excedido, reincidencia_registrada)
    return porta_or(risco_imediato, termo_bc)


def calcular_pendencia_critica(risco_imediato, prazo_excedido, reincidencia_registrada):
    # expressao S2
    termo_ab = porta_and(risco_imediato, prazo_excedido)
    termo_bc = porta_and(prazo_excedido, reincidencia_registrada)
    return porta_or(termo_ab, termo_bc)


def definir_status_visual(alerta_prioridade, pendencia_critica):
    # status visual
    if alerta_prioridade == 1 and pendencia_critica == 1:
        return "Destaque Vermelho + Amarelo"
    if alerta_prioridade == 1:
        return "Destaque Amarelo"
    return "Fila Comum"


def avaliar_ocorrencia(risco_imediato, prazo_excedido, reincidencia_registrada):
    # funcao integradora
    alerta_prioridade = calcular_alerta_prioridade(
        risco_imediato, prazo_excedido, reincidencia_registrada
    )
    pendencia_critica = calcular_pendencia_critica(
        risco_imediato, prazo_excedido, reincidencia_registrada
    )
    status_visual_dashboard = definir_status_visual(alerta_prioridade, pendencia_critica)
    return {
        "alerta_prioridade": alerta_prioridade,
        "pendencia_critica": pendencia_critica,
        "status_visual_dashboard": status_visual_dashboard,
    }
