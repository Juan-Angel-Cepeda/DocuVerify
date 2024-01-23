import pdf2image as p2i
import opencv-python as cv2

import pyzbar.pyzbar as pyzbar
import numpy as np
from datetime import datetime
import locale
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pytesseract
import re

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
        raise ValueError("Error de funcion proveedor data: {e}".format(e=e))
        
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
    try:
        texto = extract_text_from_image(imgs)
        folio = encontrar_folio_op_est(texto)

        print("Aqui esta el folio: ", folio)
        yr, second_field, third_field, fourth_field = separar_campos(folio)
        alfa, fecha, homo = separar_rfc(rfc)
        html_content = consultar_folio_navegador(yr,second_field,third_field,fourth_field,alfa,fecha,homo)
        #soup = BeautifulSoup(html_content,"html.parser")
        #span_state = soup.find('span',class_='state')
        #return span_state
        return True
    except:
        return False
    
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
        raise ValueError("Error desde extraer texto dese la imagen {e}".format(e=e))

def encontrar_folio_op_est(texto):
    texto = limpiar_ocr(texto)
    try:
        patron_folio = re.compile(r'(FOLIO:2024-\d+-\d+-\d+)')
        resultado = patron_folio.search(texto)
        if resultado:
            folio = resultado.group(1)
            return folio
    except Exception as e:
        raise ValueError("Error desde econtrar folio en texto extraido {e}".format(e=e))

def consultar_folio_navegador(yr, second_field, third_field, fourth_field,alfa,fecha,homo):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver,10)
    ipagos = "https://ipagos.chihuahua.gob.mx/consultas/opobligfisc/"
    
    print(yr, second_field, third_field, fourth_field,alfa,fecha,homo)
    try:
        driver.get(ipagos)

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
        wait.until(EC.url_changes(ipagos))
        wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="botonForm"]/span/br[5]')))
        html_content = driver.page_source
        return html_content
    except Exception as e:
        raise ValueError("Error desde interactuar con navegador, consultar folio navegador {e}".format(e=e))
    finally:
        driver.quit()


def separar_campos(folio):
    try:
        yr = '2024'
        folio = folio.replace("~","-")
        second_field = folio.split("-")[1]
        third_field = folio.split("-")[2]
        fourth_field = folio.split("-")[3]
        return yr, second_field, third_field, fourth_field
    except Exception as e:
        raise ValueError("Error desde separar campos del RFC op estatal {e}".format(e=e))

def separar_rfc(rfc):
    try:
        if len(rfc) == 12:
            alfa = rfc[:3]
            fecha = rfc[3:9]
            homo = rfc[9:]
        elif len(rfc == 13):
            alfa = rfc[:4]
            fecha = rfc[4:10]
            homo = rfc[10:]
        return alfa, fecha, homo
    except Exception as e:
        raise ValueError('Error en separar RFC en alfa fecha y homo {e}'.format(e=e))

def limpiar_ocr(texto):
    texto = texto.replace("O","0").replace("~","-").upper()
    texto = re.sub(r'[^a-zA-Z0-9-:]',"",texto)
    print(texto)
    return texto