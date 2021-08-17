import tkinter as tk
import mah
import re

OPERATOR_COLOR = "#1a1a1a"
NUM_COLOR = "#000000"
BACKGROUND = "#262626"
FOREGROUND = "#ffffff"
ANSWER = "#d9d9d9"


class Calculator:
    def __init__(self):
        self.answer = tk.StringVar()
        self.equation = tk.StringVar()
        self.expression = ""
        self.paren = False
        self.prev_expression = []
        self.itr = ""

    def set_prev_expr(self):
        self.prev_expression.append(self.expression)

    def get_prev_expr(self):
        try:
            self.expression = self.prev_expression.pop()
            self.equation.set(self.expression)
        except IndexError:
            self.answer.set("Can't undo")

    def clear(self):
        self.set_prev_expr()
        self.paren = False
        self.expression = ""
        self.answer.set(self.expression)
        self.equation.set(self.expression)
        self.itr = ""

    def insert_paren(self):
        self.set_prev_expr()
        if not self.paren:
            self.expression += "("
            self.equation.set(self.expression)
            self.paren = True
        else:
            self.expression += ")"
            self.paren = False
            self.equation.set(self.expression)

    def percent(self):
        self.set_prev_expr()
        self.expression += " / 100"
        self.evaluate(self.expression)

    def square(self):
        self.set_prev_expr()
        if True:
            match = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', self.expression)
            try:
                last = float(self.evaluate(match.pop(-1)))
                self.expression = " ".join(match) + " " + str(math.pow(last, 2))
                self.evaluate(self.expression)
            except:
                self.answer.set("Cannot Calculate self.answer")

    def press(self, num: str):
        self.set_prev_expr()
        if num in ["*", "/", "+", "-"]:
            self.expression = str(self.expression) + "" + str(num) + ""
        else:
            self.expression = str(self.expression) + str(num)
        self.equation.set(self.expression)

    def square_root(self):
        self.set_prev_expr()
        if True:
            match = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', self.expression)
            try:
                last = float(self.evaluate(match.pop(-1)))
                self.expression = " ".join(match) + " " + str(math.sqrt(last))
                self.evaluate(self.expression)
            except IndexError:
                pass
            except ValueError and TypeError:
                self.answer.set("Imaginary self.answer")

    def backspace(self):
        self.set_prev_expr()
        try:
            if self.expression[-1] == ")":
                self.paren = True
            if self.expression[-1] == "(":
                self.paren = False
            self.expression = self.expression[:-1]
        except IndexError:
            pass
        self.equation.set(self.expression)

    def _weight(self, op):
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        return 0

    def _arith(self, a, b, op):
        try:
            if op == '+':
                return a + b
            elif op == '-':
                return a - b
            elif op == '*':
                return a * b
            elif op == '/':
                return a / b
            else:
                return None
        except ZeroDivisionError:
            self.answer.set("ZeroDivisionError")
            return "ZeroDiv"
        except TypeError:
            self.answer.set("Syntax Error")
            return "Syntax Error"

    def evaluate(self, tokens: str):
        self.set_prev_expr()
        token_lst = tokens.split(" ")
        for index, elem in enumerate(token_lst):
            if "-" in elem:
                token_lst[index] = elem.replace("-", "(0 -") + ")"
        tokens = " ".join(token_lst)
        values = []
        ops = []
        i = 0
        while i < len(tokens):
            if tokens[i] == ' ':
                i += 1
                continue

            elif tokens[i] == '(':
                ops.append(tokens[i])

            elif (tokens[i].isdigit()) or (tokens[i] == "."):
                val = ""

                while (i < len(tokens) and
                       (tokens[i].isdigit() or tokens[i] == ".")):
                    val += str(tokens[i])
                    i += 1
                try:
                    val = float(val)
                except ValueError:
                    self.answer.set("Syntax Error")
                    self.get_prev_expr()
                    self.get_prev_expr()
                    return None
                except TypeError:
                    self.answer.set("Syntax Error")
                    self.get_prev_expr()
                    self.get_prev_expr()
                    return None
                values.append(val)
                i -= 1

            elif tokens[i] == ')':
                while len(ops) != 0 and ops[-1] != '(':
                    try:
                        val2 = values.pop()
                        val1 = values.pop()
                        op = ops.pop()
                    except IndexError:
                        self.answer.set("Syntax Error")
                        self.get_prev_expr()
                        self.get_prev_expr()
                        return None
                    values.append(self._arith(val1, val2, op))
                    if values[-1] == "ZeroDiv":
                        return None

                ops.pop()

            else:
                while (len(ops) != 0 and
                       self._weight(ops[-1]) >=
                       self._weight(tokens[i])):

                    try:
                        val2 = values.pop()
                        val1 = values.pop()
                        op = ops.pop()
                    except IndexError:
                        self.answer.set("Syntax Error")
                        self.get_prev_expr()  # Returns expr to previous state
                        self.get_prev_expr()
                        return None

                    values.append(self._arith(val1, val2, op))
                    if values[-1] == "ZeroDiv":
                        return None

                ops.append(tokens[i])
            i += 1

        while len(ops) != 0:
            try:
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
            except IndexError:
                self.answer.set("Syntax Error")
                self.get_prev_expr()
                self.get_prev_expr()
                return None

            values.append(self._arith(val1, val2, op))
            if values[-1] == "ZeroDiv":
                return None

        try:
            if values[-1] % 1 == 0:
                values[-1] = int(values[-1])
            if (values[-1] >= 9.9e+8) or (values[-1] <= -9.9e+8):
                raise OverflowError
            values[-1] = round(values[-1], 10)  # rounds a decimal number to 10 digits (max on screen is 20)
            self.expression = str(values[-1])  # If the self.answer starts with a dash replace with neg marker
            self.equation.set(self.expression)
            self.answer.set(self.expression)

            return values[-1]
        except SyntaxError:
            self.answer.set("Syntax Error")
            return None
        except OverflowError:
            self.answer.set("Overflow")
            self.get_prev_expr()  # Returns to previous state (for special funct) deletes extra step in normal ops
            self.get_prev_expr()
            return None
        except IndexError:
            pass
        except TypeError:
            pass


