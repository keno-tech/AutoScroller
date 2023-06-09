from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        
        # Set window properties
        self.setWindowTitle("Configuration Window")
        self.setFixedSize(640, 480)
        
        # Set dark theme colors
        self.set_dark_theme()
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create widgets
        label1 = QLabel("Setting 1:")
        label1.setStyleSheet("color: #ffffff; font-size: 16px;")
        layout.addWidget(label1)
        
        line_edit1 = QLineEdit()
        layout.addWidget(line_edit1)
        
        label2 = QLabel("Setting 2:")
        label2.setStyleSheet("color: #ffffff; font-size: 16px;")
        layout.addWidget(label2)
        
        line_edit2 = QLineEdit()
        layout.addWidget(line_edit2)
        
        # Create save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet("color: #ffffff; background-color: #222222; font-size: 16px; padding: 10px;")
        save_button.clicked.connect(self.save_configuration)
        layout.addWidget(save_button)
        
        # Set the layout
        self.setLayout(layout)
    
    def set_dark_theme(self):
        dark_palette = QPalette()
        
        # Set background color
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        
        # Set widget colors
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        # Apply the dark palette
        QApplication.instance().setPalette(dark_palette)
    
    def save_configuration(self):
        # Add your save configuration logic here
        print("Configuration saved!")

# Example usage
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())
