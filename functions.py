import pdf2image as p2i
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

def convert_pdf_to_image(documentos):
    docus_en_imagenes = []
    try:
        for documento in documentos:
            file = documento
            imagenes = p2i.convert_from_bytes(file)
            docus_en_imagenes.append(imagenes)
        
        return docus_en_imagenes

    except Exception as e:
        raise e

def search_and_decode(img_doc):
    for img in img_doc:
        img = img_to_numpy(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        qr_codes = pyzbar.decode(gray)
        if qr_codes:
            qr_data = qr_codes[0].data.decode("utf-8")
            return qr_data

def img_to_numpy(img):
    img = np.array(img)
    return img