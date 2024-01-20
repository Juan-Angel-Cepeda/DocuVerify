import streamlit as st
import functions as fn

st.markdown("### Constancia de Siutacion Fiscal")
csf = st.file_uploader("CSF", type="pdf")

st.markdown("### Opinion Infonavit")
infonavit = st.file_uploader("Infonavit", type="pdf")

st.markdown("### Opinion IMSS")
imss = st.file_uploader("IMSS", type="pdf")

st.markdown("### Opinion Estatal")
op_est = st.file_uploader("Opinion Estatal", type="pdf")

revisar = st.button("Revisar")

if revisar:
    try:
        byte_csf = csf.getvalue()
        byte_infonavit = infonavit.getvalue()
        byte_imss = imss.getvalue()
        byte_op_est = op_est.getvalue()
        
        documentos = [byte_csf, byte_infonavit, byte_imss, byte_op_est]
        doc_en_imag = fn.convert_pdf_to_image(documentos)
        
        
        img_csf = doc_en_imag[0]
        img_infonavit = doc_en_imag[1]
        img_imss = doc_en_imag[2]
        img_op_est = doc_en_imag[3]
        
        infonavit_data = fn.search_and_decode(img_infonavit)
        st.text(infonavit_data)
        st.success("Todo bien")
    
    except Exception as e:
        st.text(e)
        
    