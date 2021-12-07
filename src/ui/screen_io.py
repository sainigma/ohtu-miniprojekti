import os
import sys
import curses
import npyscreen

class ScreenIO(npyscreen.NPSApp):
    def main(self):
      pass

    def write(self, value) -> None:
      print(value)

    def read(self, prompt) -> str:
      return input(prompt)

if os.getenv("EXPERIMENTAL") == "True":
  screen_io = ScreenIO()
else:
  screen_io = None