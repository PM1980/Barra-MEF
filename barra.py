import streamlit as st
import pandas as pd
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
    st.title("Structural Analysis")

    st.subheader("Upload Coordinates (coord)")
    coord_file = st.file_uploader("Upload CSV", type="csv")
    if coord_file is not None:
        coord_df = pd.read_csv(coord_file)
        st.write(coord_df)

    st.subheader("Upload Connectivities (conec)")
    conec_file = st.file_uploader("Upload CSV", type="csv")
    if conec_file is not None:
        conec_df = pd.read_csv(conec_file)
        st.write(conec_df)

    kb_values = st.text_input("Values of Stiffness Coefficients (separated by space)")
    force_node = st.number_input("Node where the force will be applied")
    force_value = st.number_input("Value of the force")

    blocked_nodes = st.text_input("Blocked Nodes (separated by space)")

    if st.button("Calculate"):
        if coord_file is None or conec_file is None:
            st.error("Please upload both coord and conec files.")
        else:
            coord = coord_df.values
            conec = conec_df.values
            kb = np.fromstring(kb_values, sep=" ")

            blocked_nodes = np.fromstring(blocked_nodes, sep=" ", dtype=int)

            xcomp = calculate_displacements(coord, conec, kb, force_node, force_value, blocked_nodes)
            st.write("Calculated Displacements:")
            st.write(xcomp)


if __name__ == "__main__":
    main()
