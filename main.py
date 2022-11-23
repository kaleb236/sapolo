import sys
import requests
import json

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from ui_sapolo import Ui_MainWindow

from PyQt5.QtWidgets import *

class ui_windows(QMainWindow):
    def __init__(self):
        super(ui_windows, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.home_index = 0
        self.prescription_index = 1

        # self.ui.stackedWidget.setCurrentIndex(self.prescription_index)

        self.ui.bottom_frame.setStyleSheet(''' QFrame#bottom_frame{
        border-image: url(resources/vector 1.png);}
        ''')
        self.ui.call_logo.setStyleSheet('''
        image: url(resources/vector.png);
        ''')
    
    def keyPressEvent(self, event):
        key = event.key()

        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.token_check()
    
    def token_check(self):
        self.data = self.api_try()['data']
        if int(self.ui.token_line_edit.text()) == self.data['token']:
            self.ui.stackedWidget.setCurrentIndex(self.prescription_index)
            self.set_data(self.data)
        
        else:
            self.ui.token_status.setStyleSheet('''
                    color: #e95222;
                    font: 24pt "Mulish";
            ''')
            self.ui.token_status.setText('ERROR_INCORRECT TOKEN#0112')
    
    def api_try(self):
        sapolo = requests.get('https://atlp-mybrand-backend.herokuapp.com/api/v1/prescriptions/637bae1616c96c13b9d60bbc')
        return sapolo.json()
    
    def set_data(self, data):
        self.ui.doctor.setText(data['doctor'])
        self.ui.institution.setText(data['institution'])
        self.ui.receiver.setText(data['patient'])
        self.ui.offering_date.setText(data['offeredDate'])
        if data['payment'] == 'not-paid':
            self.ui.payment.setStyleSheet('''
            font: 8pt "Mulish";
            color: #e95222;
            ''')
        self.ui.payment.setText(data['payment'])
        meds = self.data['medicines']
        self.ui.meds.setText(f'MEDS({len(meds)})')

        med_index = 0

        for i in meds:
            self.ui.meds_gridlayout.addWidget(self.qlabel(i['medName']), med_index,0)
            self.ui.meds_gridlayout.addWidget(self.qlabel(str(i['medNumber'])), med_index,1)
            self.ui.meds_gridlayout.addWidget(self.qlabel(i['pattern']), med_index,2)
            med_index += 1
    
    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
    
    def qlabel(self, text):
        med_label = QLabel(text)
        med_label.setStyleSheet("""font: 8pt "Mulish";""")
        return med_label



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ui_windows()

    win.show()
    sys.exit(app.exec_())