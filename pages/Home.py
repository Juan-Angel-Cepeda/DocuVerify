import streamlit as st
import functions as fn
import revisiones as rev


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
        imagenes_op_est = rev.imagenes_opinion_estatal(byte_op_est)
        
        
        
        infonavit_data = rev.respuesta_qr_infonavit(byte_infonavit)
        imss_data = rev.respuesta_qr_imss(byte_imss)
        op_sat_data = rev.respuesta_qr_sat(byte_op_sat)
        
        
        rfc, razon_social = rev.informacion_del_proveedor(imss_data)
        
        st.markdown("## Razón Social o Nombre: {}".format(razon_social))
        st.markdown("## RFC: {}".format(rfc))
        
        #unas pruebas
        
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

        if fn.check_op_est(imagenes_op_est, rfc):
            st.success("ESTATAL: Verificación exitosa")
        else:
            st.error("ESTATAL: Verificación fallida")
    
    except Exception as e:
        st.text(e)