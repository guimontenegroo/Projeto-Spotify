
from servicos import (
    ARQUIVO_PADRAO,
    carregar_dados,
    criar_usuario,
    salvar_dados,
)

from catalogo import catalogo_padrao, propagandas_padrao

def escolher_musica(catalogo):
    for i, m in enumerate(catalogo, 1):
        print(f"{i} - {m.titulo} - {m.artista}")
    while True:
        numero = input("Numero da musica (0 para voltar): ")
        if numero == "0":
            return None
        if numero.isdigit() and 1 <= int(numero) <= len(catalogo):
            return catalogo[int(numero) - 1]
        print("Numero invalido.")


def escolher_perfil(usuarios, user):
    while user is None:
        nome = input("Nenhum perfil encontrado. Nome do novo perfil: ")
        try:
            user = criar_usuario(usuarios, nome)
        except ValueError as e:
            print(f"Erro: {e}")
    return user


def main():
    propagandas = propagandas_padrao()
    usuarios, catalogo, user = carregar_dados(ARQUIVO_PADRAO, catalogo_padrao())
    user = escolher_perfil(usuarios, user)
    salvar_dados(usuarios, catalogo, user.id_usuario)

    while True:
        print(f"\n=== MENU ({user.nome}) ===")
        print("1 - Ver musicas / Tocar")
        print("2 - Playlists")
        print("3 - Avaliacoes")
        print("0 - Sair")
        opcao = input("> ")

        if opcao == "1":
            musica = escolher_musica(catalogo)
            if musica:
                try:
                    print(musica.reproduzir())
                    musica.parar()
                except RuntimeError as e:
                    print(f"Erro: {e}")

        elif opcao == "2":
            print("1 - Criar playlist")
            print("2 - Tocar playlist")
            sub = input("> ")

            if sub == "1":
                try:
                    playlist = user.criar_playlist(input("Nome da playlist: "))
                    print(f"Playlist '{playlist.nome}' criada!")
                except ValueError as e:
                    print(f"Erro: {e}")
                else:
                    while True:
                        musica = escolher_musica(catalogo)
                        if musica is None:
                            break
                        try:
                            playlist.adicionar_faixa(musica)
                            salvar_dados(usuarios, catalogo, user.id_usuario)
                            print("Musica adicionada!")
                        except ValueError as e:
                            print(f"Erro: {e}")

            elif sub == "2":
                if not user.playlists:
                    print("Voce ainda nao possui playlists.")
                else:
                    for i, p in enumerate(user.playlists, 1):
                        print(f"{i} - {p.nome}")
                    numero = input("Numero da playlist: ")
                    if numero.isdigit() and 1 <= int(numero) <= len(user.playlists):
                        pl = user.playlists[int(numero) - 1]
                        try:
                            print(f"\n--- Reproduzindo Playlist: {pl.nome} ---")
                            for linha in pl.reproduzir(propagandas):
                                print(linha)
                        except (ValueError, RuntimeError) as e:
                            print(f"Erro: {e}")
                    else:
                        print("Numero invalido.")

        elif opcao == "3":
            musica = escolher_musica(catalogo)
            if musica:
                print(f"\n{musica.titulo} - Media: {musica.media_notas}")
                for a in musica.avaliacoes:
                    print(f"Nota {a.nota:g}: {a.comentario}")

                texto = input("\nNota de 1 a 5 (Enter para voltar): ")
                if texto != "":
                    try:
                        user.avaliar_musica(musica, texto, input("Comentario: "))
                        salvar_dados(usuarios, catalogo, user.id_usuario)
                        print("Avaliacao registrada!")
                    except ValueError as e:
                        print(f"Erro: {e}")

        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
