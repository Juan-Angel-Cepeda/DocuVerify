import pdf2image as p2i
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
from datetime import datetime
import locale
from bs4 import BeautifulSoup
from selenium import webdriver

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
    qr_codes = []
    for img in img_doc:
        img = img_to_numpy(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        qr_codes = pyzbar.decode(gray)
    
    if qr_codes:
        qr_data = qr_codes[0].data.decode("utf-8")
        return qr_data
    else:
        return "No se encontró código QR"

def img_to_numpy(img):
    img = np.array(img)
    return img

def check_infonavit(infonavit_data):
    
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    print(infonavit_data)
    try:
        process_line = infonavit_data.split("\n")[1]
        date= process_line.split(":")[1]
        emision = datetime.strptime(date, "%d/%B/%Y")
        delta_time = (datetime.now() - emision).days
    
        if ("Sin adeudos" in infonavit_data) and (delta_time < 30):
            return True, delta_time
        else:
            return False
    
    except Exception as e:
        return False

def check_imss(imss_data):
    print(imss_data)
    if ("SIN OPINION" in imss_data) or ("POSITIVA" in imss_data):
        return True
    else:
        return False

def proveedor_data(imss_data):
    try:
        RFC = imss_data.split(":")[12]
        print(RFC)
        Nombre_Razonsocial = imss_data.split(":")[8]
        print(Nombre_Razonsocial)
        return RFC, Nombre_Razonsocial
    except Exception as e:
        return e
        
def check_op_sat(op_sat_data):
    driver = webdriver.Chrome()
    driver.get(op_sat_data)
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, "html.parser")
    td_elemets = soup.find_all('td')
    if "Positivo" in td_elemets[8].text:
        return True
    else:
        return False
    #for td_element in td_elemets:
    #    print(td_element.text)
    