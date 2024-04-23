import flet as ft
import pyautogui as screen
import time, threading, random
from datetime import datetime

screen_width, screen_height = screen.size()

def main(page: ft.Page):
    page.title = "Automatic Cursor"
    page.padding = ft.padding.symmetric(0, 50)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def write_log(message: str):
        """
        Write a message to the log.

        Parameters:
            message (str): The message to be written to the log.
        """

        text = ft.Text(message, color=ft.colors.GREY_600)
        log_column.controls.append(text)
        page.update()


    def move_cursor():
        """
        Move the cursor to a random position on the screen and click on the taskbar.
        """

        x1 = random.randint(0, screen_width)
        y1 = random.randint(0, screen_height)
        task_bar_x = int(screen_width * 0.8)
        task_bar_y = screen_height - 30
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            screen.moveTo(x1, y1)
            log_message = f"{timestamp}: Cursor moved to ({screen.position().x}, {screen.position().y})\n"
            screen.click(task_bar_x, task_bar_y)
            write_log(log_message)
            
        except screen.FailSafeException as e:
            print(f"A fail-safe error has occurred: {e}")
            print(f"Recalculating coordinates...")
            move_cursor()

        
    def move_loop(wait_time: float):
        """
        Continuously move the cursor with a given interval.
        
        Parameters:
            wait_time (float): The interval between cursor movements.
        """

        while not stop_movement_flag.is_set():
            move_cursor()
            time.sleep(wait_time)


    def start_movement():
        """
        Start cursor movement with user-defined interval.
        """

        interval_str = seconds_input.value

        try:
            interval = float(interval_str)
            if interval <= 0:
                raise ValueError("The time interval must be a positive number.")

            global stop_movement_flag
            stop_movement_flag = threading.Event()
            write_log("Movement Started.\n")

            movement_thread = threading.Thread(target=move_loop, args=(interval,))
            movement_thread.start()
        
        except ValueError:
            seconds_input.focus()

        
    def stop_movement_func():
        """
        Stop cursor movement.
        """

        stop_message = "Movement Stopped.\n"
        write_log(stop_message)
        if stop_movement_flag:
            stop_movement_flag.set()

    def clear_log():
        """
        Clear log messages.
        """

        log_column.controls = []
        page.update()


    start_button = ft.ElevatedButton(
        "Start Movement",
        adaptive=True,
        width=160,
        on_click=lambda e : start_movement()
    )

    stop_button = ft.ElevatedButton(
        "Stop Movement",
        adaptive=True,
        width=160,
        on_click=lambda e : stop_movement_func()
    )

    clear_button = ft.ElevatedButton(
        "Clear Log",
        adaptive=True,
        width=160,
        on_click=lambda e : clear_log()
    )

    seconds_input = ft.TextField(label="Interval time (seconds)", hint_text=40)

    column = ft.Column(
        spacing=30,
        tight=True,
        controls=[start_button, stop_button, seconds_input, clear_button]
    )

    buttons_container = ft.Container(
        expand=1,
        content=column,
        margin=10,
        padding=ft.padding.symmetric(10, 0),
        height=500
    )
    
    log_column = ft.ListView(
        spacing=0.2,
        padding=10,
        auto_scroll=True,
    )

    log_container = ft.Container(
        expand=3,
        content=log_column,
        margin=ft.margin.all(0),
        padding=ft.padding.all(15), 
        bgcolor=ft.colors.WHITE,
        border=ft.border.all(2, ft.colors.BLACK),
        width=800,
        height=500
        )
    
    row = ft.Row(
        spacing=10,
        controls=[buttons_container, log_container],
    )
    
    page.add(row)

if __name__ == "__main__":
    ft.app(target=main)