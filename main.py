import customtkinter as ctk
import pyperclip
import threading
import time

class GlassClipboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Glass Clipboard")
        self.geometry("400x600")
        
        # Making the window slightly transparent for that "Glass" feel
        self.attributes("-alpha", 0.95) 
        
        self.history = []
        self.last_copied = ""

        # UI Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.label = ctk.CTkLabel(self, text="Clipboard History", font=("Segoe UI", 20, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        # Scrollable Frame for Clips
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Background thread to monitor clipboard
        self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.monitor_thread.start()

    def monitor_clipboard(self):
        while True:
            current_clipboard = pyperclip.paste()
            if current_clipboard != self.last_copied and current_clipboard.strip() != "":
                self.last_copied = current_clipboard
                self.add_to_history(current_clipboard)
            time.sleep(0.5)

    def add_to_history(self, text):
        if text not in self.history:
            self.history.insert(0, text)
            self.update_ui()

    def select_clip(self, text):
        self.last_copied = text
        pyperclip.copy(text)
        # Visual feedback: update the UI to show what's currently active
        self.update_ui()

    def update_ui(self):
        # Clear current list
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Add clips as buttons
        for item in self.history:
            # Highlight the currently "active" paste item
            is_active = (item == self.last_copied)
            border_color = "#60a5fa" if is_active else "#333333"
            
            btn = ctk.CTkButton(
                self.scroll_frame, 
                text=item[:50] + "..." if len(item) > 50 else item,
                fg_color="rgba(255, 255, 255, 0.1)", # Semi-transparent
                border_color=border_color,
                border_width=2,
                hover_color="rgba(255, 255, 255, 0.2)",
                anchor="w",
                command=lambda t=item: self.select_clip(t)
            )
            btn.pack(fill="x", pady=5, padx=5)

if __name__ == "__main__":
    app = GlassClipboard()
    app.mainloop()
