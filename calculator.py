import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

from functools import partial

window_Size = 235
display_Height = 35
Button_Size = 40
Error_msg = "Error"

# model starts
# evaluateExpression is model

def evaluateExpression(expression):
    """Evaluate the expression model."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = Error_msg
    return result
# model ends

# View starts
# calculator is View
class Calculator(QMainWindow):
    """ Calculator's main window or View """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5-Calculator")
        self.setFixedSize(window_Size, window_Size)
        self.generalLayout = QVBoxLayout() #creating object
        centralWidget = QWidget(self) #creating object
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.createDisplay()
        self.createButtons()

    def createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(display_Height)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout() #creating object
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", ")"],
            ["1", "2", "3", "-", "("],
            ["0", "00", ".", "+", "="]
        ]
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(Button_Size, Button_Size)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()
    
    def clearDisplay(self):
        self.setDisplayText("")

# view ends

# Controller Starts

class calcController:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self.connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == Error_msg:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(partial(self._buildExpression, keySymbol))
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)
# controller ends
def main():
    """Main function"""
    pyCalcApp = QApplication([])
    calc = Calculator()
    calc.show()
    calcController(model=evaluateExpression, view=calc)
    sys.exit(pyCalcApp.exec())

if __name__ == "__main__":
    main()
