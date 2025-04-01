from datetime import datetime, timedelta, date
import threading
import subprocess
from pathlib import Path
from collections import defaultdict
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static, Input
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from rich.style import Style



# History file path
HISTORY_DIR = Path.home() / ".timy"
HISTORY_FILE = HISTORY_DIR / "history.log"

class PomodoroGraph(Static):
    """A widget to display Pomodoro history like a GitHub contribution graph."""

    pomodoro_data = reactive(lambda: defaultdict(int), layout=True)

    def __init__(self, days=91, **kwargs): # Approx 3 months (13 weeks * 7 days)
        super().__init__(**kwargs)
        self.days_to_display = days
        self.styles.padding = (0, 1)
        self.styles.content_align = ("center", "middle")
        self.load_history()

    def load_history(self) -> None:
        """Load Pomodoro completion data from the history file."""
        counts = defaultdict(int)
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                timestamp = datetime.fromisoformat(line)
                                counts[timestamp.date()] += 1
                            except ValueError:
                                self.app.log(f"Skipping invalid date format in history: {line}")
            except OSError as e:
                self.app.log(f"Error reading history file {HISTORY_FILE}: {e}")
            except Exception as e:
                 self.app.log(f"Unexpected error loading history: {e}")

        self.pomodoro_data = counts
        self.refresh() # Trigger a refresh to render the new data

    def _get_intensity_style(self, count: int) -> Style:
        """Return a style based on the Pomodoro count for a day."""
        if count == 0:
            return Style(color="grey30") # Dark grey for no activity
        elif count == 1:
            return Style(color="bright_green")
        elif count <= 3:
            return Style(color="green")
        elif count <= 6:
            return Style(color="dark_green")
        else: # > 6
            return Style(color="green4") # Darkest green

    def render(self) -> Text:
        """Render a simple placeholder."""
        # return Text("thats nice Graph Placeholder", style="bold red") # Temporarily return this
        # --- Comment out the complex grid logic below ---
        today = date.today()
        print(f"HERE: {HISTORY_FILE}")
        start_date = today - timedelta(days=self.days_to_display -1) # Go back N days inclusive

        # Find the Sunday before or on the start_date to align columns
        start_offset = (start_date.weekday() + 1) % 7 # weekday() is 0=Mon, 6=Sun. We want Sun=0.
        render_start_date = start_date - timedelta(days=start_offset)

        grid = [[" " for _ in range(self.days_to_display // 7 + 1)] for _ in range(7)] # 7 days, ~13 weeks
        num_weeks = 0

        current_date = render_start_date
        while current_date <= today:
            week_index = (current_date - render_start_date).days // 7
            day_index = (current_date.weekday() + 1) % 7 # Sunday = 0

            if week_index >= len(grid[0]): # Avoid index out of bounds if calculation slightly off
                 break

            if current_date >= start_date: # Only render squares from the actual start date
                count = self.pomodoro_data.get(current_date, 0)
                style = self._get_intensity_style(count)
                # Use a simple square character for now
                grid[day_index][week_index] = ( "■", style)
            else:
                 # Keep cells before start_date blank
                 grid[day_index][week_index] = " "

            num_weeks = max(num_weeks, week_index + 1)
            current_date += timedelta(days=1)


        # Trim empty columns from the end if any
        # grid = [row[:num_weeks] for row in grid]

        # Add day labels (optional, adds height) - Mon, Wed, Fri
        day_labels = ["S", "M", "T", "W", "T", "F", "S"]
        rendered_grid = Text(f" Pomodoros ({self.days_to_display} days)\n", style="bold")
        for r, label in enumerate(day_labels):
            rendered_grid.append(f"{label} ", style="dim")
            for c in range(num_weeks):
                 cell = grid[r][c]
                 if isinstance(cell, tuple):
                     rendered_grid.append(cell[0], style=cell[1])
                 else:
                     rendered_grid.append(cell) # Append space
                 rendered_grid.append(" ") # Spacing between columns
            rendered_grid.append("\n")

        return rendered_grid

class TimerDisplay(Static):
    """A widget to display the current timer value."""
    def __init__(self):
        super().__init__()
        self._time_left = timedelta(minutes=30)  # Default work time
        self._is_running = False
        self._is_break = False
        self._work_duration = 30
        self._break_duration = 5

    def _play_notification_sound(self, is_break: bool) -> None:
        """Play the appropriate notification sound using afplay."""
        try:
            sound_file = "/System/Library/Sounds/Glass.aiff" if is_break else "/System/Library/Sounds/Ping.aiff"

            def play():
                try:
                    # Use subprocess.run to call afplay with increased volume
                    volume = "5" # Adjust this value as needed (e.g., "1.5", "3")
                    subprocess.run(["afplay", "-v", volume, sound_file], check=True, capture_output=True)
                except FileNotFoundError:
                    # Handle case where afplay command is not found (unlikely on macOS)
                    self.app.log(f"Error: 'afplay' command not found.")
                except subprocess.CalledProcessError as e:
                    # Handle errors from afplay (e.g., sound file not found)
                    self.app.log(f"Error playing sound {sound_file}: {e}")
                except Exception as e:
                    # Catch any other unexpected errors during playback
                    self.app.log(f"Error in sound playback thread: {e}")

            threading.Thread(target=play, daemon=True).start()
        except Exception as e:
            # Catch errors setting up the thread
            self.app.log(f"Error starting sound thread: {e}")
            # Silently fail if sound can't be played
            pass

    @property
    def time_left(self) -> timedelta:
        return self._time_left

    @time_left.setter
    def time_left(self, value: timedelta) -> None:
        self._time_left = value

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, value: bool) -> None:
        self._is_running = value

    @property
    def is_break(self) -> bool:
        return self._is_break

    @is_break.setter
    def is_break(self, value: bool) -> None:
        self._is_break = value

    @property
    def work_duration(self) -> int:
        return self._work_duration

    @work_duration.setter
    def work_duration(self, value: int) -> None:
        self._work_duration = value

    @property
    def break_duration(self) -> int:
        return self._break_duration

    @break_duration.setter
    def break_duration(self, value: int) -> None:
        self._break_duration = value

    def on_mount(self) -> None:
        self.update_timer()

    def update_timer(self) -> None:
        minutes = self.time_left.seconds // 60
        seconds = self.time_left.seconds % 60
        status = "Break" if self.is_break else "Work"
        self.update(f"{status} Time: {minutes:02d}:{seconds:02d}")

    def tick(self) -> None:
        if self.is_running:
            self.time_left -= timedelta(seconds=1)
            self.update_timer()
            if self.time_left.total_seconds() <= 0:
                self.timer_complete()

    def _log_completion(self) -> None:
        """Logs the completion of a work Pomodoro session."""
        try:
            # Ensure the directory exists
            HISTORY_DIR.mkdir(parents=True, exist_ok=True)
            now = datetime.now().isoformat()
            with open(HISTORY_FILE, "a") as f:
                f.write(f"{now}\n")
        except OSError as e:
            print(f"Error creating directory or writing to history file {HISTORY_FILE}: {e}")
            self.app.log(f"Error creating directory or writing to history file {HISTORY_FILE}: {e}")
        except Exception as e:
            print(f"Unexpected error logging completion: {e}")
            self.app.log(f"Unexpected error logging completion: {e}")

    def timer_complete(self) -> None:
        self.is_running = False
        was_break = self.is_break

        if not self.is_break:
            # Work session just finished, log it!
            self._log_completion()
            # Now start the break
            self.is_break = True
            self.time_left = timedelta(minutes=self.break_duration)
            self.notify("Break time! 🎉", timeout=3)
        else:
            # Break session finished, start work
            self.is_break = False
            self.time_left = timedelta(minutes=self.work_duration)
            self.notify("Back to work! 💪", timeout=3)

        # Play the appropriate sound
        self._play_notification_sound(was_break)

        # If a work session just completed, tell the graph to update
        if not was_break:
            try:
                graph_widget = self.app.query_one(PomodoroGraph)
                graph_widget.load_history()
            except Exception as e:
                 print(f"Unexpected error logging completion: {e}")
                 self.app.log(f"Error updating graph: {e}")

class PomodoroApp(App):
    """A Pomodoro timer application."""
    CSS = """
    Screen {
        align: center middle;
    }

    #app-wrapper {
        width: auto;
        height: auto;
        align: center middle;
        padding: 0 4; /* Add some padding to the overall wrapper */
    }

    #main-container {
        width: 60;
        height: auto;
        border: solid green;
        padding: 2 4;
        margin-right: 5; /* Increase space between containers */
    }

    #graph-container {
        width: 60; /* Slightly wider graph container */
        height: auto;
        margin-top: 3; /* Align with main container */
        padding: 0 1; /* Add some padding around the graph */
    }

    PomodoroGraph {
        border: heavy green;
        height: 11;
    }

    #timer-display {
        height: 3;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        margin: 1 0;
        background: $boost;
    }

    #controls {
        height: auto;
        align: center middle;
        margin: 1 0;
    }

    Button {
        margin: 1;
        min-width: 16;
    }

    #settings {
        height: auto;
        align: center middle;
        margin: 1 0;
        layout: horizontal;
    }

    .setting-group {
        width: auto;
        height: 3;
        content-align: center middle;
        padding: 0 1;
    }

    Input {
        width: 10;
        margin: 0 1;
        background: $boost;
    }

    Label {
        padding: 0 1;
        color: $text;
    }
    """

    BINDINGS = [
        Binding("space", "toggle_timer", "Start/Stop"),
        Binding("r", "reset_timer", "Reset"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.timer_display = TimerDisplay()
        self.pomodoro_graph = PomodoroGraph() # Instantiate the graph

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Horizontal( # Use Horizontal directly for side-by-side layout
            # Left side: Timer controls
            Container(
                Vertical(
                    self.timer_display,
                    Container(
                        Button("Start/Stop (Space)", id="start-stop"),
                        Button("Reset (R)", id="reset"),
                        id="controls",
                    ),
                    Container(
                        Container(
                            Static("Work:", classes="label"),
                            Input(placeholder="30", id="work-input"),
                            classes="setting-group"
                        ),
                        Container(
                            Static("Break:", classes="label"),
                            Input(placeholder="5", id="break-input"),
                            classes="setting-group"
                        ),
                        Button("Update Settings", id="update-settings"),
                        id="settings",
                    ),
                ),
                id="main-container",
            ),
            # Right side: Graph
            Container(
                self.pomodoro_graph,
                id="graph-container",
            ),
            id="app-wrapper", # ID for the horizontal wrapper
        )
        yield Footer()

    def on_mount(self) -> None:
        """Set up the timer and ensure history directory exists."""
        # Ensure the history directory exists on startup
        try:
            HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.log(f"Error creating history directory {HISTORY_DIR}: {e}")

        # Start the timer tick
        self.set_interval(1, self.timer_display.tick)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "start-stop":
            self.timer_display.is_running = not self.timer_display.is_running
        elif event.button.id == "reset":
            self.timer_display.is_running = False
            self.timer_display.is_break = False
            self.timer_display.time_left = timedelta(minutes=self.timer_display.work_duration)
            self.timer_display.update_timer()
        elif event.button.id == "update-settings":
            try:
                work_input = self.query_one("#work-input")
                break_input = self.query_one("#break-input")

                if work_input.value:
                    self.timer_display.work_duration = int(work_input.value)
                if break_input.value:
                    self.timer_display.break_duration = int(break_input.value)

                if not self.timer_display.is_running:
                    self.timer_display.time_left = timedelta(minutes=self.timer_display.work_duration)
                    self.timer_display.update_timer()

                self.notify("Settings updated! ⚙️", timeout=2)
            except ValueError:
                self.notify("Please enter valid numbers! ❌", timeout=2)

    def action_toggle_timer(self) -> None:
        """Toggle the timer on/off."""
        self.timer_display.is_running = not self.timer_display.is_running

    def action_reset_timer(self) -> None:
        """Reset the timer to the work duration."""
        self.timer_display.is_running = False
        self.timer_display.is_break = False
        self.timer_display.time_left = timedelta(minutes=self.timer_display.work_duration)
        self.timer_display.update_timer()

def main() -> None:
    """Entry point for the application."""
    app = PomodoroApp()
    app.run()

if __name__ == "__main__":
    main()
