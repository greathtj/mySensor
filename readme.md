# Sensor Maker

This project is a tool for creating sensor applications.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd sensor_maker
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Prerequisites

Before running the application, you need to install and configure `arduino-cli`.

1.  **Install `arduino-cli`:**
    Follow the official instructions to install `arduino-cli` on your system:
    [https://arduino.github.io/arduino-cli/latest/installation/](https://arduino.github.io/arduino-cli/latest/installation/)

2.  **Update the core index:**
    ```bash
    arduino-cli core update-index
    ```

3.  **Install the ESP32 core:**
    ```bash
    arduino-cli core install esp32:esp32
    ```

### Running the Application

Once the prerequisites are met, you can run the application:

```bash
python main.py
```

**Note on Libraries:** The application will automatically attempt to install the necessary Arduino libraries for the selected sensor using `arduino-cli`.
