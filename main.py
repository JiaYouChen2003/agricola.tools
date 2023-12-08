import sys
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QStyleFactory, QGridLayout, QMessageBox, QApplication
from PySide2.QtGui import QIcon

class GUI(QWidget):
	def __init__(self, parent=None):
		super().__init__()
		self.setWindowTitle('agricola.tools')
		self.setWindowIcon(QIcon('raw_asset/agricola-en.jpg'))
		self.label1 = QLabel('URL:')
		self.line_edit = QLineEdit()
		self.label2 = QLabel('Results:')
		self.text = QTextEdit()
		self.button = QPushButton()
		self.button.setText('scrape')
		self.cmb = QComboBox()
		self.cmb.setStyle(QStyleFactory.create('Fusion'))
		self.cmb.addItem('匹配度: 100%')
		self.grid = QGridLayout()
		self.grid.setSpacing(12)
		self.grid.addWidget(self.label1, 1, 0)
		self.grid.addWidget(self.line_edit, 1, 1, 1, 38)
		self.grid.addWidget(self.button, 1, 39)
		self.grid.addWidget(self.label2, 2, 0)
		self.grid.addWidget(self.text, 2, 1, 1, 40)
		self.grid.addWidget(self.cmb, 1, 40)
		self.setLayout(self.grid)
		self.resize(600, 400)
		self.button.clicked.connect(self.inquiry)
		
	def inquiry(self):
		sentence = self.line_edit.text()
		matched = []
		score_thresh = self.getScoreThresh()
		if not sentence:
			QMessageBox.warning(self, "Warning", '请先输入需要查询的鲁迅名言')
		else:
			for p in self.paragraphs:
				score = fuzz.partial_ratio(p, sentence)
				if score >= score_thresh and len(sentence) <= len(p):
					matched.append([score, p])
			infos = []
			for match in matched:
				infos.append('[匹配度]: %d\n[内容]: %s\n' % (match[0], match[1]))
			if not infos:
				infos.append('未匹配到任何相似度大于%d的句子.\n' % score_thresh)
			self.text.setText('\n\n\n'.join(infos)[:-1])

if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = GUI()
	gui.show()
	sys.exit(app.exec_())