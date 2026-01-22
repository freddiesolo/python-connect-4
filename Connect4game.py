from tkinter import *
from tkinter import messagebox


class ConnectFourController:
    def __init__(self, columns=7, rows=6, player1='X', player2='O'):
        self.size = {'c': columns, 'r': rows}  # 7 columns x 6 rows
        self.grid = []
        self.first_player = True  # Set player 1 to active if True,  But False -  set player 2 active and on the move
        self.players = {True: player1, False: player2}  # Anything except ? (question mark) AND 1 character only!
        self.game_over = False
        self.grid = [[] for i in range(self.size['c'])]

    # Check and Returns True if disc was successfully dropped, False if not
    def drop(self, column):  # Drop a disc into a column
        if self.game_over: return False  # game ended.

        if column < 0 or column >= self.size['c']:
            return False
        if len(self.grid[column]) >= self.size['r']:
            return False

        self.grid[column].append(self.players[self.first_player])

        c = self.check_progress()
        if c == False:
            self.first_player = not self.first_player
            return True
        else:
            self.game_over = c
            return True

    # Returns False - meaning game is on OR 'win'/'draw' meaning game is over.
    def check_progress(self):  # Check whether player has won or forced draw.
        disk = 0  # Number of discs
        for i, column in enumerate(self.grid):
            disk += len(self.grid[i])
            for j, row in enumerate(column):
                h = i + 4 <= self.size['c']
                v = j + 4 <= len(self.grid[i])

                if v:  # Check vertically (four fields to the right)
                    if 1 == len(set(self.grid[i][j:j + 4])):
                        return 'win'

                if h:  # Check horizontally (four fields up)
                    if len(self.grid[i]) > j and len(self.grid[i + 1]) > j and len(self.grid[i + 2]) > j and len(
                            self.grid[i + 3]) > j:
                        s_r = set()
                        for k in range(4):
                            s_r.add(self.grid[i + k][j])
                        if 1 == len(s_r):
                            return 'win'

                if h:  # Check diagonally (up-right)
                    s = set()
                    for k in range(4):
                        if len(self.grid[i + k]) > j + k:
                            s.add(self.grid[i + k][j + k])
                        else:
                            s.add('??')
                    if 1 == len(s):
                        return 'win'

                if h and j - 4 + 1 >= 0:  # Check diagonally (down-right)
                    s = set()
                    for k in range(4):
                        if len(self.grid[i + k]) > j - k:
                            s.add(self.grid[i + k][j - k])
                        else:
                            s.add('??')
                    if 1 == len(s):
                        return 'win'

        if disk == self.size['c'] * self.size['r']:
            return 'draw'
        return False


