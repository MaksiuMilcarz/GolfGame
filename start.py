from Visualization.GUI import GolfSimulationApp
import tkinter as tk

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Set full screen mode
    app = GolfSimulationApp(root)
    app.plot_map()  # Plot initial map
    root.mainloop()

if __name__ == "__main__":
    main()