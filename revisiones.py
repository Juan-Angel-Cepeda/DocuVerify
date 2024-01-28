import functions as fn

def respuesta_qr_infonavit(bytes_infonavit):
    try:
        imagenes_infonavit = fn.convertir_bytes_a_imagenes(bytes_infonavit)
        respuesta_qr_infonavit = fn.search_and_decode(imagenes_infonavit)
        return respuesta_qr_infonavit
    
    except Exception as e:
        raise e

def respuesta_qr_imss(bytes_imss):
    try:
        imagenes_imss = fn.convertir_bytes_a_imagenes(bytes_imss)
        respuesta_qr_imss = fn.search_and_decode(imagenes_imss)
        return respuesta_qr_imss
    
    except Exception as e:
        raise e

def respuesta_qr_sat(bytes_sat):
    try:
        imagenes_sat = fn.convertir_bytes_a_imagenes(bytes_sat)
        respuesta_qr_sat = fn.search_and_decode(imagenes_sat)
        return respuesta_qr_sat
    
    except Exception as e:
        raise e

def imagenes_opinion_estatal(bytes_estatal):
    imagenes_estatal = fn.convertir_bytes_a_imagenes(bytes_estatal)
    return imagenes_estatal
    
def informacion_del_proveedor(respuesta_qr_imss):
    try:
        rfc, razon_social = fn.proveedor_data(respuesta_qr_imss)
        return rfc, razon_social
    except Exception as e:
        raise e