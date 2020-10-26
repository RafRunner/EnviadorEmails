from typing import *
from backend.pessoa import Pessoa

import re


email_regex = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")


def email_eh_invalido(email: str) -> bool:
    return email_regex.fullmatch(email) is None


def formata_nome(nome: str) -> str:
    return nome.lower().strip().title()


def formata_email(email: str) -> str:
    return email.strip()


def parse_verdadeiro_falso(valor: Any) -> bool:
    if isinstance(valor, (bool, int)):
        return bool(valor)

    valor_tratado: str = str(valor).lower().strip()

    if valor_tratado == 'sim' or valor_tratado == 's' or valor_tratado == 'verdadeiro' or valor_tratado == 'v' or valor_tratado == 'true' or valor_tratado == 't' or valor_tratado == '1':
        return True

    if valor_tratado == 'nao' or valor_tratado == 'não' or valor_tratado == 'n' or valor_tratado == 'falso' or valor_tratado == 'f' or valor_tratado == 'false' or valor_tratado == '0':
        return False

    return bool(valor_tratado)


def formatar_partes_em_email(email_origem:str, partes: List[str], pessoa: Pessoa) -> str:
    partes_formatadas: List[str] = []

    for parte in partes:
        parte_formatada = parte.replace('%nome', pessoa.nome)
        parte_formatada = parte_formatada.replace('%primeiro_nome', pessoa.primeiro_nome)

        if pessoa.infos_adicionais is not None:
            for info in pessoa.infos_adicionais:
                parte_formatada = parte.replace('%' + info.nome_info, info.get_substituicao(pessoa))

        partes_formatadas.append(parte_formatada)

    email_formatado: str = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'.format(email_origem, pessoa.email, partes_formatadas[0], '\n'.join(partes_formatadas[1:]))

    return email_formatado
