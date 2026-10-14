from tkinter import *
from tkinter import messagebox
import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    user='root',
    password='pass@123',
    host='localhost',
    database='KumarAyush_S025'
)

cursor = conn.cursor()


class EmployeeManagement:

    def __init__(self, root):
        self.root = root
        self.root.title("Employee Update and Delete")
        self.root.geometry("500x350")

        self.f = Frame(root, height=350, width=500)
        self.f.pack()

        # Labels
        self.l1 = Label(self.f, text="Employee ID:")
        self.l2 = Label(self.f, text="Employee Name:")
        self.l3 = Label(self.f, text="Employee Skill:")

        # Entry fields
        self.e1 = Entry(self.f, width=25)
        self.e2 = Entry(self.f, width=25)
        self.e3 = Entry(self.f, width=25)

        # Place labels and entry fields
        self.l1.place(x=50, y=40)
        self.e1.place(x=200, y=40)

        self.l2.place(x=50, y=80)
        self.e2.place(x=200, y=80)

        self.l3.place(x=50, y=120)
        self.e3.place(x=200, y=120)

        # Buttons
        self.b1 = Button(
            self.f, text="Update",
            command=self.update_employee
        )
        self.b1.place(x=100, y=180)

        self.b2 = Button(
            self.f, text="Delete",
            command=self.delete_employee
        )
        self.b2.place(x=200, y=180)

        self.b3 = Button(
            self.f, text="Clear",
            command=self.clear_fields
        )
        self.b3.place(x=300, y=180)

    # Update employee details
    def update_employee(self):
        try:
            emp_id = int(self.e1.get())
            emp_name = self.e2.get().strip()
            emp_skill = self.e3.get().strip()

            if not emp_name:
                messagebox.showerror(
                    "Error", "Employee name cannot be empty."
                )
                return

            if len(emp_name) > 20 or len(emp_skill) > 20:
                messagebox.showerror(
                    "Error",
                    "Name and skill must not exceed 20 characters."
                )
                return

            # First, check whether the employee exists
            cursor.execute(
                "SELECT e_id FROM Employee WHERE e_id = %s",
                (emp_id,)
            )

            if cursor.fetchone() is None:
                messagebox.showerror(
                    "Error", "Employee ID does not exist."
                )
                return

            # Update the employee record
            sql = """
                UPDATE Employee
                SET e_name = %s, e_skill = %s
                WHERE e_id = %s
            """

            cursor.execute(sql, (emp_name, emp_skill, emp_id))

            if cursor.rowcount == 0:
                conn.commit()
                messagebox.showinfo(
                    "Result",
                    "Employee exists, but the values are unchanged."
                )
            else:
                conn.commit()
                messagebox.showinfo(
                    "Success",
                    "Employee details updated successfully."
                )

        except ValueError:
            messagebox.showerror(
                "Input Error", "Employee ID must be an integer."
            )

        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Database Error", str(err))

    # Delete employee record
    def delete_employee(self):
        try:
            emp_id = int(self.e1.get())

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete Employee ID {emp_id}?"
            )

            if not confirm:
                return

            sql = "DELETE FROM Employee WHERE e_id = %s"
            cursor.execute(sql, (emp_id,))

            if cursor.rowcount == 0:
                conn.rollback()
                messagebox.showinfo(
                    "Result", "Employee ID not found."
                )
            else:
                conn.commit()
                messagebox.showinfo(
                    "Success", "Employee record deleted successfully."
                )
                self.clear_fields()

        except ValueError:
            messagebox.showerror(
                "Error", "Employee ID must be an integer."
            )
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Database Error", str(err))

    # Clear all entry fields
    def clear_fields(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)

    # Close database connection when window closes
    def close_app(self):
        cursor.close()
        conn.close()
        self.root.destroy()


root = Tk()
obj = EmployeeManagement(root)
root.protocol("WM_DELETE_WINDOW", obj.close_app)
root.mainloop()