# Timy - A Simple Pomodoro Timer TUI

![Timy Screenshot](docs/screenshot.png) <!-- You'll need to create this screenshot -->

Timy is a minimalist terminal-based Pomodoro timer application built with Python and the [Textual](https://github.com/Textualize/textual) framework. It helps you stay focused by alternating work and break sessions.

## Features

*   Simple and intuitive Terminal User Interface (TUI).
*   Configurable work and break durations.
*   Visual timer display.
*   Notification sounds (using `beepy`) for session changes.
*   Keyboard shortcuts for quick control (Start/Stop, Reset, Quit).

## Installation

### Prerequisites

*   Python 3.8 or higher
*   `uv` (recommended) or `pip`
*   For notification sounds, platform-specific dependencies might be needed for `beepy` (refer to the [beepy documentation](https://github.com/kosua20/beepy)).

### From Source (using uv)

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/timy.git # Replace with your repo URL
    cd timy
    ```
2.  Install using `uv`:
    ```bash
    uv pip install .
    ```
    Alternatively, for development (editable install):
    ```bash
    uv pip install -e .
    ```
3.  Run the application:
    ```bash
    timy
    ```

### From Source (using pip)

1.  Clone the repository (see above).
2.  Install using `pip`:
    ```bash
    pip install .
    ```
    Alternatively, for development (editable install):
    ```bash
    pip install -e .
    ```
3.  Run the application:
    ```bash
    timy
    ```

### Homebrew (Planned)

Installation via Homebrew is planned for future releases.

## Development (Using Makefile)

This project includes a `Makefile` to streamline common development tasks. Ensure you have `make` installed on your system.

*   **Install dependencies and the package:**
    ```bash
    make install
    ```
*   **Install in editable mode (for development):** This allows you to test changes without reinstalling.
    ```bash
    make develop
    ```
*   **Run the application (after installing):**
    ```bash
    make run
    # or directly
    timy
    ```
*   **Build the source distribution and wheel:** Outputs will be in the `dist/` directory.
    ```bash
    make build
    ```
*   **Clean build artifacts and caches:**
    ```bash
    make clean
    ```
*   **Linting and Testing (Placeholders):**
    The `Makefile` includes placeholder targets for linting (`make lint`) and testing (`make test`). You can integrate tools like Ruff or Flake8 for linting and Pytest for testing by uncommenting and adjusting the relevant lines in the `Makefile` and adding the tools as development dependencies.

## Usage

Launch the application by running `timy` in your terminal.

*   **Spacebar:** Start or stop the timer.
*   **R:** Reset the current timer to the work duration.
*   **Q:** Quit the application.
*   Use the input fields to set custom work and break durations (in minutes) and press "Update Settings".

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally (`git clone https://github.com/yourusername/timy.git`).
3.  **Create a new branch** for your feature or bug fix (`git checkout -b feature/your-feature-name` or `bugfix/your-bug-fix-name`).
4.  **Make your changes** and commit them with clear messages.
5.  **Push your changes** to your fork (`git push origin feature/your-feature-name`).
6.  **Open a Pull Request** on the original repository.

Please ensure your code adheres to basic Python style guidelines and consider adding tests if applicable.

You can also contribute by reporting bugs or suggesting features through the [GitHub Issues](https://github.com/yourusername/timy/issues) page. # Replace with your repo URL

## License

This project is licensed under the MIT License - see the LICENSE file for details (if you create one). 