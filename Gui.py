import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

class AdvancedPasswordGenerator:
    def __init__(self, length=16, use_upper=True, use_lower=True,
                 use_digits=True, use_special=True,
                 avoid_similar=True, avoid_ambiguous=True):
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_special = use_special
        self.avoid_similar = avoid_similar
        self.avoid_ambiguous = avoid_ambiguous

        self.similar_chars = 'ilLI|`oO0'
        self.ambiguous_chars = '{}[]()/\\\'"`~,;:.<>'
        self.char_sets = {
            'upper': string.ascii_uppercase,
            'lower': string.ascii_lowercase,
            'digits': string.digits,
            'special': '!@#$%^&*()-_=+'
        }

    def _filter_characters(self, charset):
        if self.avoid_similar:
            charset = ''.join(c for c in charset if c not in self.similar_chars)
        if self.avoid_ambiguous and charset == self.char_sets['special']:
            charset = ''.join(c for c in charset if c not in self.ambiguous_chars)
        return charset

    def generate(self):
        selected_sets = []
        all_chars = ''

        if self.use_upper:
            upper = self._filter_characters(self.char_sets['upper'])
            selected_sets.append(upper)
            all_chars += upper
        if self.use_lower:
            lower = self._filter_characters(self.char_sets['lower'])
            selected_sets.append(lower)
            all_chars += lower
        if self.use_digits:
            digits = self._filter_characters(self.char_sets['digits'])
            selected_sets.append(digits)
            all_chars += digits
        if self.use_special:
            special = self._filter_characters(self.char_sets['special'])
            selected_sets.append(special)
            all_chars += special

        if not all_chars:
            raise ValueError("At least one character type must be selected.")

        password = [random.choice(char_set) for char_set in selected_sets]
        password += random.choices(all_chars, k=self.length - len(password))
        random.shuffle(password)

        final_password = ''.join(password)
        pyperclip.copy(final_password)
        return final_password

# -------------------- GUI Setup -------------------- #

def generate_password():
    try:
        generator = AdvancedPasswordGenerator(
            length=int(length_entry.get()),
            use_upper=var_upper.get(),
            use_lower=var_lower.get(),
            use_digits=var_digits.get(),
            use_special=var_special.get(),
            avoid_similar=var_similar.get(),
            avoid_ambiguous=var_ambiguous.get()
        )
        password = generator.generate()
        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x400")
root.resizable(False, False)

# Input and checkbox fields
tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.insert(0, "16")
length_entry.pack(pady=5)

var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)
var_similar = tk.BooleanVar(value=True)
var_ambiguous = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Uppercase", variable=var_upper).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Lowercase", variable=var_lower).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Digits", variable=var_digits).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Special Characters", variable=var_special).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Avoid Similar Characters (O,0,I,l)", variable=var_similar).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Avoid Ambiguous Characters", variable=var_ambiguous).pack(anchor='w', padx=20)

tk.Button(root, text="Generate Password", command=generate_password, bg='green', fg='white').pack(pady=10)

tk.Label(root, text="Generated Password:").pack()
result_entry = tk.Entry(root, width=40)
result_entry.pack(pady=5)

# Run the GUI loop
root.mainloop()
