import pandas as pd

notas = pd.read_csv("ml-latest-small/ratings.csv")
notas.columns = ["usuarioId", "filmeId", "nota", "momento"]

notas_com_remocao_aleatoria = 0


# function that returns the notes of a user
def notas_do_usuario(usuario):
    salvar_notas_do_usuario = notas.query(f"usuarioId == {usuario}")
    salvar_notas_do_usuario = salvar_notas_do_usuario[["filmeId", "nota"]].set_index("filmeId")
    return salvar_notas_do_usuario


# function that returns how many notes a user has
def quantidade_de_notas_do_usuario(usuario):
    salvar_notas_do_usuario = notas.query(f"usuarioId == {usuario}")
    salvar_notas_do_usuario = salvar_notas_do_usuario[["filmeId", "nota"]].set_index("filmeId")
    return len(salvar_notas_do_usuario)


# function that returns the notes of a user but remove random notes given by a % of the total notes
def notas_do_usuario_com_remocao_aleatoria(usuario, porcentagem_de_remocao):
    salvar_notas_do_usuario = notas_do_usuario(usuario)
    salvar_notas_do_usuario = salvar_notas_do_usuario.sample(frac=porcentagem_de_remocao)
    return salvar_notas_do_usuario


# function that returns the notes off all users but remove random notes given by a % of the total notes and add the usuarioId, use pandas to store the notes and have a index biging with 0
# The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
def notas_de_todos_os_usuarios_com_remocao_aleatoria(porcentagem_de_remocao):
    notas_de_todos_os_usuarios = pd.DataFrame(columns=["usuarioId", "filmeId", "nota"])
    for usuario in notas.usuarioId.unique():
        notas_do_usuario_com_remocao = notas_do_usuario_com_remocao_aleatoria(usuario, porcentagem_de_remocao)
        notas_do_usuario_com_remocao["usuarioId"] = usuario
        notas_do_usuario_com_remocao.reset_index(inplace=True)
        notas_do_usuario_com_remocao.rename(columns={"index": "filmeId"}, inplace=True)
        notas_de_todos_os_usuarios = pd.concat([notas_de_todos_os_usuarios, notas_do_usuario_com_remocao])
    return notas_de_todos_os_usuarios


# given a pandas datframe generate a csv file
def gerar_csv_do_pandas(pandas_dataframe, nome_do_arquivo):
    pandas_dataframe.to_csv(nome_do_arquivo, index=False)


if __name__ == '__main__':
    # print(notas.head())
    # print(notas_do_usuario(1))
    # notas_do_usuario_com_remocao_aleatoria(1, 0.5)
    teste = notas_de_todos_os_usuarios_com_remocao_aleatoria(0.1)
    print(len(teste))
    print(len(notas))
    gerar_csv_do_pandas(teste, "teste_10.csv")
    # print(len(notas))
