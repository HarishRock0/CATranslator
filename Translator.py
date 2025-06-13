import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import asyncio

# Initialize translator
translator = Translator()

root = tk.Tk()
root.title("CodeAlpha Translator") 
root.geometry("1000x600+100+0")
root.config(bg="#3D5675")
root.resizable(False, False)

# Title
tk.Label(root, text="CodeAlpha Translator", font=("Arial", 20, "bold"), bg="#3D5675").pack(pady=10)

# Main frame
frame1 = tk.Frame(root, height=300, width=950, relief="ridge", bg="white", bd=3)
frame1.place(anchor="center", relx=0.5, rely=0.5)

# Input text box
text_input1 = tk.Text(frame1, width=45, height=10, font=("Arial", 12), bg="white", wrap="word")
text_input1.place(x=50, y=50)

# Output text box
text_input2 = tk.Text(frame1, width=45, height=10, font=("Arial", 12), bg="white", wrap="word", state="disabled")
text_input2.place(x=500, y=50)

# Language selection
languages = list(LANGUAGES.values())
source_lang = tk.StringVar()
target_lang = tk.StringVar()

# Default languages
source_lang.set("english")
target_lang.set("tamil")

# Source language dropdown
tk.Label(frame1, text="From:", bg="white").place(x=50, y=20)
source_menu = ttk.Combobox(frame1, textvariable=source_lang, values=languages, state="readonly")
source_menu.place(x=100, y=20, width=150)

# Target language dropdown
tk.Label(frame1, text="To:", bg="white").place(x=500, y=20)
target_menu = ttk.Combobox(frame1, textvariable=target_lang, values=languages, state="readonly")
target_menu.place(x=550, y=20, width=150)

def get_language_code(language_name):
    """Get language code from language name"""
    for code, name in LANGUAGES.items():
        if name.lower() == language_name.lower():
            return code
    return 'en'  # Default to English if not found

async def async_translate_text():
    """Translate the input text asynchronously"""
    input_text = text_input1.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter text to translate")
        return
    
    try:
        src_lang = get_language_code(source_lang.get())
        dest_lang = get_language_code(target_lang.get())

        translated = await translator.translate(input_text, src=src_lang, dest=dest_lang)

        text_input2.config(state="normal")
        text_input2.delete("1.0", tk.END)
        text_input2.insert(tk.END, translated.text)
        text_input2.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {str(e)}")

def translate_text():
    """Run the asynchronous translation function safely"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_translate_text())

def clear_text():
    """Clear both text boxes"""
    text_input1.delete("1.0", tk.END)
    text_input2.config(state="normal")
    text_input2.delete("1.0", tk.END)
    text_input2.config(state="disabled")

def swap_languages():
    """Swap source and target languages"""
    current_source = source_lang.get()
    current_target = target_lang.get()
    
    # Get current texts
    input_text = text_input1.get("1.0", tk.END).strip()
    output_text = text_input2.get("1.0", tk.END).strip() if not text_input2.compare("end-1c", "==", "1.0") else ""
    
    # Swap languages
    source_lang.set(current_target)
    target_lang.set(current_source)
    
    # Swap texts if output exists
    if output_text:
        text_input1.delete("1.0", tk.END)
        text_input1.insert(tk.END, output_text)
        
        text_input2.config(state="normal")
        text_input2.delete("1.0", tk.END)
        text_input2.insert(tk.END, input_text)
        text_input2.config(state="disabled")

# Buttons
button_frame = tk.Frame(root, bg="#3D5675")
button_frame.place(relx=0.5, rely=0.85, anchor="center")

translate_btn = tk.Button(button_frame, text="Translate", font=("Arial", 12), 
                         bg="#3D5675", command=translate_text)
translate_btn.pack(side="left", padx=10)

clear_btn = tk.Button(button_frame, text="Clear", font=("Arial", 12), 
                     bg="#3D5675", command=clear_text)
clear_btn.pack(side="left", padx=10)

swap_btn = tk.Button(button_frame, text="Swap Languages", font=("Arial", 12), 
                    bg="#3D5675", command=swap_languages)
swap_btn.pack(side="left", padx=10)

root.mainloop()