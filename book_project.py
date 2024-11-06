import tkinter as tk
from tkinter import messagebox
import time ##Cami esto es para ordenarlo por antiguedad 

##Validacion para que no tenga libros duplicados, numeros entre letras ni viceversa ##
books = []
def valid_book(book):
    pattern = []

    ## Que los números y las letras no este mezclados ##
    for i, char in enumerate(book):
        if i > 0 and char.isdigit() and book[i-1].isalpha():
            pattern.append(True)
        else:
            pattern.append(False)
    if any(pattern):
        messagebox.showerror("ERROR", "No puede tener números entre letras, ni viceversa")
        return False

    ## Que no hayan duplicados ##
    if book in books:
        messagebox.showerror("ERROR", "El libro ya existe en la biblioteca")
        return False
    return True

## Verificar que el autor contenga solo letras ##
def valid_author(author):
    if not author.isalpha():
        messagebox.showerror("ERROR", "En 'autor' solo debe contener letras")
        return False
    return True

## Verificar que el año contenga solo números ##
def valid_year(year):
    if not year.isdigit():
        messagebox.showerror("ERROR", "En 'año de publicación' solo debe contener números")
        return False
    return True

## Algoritmos de ordenamiento personalizado ##
def quick_sort(books, start, end, sort):
    def partition(books, start, end, sort):
        pivot1 = books[end]
        i = start - 1
        for j in range(start, end):
            if sort(books[j]) <= sort(pivot1):
                i += 1
                books[i], books[j] = books[j], books[i]
        books[i + 1], books[end] = books[end], books[i + 1]
        return i + 1

    if start < end:
        pivot = partition(books, start, end, sort)
        quick_sort(books, start, pivot - 1, sort)
        quick_sort(books, pivot + 1, end, sort)
    return books

def open_quick(self, books, sort):
    return self.quick_sort(books, 0, len(books) - 1, sort)

## Ordenar por: Año, Autor, titulo, Antiguedad, recomendado ##
def sort_year(book):
    return book.year
def sort_author(book):
    return book.author
def sort_title(book):
    return book.title
def sort_oldest(book):
    return book.sort_oldest
def sort_recommended(book):
    return book.recommended

## Objeto libro ##
class Book:
    def __init__(self, title, author, year, recommended = False):
        self.title = title
        self.author = author
        self.year = year
        self.recommended = recommended
        self.arrival_date = time.time() ## Cami esto es para lo de la antiguedad

## Listas Enlazadas ##

## Lista Simple ##
class SimpleNode:
    def __init__(self, book):
        self.book = book
        self.next = None

class SimpleList:
    def __init__(self):
        self.head = None

    def add_book(self, book):
        new_node = SimpleNode(book)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def search_book(self, title):
        current = self.head
        while current:
            if current.book.title == title:
                return current.book
            current = current.next
        return None

    def delete_book(self, title):
        current = self.head
        previous = None
        while current:
            if current.book.title == title:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    def show_books(self):
        current = self.head
        books = []
        while current:
            books.append(f"{current.book.title} by {current.book.author} ({current.book.year})")
            current = current.next
        return books

## Lista Doble ##
class DoublyNode:
    def __init__(self, book):
        self.book = book
        self.next = None
        self.prev = None

class DoublyList:
    def __init__(self):
        self.head = None

    def add_book(self, book):
        new_node = DoublyNode(book)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current:
                if (book.year < current.book.year or
                    (book.year == current.book.year and book.author < current.book.author) or
                    (book.year == current.book.year and book.author == current.book.author and book.title < current.book.title)):
                    if current == self.head:
                        new_node.next = self.head
                        self.head.prev = new_node
                        self.head = new_node
                        new_node.prev = None
                    else:
                        new_node.prev = current.prev
                        new_node.next = current
                        current.prev.next = new_node
                        current.prev = new_node
                    return
                if not current.next:  # Si llegamos al final de la lista
                    break
                current = current.next

            # Si el libro es el más grande, lo añadimos al final
            current.next = new_node
            new_node.prev = current
            new_node.next = None

    def search_book(self, title):
        current = self.head
        while current:
            if current.book.title == title:
                return current.book
            current = current.next
        return None

    def delete_book(self, title):
        current = self.head
        while current:
            if current.book.title == title:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                return True
            current = current.next
        return False

    def show_books(self):
        current = self.head
        books = []
        while current:
            books.append(f"{current.book.title} by {current.book.author} ({current.book.year})")
            current = current.next
        return books

## Lista Circular ##
class CircularNode:
    def __init__(self, book):
        self.book = book
        self.next = None

class CircularList:
    def __init__(self):
        self.head = None

    def add_book(self, book):
        new_node = CircularNode(book)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def search_book(self, title):
        if not self.head:
            return None
        current = self.head
        while True:
            if current.book.title == title:
                return current.book
            current = current.next
            if current == self.head:
                break
        return None

    def delete_book(self, title):
        current = self.head
        prev = None

        if current.book.title == title:
            if current.next == self.head:
                self.head = None
            else:
                while current.next != self.head:
                    current = current.next
                current.next = self.head.next
                self.head = self.head.next
            return True

    def show_books(self):
        current = self.head
        books = []
        while True:
            books.append(current.book.title)
            current = current.next
            if current == self.head:
                break
        return books

## Funcionamiento de la Biblioteca ##
class Library:
    def __init__(self):
        self.simplelist = SimpleList()
        self.doublylist = DoublyList()
        self.circularlist = CircularList()

    def add_book(self, title, author, year, recommended = False):
        if valid_author(author) and valid_year(year) and valid_book(title):
            new_book = Book(title, author, year, recommended)
            self.simplelist.add_book(new_book)
            self.doublylist.add_book(new_book)
            if recommended:
                self.circularlist.add_book(new_book)
            Library.books.append(title)

    def search_book(self, title):
        book = self.simplelist.search_book(title) or self.doublylist.search_book(title) or self.circularlist.search_book(title)
        return book

    def delete_book(self, title):
        if title in Library:
            self.simplelist.delete_book(title)
            self.doublylist.delete_book(title)
            self.circularlist.delete_book(title)
            Library.remove(title)
        else:
            messagebox.showerror("ERROR", "El libro no existe en la biblioteca")

    def show_book(self, linked_lists = "todas", bibliographic = "bibliografía"):

        if bibliographic == "year":
            sort_b = sort_year
        elif bibliographic == "author":
            sort_b = sort_author
        elif bibliographic == "title":
            sort_b = sort_title
        elif bibliographic == "oldest":
            sort_b = sort_oldest
        elif bibliographic == "recommended":
            sort_b = sort_recommended
        else:
            messagebox.showerror("ERROR", "Criterio de ordenación no válido.")
            return
        books = self.simplelist.show_books() + self.doublylist.show_books() + self.circularlist.show_books()
        books_sorted = quick_sort(books, 0, len(books) - 1, sort_b)

        if linked_lists == "Simple":
            return self.simplelist.show_books()
        elif linked_lists == "Doble":
            return self.doublylist.show_books()
        elif linked_lists == "Circular":
            return self.circularlist.show_books()
        else: 
            books_sorted
