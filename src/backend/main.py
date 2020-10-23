from typing import *
from backend.planilha import Planilha
from backend.info_adicional import InformacaoAdicionalASerObtida
from backend.pessoa import Pessoa

nome_planilha: str = 'Testes'
numero_sheet: int = 0
linha_inicial: int = 3
linha_final: int = 5
coluna_nome: str = 'B'
coluna_email: str = 'C'
coluna_check: str = 'D'

infos_adicionais: List[InformacaoAdicionalASerObtida] = \
    []


def funcao_deve_enviar(_: Pessoa) -> bool:
    return True


nome_arquivo_resultado: str = 'teste bot arquivos'

planilha: Planilha = Planilha(nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nome, coluna_email, coluna_check,
                              infos_adicionais, funcao_deve_enviar)

mensagens: List[str] = ['Essa é uma mensagem de teste', 'C:\\Users\\rafae\\Pictures\\stickbug.jpg', '%CaminhoArquivo']

# Para testes
for pessoa in planilha.get_pessoas():
    print(pessoa)
