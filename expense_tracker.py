import tkinter as tk
from tkinter import messagebox

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.roommates = []
        self.expenses = {}

        # Labels for adding roommate
        self.label_roommate = tk.Label(root, text="Roommate:")
        self.label_roommate.grid(row=0, column=0, padx=10, pady=10)

        # Entry widget for entering roommate name
        self.entry_roommate = tk.Entry(root)
        self.entry_roommate.grid(row=0, column=1, padx=10, pady=10)

        # Button to add roommate
        self.add_roommate_button = tk.Button(root, text="Add Roommate", command=self.add_roommate)
        self.add_roommate_button.grid(row=0, column=2, padx=10, pady=10)

        # Label to display success message
        self.label_success_message = tk.Label(root, text="")
        self.label_success_message.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Labels for entering expense details
        self.label_amount = tk.Label(root, text="Bill Amount:")
        self.label_amount.grid(row=2, column=0, padx=10, pady=10)

        self.entry_amount = tk.Entry(root)
        self.entry_amount.grid(row=2, column=1, padx=10, pady=10)

        self.label_payer = tk.Label(root, text="Payer:")
        self.label_payer.grid(row=3, column=0, padx=10, pady=10)

        self.entry_payer = tk.Entry(root)
        self.entry_payer.grid(row=3, column=1, padx=10, pady=10)

        self.add_expense_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=3, column=2, padx=10, pady=10)

        self.text_expenses = tk.Text(root, height=10, width=40)
        self.text_expenses.grid(row=4, column=0, columnspan=3, pady=10)

        self.view_button = tk.Button(root, text="View Individual Expenses", command=self.view_individual_expenses)
        self.view_button.grid(row=5, column=0, columnspan=3, pady=10)

    def add_roommate(self):
       roommate_name = self.entry_roommate.get().strip()
       if not roommate_name:
           self.label_success_message.config(text="Please enter a roommate name.")
           return
       if roommate_name in self.roommates:
           self.label_success_message.config(text="Roommate already added.")
           return
       self.roommates.append(roommate_name)
       self.expenses[roommate_name] = 0
       self.label_success_message.config(text=f"Roommate {roommate_name} added successfully.")
       self.entry_roommate.delete(0, tk.END)

    def add_expense(self):
        amount = self.entry_amount.get()
        payer = self.entry_payer.get()

        if not amount or not payer:
            messagebox.showwarning("Error", "Please enter both bill amount and payer's name.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Error", "Invalid amount. Please enter a number.")
            return

        if payer not in self.roommates:
            messagebox.showwarning("Error", "Payer not found in the list of roommates.")
            return

        self.expenses[payer] -= amount
        share_per_person = amount / (len(self.roommates) - 1)

        for roommate in self.roommates:
            if roommate != payer:
                self.expenses[roommate] += share_per_person

        self.update_expenses_text()
        messagebox.showinfo("Success", f"Expense of ₹{amount} paid by {payer} added successfully.")
        self.entry_amount.delete(0, tk.END)
        self.entry_payer.delete(0, tk.END)

    def update_expenses_text(self):
        self.text_expenses.delete(1.0, tk.END)
        self.text_expenses.insert(tk.END, "Individual Expenses:\n")
        
        for roommate, expense in self.expenses.items():
            if expense > 0:
                self.text_expenses.insert(tk.END, f"{roommate} owes ₹{expense:.2f} to {self.entry_payer.get()}\n")
            elif expense < 0:
                self.text_expenses.insert(tk.END, f"{roommate} is owed ₹{-expense:.2f} by {self.entry_payer.get()}\n")
            else:
                self.text_expenses.insert(tk.END, f"{roommate} has no transactions with {self.entry_payer.get()}\n")

    def view_individual_expenses(self):
        self.update_expenses_text()
        messagebox.showinfo("Individual Expenses", self.text_expenses.get(1.0, tk.END))


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()