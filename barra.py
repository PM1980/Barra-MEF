import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


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


def plot_structure(coord, conec, kb):
    fig, ax = plt.subplots()

    for i in range(conec.shape[0]):
        no1 = conec[i, 1]
        no2 = conec[i, 2]

        x = [coord[no1, 0], coord[no2, 0]]
        y = [coord[no1, 1], coord[no2, 1]]

        ax.plot(x, y, 'k-', linewidth=2)

        center_x = (coord[no1, 0] + coord[no2, 0]) / 2
        center_y = (coord[no1, 1] + coord[no2, 1]) / 2

        ax.text(center_x, center_y, f'k = {kb[i]}', ha='center', va='center')

    ax.scatter(coord[:, 0], coord[:, 1], color='red')

    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    ax.set_title('Geometria da Estrutura')

    st.pyplot(fig)


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

        plot_structure(coord, conec, kb)


if __name__ == "__main__":
    main()
