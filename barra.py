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

    st.subheader("Coordenadas")
    coord_table = st.table(np.zeros((4, 3)))  # Example initial table with 4 rows and 3 columns

    st.subheader("Conectividades")
    conec_table = st.table(np.zeros((3, 3)))  # Example initial table with 3 rows and 3 columns

    st.subheader("Constantes de Rigidez")
    kb_values = st.text_input("Valores das constantes de rigidez (separados por espaço)")

    force_node = st.number_input("Nó onde a força será aplicada", value=4)
    force_value = st.number_input("Valor da força", value=5000)

    blocked_nodes = st.text_input("Nós bloqueados (separados por espaço)")

    if st.button("Calcular"):
        coord = np.array(coord_table.data)
        conec = np.array(conec_table.data)
        kb = np.fromstring(kb_values, sep=" ")

        blocked_nodes = np.fromstring(blocked_nodes, sep=" ", dtype=int)

        xcomp = calculate_displacements(coord, conec, kb, force_node, force_value, blocked_nodes)
        st.write("Deslocamentos calculados:")
        st.write(xcomp)


if __name__ == "__main__":
    main()
