import json
import os
import shutil
from typing import List, Optional, Tuple
from usuario import Usuario
from musica import Musica

ARQUIVO_PADRAO = "dados.json"

def criar_usuario(usuarios: List[Usuario], nome: str) -> Usuario:
    nome = nome.strip()
    if any(u.nome.lower() == nome.lower() for u in usuarios):
        raise ValueError(f"Ja existe um perfil chamado '{nome}'.")
    novo_id = max((u.id_usuario for u in usuarios), default=0) + 1
    usuario = Usuario(novo_id, nome)
    usuarios.append(usuario)
    return usuario

def renomear_usuario(usuarios: List[Usuario], usuario: Usuario, novo_nome: str) -> None:
    novo_nome = novo_nome.strip()
    if any(u is not usuario and u.nome.lower() == novo_nome.lower() for u in usuarios):
        raise ValueError(f"Ja existe um perfil chamado '{novo_nome}'.")
    usuario.nome = novo_nome

def salvar_dados(
    usuarios: List[Usuario],
    catalogo: List[Musica],
    id_usuario_atual: Optional[int] = None,
    arquivo: str = ARQUIVO_PADRAO,
) -> bool:
    dados = {
        "id_usuario_atual": id_usuario_atual,
        "usuarios": [u.to_dict() for u in usuarios],
        "catalogo": [m.to_dict() for m in catalogo],
    }
    temporario = arquivo + ".tmp"
    try:
        with open(temporario, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        os.replace(temporario, arquivo)
        return True
    except OSError:
        return False

def mesclar_catalogo(
    catalogo: List[Musica], catalogo_base: Optional[List[Musica]]
) -> List[Musica]:
    if not catalogo_base:
        return catalogo
    existentes = {m.titulo.lower() for m in catalogo}
    catalogo.extend(m for m in catalogo_base if m.titulo.lower() not in existentes)
    return catalogo

def carregar_dados(
    arquivo: str = ARQUIVO_PADRAO,
    catalogo_base: Optional[List[Musica]] = None,
) -> Tuple[List[Usuario], List[Musica], Optional[Usuario]]:
    catalogo_base = catalogo_base or []
    if not os.path.exists(arquivo):
        return [], catalogo_base, None

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        catalogo = [Musica.from_dict(m) for m in dados.get("catalogo", [])]
        catalogo = mesclar_catalogo(catalogo, catalogo_base)
        usuarios = [Usuario.from_dict(u, catalogo) for u in dados.get("usuarios", [])]

        id_atual = dados.get("id_usuario_atual")
        usuario_atual = next((u for u in usuarios if u.id_usuario == id_atual), None)
        if usuario_atual is None and usuarios:
            usuario_atual = usuarios[0]
        return usuarios, catalogo, usuario_atual
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        try:
            shutil.copy(arquivo, arquivo + ".corrompido")
        except OSError:
            pass
        return [], catalogo_base, None
