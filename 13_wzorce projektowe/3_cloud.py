import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


class DesignPatternExamples:
    def __init__(self):
        self.patterns = {
            "Creational": ["Singleton", "Factory", "Abstract Factory", "Builder", "Prototype"],
            "Structural": ["Adapter", "Bridge", "Composite", "Decorator", "Facade", "Flyweight", "Proxy"],
            "Behavioral": ["Observer", "Strategy", "Command", "State", "Template Method", "Iterator", "Mediator"]
        }

        self.examples = {
            "python": {
                "Singleton": """
# Python Singleton Pattern Example
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def some_business_logic(self):
        pass
""",
                "Factory": """
# Python Factory Pattern Example
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        raise ValueError("Invalid animal type")
""",
            },
            "java": {
                "Singleton": """
// Java Singleton Pattern Example
public class Singleton {
    private static Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }

    public void someBusinessLogic() {
        // business logic here
    }
}
""",
                "Factory": """
// Java Factory Pattern Example
interface Animal {
    String speak();
}

class Dog implements Animal {
    @Override
    public String speak() {
        return "Woof!";
    }
}

class Cat implements Animal {
    @Override
    public String speak() {
        return "Meow!";
    }
}

class AnimalFactory {
    public Animal createAnimal(String animalType) {
        if (animalType.equalsIgnoreCase("dog")) {
            return new Dog();
        } else if (animalType.equalsIgnoreCase("cat")) {
            return new Cat();
        }
        throw new IllegalArgumentException("Invalid animal type");
    }
}
""",
            },
            "c#": {
                "Singleton": """
// C# Singleton Pattern Example
public sealed class Singleton
{
    private static Singleton instance = null;
    private static readonly object padlock = new object();

    private Singleton() {}

    public static Singleton Instance
    {
        get
        {
            lock (padlock)
            {
                if (instance == null)
                {
                    instance = new Singleton();
                }
                return instance;
            }
        }
    }

    public void SomeBusinessLogic()
    {
        // business logic here
    }
}
""",
                "Factory": """
// C# Factory Pattern Example
public interface IAnimal
{
    string Speak();
}

public class Dog : IAnimal
{
    public string Speak()
    {
        return "Woof!";
    }
}

public class Cat : IAnimal
{
    public string Speak()
    {
        return "Meow!";
    }
}

public class AnimalFactory
{
    public IAnimal CreateAnimal(string animalType)
    {
        switch (animalType.ToLower())
        {
            case "dog":
                return new Dog();
            case "cat":
                return new Cat();
            default:
                throw new ArgumentException("Invalid animal type");
        }
    }
}
"""
            }
        }


class DesignPatternsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Design Patterns Examples")
        self.root.geometry("800x600")

        self.pattern_examples = DesignPatternExamples()

        # Create main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Pattern Category Selection
        ttk.Label(main_frame, text="Pattern Category:").grid(row=0, column=0, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(main_frame, textvariable=self.category_var)
        self.category_combo['values'] = list(self.pattern_examples.patterns.keys())
        self.category_combo.grid(row=0, column=1, sticky=tk.W)
        self.category_combo.bind('<<ComboboxSelected>>', self.update_patterns)

        # Pattern Selection
        ttk.Label(main_frame, text="Design Pattern:").grid(row=1, column=0, sticky=tk.W)
        self.pattern_var = tk.StringVar()
        self.pattern_combo = ttk.Combobox(main_frame, textvariable=self.pattern_var)
        self.pattern_combo.grid(row=1, column=1, sticky=tk.W)

        # Programming Language Selection
        ttk.Label(main_frame, text="Programming Language:").grid(row=2, column=0, sticky=tk.W)
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(main_frame, textvariable=self.language_var)
        self.language_combo['values'] = ['python', 'java', 'c#']
        self.language_combo.grid(row=2, column=1, sticky=tk.W)

        # Show Example Button
        ttk.Button(main_frame, text="Show Example", command=self.show_example).grid(row=3, column=0, columnspan=2,
                                                                                    pady=10)

        # Code Display Area
        self.code_display = scrolledtext.ScrolledText(main_frame, width=80, height=30)
        self.code_display.grid(row=4, column=0, columnspan=2, pady=10)

        # Set initial values
        self.category_combo.set("Creational")
        self.update_patterns(None)
        self.language_combo.set("python")

    def update_patterns(self, event):
        category = self.category_var.get()
        self.pattern_combo['values'] = self.pattern_examples.patterns[category]
        if self.pattern_combo['values']:
            self.pattern_combo.set(self.pattern_combo['values'][0])

    def show_example(self):
        pattern = self.pattern_var.get()
        language = self.language_var.get()

        try:
            example = self.pattern_examples.examples[language][pattern]
            self.code_display.delete(1.0, tk.END)
            self.code_display.insert(tk.END, example)
        except KeyError:
            messagebox.showwarning("Warning", f"Example for {pattern} in {language} is not available yet!")
            self.code_display.delete(1.0, tk.END)
            self.code_display.insert(tk.END, "Example not available for this combination.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesignPatternsGUI(root)
    root.mainloop()