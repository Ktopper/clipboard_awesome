import tkinter as tk
from tkinter import ttk
import pyperclip
import threading
import time

class ClipboardManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clipboard Manager")
        self.root.geometry("400x500")
        
        # Store clipboard history
        self.clipboard_history = []
        self.max_history = 20
        
        # Create GUI elements
        self.create_widgets()
        
        # Start clipboard monitoring
        self.last_clipboard = pyperclip.paste()
        self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.monitor_thread.start()
        
    def create_widgets(self):
        # Create listbox to show clipboard history
        self.history_listbox = tk.Listbox(self.root, width=50, height=20)
        self.history_listbox.pack(padx=10, pady=10)
        
        # Bind double-click event to paste selected item
        self.history_listbox.bind("<Double-1>", self.paste_selected)
        
        # Create copy button
        copy_button = ttk.Button(self.root, text="Copy Selected", command=self.copy_selected)
        copy_button.pack(pady=5)
        
        # Create clear button
        clear_button = ttk.Button(self.root, text="Clear History", command=self.clear_history)
        clear_button.pack(pady=5)
        
    def monitor_clipboard(self):
        while True:
            current_clipboard = pyperclip.paste()
            if current_clipboard != self.last_clipboard:
                self.last_clipboard = current_clipboard
                if current_clipboard not in self.clipboard_history:
                    self.clipboard_history.insert(0, current_clipboard)
                    if len(self.clipboard_history) > self.max_history:
                        self.clipboard_history.pop()
                    self.update_listbox()
            time.sleep(0.1)
    
    def update_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.clipboard_history:
            # Truncate long items for display
            display_text = item[:50] + "..." if len(item) > 50 else item
            self.history_listbox.insert(tk.END, display_text)
    
    def copy_selected(self):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            pyperclip.copy(self.clipboard_history[index])
    
    def paste_selected(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            pyperclip.copy(self.clipboard_history[index])
            # Simulate pasting at the current cursor position
            self.root.clipboard_clear()
            self.root.clipboard_append(self.clipboard_history[index])
            self.root.update()  # Keep the clipboard updated

    def clear_history(self):
        self.clipboard_history.clear()
        self.update_listbox()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ClipboardManager()
    app.run()