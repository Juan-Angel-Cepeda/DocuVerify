import streamlit as st
import functions as fn
import revisiones as rv

st.markdown("### Opinion SAT")
opinion_sat_pdf = st.file_uploader("D-32", type="pdf")

st.markdown("### Opinion Infonavit")
opinion_infonavit_pdf = st.file_uploader("Infonavit", type="pdf")

st.markdown("### Opinion IMSS")
opinion_imss_pdf = st.file_uploader("IMSS", type="pdf")

st.markdown("### Opinion Estatal")
opinion_estatal_pdf = st.file_uploader("Opinion Estatal", type="pdf")
fecha_de_carga_del_proveedor = st.date_input("Ingresa la fecha de carga del proveedor")

revisar = st.button("Revisar")

if revisar:
    
    try:
        try:
            bytes_imss = opinion_imss_pdf.getvalue()
            rfc, razon_social = rv.informacion_del_proveedor(rv.respuesta_qr_imss(bytes_imss))
            st.markdown("## Razón Social o Nombre: {}".format(razon_social))
            st.markdown("## RFC: {}".format(rfc))
        except Exception as e:
            st.error('Error en extraer Información: {e}'.format(e=e))

        try:
            bytes_infonavit = opinion_infonavit_pdf.getvalue()
            informacion_qr_infonavit = rv.respuesta_qr_infonavit(bytes_infonavit)
        except Exception as e:
            st.error('Error {e}'.format(e=e))
        
        try:
            bytes_imss = opinion_imss_pdf.getvalue()
            informacion_qr_imss = rv.respuesta_qr_imss(bytes_imss)
        except Exception as e:
            st.error('Error {e}'.format(e=e))
        
        try:
            bytes_sat = opinion_sat_pdf.getvalue()
            informacion_qr_sat = rv.respuesta_qr_sat(bytes_sat)
        except Exception as e:
            st.error('Error {e}'.format(e=e))    
          
        try:      
            if fn.check_infonavit(informacion_qr_infonavit, fecha_de_carga_del_proveedor):
                st.success("INFONAVIT: Sin Adeudos y al corriente")
            else:
                st.error("INFONAVIT: Con Adeudos o no se encuentra al corriente")                
        except Exception as e:
            st.error('Error en verificación Opinion Infonavit: {e}'.format(e=e))
        
        try:
            if fn.check_imss(informacion_qr_imss,fecha_de_carga_del_proveedor):
                st.success("IMSS: Sin Adeudos y al corriente")
            else:
                st.error("IMSS: Con Adeudos o no se encuentra al corriente")
        except:
            st.error('Error en verificación Opinion IMSS')
            
        
        try:
            if fn.check_op_sat(informacion_qr_sat,fecha_de_carga_del_proveedor):
                st.success("SAT: Sin Adeudos y al corriente")
            else:
                st.error("SAT: Con Adeudos o no se encuentra al corriente")
        except:
            st.error('Error en verificación Opinion SAT')

        try:
            bytes_estatal = opinion_estatal_pdf.getvalue()
            imagenes_op_estatal = rv.imagenes_opinion_estatal(bytes_estatal)
            if fn.check_op_est(imagenes_op_estatal, rfc):
                st.success("ESTATAL: Verificación exitosa")
            else:
                st.error("ESTATAL: Verificación fallida")
        except:
            st.error('Error en verificación Opinion Estatal')
    
    except Exception as e:
        st.text(e)
        
