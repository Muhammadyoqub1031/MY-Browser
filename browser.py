import sys
import validators
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QLineEdit, QPushButton, QToolBar, QAction
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        #Title
        self.setWindowTitle('MY-Browser')
        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_page)

        # Search button
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search)

        # Back button
        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        back_button.triggered.connect(self.browser.back)

        # Forward button
        forward_button = QAction(QIcon('icons/forward.png'), 'Forward', self)
        forward_button.triggered.connect(self.browser.forward)

        # Home button
        home_button = QAction(QIcon('icons/home.png'), 'Home', self)
        home_button.triggered.connect(self.go_home)

        # Reload button
        reload_button = QAction(QIcon('icons/reload.png'), 'Reload', self)
        reload_button.triggered.connect(self.browser.reload)

        # Toolbar
        self.toolbar = QToolBar('Navigation')
        self.toolbar.addAction(back_button)
        self.toolbar.addAction(forward_button)
        self.toolbar.addAction(home_button)
        self.toolbar.addAction(reload_button)
        self.addToolBar(self.toolbar)

        # Status bar
        self.statusBar().addWidget(self.address_bar)
        self.statusBar().addWidget(self.search_button)

        # Load DuckDuckGo on startup
        self.load_page()

        # Add logo
        logo = QPixmap('icons/logo')
        self.setWindowIcon(QIcon(logo))

    def load_page(self):
        text = self.address_bar.text()
        if validators.url(text):
            url = QUrl(text)
        else:
            url = QUrl('https://duckduckgo.com/')
            self.search()

        self.browser.setUrl(url)

    def search(self):
        search_term = self.address_bar.text()
        url = f'https://duckduckgo.com/?q={search_term}'
        self.browser.setUrl(QUrl(url))

    def go_home(self):
        self.browser.setUrl(QUrl('https://duckduckgo.com/'))

    def create_view(self, url):
        # Create a new web engine view and add it to the dictionary
        view = QWebEngineView()
        view.setUrl(QUrl(url))
        self.views[id(view)] = view

        # Set the current view to the new view
        self.current_view = id(view)

        # Set the new view as the central widget
        self.setCentralWidget(view)

        # Connect the view's titleChanged signal to update the window title
        view.titleChanged.connect(self.update_title)

    def new_tab(self):
        # Create a new tab with the DuckDuckGo homepage
        self.create_view('https://duckduckgo.com/')

    def update_title(self, title):
        # Update the window title with the current view's title
        self.setWindowTitle(f"{title} - MuhYo")

    def load_page(self):
        text = self.address_bar.text()
        if validators.url(text):
            url = QUrl(text)
        else:
            url = QUrl('https://duckduckgo.com/')
            self.search()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
