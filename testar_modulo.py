from dados_simulados import ocorrencias_simuladas
from modulo_logico import avaliar_ocorrencia

STATUS_POR_SAIDA = {
    (0, 0): "Fila Comum",
    (1, 0): "Destaque Amarelo",
    (1, 1): "Destaque Vermelho + Amarelo",
}

COMBINACOES_ESPERADAS = {"000", "001", "010", "011", "100", "101", "110", "111"}

assert len(ocorrencias_simuladas) == 8, "quantidade incorreta"

# testes
print("Testes do modulo logico")
print("-" * 60)
print(f"{'Caso':<5}{'ID':<8}{'Entradas':<9}{'S1':<4}{'S2':<4}Status")
print("-" * 60)

combinacoes = set()

for numero, ocorrencia in enumerate(ocorrencias_simuladas, start=1):
    resultado = avaliar_ocorrencia(
        ocorrencia["risco_imediato"],
        ocorrencia["prazo_excedido"],
        ocorrencia["reincidencia_registrada"],
    )

    assert resultado["alerta_prioridade"] == ocorrencia["esperado_s1"], "erro no alerta"
    assert resultado["pendencia_critica"] == ocorrencia["esperado_s2"], "erro na pendencia"

    chave_status = (ocorrencia["esperado_s1"], ocorrencia["esperado_s2"])
    assert resultado["status_visual_dashboard"] == STATUS_POR_SAIDA[chave_status], "erro no status"

    combinacao = (
        f"{ocorrencia['risco_imediato']}"
        f"{ocorrencia['prazo_excedido']}"
        f"{ocorrencia['reincidencia_registrada']}"
    )
    combinacoes.add(combinacao)

    print(
        f"{numero:<5}{ocorrencia['id']:<8}{combinacao:<9}"
        f"{resultado['alerta_prioridade']:<4}{resultado['pendencia_critica']:<4}"
        f"{resultado['status_visual_dashboard']}"
    )

assert combinacoes == COMBINACOES_ESPERADAS, "combinacoes incorretas"

print("-" * 60)
print("Casos validados:", len(ocorrencias_simuladas))
print("Cobertura:", "000 a 111")
print("Todos os testes passaram.")
