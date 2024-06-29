import functions as fn
import revisiones as rev
import streamlit as st


acta_objeto_social = st.file_uploader("Acta Objeto Social", type="pdf")
texto_objeto_social = st.text_input("Pega aquí el objet social")

comparar = st.button("Comparar")

if comparar:
    try:
        bytes_acta_objeto_social = acta_objeto_social.getvalue()
        
        if fn.compare_objeto_social(bytes_acta_objeto_social, texto_objeto_social):
            st.success("El objeto social coincide")
        else:
            st.error("El objeto social no coincide")
    except:
        st.error("Error al comparar el objeto social")