class ConnectFour:
    element_size = 50
    border_grid = 3
    grid_color = "#D7D7D7"
    player_one_color = "#E7E700"
    player_two_color = "#EE0000"
    background_color = "#A08C64"
    start_game = False

    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Connect 4 Game")

        self.admin_radio_value = IntVar()
        self.admin_radio_value.set(0)

        self.admin_operation = IntVar()
        self.admin_operation.set(0)

        self.main_window()

    def main_window(self):
        main_frame = Frame(self.root)
        main_frame.pack(pady=10)

        mode_label = Label(main_frame, text="Please select how you would like to enter:", font=("Arial", 14))
        mode_label.pack()

        admin_radio = Radiobutton(main_frame, text="Administrator", variable=self.admin_radio_value, value=1,
                                  font=("Arial", 12))
        admin_radio.pack(pady=5)

        user_radio = Radiobutton(main_frame, text="User/Player", variable=self.admin_radio_value, value=2,
                                 font=("Arial", 12))
        user_radio.pack(pady=5)

        submit_button = Button(main_frame, text="Submit", font=("Arial", 12), command=self.submit)
        submit_button.pack(pady=10)

    def submit(self):
        if self.admin_radio_value.get() == 1:
            self.admin_window()
        else:
            self.user_form()

    def admin_window(self):
        admin_login_window_frame = Toplevel(self.root)
        admin_login_window_frame.title("Administrator Login")
        admin_login_window_frame.resizable(False, False)
        admin_login_window_frame.geometry("250x200")
        admin_login_window_frame.grab_set()

        width_for_label = '300'  # Set the width of the label to the width of the parent window

        label_text = "Administrator"  # Create a label with bold text
        header = Label(admin_login_window_frame, text=label_text, bg="#A2C1E5", font=("Arial", 14, "bold"))

        # Pack the label into the window
        header.place(x=0, y=0, width=250)

        lbl_info = Label(admin_login_window_frame, text="Enter The Administrator Details:", font=("Arial", 10, "bold"))
        lbl_info.place(x=10, y=40)

        lbl_username = Label(admin_login_window_frame, text="Username:")
        lbl_username.place(x=10, y=80)

        txt_username = Entry(admin_login_window_frame)
        txt_username.place(x=100, y=80)

        lbl_password = Label(admin_login_window_frame, text="Password:")
        lbl_password.place(x=10, y=110)

        txt_password = Entry(admin_login_window_frame, show="*")
        txt_password.place(x=100, y=110)

        btn_submit = Button(admin_login_window_frame, text="Submit",
                            command=lambda: self.admin_login(admin_login_window_frame, txt_username.get(),
                                                                    txt_password.get()))
        btn_submit.place(x=100, y=150)

    def admin_login(self, admin_window, username, password):
        # Validate the username and password
        with open("users_information.txt", "r") as f:
            users = [line.strip().split(",") for line in f]

        # Check if the entered username and password match any of the users in the file
        for user in users:
            if username == user[0] and password == user[1]:
                if user[2] == 'administrator':
                    messagebox.showinfo("Login", "Login Successful!")
                    self.admin_dashboard()
                    admin_window.destroy()
                    return
                else:
                    messagebox.showerror("Access Denied", "You are not authorized to access this page")
                    return

        messagebox.showerror("Error", "Invalid username or password")

    def user_form(self):
        users_form = Toplevel(self.root)
        users_form.title("User Login")
        users_form.resizable(False, False)
        users_form.geometry("300x300")
        users_form.grab_set()

        width_for_label = '300'  # Set the width of the label to the width of the parent window

        label_text = "Login For Connect 4 Game"  # Create a label with bold text
        header = Label(users_form, text=label_text, bg="#A2C1E5", font=("Arial", 14, "bold"))

        header.place(x=0, y=0, width=300)  # Place the label into the window

        lbl_info = Label(users_form, text="Player 1:", font=("Arial", 10, "bold"))
        lbl_info.place(x=10, y=40)

        username_one = Label(users_form, text="Username:")
        username_one.place(x=10, y=70)

        txt_username_one = Entry(users_form)
        txt_username_one.place(x=100, y=70)

        password_one = Label(users_form, text="Password:")
        password_one.place(x=10, y=100)

        txt_password_one = Entry(users_form, show="*")
        txt_password_one.place(x=100, y=100)

        lbl_info = Label(users_form, text="Player 2:", font=("Arial", 10, "bold"))
        lbl_info.place(x=10, y=140)

        username_one = Label(users_form, text="Username:")
        username_one.place(x=10, y=170)

        txt_username_two = Entry(users_form)
        txt_username_two.place(x=100, y=170)

        password_two = Label(users_form, text="Password:")
        password_two.place(x=10, y=200)

        txt_password_two = Entry(users_form, show="*")
        txt_password_two.place(x=100, y=200)

        btn_submit = Button(users_form, text="Submit",
                            command=lambda: self.check_users_login(users_form, txt_username_one.get(),
                                                                   txt_password_one.get(), txt_username_two.get(),
                                                                   txt_password_two.get()))
        btn_submit.place(x=100, y=250)

    def check_users_login(self, admin_window, username1, password1, username2, password2):

        user_one = user_two = False

        # Open the text file and read the usernames and passwords
        with open("users_information.txt", "r") as f:
            users = [line.strip().split(",") for line in f]

        # Check if the entered username and password match any of the users in the file
        for user in users:
            if username1 == user[0] and password1 == user[1]:
                user_one = True

            if username2 == user[0] and password2 == user[1]:
                user_two = True

        if user_one and user_two:
            messagebox.showinfo("Login", "Login Successful!")
            admin_window.destroy()
            self.connect_4_ui()
            return

        messagebox.showerror("Login", "Invalid Username or Password")

    def admin_dashboard(self):
        administrator_panel = Toplevel(self.root)
        administrator_panel.title("Administrator Panel")
        administrator_panel.resizable(False, False)
        administrator_panel.geometry("250x300")
        administrator_panel.grab_set()

        width_for_label = '300'  # Set the width of the label to the width of the parent window

        lbl_admin_panel_label_text = "Administrator Panel"  # Create a label with bold text
        lbl_admin_panel_header = Label(administrator_panel, text=lbl_admin_panel_label_text, bg="#A2C1E5",
                                       font=("Arial", 14, "bold"))
        lbl_admin_panel_header.place(x=0, y=0, width=250)

        lbl_admin_panel_info = Label(administrator_panel, text="Enter User Details:", font=("Arial", 10, "bold"))
        lbl_admin_panel_info.place(x=10, y=40)

        admin_panel_username = Label(administrator_panel, text="Username:")
        admin_panel_username.place(x=10, y=80)

        txt_admin_panel_username = Entry(administrator_panel)
        txt_admin_panel_username.place(x=100, y=80)

        admin_panel_password = Label(administrator_panel, text="Password:")
        admin_panel_password.place(x=10, y=110)

        txt_admin_panel_password = Entry(administrator_panel, show="*")
        txt_admin_panel_password.place(x=100, y=110)

        lbl_admin_panel_info2 = Label(administrator_panel, text="What do you want to do?:", font=("Arial", 11, "bold"))
        lbl_admin_panel_info2.place(x=10, y=140)

        admin_panel_create = Radiobutton(administrator_panel, text="Create user account",
                                               variable=self.admin_operation, value=1, font=("Arial", 10))
        admin_panel_create.place(x=10, y=170)

        admin_panel_delete = Radiobutton(administrator_panel, text="Remove user account",
                                               variable=self.admin_operation, value=2, font=("Arial", 10))
        admin_panel_delete.place(x=10, y=200)

        admin_panel_btn_submit = Button(administrator_panel, text="Submit",
                                        command=lambda: self.perform_admin_operation(txt_admin_panel_username.get(),
                                                                                     txt_admin_panel_password.get()))
        admin_panel_btn_submit.place(x=100, y=240)

    def perform_admin_operation(self, username, password):
        if self.admin_operation.get() == 1:
            self.create_new_user(username, password)
        else:
            self.remove_user_record(username, password)

    def create_new_user(self, username, password):
        # Open users information text file in append mode i.e you can add record to it
        with open('users_information.txt', 'a') as users_file:
            # Write the username supplied and password supplied to the text file
            if users_file.write(username + ',' + password + ',user' + '\n'):
                messagebox.showinfo("New User", "New user has been added successfully!")
            else:
                messagebox.showerror("Error", "An error occured, unable to add new user record!")

    def remove_user_record(self, username, password):
        exist = 0
        with open("users_information.txt", "r") as f:
            lines = f.readlines()

        with open("users_information.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != f"{username},{password}":
                    f.write(line)
                else:
                    exist = 1
        if exist == 1:
            messagebox.showinfo("Remove User", "User has been deleted successfully!")
        else:
            messagebox.showerror("Not Found", "The username and password not exist in the record list!")

    def connect_4_ui(self):
        self.game_panel = Toplevel(self.root)
        self.canvas = Canvas(self.game_panel, width=200, height=50, background=self.background_color,
                             highlightthickness=0)
        self.canvas.grid(row=2)

        self.current_player_variable = StringVar(self.game_panel, value="")
        self.current_player_label = Label(self.game_panel, textvariable=self.current_player_variable, anchor=W)
        self.current_player_label.grid(row=3)

        self.canvas.bind('<Button-1>', self.click_canvas)
        self.newGame()

    def newGame(self):
        self.player1 = 'Yellow'
        self.player2 = 'Red'

        columns = 7
        rows = 6

        self.game = ConnectFourController(columns=columns, rows=rows)

        self.canvas.delete(ALL)
        self.canvas.config(width=(self.element_size) * self.game.size['c'],
                           height=(self.element_size) * self.game.size['r'])
        self.game_panel.update()  
        self.draw_grid_layout()
        self.draw_layout()

        self.update_player_state()

        self.start_game = True

    def draw_layout(self):
        for c in range(self.game.size['c']):
            for r in range(self.game.size['r']):
                if r >= len(self.game.grid[c]): continue

                x0 = c * self.element_size
                y0 = r * self.element_size
                x1 = (c + 1) * self.element_size
                y1 = (r + 1) * self.element_size
                fill = self.player_one_color if self.game.grid[c][r] == self.game.players[
                    True] else self.player_two_color
                self.canvas.create_oval(x0 + 2,
                                        self.canvas.winfo_height() - (y0 + 2),
                                        x1 - 2,
                                        self.canvas.winfo_height() - (y1 - 2),
                                        fill=fill, outline=self.grid_color)

    def draw_grid_layout(self):
        x0, x1 = 0, self.canvas.winfo_width()
        for row in range(1, self.game.size['r']):
            y = row * self.element_size
            self.canvas.create_line(x0, y, x1, y, fill=self.grid_color)

        y0, y1 = 0, self.canvas.winfo_height()
        for column in range(1, self.game.size['c']):
            x = column * self.element_size
            self.canvas.create_line(x, y0, x, y1, fill=self.grid_color)

    def drop_column(self, column):
        return self.game.drop(column)

    def update_player_state(self):
        player = self.player1 if self.game.first_player else self.player2
        self.current_player_variable.set('Current player: ' + player)

    def click_canvas(self, activity):
        if not self.start_game: return
        if self.game.game_over: return

        column = activity.x // self.element_size

        if (0 <= column < self.game.size['c']):
            self.drop_column(column)
            self.draw_layout()
            self.update_player_state()

        if self.game.game_over:
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            if self.game.game_over == 'draw':
                response = 'DRAW!'
            else:
                winner = self.player1 if self.game.first_player else self.player2
                response = winner + ' won!'
            self.canvas.create_text(x, y, text=response, font=("Helvetica", 32), fill="#333")
            result = messagebox.askyesno("Confirmation", response + "\nDo you want to start a new game?")
            if result == 1:
                self.newGame()
            else:
                self.game_panel.destroy()


if __name__ == '__main__':
    root = Tk()
    root.geometry("400x300")  # this will set the width size and height size of the window
    root.resizable(False, False)  # this will disable resizing in both directions of the window
    connect_four = ConnectFour(root)
    root.mainloop()
