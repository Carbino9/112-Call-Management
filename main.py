import sys
import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6 import QtGui
from PyQt6 import QtCore

# Conectare la baza de date
def create_connection():
    conn = None
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=CLAUDIU\SQLEXPRESS;'
            'DATABASE=Serviciul 112;'
            'Trusted_Connection=yes;'
        )
        print("Conexiunea la baza de date a fost realizată cu succes!")
    except pyodbc.Error as e:
        print("Eroare la conectarea la baza de date:", e)
    return conn

# Verificarea credențialelor de conectare
def check_login(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Login WHERE Username=? AND Parola=?", (username, password))
    return cursor.fetchone() is not None

# Insert Apelant
def insert_apelant(conn, nume, prenume, varsta, cnp, adresa, localitate, sex):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Apelanti (Nume, Prenume, Varsta, CNP, Adresa, Localitate, Sex)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nume, prenume, varsta, cnp, adresa, localitate, sex))
    conn.commit()

# Update Apelant
def update_apelant(conn, cnp, nume, prenume, varsta, adresa, localitate, sex):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Apelanti
        SET Nume=?, Prenume=?, Varsta=?, Adresa=?, Localitate=?, Sex=?
        WHERE CNP=?
    """, (nume, prenume, varsta, adresa, localitate, sex, cnp))
    conn.commit()

# Stergere Apelant
def delete_apelant(conn, cnp):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Apelanti WHERE CNP=?", (cnp,))
    conn.commit()

# Preia datele apelanților din baza de date
def fetch_apelanti_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT Nume, Prenume, Varsta, CNP, Adresa, Localitate, Sex FROM Apelanti")
    return cursor.fetchall()

# Preia datele apelurilor din baza de date
def fetch_apeluri_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Apelant, Dispecer, DurataApel, DataApelului, 
               OraInitieriiApelului, MotivApel
        FROM Apeluri
    """)
    return cursor.fetchall()

# Preia datele dispecerilor din baza de date
def fetch_dispeceri_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Nume, Prenume, IncepereaServiciului, IncheiereaServiciului, 
               DataAngajarii, ApeluriPreluate, Sex, NumeSupervizor
        FROM Dispeceri
    """)
    return cursor.fetchall()

# Preia datele intervențiilor din baza de date
def fetch_interventii_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DataInterventiei, Dispecer, Incident, OraInceperiiInterventiei, 
               TipInterventie, CostInterventie, ConditiiMeteo, StatusInterventie
        FROM Interventii
    """)
    return cursor.fetchall()

# Preia datele incidentelor din baza de date
def fetch_incident_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Incident, Locatie, NumarVictime, ProcentDaune, Status
        FROM Incidente
    """)
    return cursor.fetchall()

# Preia datele echipajelor din baza de date
def fetch_echipaje_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Echipaj, ZonaDeAcoperire, IncepereaDisponibilitatii, IncheiereaDisponibilitatii, InterventiiRealizate
        FROM Echipaje
    """)
    return cursor.fetchall()

# Obține ID-ul echipajului pe baza numelui echipajului
def get_echipaj_id(conn, echipaj_name):
    cursor = conn.cursor()
    cursor.execute("SELECT EchipajID FROM Echipaje WHERE Echipaj=?", (echipaj_name,))
    result = cursor.fetchone()
    return result[0] if result else None

# Preia datele personalului din baza de date
def fetch_personal_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Echipaj, Nume, Prenume, Varsta, Specialitate, Sex
        FROM Personal_Echipaj
    """)
    return cursor.fetchall()

# Inserează personal în baza de date
def insert_personal(conn, nume, prenume, varsta, echipaj, echipaj_id, specialitate, sex):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Personal_Echipaj (Nume, Prenume, Varsta, Echipaj, EchipajID, Specialitate, Sex)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nume, prenume, varsta, echipaj, echipaj_id, specialitate, sex))
    conn.commit()

# Actualizează personal în baza de date
def update_personal(conn, nume, prenume, varsta, echipaj, echipaj_id, specialitate, sex):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Personal_Echipaj
        SET Varsta=?, Echipaj=?, EchipajID=?, Specialitate=?, Sex=?
        WHERE Nume=? AND Prenume=?
    """, (varsta, echipaj, echipaj_id, specialitate, sex, nume, prenume))
    conn.commit()

