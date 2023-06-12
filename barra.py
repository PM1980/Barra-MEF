import streamlit as st
import numpy as np


def calculate_displacements(coord, conec, kb, force_node, force_value, blocked_nodes):
    nn = coord.shape[0]
    nel = conec.shape[0]
    K = np.zeros((nn, nn))

    for i in range(nel):
        no1 = conec[i, 1]
        no2 = conec[i, 2]

        ke = np.array([[kb[i], -kb[i]], [-kb[i], kb[i]]])

        Kaux = np.zeros((nn, nn))
        Kaux[no1, no1] = ke[0, 0]
        Kaux[no1, no2] = ke[0, 1]
        Kaux[no2, no1] = ke[1, 0]
        Kaux[no2, no2] = ke[1, 1]

        K += Kaux

    F = np.zeros(nn)
    F[force_node] = force_value

    K_reduced = np.delete(K, blocked_nodes, axis=0)
    K_reduced = np.delete(K_reduced, blocked_nodes, axis=1)
    F_reduced = np.delete(F, blocked_nodes)

    sol = np.linalg.solve(K_reduced, F_reduced)

    xcomp = np.zeros(nn + 2)
    xcomp[1:-1] = sol

    return xcomp


def main():
    st.title("Análise de Estruturas")
    st.write("Informe as coordenadas, conectividades e restrições para análise da estrutura.")

    coord = st.text_area("Matriz de coordenadas (formato: linha por linha, separadas por espaço)")
    coord = np.fromstring(coord, sep=" ").reshape(-1, 3)

    conec = st.text_area("Matriz de conectividades (formato: linha por linha, separadas por espaço)")
    conec = np.fromstring(conec, sep=" ").reshape(-1, 3)

    kb = st.text_input("Constantes de rigidez (separadas por espaço)")
    kb = np.fromstring(kb, sep=" ")

    force_node = st.number_input("Nó onde a força será aplicada", value=4)
    force_value = st.number_input("Valor da força", value=5000)

    blocked_nodes = st.text_input("Nós bloqueados (separados por espaço)")
    blocked_nodes = np.fromstring(blocked_nodes, sep=" ", dtype=int)

    if st.button("Calcular"):
        xcomp = calculate_displacements(coord, conec, kb, force_node, force_value, blocked_nodes)
        st.write("Deslocamentos calculados:")
        st.write(xcomp)


if __name__ == "__main__":
    main()

