import time 
import subprocess
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import os
import argparse



class ReportBot:
    def __init__(self,nombreEmpresa:str,pathReport,userData:str,passData:str,cadenaConexion:str,dir_cookies:str):
        options=Options()
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--user-data-dir={}'.format(dir_cookies))    
        self.drive=webdriver.Edge(options=options)
        self.drive.get('http://reports.exikhan.com.mx/Reports')
        
        self.nombreEmpresa=nombreEmpresa
        self.pathReport=pathReport
        self.userData=userData
        self.passData=passData
        self.cadenaConexion=cadenaConexion
        self.nombreData=f"DataSource_{nombreEmpresa}"
        
        time.sleep(2)
        self.authenticarse()
        time.sleep(5)
        self.crearCarpetas()
        time.sleep(1)
        self.crearData()
        self.uploadReport()
        self.data_report()
        
        
    def authenticarse(self):
        subprocess.Popen('login.exe')
        
    def uploadReport(self):
        self.drive.find_element(by=By.LINK_TEXT,value=self.nombreEmpresa).click()
        time.sleep(1)
        archivos = os.listdir(self.pathReport)
        for archivo in archivos:
            btnupload = self.drive.find_element(by=By.XPATH,value="//*[@id='ui_btnUpload']")
            btnupload.click()
            time.sleep(1)
            btncargar=self.drive.find_element(by=By.XPATH,value="//input[@id='ui_fiImport']")
            btncargar.send_keys(f"{self.pathReport}\{archivo}")
            self.drive.implicitly_wait(2)
            self.drive.find_element(by=By.XPATH,value="//input[@id='ui_btnSaveImportCtrl']").click()
            time.sleep(1)
        
    def data_report(self):
        """ self.drive.find_element(by=By.XPATH,value=f"//a[@title='udemy']").click()
        time.sleep(1) """
        elementos=self.drive.find_elements(by=By.CLASS_NAME,value="msrs-UnSelectedItem")
        """ print(len(elementos)) """
        for i,e in enumerate(elementos):
            self.drive.find_element(by=By.XPATH,value=f"//*[@id='ui_a{i}']/tbody/tr/td[3]").click()
            self.drive.find_element(by=By.XPATH,value="//span[@class='msrs-menuItemLabelContainer' and text()='Administrar']").click()
            self.drive.find_element(by=By.XPATH,value="//*[@id='ui_form']/span/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[4]/td").click()
            self.drive.find_element(by=By.XPATH,value="//*[@id='ui_rdoSharedDataSourceDataSource_0']").click()
            self.drive.find_element(by=By.XPATH,value="//input[@id='ui_btnSharedFindDataSource_0']").click()
            time.sleep(1)
            inpDirr=self.drive.find_element(by=By.XPATH,value="//input[@id='ui_txtMpParent']")
            inpDirr.clear()
            inpDirr.send_keys(f"/{self.nombreData}/{self.nombreData}")
            time.sleep(1)
            self.drive.find_element(by=By.XPATH,value="//input[@id='ui_btnSave']").click()
            self.drive.find_element(by=By.XPATH,value="//*[@id='ui_form']/span/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr/td[2]/span/span/table/tbody/tr[4]/td[1]").click()
            time.sleep(1)
            self.drive.find_element(by=By.XPATH,value="//input[@id='ui_btnSaveDataSource']").click()
            self.drive.find_element(by=By.XPATH,value="/html/body/form/span/table/tbody/tr[1]/td/div/table[1]/tbody/tr/td[1]/span/div/a[2]").click()        
    
    def crearCarpetas(self):
        self.newCarpetas(self.nombreEmpresa)
        time.sleep(1)
        self.newCarpetas(self.nombreData)
    
    def crearData(self):
        self.drive.find_element(by=By.LINK_TEXT,value=self.nombreData).click()
        self.drive.find_element(by=By.XPATH,value="//*[@id='ui_btnNewDataSource']").click()
        time.sleep(1)
        self.drive.find_element(by=By.XPATH,value="//input[@id='ui_txtChooseName']").send_keys(self.nombreData)
        self.drive.find_element(by=By.ID,value="ui_txtConnectionString").send_keys(self.cadenaConexion)
        self.drive.find_element(by=By.ID,value="ui_rdoStored").click()
        self.drive.find_element(by=By.ID,value="ui_txtStoredName").send_keys(self.nombreData)
        self.drive.find_element(by=By.ID,value="ui_txtStoredPwd").send_keys(self.passData)
        self.drive.find_element(by=By.ID,value="ui_btnSave").click()
        self.drive.find_element(by=By.LINK_TEXT,value="Inicio").click()
        time.sleep(1)

        
    def newCarpetas(self,nombre:str):
        self.drive.find_element(by=By.XPATH,value="//*[@id='ui_form']/span/table/tbody/tr[2]/td/table/tbody/tr/td/span/table/tbody/tr/td/span/span/table/tbody/tr[2]/td/table/tbody/tr/td[2]").click()
        inpNom=self.drive.find_element(by=By.XPATH,value="//*[@id='ui_txtChooseName']")
        inpNom.clear()
        inpNom.send_keys(nombre)
        self.drive.find_element(by=By.XPATH,value="//*[@id='ui_btnSave']").click()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reporte")
    parser.add_argument("nombreEmpresa", type=str, help="nombreEmpresa")
    parser.add_argument("pathReport", type=str, help="pathReport")
    parser.add_argument("userData", type=str, help="userData")
    parser.add_argument("passData", type=str, help="passData")
    parser.add_argument("cadenaConexion", type=str, help="cadenaConexion")
    parser.add_argument("catalogo", type=str, help="catalogo")
    parser.add_argument("dir_cookies", type=str, help="dir_cookies")
    args = parser.parse_args()
    ReportBot(
        args.nombreEmpresa,
        args.pathReport,
        args.userData,
        args.passData,
        args.cadenaConexion.replace("*"," ")+';'+args.catalogo.replace("*"," "),
        args.dir_cookies
        )
