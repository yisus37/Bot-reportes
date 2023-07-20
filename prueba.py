from selenium import webdriver


drive=webdriver.Chrome()
drive.get("http://reports.exikhan.com.mx/reports")

    # Obtener los campos de entrada
try:
    # Esperar a que aparezca la alerta
    alert = drive.switch_to.alert.accept()
    print("hola")

except Exception as e:
    print("Error:", e)