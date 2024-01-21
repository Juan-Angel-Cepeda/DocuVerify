import streamlit as st
import functions as fn


st.markdown("### Opinion SAT")
op_sat = st.file_uploader("D-32", type="pdf")

st.markdown("### Opinion Infonavit")
infonavit = st.file_uploader("Infonavit", type="pdf")

st.markdown("### Opinion IMSS")
imss = st.file_uploader("IMSS", type="pdf")

st.markdown("### Opinion Estatal")
op_est = st.file_uploader("Opinion Estatal", type="pdf")

revisar = st.button("Revisar")

if revisar:
    try:
        byte_op_sat = op_sat.getvalue()
        byte_infonavit = infonavit.getvalue()
        byte_imss = imss.getvalue()
        byte_op_est = op_est.getvalue()
        
        documentos = [byte_op_sat, byte_infonavit, byte_imss, byte_op_est]
        doc_en_imag = fn.convert_pdf_to_image(documentos)
        
        
        img_op_sat = doc_en_imag[0]
        img_infonavit = doc_en_imag[1]
        img_imss = doc_en_imag[2]
        img_op_est = doc_en_imag[3]
        
        
        infonavit_data = fn.search_and_decode(img_infonavit)
        imss_data = fn.search_and_decode(img_imss)
        op_sat_data = fn.search_and_decode(img_op_sat)
        
        rfc, razon_social = fn.proveedor_data(imss_data)
        
        st.markdown("## Razón Social o Nombre: {}".format(razon_social))
        st.markdown("## RFC: {}".format(rfc))
        
        #unas pruebas
        st.text(fn.check_op_est(img_op_est,rfc))
        
        if fn.check_op_sat(op_sat_data):
            st.success("SAT: Sin Adeudos y al corriente")
        else:
            st.error("SAT: Con Adeudos o no se encuentra al corriente")
        
        if fn.check_infonavit(infonavit_data):
            st.success("INFONAVIT: Sin Adeudos y al corriente")
        else:
            st.error("INFONAVIT: Con Adeudos o no se encuentra al corriente")                
        
        if fn.check_imss(imss_data):
            st.success("IMSS: Sin Adeudos y al corriente")
        else:
            st.error("IMSS: Con Adeudos o no se encuentra al corriente")
    
        st.success("Todo bien")
    
    except Exception as e:
        st.text(e)
        
    