# Șterge personal din baza de date
def delete_personal(conn, nume, prenume):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Personal_Echipaj WHERE Nume=? AND Prenume=?", (nume, prenume))
    conn.commit()

# Preia datele intervențiilor echipajelor din baza de date
def fetch_interventii_echipaje_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DataInterventiei, Echipaj, OraSosiriilaIncident, DurataInterventiei, NumarUtilaje, StatusEchipaj, EvaluarePerformanta
        FROM Interventii_Echipaje
    """)
    return cursor.fetchall()

# Aplicația principală
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('login.ui', self)
        self.pushButton.clicked.connect(self.handle_login)
        self.show()

    # Gestionarea login-ului
    def handle_login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if check_login(connection, username, password):
            print("Login successful")
            self.load_main_page()
        else:
            print("Login failed")

    # Încărcarea paginii principale
    def load_main_page(self):
        self.main_window = QtWidgets.QMainWindow()
        uic.loadUi('main.ui', self.main_window)
        self.main_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.load_apelanti_page)
        self.main_window.findChild(QtWidgets.QPushButton, 'pushButton_2').clicked.connect(self.load_apeluri_page)
        self.main_window.findChild(QtWidgets.QPushButton, 'pushButton_3').clicked.connect(self.load_dispeceri_page)
        self.main_window.findChild(QtWidgets.QPushButton, 'pushButton_4').clicked.connect(self.load_interventii_page)
        self.main_window.findChild(QtWidgets.QPushButton, 'pushButton_5').clicked.connect(self.load_incident_page)
        self.main_window.findChild(QtWidgets.QPushButton, 'pushButton_6').clicked.connect(self.load_echipaje_page)
        self.main_window.findChild(QtWidgets.QPushButton, 'pushButton_7').clicked.connect(self.load_personal_page)
        self.main_window.findChild(QtWidgets.QPushButton, 'pushButton_8').clicked.connect(self.load_interventii_echipaje_page)
        self.main_window.show()
        self.close()

    # Încărcarea paginii Apelanti
    def load_apelanti_page(self):
        self.apelanti_window = QtWidgets.QMainWindow()
        uic.loadUi('Apelanti.ui', self.apelanti_window)
        self.apelanti_window.findChild(QtWidgets.QPushButton, 'pushButton_4').clicked.connect(self.load_main_page_from_apelanti)
        self.apelanti_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.insert_apelant)
        self.apelanti_window.findChild(QtWidgets.QPushButton, 'pushButton_2').clicked.connect(self.update_apelant)
        self.apelanti_window.findChild(QtWidgets.QPushButton, 'pushButton_3').clicked.connect(self.delete_apelant)
        self.populate_apelanti_list()
        self.execute_apelanti_query()
        self.apelanti_window.show()
        self.main_window.close()

    # Întoarcerea la pagina principală din pagina Apelanti
    def load_main_page_from_apelanti(self):
        self.main_window.show()
        self.apelanti_window.close()

    # Populează lista apelanților
    def populate_apelanti_list(self):
        table_view = self.apelanti_window.findChild(QtWidgets.QTableView, 'tableView')
        data = fetch_apelanti_data(connection)
        headers = ["Nume", "Prenume", "Varsta", "CNP", "Adresa", "Localitate", "Sex"]
        model = QtGui.QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Afișează un mesaj de avertizare
    def show_warning(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec()

    # Validează datele apelantului
    def validate_apelant_data(self, nume, prenume, varsta, cnp, adresa, localitate, sex):
        if not nume:
            self.show_warning("Numele este obligatoriu.")
            return False
        if not prenume:
            self.show_warning("Prenumele este obligatoriu.")
            return False
        if not varsta.isdigit():
            self.show_warning("Vârsta trebuie să fie un număr.")
            return False
        if not cnp.isdigit() or len(cnp) != 13:
            self.show_warning("CNP trebuie să fie un număr din 13 cifre.")
            return False
        if not adresa:
            self.show_warning("Adresa este obligatorie.")
            return False
        if not localitate:
            self.show_warning("Localitatea este obligatorie.")
            return False
        if sex and sex not in ["M", "F"]:
            self.show_warning("Sexul trebuie să fie 'M' sau 'F'.")
            return False
        return True

    # Validează datele personalului
    def validate_personal_data(self, nume, prenume, varsta, echipaj, specialitate, sex):
        if not nume:
            self.show_warning("Numele este obligatoriu.")
            return False
        if not prenume:
            self.show_warning("Prenumele este obligatoriu.")
            return False
        if not varsta.isdigit():
            self.show_warning("Vârsta trebuie să fie un număr.")
            return False
        if not echipaj:
            self.show_warning("Echipajul este obligatoriu.")
            return False
        if not specialitate:
            self.show_warning("Specialitatea este obligatorie.")
            return False
        if sex and sex not in ["M", "F"]:
            self.show_warning("Sexul trebuie să fie 'M' sau 'F'.")
            return False
        return True

    # Inserează un apelant
    def insert_apelant(self):
        nume = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit').text()
        prenume = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_2').text()
        varsta = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_3').text()
        cnp = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_4').text()
        adresa = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_5').text()
        localitate = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_6').text()
        sex = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_7').text()

        if sex == "":
            sex = None

        if self.validate_apelant_data(nume, prenume, varsta, cnp, adresa, localitate, sex):
            insert_apelant(connection, nume, prenume, varsta, cnp, adresa, localitate, sex)
            self.populate_apelanti_list()

    # Actualizează un apelant
    def update_apelant(self):
        cnp = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_8').text()
        nume = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_9').text()
        prenume = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_10').text()
        varsta = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_11').text()
        adresa = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_12').text()
        localitate = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_13').text()
        sex = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_14').text()

        if sex == "":
            sex = None

        if self.validate_apelant_data(nume, prenume, varsta, cnp, adresa, localitate, sex):
            update_apelant(connection, cnp, nume, prenume, varsta, adresa, localitate, sex)
            self.populate_apelanti_list()

    # Șterge un apelant
    def delete_apelant(self):
        cnp = self.apelanti_window.findChild(QtWidgets.QLineEdit, 'lineEdit_15').text()
        if not cnp.isdigit() or len(cnp) != 13:
            self.show_warning("CNP-ul trebuie să fie un număr din 13 cifre.")
            return
        delete_apelant(connection, cnp)
        self.populate_apelanti_list()

    # Încărcarea paginii Apeluri
    def load_apeluri_page(self):
        self.apeluri_window = QtWidgets.QMainWindow()
        uic.loadUi('Apeluri.ui', self.apeluri_window)
        self.apeluri_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.load_main_page_from_apeluri)
        self.populate_apeluri_list()
        self.execute_apeluri_query()
        self.apeluri_window.show()
        self.main_window.close()

    # Întoarcerea la pagina principală din pagina Apeluri
    def load_main_page_from_apeluri(self):
        self.main_window.show()
        self.apeluri_window.close()

    # Populează lista apelurilor    
    def populate_apeluri_list(self):
        table_view = self.apeluri_window.findChild(QtWidgets.QTableView, 'tableView')
        data = fetch_apeluri_data(connection)
        headers = ["Apelant", "Dispecer", "Durată apel", "Data apelului", "Ora inițierii apelului", "Motiv apel"]
        model = QtGui.QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Creează o nouă fereastră pentru pagina Dispeceri
    def load_dispeceri_page(self):
        self.dispeceri_window = QtWidgets.QMainWindow()
        uic.loadUi('Dispeceri.ui', self.dispeceri_window)
        self.dispeceri_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.load_main_page_from_dispeceri)
        
        combo_box = self.dispeceri_window.findChild(QtWidgets.QComboBox, 'comboBox')
        combo_box.currentIndexChanged.connect(self.execute_dispeceri_query)

        self.populate_dispeceri_combobox()
        self.populate_dispeceri_list()
        self.dispeceri_window.show()
        self.main_window.close()

    # Întoarcerea la pagina principală din pagina Dispeceri
    def load_main_page_from_dispeceri(self):
        self.main_window.show()
        self.dispeceri_window.close()

    # Populează lista dispecerilor
    def populate_dispeceri_list(self):
        table_view = self.dispeceri_window.findChild(QtWidgets.QTableView, 'tableView')
        data = fetch_dispeceri_data(connection)
        headers = ["Nume", "Prenume", "Începerea serviciului", "Încheierea serviciului", "Data angajării", "Apeluri preluate", "Sex", "Nume supervizor"]
        model = QtGui.QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Creează o nouă fereastră pentru pagina Intervenții
    def load_interventii_page(self):
        self.interventii_window = QtWidgets.QMainWindow()
        uic.loadUi('Interventii.ui', self.interventii_window)
        self.interventii_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.load_main_page_from_interventii)
        self.populate_interventii_list()
        self.execute_interventii_query()
        self.interventii_window.show()
        self.main_window.close()

    # Întoarcerea la pagina principală din pagina Intervenții
    def load_main_page_from_interventii(self):
        self.main_window.show()
        self.interventii_window.close()

    # Populează lista intervențiilor
    def populate_interventii_list(self):
        table_view = self.interventii_window.findChild(QtWidgets.QTableView, 'tableView')
        data = fetch_interventii_data(connection)
        headers = ["Data intervenției", "Dispecer", "Incident", "Ora începerii intervenției", "Tip intervenție", "Cost intervenție", "Condiții meteo", "Status intervenție"]
        model = QtGui.QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Încărcarea paginii Incident
    def load_incident_page(self):
        self.incident_window = QtWidgets.QMainWindow()
        uic.loadUi('Incident.ui', self.incident_window)
        self.incident_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.load_main_page_from_incident)

        combo_box = self.incident_window.findChild(QtWidgets.QComboBox, 'comboBox')
        combo_box.currentIndexChanged.connect(self.execute_incident_query)

        self.populate_procentdaune_combobox()
        self.populate_incident_list()
        self.execute_incident_query2()
        self.incident_window.show()
        self.main_window.close()

    # Populează lista procentelor de daune
    def populate_procentdaune_combobox(self):
        combo_box = self.incident_window.findChild(QtWidgets.QComboBox, 'comboBox')
        for i in range(0, 101, 10):
            combo_box.addItem(str(i))

    # Întoarcerea la pagina principală din pagina Incident
    def load_main_page_from_incident(self):
        self.main_window.show()
        self.incident_window.close()

    # Populează lista incidentelor
    def populate_incident_list(self):
        table_view = self.incident_window.findChild(QtWidgets.QTableView, 'tableView')
        data = fetch_incident_data(connection)
        headers = ["Incident", "Locație", "Număr Victime", "Procent Daune", "Status"]
        model = QtGui.QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea 2 pentru pagina echipaje
    def execute_echipaje_query2(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                e.Echipaj,
                COUNT(pe.PersonalID) AS NumarMembri
            FROM 
                Echipaje e
            JOIN 
                Personal_Echipaj pe ON e.EchipajID = pe.EchipajID
            WHERE 
                e.EchipajID IN (
                    SELECT 
                        ie.EchipajID
                    FROM 
                        Interventii_Echipaje ie
                    JOIN 
                        Interventii i ON ie.InterventieID = i.InterventieID
                    WHERE 
                        i.CostInterventie > (
                            SELECT 
                                AVG(CostInterventie)
                            FROM 
                                Interventii
                        )
                )
            GROUP BY 
                e.Echipaj
        """)
        results = cursor.fetchall()

        table_view = self.echipaje_window.findChild(QtWidgets.QTableView, 'tableView_3')
        if table_view is None:
            print("Error: 'tableView_3' not found in 'Echipaje.ui'")
            return

        headers = ["Echipaj", "Număr membri"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Încărcarea paginii Echipaje
    def load_echipaje_page(self):
        self.echipaje_window = QtWidgets.QMainWindow()
        uic.loadUi('Echipaje.ui', self.echipaje_window)
        self.echipaje_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.load_main_page_from_echipaje)
        self.populate_echipaje_list()
        self.execute_echipaje_query()
        self.execute_echipaje_query2() 
        self.echipaje_window.show()
        self.main_window.close()

    # Întoarcerea la pagina principală din pagina Echipaje  
    def load_main_page_from_echipaje(self):
        self.main_window.show()
        self.echipaje_window.close()


    # Populează lista echipajelor
    def populate_echipaje_list(self):
        table_view = self.echipaje_window.findChild(QtWidgets.QTableView, 'tableView')
        data = fetch_echipaje_data(connection)
        headers = ["Echipaj", "Zona De Acoperire", "Începerea Disponibilității", "Încheierea Disponibilității", "Intervenții Realizate"]
        model = QtGui.QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Încărcarea paginii Personal
    def load_personal_page(self):
        self.personal_window = QtWidgets.QMainWindow()
        uic.loadUi('Personal.ui', self.personal_window)
        self.personal_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.load_main_page_from_personal)
        self.personal_window.findChild(QtWidgets.QPushButton, 'pushButton_2').clicked.connect(self.insert_personal)
        self.personal_window.findChild(QtWidgets.QPushButton, 'pushButton_3').clicked.connect(self.update_personal)
        self.personal_window.findChild(QtWidgets.QPushButton, 'pushButton_4').clicked.connect(self.delete_personal)
        self.populate_personal_list()
        self.execute_personal_query()
        self.personal_window.show()
        self.main_window.close()

    # Întoarcerea la pagina principală din pagina Personal
    def load_main_page_from_personal(self):
        self.main_window.show()
        self.personal_window.close()

    # Populează lista personalului
    def populate_personal_list(self):
        table_view = self.personal_window.findChild(QtWidgets.QTableView, 'tableView')
        data = fetch_personal_data(connection)
        headers = ["Echipaj", "Nume", "Prenume", "Vârstă", "Specialitate", "Sex"]
        model = QtGui.QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Inserarea unui nou personal
    def insert_personal(self):
        nume = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit').text()
        prenume = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_2').text()
        varsta = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_3').text()
        echipaj = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_4').text()
        specialitate = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_5').text()
        sex = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_6').text() or None

        if self.validate_personal_data(nume, prenume, varsta, echipaj, specialitate, sex):
            echipaj_id = get_echipaj_id(connection, echipaj)
            if echipaj_id is None:
                self.show_warning("Echipajul specificat nu există.")
                return
            print(f"EchipajID: {echipaj_id}")
            insert_personal(connection, nume, prenume, varsta, echipaj, echipaj_id, specialitate, sex)
            self.populate_personal_list()

    # Actualizarea unui personal
    def update_personal(self):
        nume = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_7').text()
        prenume = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_8').text()
        varsta = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_9').text()
        echipaj = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_10').text()
        specialitate = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_11').text()
        sex = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_12').text() or None

        if self.validate_personal_data(nume, prenume, varsta, echipaj, specialitate, sex):
            echipaj_id = get_echipaj_id(connection, echipaj)
            if echipaj_id is None:
                self.show_warning("Echipajul specificat nu există.")
                return
            update_personal(connection, nume, prenume, varsta, echipaj, echipaj_id, specialitate, sex)
        self.populate_personal_list()

    # Șterge un personal
    def delete_personal(self):
        nume = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_13').text()
        prenume = self.personal_window.findChild(QtWidgets.QLineEdit, 'lineEdit_14').text()

        if not nume or not prenume:
            self.show_warning("Numele și Prenumele sunt necesare pentru ștergere.")
            return

        delete_personal(connection, nume, prenume)
        self.populate_personal_list()

    # Încărcarea paginii Interventii_Echipaje
    def load_interventii_echipaje_page(self):
        self.interventii_echipaje_window = QtWidgets.QMainWindow()
        uic.loadUi('Interventii_Echipaje.ui', self.interventii_echipaje_window)
        self.interventii_echipaje_window.findChild(QtWidgets.QPushButton, 'pushButton').clicked.connect(self.load_main_page_from_interventii_echipaje)
        self.populate_interventii_echipaje_list()
        self.execute_interventii_echipaje_query()
        self.interventii_echipaje_window.show()
        self.main_window.close()

    # Întoarcerea la pagina principală din pagina Interventii_Echipaje
    def load_main_page_from_interventii_echipaje(self):
        self.main_window.show()
        self.interventii_echipaje_window.close()

    # Populează lista intervențiilor echipajelor
    def populate_interventii_echipaje_list(self):
        table_view = self.interventii_echipaje_window.findChild(QtWidgets.QTableView, 'tableView')
        data = fetch_interventii_echipaje_data(connection)
        headers = ["Data intervenției", "Echipaj", "Ora sosirii la incident", "Durata intervenției", "Număr utilaje", "Status echipaj", "Evaluare performanță"]
        model = QtGui.QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Populează combobox-ul cu dispeceri
    def populate_dispeceri_combobox(self):
        combo_box = self.dispeceri_window.findChild(QtWidgets.QComboBox, 'comboBox')
        cursor = connection.cursor()
        cursor.execute("SELECT Nume, Prenume FROM Dispeceri")
        dispeceri = cursor.fetchall()
        for dispecer in dispeceri:
            combo_box.addItem(f"{dispecer[0]} {dispecer[1]}")

    # Execută interogarea pentru pagina Dispeceri
    def execute_dispeceri_query(self):
        combo_box = self.dispeceri_window.findChild(QtWidgets.QComboBox, 'comboBox')
        selected_dispecer = combo_box.currentText()
        if not selected_dispecer:
            self.show_warning("Selectați un dispecer.")
            return

        nume, prenume = selected_dispecer.split(' ')
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                Dispeceri.Nume + ' ' + Dispeceri.Prenume AS NumeDispecer,
                Interventii.TipInterventie,
                COUNT(Interventii_Echipaje.EchipajID) AS NumarEchipajeImplicate
            FROM 
                Interventii
            INNER JOIN 
                Dispeceri ON Interventii.DispecerID = Dispeceri.DispecerID
            INNER JOIN 
                Interventii_Echipaje ON Interventii.InterventieID = Interventii_Echipaje.InterventieID
            WHERE 
                Dispeceri.Nume = ? AND Dispeceri.Prenume = ?
            GROUP BY
                Dispeceri.Nume, 
                Dispeceri.Prenume, 
                Interventii.TipInterventie
        """, (nume, prenume))
        results = cursor.fetchall()

        table_view = self.dispeceri_window.findChild(QtWidgets.QTableView, 'tableView_2')
        headers = ["Nume dispecer", "Tip intervenție", "Număr echipaje implicate"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea pentru pagina Apelanți
    def execute_apelanti_query(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                Apelanti.Nume + ' ' + Apelanti.Prenume AS NumeApelant,
                Apelanti.Varsta as VarstaApelant,
                Apeluri.MotivApel,
                Dispeceri.Nume + ' ' + Dispeceri.Prenume AS NumeDispecer
            FROM 
                Apeluri
            INNER JOIN 
                Apelanti ON Apeluri.ApelantID = Apelanti.ApelantID
            INNER JOIN 
                Dispeceri ON Apeluri.DispecerID = Dispeceri.DispecerID
            WHERE 
                Dispeceri.ApeluriPreluate >= 100
        """)
        results = cursor.fetchall()

        table_view = self.apelanti_window.findChild(QtWidgets.QTableView, 'tableView_2')
        headers = ["Nume Apelant", "Vârstă Apelant", "Motiv apel", "Nume dispecer"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea pentru pagina Personal_Echipaj
    def execute_personal_query(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                Personal_Echipaj.Nume + ' ' + Personal_Echipaj.Prenume AS NumePersonal,
                Echipaje.ZonaDeAcoperire,
                Echipaje.Echipaj,
                COUNT(Interventii_Echipaje.InterventieID) AS NumarInterventii
            FROM 
                Personal_Echipaj
            INNER JOIN 
                Echipaje ON Personal_Echipaj.EchipajID = Echipaje.EchipajID
            INNER JOIN 
                Interventii_Echipaje ON Echipaje.EchipajID = Interventii_Echipaje.EchipajID
            GROUP BY 
                Personal_Echipaj.Nume, 
                Personal_Echipaj.Prenume, 
                Echipaje.ZonaDeAcoperire,
                Echipaje.Echipaj
            HAVING 
                COUNT(Interventii_Echipaje.InterventieID) >= 2
        """)
        results = cursor.fetchall()

        table_view = self.personal_window.findChild(QtWidgets.QTableView, 'tableView_2')
        headers = ["Nume personal", "Zona de acoperire", "Echipaj", "Număr intervenții"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea pentru pagina Interventii
    def execute_interventii_query(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                Interventii.DataInterventiei,
                Interventii.Incident,
                Dispeceri.Nume + ' ' + Dispeceri.Prenume AS NumeDispecer,
                Incidente.Locatie
            FROM 
                Interventii
            INNER JOIN 
                Dispeceri ON Interventii.DispecerID = Dispeceri.DispecerID
            INNER JOIN 
                Incidente ON Interventii.IncidentID = Incidente.IncidentID
            WHERE 
                Incidente.NumarVictime < 3
        """)
        results = cursor.fetchall()

        table_view = self.interventii_window.findChild(QtWidgets.QTableView, 'tableView_2')
        headers = ["Data intervenției", "Incident", "Nume dispecer", "Locație"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea pentru pagina Incident
    def execute_incident_query(self):
        combo_box = self.incident_window.findChild(QtWidgets.QComboBox, 'comboBox')
        selected_procentdaune = combo_box.currentText()
        if not selected_procentdaune:
            self.show_warning("Selectați un procent de daune.")
            return

        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                i.Incident,
                i.Locatie,
                i.NumarVictime
            FROM 
                Incidente i
            WHERE 
                i.IncidentID IN (
                    SELECT 
                        IncidentID
                    FROM 
                        Incidente
                    WHERE 
                        NumarVictime > (
                            SELECT 
                                AVG(NumarVictime)
                            FROM 
                                Incidente
                        )
                )
            AND 
                i.IncidentID IN (
                    SELECT 
                        IncidentID
                    FROM 
                        Incidente
                    WHERE 
                        ProcentDaune > ?
                )
        """, (selected_procentdaune,))
        results = cursor.fetchall()

        table_view = self.incident_window.findChild(QtWidgets.QTableView, 'tableView_3')

        headers = ["Incident", "Locație", "Număr victime"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea pentru pagina Echipaje
    def execute_echipaje_query(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                Echipaje.Echipaj,
                Interventii_Echipaje.DataInterventiei AS DataInterventiei,
                Interventii_Echipaje.EvaluarePerformanta,
                AVG(Personal_Echipaj.Varsta) AS VarstaMedie
            FROM 
                Echipaje
            INNER JOIN 
                Interventii_Echipaje ON Echipaje.EchipajID = Interventii_Echipaje.EchipajID
            INNER JOIN 
                Personal_Echipaj ON Echipaje.EchipajID = Personal_Echipaj.EchipajID
            WHERE 
                Interventii_Echipaje.EvaluarePerformanta >= 9
            GROUP BY 
                Echipaje.Echipaj, 
                Interventii_Echipaje.DataInterventiei,
                Interventii_Echipaje.EvaluarePerformanta
            HAVING 
                AVG(Interventii_Echipaje.EvaluarePerformanta) >= 9 AND COUNT(Personal_Echipaj.EchipajID) >= 2
        """)
        results = cursor.fetchall()

        table_view = self.echipaje_window.findChild(QtWidgets.QTableView, 'tableView_2')

        headers = ["Echipaj", "Data intervenției", "Evaluare performanță", "Vârstă medie"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea pentru pagina Apeluri
    def execute_apeluri_query(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                a.DataApelului, 
                ap.Nume + ' ' + ap.Prenume AS Apelant, 
                d.Nume + ' ' + d.Prenume AS Dispecer
            FROM 
                Apeluri a
            JOIN 
                Apelanti ap ON a.ApelantID = ap.ApelantID
            JOIN 
                Dispeceri d ON a.DispecerID = d.DispecerID
            WHERE 
                ap.Varsta > (
                    SELECT 
                        AVG(Varsta) 
                    FROM 
                        Apelanti
                )
                AND d.DispecerID IN (
                    SELECT 
                        DispecerID 
                    FROM 
                        Interventii
                    GROUP BY 
                        DispecerID
                    HAVING 
                        COUNT(*) >= 2
                )
        """)
        results = cursor.fetchall()

        table_view = self.apeluri_window.findChild(QtWidgets.QTableView, 'tableView_2')

        headers = ["Data apelului", "Apelant", "Dispecer"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea pentru Interventii_Echipaje
    def execute_interventii_echipaje_query(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                i.DataInterventiei,
                ie.DurataInterventiei,
                COUNT(ie.EchipajID) AS NumarEchipaje
            FROM 
                Interventii_Echipaje ie
            JOIN 
                Interventii i ON ie.InterventieID = i.InterventieID
            WHERE 
                ie.InterventieID = (
                    SELECT TOP 1
                        ie1.InterventieID
                    FROM 
                        Interventii_Echipaje ie1
                    WHERE 
                        ie1.InterventieID IN (
                            SELECT 
                                InterventieID
                            FROM 
                                Interventii_Echipaje
                            GROUP BY 
                                InterventieID
                            HAVING 
                                COUNT(DISTINCT EchipajID) >= 2
                        )
                    ORDER BY 
                        ie1.DurataInterventiei DESC
                )
            GROUP BY
                i.DataInterventiei, 
                ie.DurataInterventiei
        """)
        results = cursor.fetchall()

        table_view = self.interventii_echipaje_window.findChild(QtWidgets.QTableView, 'tableView_2')

        headers = ["Data intervenției", "Durata intervenției", "Număr echipaje"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

    # Execută interogarea pentru pagina Incidente
    def execute_incident_query2(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                i.Incident,
                i.Locatie,
                i.NumarVictime,
                i.ProcentDaune,
                i.Status
            FROM
                Incidente i
            JOIN
                Interventii iv ON i.IncidentID = iv.IncidentID
            JOIN
                Interventii_Echipaje ie ON iv.InterventieID = ie.InterventieID
            GROUP BY
                i.Incident, i.Locatie, i.NumarVictime, i.ProcentDaune, i.Status
            HAVING
                i.ProcentDaune > 30 AND COUNT(DISTINCT ie.EchipajID) >= 2
        """)
        results = cursor.fetchall()

        table_view = self.incident_window.findChild(QtWidgets.QTableView, 'tableView_2')
        if table_view is None:
            print("Error: 'tableView_2' not found in 'Incidente.ui'")
            return

        headers = ["Incident", "Locație", "Număr Victime", "Procent Daune", "Status"]
        model = QtGui.QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                model.setItem(row_idx, col_idx, QtGui.QStandardItem(str(item)))
        table_view.setModel(model)
        table_view.resizeColumnsToContents()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    connection = create_connection()
    window = MainWindow()
    sys.exit(app.exec())