"""Test if Tkinter works on your system"""
import tkinter as tk
from tkinter import ttk

print("Starting Tkinter test...")

root = tk.Tk()
root.title("Test Window")
root.geometry("400x300")
root.configure(bg='white')

label = tk.Label(
    root, 
    text="✅ Tkinter is working!\n\nClose this window to continue.",
    font=('Arial', 16),
    bg='white'
)
label.pack(expand=True)

print("Window should be visible now!")
print("If you can't see it, check your taskbar or press Alt+Tab")

root.mainloop()
print("Test complete.")