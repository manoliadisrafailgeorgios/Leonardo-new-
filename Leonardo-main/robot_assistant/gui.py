# -*- coding: utf-8 -*-
import tkinter as tk
import random
from tkinter import font

class RobotGUI:
    def __init__(self):
        self.root = tk.Tk()
        
        self.width = 800
        self.height = 480
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.overrideredirect(False) 
        self.root.configure(bg="black")
        self.root.config(cursor="none")
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)

        self.emo_font = font.Font(family="FreeMonoBold", size=20, weight="bold")

        self.state = "idle"
        self.current_text = ""
        self.mouth_open = False
        self.is_blinking = False
        self.face_found = False 

        self.lx, self.ly = 250, 180
        self.rx, self.ry = 550, 180
        self.dx, self.dy = 0, 0

        self.draw_face()
        self.animate_mouth()
        self.move_eyes()
        self.blink()

    def set_eye_target(self, found, dx, dy):
        self.face_found = found
        if found:
            # Eyes map exactly to your coordinates
            self.dx = -dx
            self.dy = dy
        else:
            self.dx = 0
            self.dy = 0
        self.root.after(0, self.draw_face)

    # --- Commands sent from main.py ---
    def listening(self):
        self.state = "listening"
        self.current_text = "Σε ακούω..."
        self.root.after(0, self.draw_face)

    def idle(self):
        self.state = "idle"
        self.current_text = ""
        self.root.after(0, self.draw_face)

    def error(self):
        self.state = "error"
        self.current_text = "Σφάλμα"
        self.root.after(0, self.draw_face)

    def set_emotion(self, emotion):
        self.state = "talking"
        self.current_text = ""
        self.root.after(0, self.draw_face)

    def bring_to_front(self):
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(500, lambda: self.root.attributes('-topmost', False))
        self.root.focus_force()

    # --- Face Drawing Logic ---
    def draw_rounded_square(self, x, y, size, r, color, glow_color):
        w = size // 2
        self.canvas.create_oval(x-w-10, y-w-10, x+w+10, y+w+10, fill=glow_color, outline=glow_color)
        self.canvas.create_arc(x-w, y-w, x-w+r*2, y-w+r*2, start=90, extent=90, style="pieslice", fill=color, outline=color)
        self.canvas.create_arc(x+w-r*2, y-w, x+w, y-w+r*2, start=0, extent=90, style="pieslice", fill=color, outline=color)
        self.canvas.create_arc(x-w, y+w-r*2, x-w+r*2, y+w, start=180, extent=90, style="pieslice", fill=color, outline=color)
        self.canvas.create_arc(x+w-r*2, y+w-r*2, x+w, y+w, start=270, extent=90, style="pieslice", fill=color, outline=color)
        self.canvas.create_rectangle(x-w+r, y-w, x+w-r, y+w, fill=color, outline=color)
        self.canvas.create_rectangle(x-w, y-w+r, x+w, y+w-r, fill=color, outline=color)

    def draw_face(self):
        self.canvas.delete("all")
        main_color = "#33ffff"
        glow_color = "#004444"

        if self.state == "listening":
            main_color = "#00ffcc"
        elif self.state == "error":
            main_color = "#ff3333"
            glow_color = "#440000"

        if self.current_text:
            self.canvas.create_text(self.width//2, 50, text=self.current_text, fill=main_color, font=self.emo_font)

        if self.is_blinking:
            self.canvas.create_line(self.lx-50, self.ly, self.lx+50, self.ly, fill=main_color, width=10, capstyle="round")
            self.canvas.create_line(self.rx-50, self.ry, self.rx+50, self.ry, fill=main_color, width=10, capstyle="round")
        else:
            self.draw_rounded_square(self.lx, self.ly, 110, 30, main_color, glow_color)
            self.draw_rounded_square(self.rx, self.ry, 110, 30, main_color, glow_color)
            px, py = self.lx + self.dx, self.ly + self.dy
            self.canvas.create_oval(px-10, py-10, px+10, py+10, fill="white")
            prx, pry = self.rx + self.dx, self.ry + self.dy
            self.canvas.create_oval(prx-10, pry-10, prx+10, pry+10, fill="white")

        mouth_y = 350
        if self.state == "error":
            self.canvas.create_arc(self.width//2-80, mouth_y, self.width//2+80, mouth_y+100, start=0, extent=180, style="arc", width=10, outline=main_color)
        elif self.state == "talking":
            if self.mouth_open:
                self.canvas.create_oval(self.width//2-40, mouth_y-20, self.width//2+40, mouth_y+20, fill="white")
            else:
                self.canvas.create_line(self.width//2-60, mouth_y, self.width//2+60, mouth_y, fill=main_color, width=10)
        else:
            self.canvas.create_arc(self.width//2-80, mouth_y-50, self.width//2+80, mouth_y+50, start=0, extent=-180, style="arc", width=10, outline=main_color)

    def animate_mouth(self):
        if self.state == "talking":
            self.mouth_open = not self.mouth_open
            self.draw_face()
        self.root.after(200, self.animate_mouth)

    def move_eyes(self):
        if not self.is_blinking and self.state == "idle" and not self.face_found:
            self.dx = random.choice([-20, 0, 20])
            self.dy = random.choice([-10, 0, 10])
            self.draw_face()
        self.root.after(random.randint(1000, 3000), self.move_eyes)

    def blink(self):
        if self.state != "error":
            self.is_blinking = True
            self.draw_face()
            self.root.after(150, self.unblink)
        else:
            self.root.after(3000, self.blink)

    def unblink(self):
        self.is_blinking = False
        self.draw_face()
        self.root.after(random.randint(2000, 5000), self.blink)

    def run(self):
        self.root.mainloop()
