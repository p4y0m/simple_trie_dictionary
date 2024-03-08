import os 
import tkinter as tk
from tkinter import messagebox
import re

os.system("clear")
        
class Autocomplete:
    def __init__(self, root):
        self.root = root
        self.root.title("Dictionary")
        self.root.geometry("600x400")
        self.root.configure(bg="#1a1a1a")
        self.node = build_the_node()

        self.input_text = tk.Entry(root, font=('Helvetica', 14), bg="#333333", fg="#aaafff")
        self.input_text.pack(pady=20)

        self.buttons_frame = tk.Frame(root, bg="#1a1a1a")
        self.buttons_frame.pack()

        self.search_button = tk.Button(self.buttons_frame, text="Search", command=self.search_word, font=('Helvetica', 12), bg="#3498db", fg="white")
        self.search_button.pack(side=tk.LEFT, padx=10)

        self.insert_button = tk.Button(self.buttons_frame, text="Insert", command=self.insert_word, font=('Helvetica', 12), bg="#4CAF50", fg="white")
        self.insert_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_word, font=('Helvetica', 12), bg="#FF5733", fg="white")
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.suggestions_listbox = tk.Listbox(root, height=5, font=('Helvetica', 12), bg="#333333", fg="#ffffff")
        self.suggestions_listbox.pack(pady=10)

        self.status_label = tk.Label(root, text="", font=('Helvetica', 12), bg="#1a1a1a", fg="#3498db")
        self.status_label.pack()

        self.input_text.bind('<KeyRelease>', self.on_key_release)



    def on_key_release(self, event):
        current_input = self.input_text.get().lower()
        
        
        if current_input.isalpha():
            suggestions = self.get_suggested_words(current_input)
            self.update_suggestions_listbox(suggestions)
        else:
            
            self.suggestions_listbox.delete(0, tk.END)
            self.status_label.config(text="")

    def get_suggested_words(self, prefix):
        temp = self.node
        
        for i in prefix:
            index = ord(i) - ord('a')
            
            if temp.children[index] is not None:
                temp = temp.children[index]
                
            else:
                return []

        return self.find_next_words(temp, prefix, 5)

    def find_next_words(self, node, prefix, num_words):
        suggestions = []

        if node is None:
            return suggestions


        if node.full_word:
            suggestions.append(prefix)


        for i in range(26):
            char = chr(ord('a') + i)
            next_words = self.find_next_words(node.children[i], prefix + char, num_words)
            suggestions.extend(next_words)

        return suggestions[:num_words]

    def update_suggestions_listbox(self, suggestions):
        self.suggestions_listbox.delete(0, tk.END)
        
        for suggestion in suggestions:
            self.suggestions_listbox.insert(tk.END, suggestion)

    def insert_word(self):
        word_to_insert = self.input_text.get().lower()
        result = insertion(word_to_insert, app.node)
        self.status_label.config(text=result, fg="#4CAF50")
        self.show_message_box(result)
        self.input_text.delete(0, tk.END)
        

    def delete_word(self):
        word_to_delete = self.input_text.get().lower()
        result = deletion(word_to_delete, app.node)
        self.status_label.config(text=result, fg="#FF5733")
        self.show_message_box(result)
        self.input_text.delete(0, tk.END)


    def search_word(self):
        
        word_to_search = self.input_text.get().lower()
        result = search(word_to_search, app.node)
        self.status_label.config(text=result, fg="#3498db")
        self.show_message_box(result)
        self.input_text.delete(0, tk.END)

    def show_message_box(self, message):
        messagebox.showinfo("Result", message)

    def on_key_release(self, event):
        if event.keysym == "Return":

            self.search_word()
            return

        current_input = self.input_text.get().lower()
        
        if current_input.isalpha():
            suggestions = self.get_suggested_words(current_input)
            self.update_suggestions_listbox(suggestions)
            
        else:
            self.suggestions_listbox.delete(0, tk.END)
            self.status_label.config(text="")



class Node:
    def __init__(self):
        self.children = [None] * 26
        self.full_word = False
        
        
def build_the_node():
    new_node = Node()
    new_node.full_word = False
    return new_node

def suggestor_alg(name: str):
    algorithm = ""
    closest_words = list()
    for i in range(len(name) - 1):
        temp = list(name)
        temp[i] = ".?"
        algorithm += ''.join(temp) + "|"
    algorithm += name
    with open("words.txt", "r") as file:
        words = file.read()
        
        closest_words = re.findall(algorithm, words)
    closest_words = list(set(closest_words))
    return closest_words

def insertion(name:str, root:Node):
    temp = root
    name = name.lower()
    if name.isalpha():
        for i in name:
            index = ord(i) - ord('a')
            
            if temp.children[index] is None:
                temp.children[index] = build_the_node()
            temp = temp.children[index]
            
        temp.full_word = True
    return "The insertion compeleted: " + name


def deletion(name:str, root:Node):
    temp = root
    name = name.lower()
    for i in name:
        index = ord(i) - ord('a')
        if temp.children[index] is not None:
            temp = temp.children[index]
        else:
            return "The word even not exist: " + name
            
    if temp.full_word:
        temp.full_word = False
        return "The deletion compeleted: " + name



def search(name:str, root:Node):
    temp = root
    exist_flag = True
    for i in name:
        index = ord(i) - ord('a')
        
        if temp.children[index] is not None:
            temp = temp.children[index]
        else:
            exist_flag = False
            break
            
    if temp.full_word and exist_flag :
        return "The word exsist: " + name
    else:
        w = ""
        result = suggestor_alg(name=name)
        for i in result:
            w += f"{i}\n"
        return f"The word {name} is not exist" + "\nMaybe you have a typo see this word: \n" + w
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Autocomplete(root)
    
    try:
        print("Try to find a word_file and load it ...")
        with open("words.txt", "r") as file:
            lines = file.read().split()
            for line in lines:
                insertion(line.lower(), app.node)
    except FileNotFoundError:
        os.system("wget -O words.txt https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")
        
        print("The program is loading ...")
        with open("words.txt", "r") as file:
            lines = file.read().split()
            for line in lines:
                insertion(line.lower(), app.node)
    root.mainloop()
     
