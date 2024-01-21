import pdf2image as p2i
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
from datetime import datetime
import locale
from bs4 import BeautifulSoup
from selenium import webdriver
import pytesseract
import re
from selenium.webdriver.common.by import By
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    if ("SIN OPINION" in imss_data) or ("POSITIVA" in imss_data):
        return True
    else:
        return False

def proveedor_data(imss_data):
    try:
        rfc = imss_data.split("|")[6]
        nombre_razonsocial = imss_data.split("|")[7]
        rfc = rfc.split(":")[1]
        nombre_razonsocial = nombre_razonsocial.split(":")[1]
        return rfc.strip(), nombre_razonsocial.strip()
    except Exception as e:
        return e
        
def check_op_sat(op_sat_data):
    driver = webdriver.Chrome()
    driver.get(op_sat_data)
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, "html.parser")
    td_elemets = soup.find_all('td')
    #falta sacar la fecha de aqui paps
    if "Positivo" in td_elemets[8].text:
        return True
    else:
        return False

def check_op_est(imgs,rfc):
    texto = extract_text_from_image(imgs)
    folio = encontrar_folio_op_est(texto)
    yr, second_field, third_field, fourth_field = separar_campos(folio)
    alfa, fecha, homo = separar_rfc(rfc)
    return yr, second_field, third_field, fourth_field,alfa,fecha,homo
    #consultar_folio_navegador(yr, second_field, third_field, fourth_field)
  
def extract_text_from_image(imgs):
    try:
        text = []
        for img in imgs:
            img = img_to_numpy(img)
            gray_img = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
            _, th = cv2.threshold(gray_img, 230, 255, cv2.THRESH_BINARY)
            single_text = pytesseract.image_to_string(th)
            text.append(single_text)
        print(text)
        text = " ".join(text)
        return text
    except Exception as e:
        return e

def encontrar_folio_op_est(texto):
    patron_folio = re.compile(r'Folio : (\d+-\d+-\d+-\d+)')
    resultado = patron_folio.search(texto)
    if resultado:
        folio = resultado.group(1)
        return folio
    else:
        return False

def consultar_folio_navegador(yr, second_field, third_field, fourth_field,alfa,fecha,homo):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://ipagos.chihuahua.gob.mx/consultas/opobligfisc/")
    
    #ingresa el año
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[1]').clear()
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[1]').send_keys(yr)
    
    #ingresa el segundo campo
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[2]').clear()
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[2]').send_keys(second_field)
    
    #ingresa el tercer campo
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[3]').clear()
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[3]').send_keys(third_field)
    
    #ingresa el cuarto campo
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[4]').clear()
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[4]').send_keys(fourth_field)
    
    #ingresa el apha
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[5]').clear()
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[5]').send_keys(alfa)
    
    #ingresa la fecha
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[6]').clear()
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[6]').send_keys(fecha)
    
    #ingresa la homoclave
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[7]').clear()
    driver.find_element(By.XPATH,'//*[@id="Forma"]/input[7]').send_keys(homo)
    
    #consultar
    driver.find_element(By.XPATH,'//*[@id="botonForm"]').click()
    driver.implicitly_wait(2)
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup

def separar_campos(folio):
    try:
        yr = '2024'
        second_field = folio.split("-")[1]
        third_field = folio.split("-")[2]
        fourth_field = folio.split("-")[3]
        return yr, second_field, third_field, fourth_field
    except Exception as e:
        return e

def separar_rfc(rfc):
    if len(rfc) == 12:
        alfa = rfc[:3]
        fecha = rfc[3:9]
        homo = rfc[9:]
    elif len(rfc == 13):
        alfa = rfc[:4]
        fecha = rfc[4:10]
        homo = rfc[10:]
    else:
        raise ValueError('Longitud RFC incorrecta')
    return alfa, fecha, homo