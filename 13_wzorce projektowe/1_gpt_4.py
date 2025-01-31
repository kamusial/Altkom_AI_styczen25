import tkinter as tk
from tkinter import ttk

# Przykładowe fragmenty kodu dla różnych wzorców i języków
patterns = {
    "Factory": {
        "Python": '''\nclass Button:
    def click(self):
        pass

class WindowsButton(Button):
    def click(self):
        print("Windows Button clicked")

class LinuxButton(Button):
    def click(self):
        print("Linux Button clicked")

def get_button(platform):
    if platform == "Windows":
        return WindowsButton()
    elif platform == "Linux":
        return LinuxButton()

button = get_button("Windows")
button.click()''',
        "Java": '''\npublic interface Button {
    void click();
}

public class WindowsButton implements Button {
    public void click() {
        System.out.println("Windows Button clicked");
    }
}

public class LinuxButton implements Button {
    public void click() {
        System.out.println("Linux Button clicked");
    }
}

public class ButtonFactory {
    public static Button getButton(String platform) {
        if (platform.equals("Windows")) {
            return new WindowsButton();
        } else if (platform.equals("Linux")) {
            return new LinuxButton();
        }
        return null;
    }
}''',
        "C#": '''\ninterface IButton {
    void Click();
}

class WindowsButton : IButton {
    public void Click() {
        Console.WriteLine("Windows Button clicked");
    }
}

class LinuxButton : IButton {
    public void Click() {
        Console.WriteLine("Linux Button clicked");
    }
}

class ButtonFactory {
    public static IButton GetButton(string platform) {
        if (platform == "Windows") {
            return new WindowsButton();
        } else if (platform == "Linux") {
            return new LinuxButton();
        }
        return null;
    }
}'''
    },
    # Inne wzorce mogą być dodane tutaj w podobny sposób.
}

def show_example():
    pattern = pattern_var.get()
    language = language_var.get()
    code = patterns.get(pattern, {}).get(language, "No example available.")
    code_text.delete("1.0", tk.END)
    code_text.insert(tk.END, code)

# Ustawienia GUI
root = tk.Tk()
root.title("Design Patterns Examples")

# Dropdown menu dla wzorców projektowych
pattern_var = tk.StringVar()
pattern_label = tk.Label(root, text="Select a Design Pattern:")
pattern_label.pack()
pattern_menu = ttk.Combobox(root, textvariable=pattern_var)
pattern_menu['values'] = list(patterns.keys())
pattern_menu.pack()

# Dropdown menu dla języków programowania
language_var = tk.StringVar()
language_label = tk.Label(root, text="Select a Programming Language:")
language_label.pack()
language_menu = ttk.Combobox(root, textvariable=language_var)
language_menu['values'] = ["Python", "Java", "C#"]
language_menu.pack()

# Przycisk do generowania przykładu
show_button = tk.Button(root, text="Show Example", command=show_example)
show_button.pack()

# Pole tekstowe do wyświetlania kodu
code_text = tk.Text(root, height=15, width=80)
code_text.pack()

root.mainloop()
