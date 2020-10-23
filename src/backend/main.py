from typing import *
from backend.planilha import Planilha
from backend.info_adicional import InformacaoAdicionalASerObtida
from backend.pessoa import Pessoa

nome_planilha: str = 'Teste bot'
numero_sheet: int = 0
linha_inicial: int = 4
linha_final: int = 4
coluna_nome: str = 'C'
coluna_numero: str = 'B'
coluna_check: str = 'E'

infos_adicionais: List[InformacaoAdicionalASerObtida] = \
    [InformacaoAdicionalASerObtida('D', 'CaminhoArquivo', lambda info, pessoa: info.valor)]


def funcao_deve_enviar(_: Pessoa) -> bool:
    return True


nome_arquivo_resultado: str = 'teste bot arquivos'

planilha: Planilha = Planilha(nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nome, coluna_numero, coluna_check,
                              infos_adicionais, funcao_deve_enviar)

mensagens: List[str] = ['Essa é uma mensagem de teste', 'C:\\Users\\rafae\\Pictures\\stickbug.jpg', '%CaminhoArquivo']