class CalcGui(Calculator):
    BOX_HEIGHT = 2
    BOX_WIDTH = 6

    def __init__(self, main_win: object):
        self.buttons = [  # List of all button info
            # chr.    x  y  color                command
            ("%", 0, 0, OPERATOR_COLOR, self.percent),
            ("CE", 1, 0, OPERATOR_COLOR, self.get_prev_expr),
            ("C", 2, 0, OPERATOR_COLOR, self.clear),
            ("⌫", 3, 0, OPERATOR_COLOR, self.backspace),
            ("()", 0, 1, OPERATOR_COLOR, self.insert_paren),
            ("x²", 1, 1, OPERATOR_COLOR, self.square),
            ("√x", 2, 1, OPERATOR_COLOR, self.square_root),
            ("÷", 3, 1, OPERATOR_COLOR, lambda: self.press("/")),
            ("7", 0, 2, NUM_COLOR, lambda: self.press("7")),
            ("8", 1, 2, NUM_COLOR, lambda: self.press("8")),
            ("9", 2, 2, NUM_COLOR, lambda: self.press("9")),
            ("x", 3, 2, OPERATOR_COLOR, lambda: self.press("*")),
            ("4", 0, 3, NUM_COLOR, lambda: self.press("4")),
            ("5", 1, 3, NUM_COLOR, lambda: self.press("5")),
            ("6", 2, 3, NUM_COLOR, lambda: self.press("6")),
            ("-", 3, 3, OPERATOR_COLOR, lambda: self.press("-")),
            ("1", 0, 4, NUM_COLOR, lambda: self.press("1")),
            ("2", 1, 4, NUM_COLOR, lambda: self.press("2")),
            ("3", 2, 4, NUM_COLOR, lambda: self.press("3")),
            ("+", 3, 4, OPERATOR_COLOR, lambda: self.press("+")),
            ("+/-", 0, 5, NUM_COLOR, lambda: self.press("-")),
            ("0", 1, 5, NUM_COLOR, lambda: self.press("0")),
            (".", 2, 5, NUM_COLOR, lambda: self.press(".")),
            ("=", 3, 5, "#264d73", lambda: self.evaluate(self.expression)),
        ]
        self.main_win = main_win
        Calculator.__init__(self)
        self.create_text_canvas()
        self.create_button_canvas()

    def create_text_canvas(self):
        entry_canv = tk.Canvas(bg=BACKGROUND, highlightthickness=0)
        ans_box = tk.Label(entry_canv, width=20, textvariable=self.answer, bg=BACKGROUND, fg=ANSWER,
                           font=("Arial", 15, 'bold'))
        ans_box.pack(pady=(15, 5),)
        entry1 = tk.Label(entry_canv, width=10, textvariable=self.equation, bg=BACKGROUND, fg=FOREGROUND,
                          font=("Arial", 30, 'bold'), border=0)
        entry1.pack(pady=(0, 10))
        entry_canv.pack(pady=40)

    def create_button_canvas(self):
        button_canv = tk.Canvas(bg=BACKGROUND, highlightthickness=0)  # Contains Input buttons
        for (character, x, y, color, command) in self.buttons:
            button = tk.Button(button_canv, text=character, bg=color,  # Unique
                               relief=tk.RAISED, height=self.BOX_HEIGHT, width=self.BOX_WIDTH, border=0,
                               fg=FOREGROUND, font=("Arial", 14, 'normal'))  # Defaults
            button.grid(row=y, column=x, padx=1, pady=1)
            button.configure(command=command)
        button_canv.pack(padx=2, pady=(8, 2))


window = tk.Tk()
window.configure(background=BACKGROUND)
window.title("Calculator")
window.attributes('-alpha', 0.95)  # to add transparency effect
window.resizable(False, False)
CalcGui(window)

window.mainloop()
