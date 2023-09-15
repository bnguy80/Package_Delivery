import tkinter as tk


class PackageDeliveryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Package Delivery System")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Create and place widgets here, work in progress
        pass


def main():
    root = tk.Tk()
    app = PackageDeliveryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
