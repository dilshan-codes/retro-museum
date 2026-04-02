import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from core.navigation import Navigator
from core.router import Router
from widgets.navbar import NavBar
from screens.home import HomeScreen
from screens.emulators import EmulatorsScreen
from screens.history import HistoryScreen
from screens.history_detail import HistoryDetailScreen
from screens.turing import TuringScreen
from screens.baby import BabyScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and minimum size
        self.setWindowTitle("Retro Computing Museum")
        self.setMinimumSize(1024, 700)

        # Create one navigator and one router shared across the whole app
        self.navigator = Navigator()
        self.router = Router()

        self.router.register("home", HomeScreen)
        self.router.register("emulators", EmulatorsScreen)
        self.router.register("history", HistoryScreen)
        self.router.register("turing", TuringScreen)
        self.router.register("baby", BabyScreen)
        

        # QMainWindow needs a central widget to hold everything inside
        self.central = QWidget()
        self.setCentralWidget(self.central)

        # Main layout stacks widgets vertically — navbar on top, screen below
        self.main_layout = QVBoxLayout()
        self.central.setLayout(self.main_layout)

        # Create the navbar and connect its navigate signal to our handler
        self.navbar = NavBar()
        self.navbar.navigate.connect(self.handle_navigate)
        self.main_layout.addWidget(self.navbar)

        # Track the current screen so we can remove it when switching
        self.current_screen = None
        self.content_area = QWidget()
        self.main_layout.addWidget(self.content_area)

    def handle_navigate(self, route):
        # Handle back and forward separately using the navigator stack
        if route == "back":
            route = self.navigator.back()
        elif route == "forward":
            route = self.navigator.forward()
        else:
            # Normal navigation — add to history stack
            self.navigator.go_to(route)

        # Update the navbar location label and switch to the new screen
        self.navbar.update_location(route)
        self.switch_screen(route)

    def switch_screen(self, route):
        if self.current_screen is not None:
            self.main_layout.removeWidget(self.current_screen)
            self.current_screen.hide()
            self.current_screen.deleteLater()
            self.current_screen = None

        # Handle history detail routes — pass event ID
        if route.startswith("history_detail_"):
            event_id = route.replace("history_detail_", "")
            self.current_screen = HistoryDetailScreen(self.handle_navigate, event_id)
            self.main_layout.addWidget(self.current_screen)
            return

        screen_class = self.router.resolve(route)
        if screen_class is not None:
            self.current_screen = screen_class(self.handle_navigate)
            self.main_layout.addWidget(self.current_screen)

    def showEvent(self, event):
        # Runs automatically when window first appears — load home screen
        super().showEvent(event)
        if self.current_screen is None:
            self.handle_navigate("home")


if __name__ == "__main__":
    # Create the app, show the window, start the event loop
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
