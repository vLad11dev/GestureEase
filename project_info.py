import tkinter as tk

class ProjectInfo:
    def __init__(self, parent):
        self.parent = parent
        self.project_info_label = tk.Label(parent, text="Информация о проекте будет здесь", font=("Helvetica", 12))
        self.project_info_label.pack(pady=20)

        # Add any additional initialization code here

# For testing the module
if __name__ == "__main__":
    root = tk.Tk()
    project_info_instance = ProjectInfo(root)
    root.mainloop()
