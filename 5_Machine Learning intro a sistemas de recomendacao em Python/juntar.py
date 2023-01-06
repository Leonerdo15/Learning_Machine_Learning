import numpy as np
import pandas as pd

filmes = pd.read_csv("ml-latest/movies.csv")
filmes.columns = ["filmeId", "titulo", "generos"]
filmes = filmes.set_index("filmeId")

notas_10 = pd.read_csv("teste_10.csv")
notas_20 = pd.read_csv("teste_20.csv")
notas_30 = pd.read_csv("teste_30.csv")
notas_40 = pd.read_csv("teste_40.csv")
notas = pd.read_csv("teste_50.csv")
notas_60 = pd.read_csv("teste_60.csv")
notas_70 = pd.read_csv("teste_70.csv")
notas_80 = pd.read_csv("teste_80.csv")
notas_90 = pd.read_csv("teste_90.csv")
notas_100 = pd.read_csv("teste_100.csv")


def distancia_vetores(a, b):
    return np.linalg.norm(a - b) / len(a)


def notas_do_usuario_completa(usuario):
    salvar_notas_do_usuario = notas_100.query(f"usuarioId == {usuario}")
    salvar_notas_do_usuario = salvar_notas_do_usuario[["filmeId", "nota"]].set_index("filmeId")
    return salvar_notas_do_usuario


def notas_do_usuario(usuario):
    salvar_notas_do_usuario = notas.query(f"usuarioId == {usuario}")
    salvar_notas_do_usuario = salvar_notas_do_usuario[["filmeId", "nota"]].set_index("filmeId")
    return salvar_notas_do_usuario


def distancia_de_usuarios(user1, user2, minimo=5):
    notas1 = notas_do_usuario(user1)
    notas2 = notas_do_usuario(user2)
    juncao = notas1.join(notas2, lsuffix="_esquerda", rsuffix="_direita").dropna()

    if len(juncao) < minimo:
        return None

    distancia = distancia_vetores(juncao["nota_esquerda"], juncao["nota_direita"])
    return [user1, user2, distancia]


def distancia_de_todos(voce_id, n=None):
    todos_os_usuarios = notas.usuarioId.unique()
    if n:
        todos_os_usuarios = todos_os_usuarios[:n]
    distancias = [distancia_de_usuarios(voce_id, usuariosId) for usuariosId in todos_os_usuarios]
    distancias = list(filter(None, distancias))
    distancias = pd.DataFrame(distancias, columns=["voce", "outra_pessoa", "distancia"])
    return distancias


def mais_proximos_de(voce_id, n_mais_proximos=10, n=None):
    distancias = distancia_de_todos(voce_id, n=n)
    distancias = distancias.sort_values("distancia")
    distancias = distancias.set_index("outra_pessoa").drop(voce_id)
    return distancias.head(n_mais_proximos)


def knn(voce_id, k_mais_proximos=10, n=None):
    distancias = distancia_de_todos(voce_id, n=n)
    distancias = distancias.sort_values("distancia")
    distancias = distancias.set_index("outra_pessoa").drop(voce_id, errors='ignore')
    return distancias.head(k_mais_proximos)


def sugere_para(voce, k_mais_proximos=10, n=None):
    notas_de_voce = notas_do_usuario(voce)
    filmes_que_voce_ja_viu = notas_de_voce.index

    similares = knn(voce, k_mais_proximos=k_mais_proximos, n=n)
    usuarios_similares = similares.index
    notas_dos_similares = notas.set_index("usuarioId").loc[usuarios_similares]
    recomendacoes = notas_dos_similares.groupby("filmeId").mean()[["nota"]]
    aparicoes = notas_dos_similares.groupby("filmeId").count()[['nota']]

    filtro_minimo = k_mais_proximos / 2
    recomendacoes = recomendacoes.join(aparicoes, lsuffix="_media_dos_usuarios", rsuffix="_aparicoes_nos_usuarios")
    recomendacoes = recomendacoes.query("nota_aparicoes_nos_usuarios >= %.2f" % filtro_minimo)
    recomendacoes = recomendacoes.sort_values("nota_media_dos_usuarios", ascending=False)
    recomendacoes = recomendacoes.drop(filmes_que_voce_ja_viu, errors='ignore')
    return recomendacoes.join(filmes)


if __name__ == '__main__':
    number_users = 600

    for i in range(1, number_users+1):
        user_id = i

        notas_user_completo = notas_do_usuario_completa(user_id)
        notas_user = notas_do_usuario(user_id)
        sugere_user = sugere_para(user_id, n=number_users)

        difrenca = notas_user_completo.index.difference(notas_user.index)

        # how many filmeId are in the sugere_user that are in difrenca
        if len(sugere_user.index.intersection(difrenca)) == 0:
            print(f"User {i} ->  \033[91m{len(sugere_user.index.intersection(difrenca))}\033[0m")
        else:
            print(f"User {i} ->  \033[92m{len(sugere_user.index.intersection(difrenca))}\033[0m")

        # Save the i and the len(sugere_user.index.intersection(difrenca)) in csv file
        with open(f'data1/result_50_K10_N{number_users}.csv', 'a') as f:
            f.write(f"{i},{len(sugere_user.index.intersection(difrenca))}\n")
