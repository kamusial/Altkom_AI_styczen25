import tkinter as tk
from tkinter import ttk

# Słownik z przykładowymi implementacjami wzorców w różnych językach
wzorce = {
    "Singleton": {
        "Java": """\
public class Singleton {
    private static Singleton instance;

    private Singleton() {
        // Konstruktor prywatny
    }

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}
""",
        "Python": """\
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

# Użycie:
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True
""",
        "C#": """\
public sealed class Singleton {
    private static Singleton instance = null;
    private static readonly object padlock = new object();

    Singleton() {
    }

    public static Singleton Instance {
        get {
            lock (padlock) {
                if (instance == null) {
                    instance = new Singleton();
                }
                return instance;
            }
        }
    }
}
"""
    },
    "Factory": {
        "Java": """\
// Przykładowa klasa produktu
abstract class Product {
    public abstract void use();
}

// Konkretne produkty
class ConcreteProductA extends Product {
    public void use() {
        System.out.println("Używam produktu A");
    }
}

class ConcreteProductB extends Product {
    public void use() {
        System.out.println("Używam produktu B");
    }
}

// Fabryka
class ProductFactory {
    public static Product createProduct(String type) {
        if (type.equals("A")) return new ConcreteProductA();
        if (type.equals("B")) return new ConcreteProductB();
        return null;
    }
}

// Użycie:
Product product = ProductFactory.createProduct("A");
product.use();
""",
        "Python": """\
from abc import ABC, abstractmethod

class Product(ABC):
    @abstractmethod
    def use(self):
        pass

class ConcreteProductA(Product):
    def use(self):
        print("Używam produktu A")

class ConcreteProductB(Product):
    def use(self):
        print("Używam produktu B")

class ProductFactory:
    @staticmethod
    def create_product(product_type):
        if product_type == "A":
            return ConcreteProductA()
        elif product_type == "B":
            return ConcreteProductB()
        return None

# Użycie:
product = ProductFactory.create_product("A")
product.use()
""",
        "C#": """\
// Przykładowa klasa produktu
public abstract class Product {
    public abstract void Use();
}

public class ConcreteProductA : Product {
    public override void Use() {
        Console.WriteLine("Używam produktu A");
    }
}

public class ConcreteProductB : Product {
    public override void Use() {
        Console.WriteLine("Używam produktu B");
    }
}

public static class ProductFactory {
    public static Product CreateProduct(string type) {
        switch(type) {
            case "A": return new ConcreteProductA();
            case "B": return new ConcreteProductB();
            default: return null;
        }
    }
}

// Użycie:
Product product = ProductFactory.CreateProduct("A");
product.Use();
"""
    },
    "Observer": {
        "Java": """\
import java.util.ArrayList;
import java.util.List;

// Interfejs obserwatora
interface Observer {
    void update(String message);
}

// Klasa obserwowana
class Subject {
    private List<Observer> observers = new ArrayList<>();

    public void addObserver(Observer o) {
        observers.add(o);
    }

    public void removeObserver(Observer o) {
        observers.remove(o);
    }

    public void notifyObservers(String message) {
        for (Observer o : observers) {
            o.update(message);
        }
    }
}

// Przykładowa klasa obserwatora
class ConcreteObserver implements Observer {
    private String name;

    public ConcreteObserver(String name) {
        this.name = name;
    }

    @Override
    public void update(String message) {
        System.out.println(name + " otrzymał wiadomość: " + message);
    }
}

// Użycie:
public class Main {
    public static void main(String[] args) {
        Subject subject = new Subject();
        Observer obs1 = new ConcreteObserver("Obserwator1");
        Observer obs2 = new ConcreteObserver("Obserwator2");

        subject.addObserver(obs1);
        subject.addObserver(obs2);

        subject.notifyObservers("Wiadomość testowa");
    }
}
""",
        "Python": """\
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer:
    def update(self, message):
        pass

class ConcreteObserver(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} otrzymał wiadomość: {message}")

# Użycie:
subject = Subject()
obs1 = ConcreteObserver("Obserwator1")
obs2 = ConcreteObserver("Obserwator2")

subject.attach(obs1)
subject.attach(obs2)
subject.notify("Wiadomość testowa")
""",
        "C#": """\
using System;
using System.Collections.Generic;

// Interfejs obserwatora
public interface IObserver {
    void Update(string message);
}

// Klasa obserwowana
public class Subject {
    private List<IObserver> observers = new List<IObserver>();

    public void Attach(IObserver observer) {
        observers.Add(observer);
    }

    public void Detach(IObserver observer) {
        observers.Remove(observer);
    }

    public void Notify(string message) {
        foreach (var obs in observers) {
            obs.Update(message);
        }
    }
}

// Przykładowy obserwator
public class ConcreteObserver : IObserver {
    private string name;

    public ConcreteObserver(string name) {
        this.name = name;
    }

    public void Update(string message) {
        Console.WriteLine($"{name} otrzymał wiadomość: {message}");
    }
}

// Użycie:
public class Program {
    public static void Main() {
        Subject subject = new Subject();
        IObserver obs1 = new ConcreteObserver("Obserwator1");
        IObserver obs2 = new ConcreteObserver("Obserwator2");

        subject.Attach(obs1);
        subject.Attach(obs2);

        subject.Notify("Wiadomość testowa");
    }
}
"""
    }
}


def pobierz_przyklad():
    wybrany_wzorzec = combo_wzorzec.get()
    wybrany_jezyk = combo_jezyk.get()

    # Pobranie tekstu z słownika (lub komunikat o braku danych)
    if wybrany_wzorzec in wzorce and wybrany_jezyk in wzorce[wybrany_wzorzec]:
        kod = wzorce[wybrany_wzorzec][wybrany_jezyk]
    else:
        kod = "Brak przykładu dla wybranego wzorca lub języka."

    # Wstawienie kodu do pola tekstowego (wyczyszczenie poprzedniego i wklejenie nowego)
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, kod)
    text_area.config(state=tk.DISABLED)


# Tworzenie głównego okna
root = tk.Tk()
root.title("Wzorce projektowe")

# Etykieta: wybór wzorca
label_wzorzec = tk.Label(root, text="Wybierz wzorzec:")
label_wzorzec.grid(row=0, column=0, padx=5, pady=5)

# Combobox z listą wzorców
combo_wzorzec = ttk.Combobox(root, values=list(wzorce.keys()), state="readonly")
combo_wzorzec.grid(row=0, column=1, padx=5, pady=5)
combo_wzorzec.current(0)  # Domyślny wybór pierwszego elementu

# Etykieta: wybór języka
label_jezyk = tk.Label(root, text="Wybierz język:")
label_jezyk.grid(row=1, column=0, padx=5, pady=5)

# Combobox z listą języków
lista_jezykow = ["Java", "Python", "C#"]
combo_jezyk = ttk.Combobox(root, values=lista_jezykow, state="readonly")
combo_jezyk.grid(row=1, column=1, padx=5, pady=5)
combo_jezyk.current(0)

# Przycisk pobierania przykładu
button_pobierz = tk.Button(root, text="Pobierz przykład", command=pobierz_przyklad)
button_pobierz.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

# Pole tekstowe do wyświetlania kodu
text_area = tk.Text(root, wrap="word", width=80, height=25, state=tk.DISABLED)
text_area.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Uruchomienie pętli głównej aplikacji
root.mainloop()
