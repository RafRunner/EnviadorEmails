from typing import *
from backend.info_adicional import InformacaoAdicionalEspecifica


class Pessoa(object):

    def __init__(self, linha: int, nome: str, email: str, deve_enviar: bool, invalido: bool, infos_adicionais: List[InformacaoAdicionalEspecifica]):
        self.linha: int = linha
        self.nome: str = nome
        self.email: str = email
        self.deve_enviar: bool = deve_enviar
        self.invalido: bool = invalido
        self.infos_adicionais: List[InformacaoAdicionalEspecifica] = infos_adicionais

        self.primeiro_nome: str = nome.split()[0]

    def get_informacao_adicional(self, nome_informacao) -> Optional[InformacaoAdicionalEspecifica]:
        for info_especifica in self.infos_adicionais:
            if info_especifica.nome_info == nome_informacao:
                return info_especifica

        return None

    def __str__(self):
        return 'Linha: ' + str(self.linha) + '\nNome: ' + self.nome + '\nEmail: ' + self.email + '\nDeve enviar: ' + \
               str(self.deve_enviar) + '\nInvalido: ' + str(self.invalido)
