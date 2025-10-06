import sys
import os
import time
import subprocess
import shutil
import tempfile
from typing import Callable
import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QWidget
)
from PySide6.QtCore import QThread, Signal, Slot
from numpy import true_divide

# Assuming main_ui.py contains the converted UI class
from main_ui import Ui_MainWindow
import serial

# --- Configuration Constants ---
ARDUINO_CLI = "arduino-cli"  # Ensure this is in your system's PATH
BOARD_FQBN = "esp32:esp32:esp32"  # Fully Qualified Board Name (e.g., ESP32 Dev Module)


class ESP32Flasher:
    """
    Handles code generation, compilation, and uploading for ESP32 using Arduino CLI.
    """

    def __init__(self, log_callback: Callable[[str], None]):
        """
        Initializes the flasher with a callback function to send log messages to the GUI.

        Args:
            log_callback: A function (e.g., self.log_area.append) to output messages.
        """
        self.log_callback = log_callback
        self.temp_dir = None

    def _log(self, message: str):
        """Internal helper to call the provided log function."""
        self.log_callback(message)

    def _run_cli_command(self, command: list) -> bool:
        """
        Executes an Arduino CLI command and streams output to the log.
        Returns True on success, False on failure.
        """
        full_command = [ARDUINO_CLI] + command
        self._log(f"\n---> Executing: {" ".join(full_command)}")
        
        try:
            # Use Popen to run the command and stream output in a non-blocking way
            process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            line_buffer = bytearray()
            while True:
                byte = process.stdout.read(1)
                if not byte:
                    # End of stream
                    if line_buffer:
                        self._log(line_buffer.decode('utf-8', errors='replace').strip())
                    break
                
                line_buffer.append(byte[0])

                if byte == b'\n' or byte == b'\r':
                    self._log(line_buffer.decode('utf-8', errors='replace').strip())
                    line_buffer.clear()

            # Wait for the process to finish and check the return code
            process.stdout.close()
            return_code = process.wait()

            if return_code == 0:
                self._log("COMMAND SUCCESSFUL.")
                return True
            else:
                self._log(f"COMMAND FAILED with return code {return_code}.")
                return False

        except FileNotFoundError:
            self._log(f"ERROR: '{ARDUINO_CLI}' not found. Make sure Arduino CLI is installed and in your PATH.")
            return False
        except Exception as e:
            self._log(f"An unexpected error occurred: {e}")
            return False

    def generate_and_prepare_code(self, sketch_name: str, code_content: str) -> bool:
        """
        Generates the code and writes it to a temporary directory structure.
        
        Args:
            sketch_name: The name of the sketch (must match the folder name, e.g., 'BlinkSketch').
            code_content: The Arduino code string (e.g., the setup()/loop() sketch).
            
        Returns:
            True if successful, False otherwise.
        """
        # Cleanup any previous temporary directory
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
        # 1. Create a temporary directory for the sketch
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="esp32_gui_")
            sketch_folder = os.path.join(self.temp_dir, sketch_name)
            os.makedirs(sketch_folder)
            sketch_file_path = os.path.join(sketch_folder, f"{sketch_name}.ino")
            
            # 2. Write the code content to the .ino file
            with open(sketch_file_path, 'w') as f:
                f.write(code_content)
                
            self._log(f"Code generated and saved to: {sketch_file_path}")
            return True
            
        except Exception as e:
            self._log(f"Error preparing temporary files: {e}")
            return False


    def compile_code(self, sketch_name: str) -> bool:
        """Compiles the sketch located in the temporary directory."""
        if not self.temp_dir:
            self._log("ERROR: Code not prepared. Call generate_and_prepare_code first.")
            return False
            
        sketch_path = os.path.join(self.temp_dir, sketch_name)
        
        self._log("\n--- Starting Compilation ---")
        command = [
            "compile",
            "--fqbn", BOARD_FQBN,
            sketch_path
        ]
        return self._run_cli_command(command)

    def upload_code(self, sketch_name: str, port: str) -> bool:
        """Uploads the compiled sketch to the specified serial port."""
        if not self.temp_dir:
            self._log("ERROR: Code not prepared. Call generate_and_prepare_code first.")
            return False
            
        sketch_path = os.path.join(self.temp_dir, sketch_name)
        
        self._log(f"\n--- Starting Upload to Port: {port} ---")
        command = [
            "upload",
            "--fqbn", BOARD_FQBN,
            "-p", port,
            sketch_path
        ]
        return self._run_cli_command(command)
        
    def cleanup(self):
        """Removes the temporary directory and all generated files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                self._log(f"\nCleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                self._log(f"Error during cleanup: {e}")
                
    @staticmethod
    def get_serial_ports() -> list[str]:
        """
        Uses the 'pyserial' library to list available serial ports.
        NOTE: You must install the pyserial library (`pip install pyserial`).
        """
        try:
            import serial.tools.list_ports
            ports = [port.device for port in serial.tools.list_ports.comports()]
            return ports
        except ImportError:
            # Fallback for systems without pyserial installed
            return ["/dev/ttyUSB0 (Install pyserial)", "COM3 (Install pyserial)"]
        except Exception as e:
            return [f"Error listing ports: {e}"]

class FlasherWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal()
    sensorType = ""

    def __init__(self, flasher, sketch_name, target_port, modified_code):
        super().__init__()
        self.flasher:ESP32Flasher = flasher
        self.sketch_name = sketch_name
        self.target_port = target_port
        self.modified_code = modified_code

    def run(self):
        try:
            # 1. Install libraries
            self.log_signal.emit("--- Installing libraries ---")

            if self.sensorType == "DHT":
                if not self.flasher._run_cli_command(["lib", "install", "DHT sensor library"]):
                    self.log_signal.emit("Failed to install DHT sensor library.")
                    self.finished_signal.emit()
                    return
                if not self.flasher._run_cli_command(["lib", "install", "Adafruit Unified Sensor"]):
                    self.log_signal.emit("Failed to install Adafruit Unified Sensor library.")
                    self.finished_signal.emit()
                    return
            
            elif self.sensorType == "BME280":
                if not self.flasher._run_cli_command(["lib", "install", "Adafruit BME280 Library"]):
                    self.log_signal.emit("Failed to install Adafruit BME280 Library.")
                    self.finished_signal.emit()
                    return
                if not self.flasher._run_cli_command(["lib", "install", "Adafruit Unified Sensor"]):
                    self.log_signal.emit("Failed to install Adafruit Unified Sensor library.")
                    self.finished_signal.emit()
                    return
            
            elif self.sensorType == "MPU6050":
                if not self.flasher._run_cli_command(["lib", "install", "Adafruit MPU6050"]):
                    self.log_signal.emit("Failed to install Adafruit MPU6050 Library.")
                    self.finished_signal.emit()
                    return
                if not self.flasher._run_cli_command(["lib", "install", "Adafruit Unified Sensor"]):
                    self.log_signal.emit("Failed to install Adafruit Unified Sensor library.")
                    self.finished_signal.emit()
                    return
                if not self.flasher._run_cli_command(["lib", "install", "Adafruit BusIO"]):
                    self.log_signal.emit("Failed to install Adafruit BusIO library.")
                    self.finished_signal.emit()
                    return
                if not self.flasher._run_cli_command(["lib", "install", "arduinoFFT"]):
                    self.log_signal.emit("Failed to install Adafruit BusIO library.")
                    self.finished_signal.emit()
                    return
                
            elif self.sensorType == "HX711":
                if not self.flasher._run_cli_command(["lib", "install", "HX711"]):
                    self.log_signal.emit("Failed to install HX711 Library.")
                    self.finished_signal.emit()
                    return

            if not self.flasher._run_cli_command(["lib", "install", "PubSubClient"]):
                self.log_signal.emit("Failed to install PubSubClient library.")
                self.finished_signal.emit()
                return
            
            self.log_signal.emit("--- Libraries installed ---")

            # A. Get available ports for the GUI ComboBox
            ports = self.flasher.get_serial_ports()
            self.log_signal.emit(f"Available Ports: {ports}")
            
            if not ports:
                self.log_signal.emit("ERROR: No serial ports detected. Cannot proceed with upload.")
            
            # B. Generate the code files
            if self.flasher.generate_and_prepare_code(self.sketch_name, self.modified_code):
                
                # C. Compile the code
                if self.flasher.compile_code(self.sketch_name):
                    
                    # D. Upload the compiled code
                    if ports and self.flasher.upload_code(self.sketch_name, self.target_port):
                        self.log_signal.emit("\n*** SUCCESS: CODE COMPILED AND UPLOADED ***")
                    else:
                        self.log_signal.emit("\n*** FAILED: UPLOAD FAILED OR PORT NOT FOUND ***")
                else:
                    self.log_signal.emit("\n*** FAILED: COMPILATION FAILED ***")
                    
        finally:
            # E. Cleanup the temporary files
            self.flasher.cleanup()
            self.finished_signal.emit()

class serial_monitor(QThread):
    port = ""
    baudrate = 115200
    inComming = Signal(bytearray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self.serial_device = serial.Serial()

    def run(self):
        if self.serial_device.is_open:
            self.serial_device.close()
            time.sleep(1)

        self.serial_device.port = self.port
        self.serial_device.baudrate = self.baudrate
        self.serial_device.open()
        self._running = True

        while self._running:
            while (self.serial_device.in_waiting):
                inLine = self.serial_device.readline()
                self.inComming.emit(inLine)

            time.sleep(0.1)
        
        self.serial_device.close()

    def stop(self):
        self._running = False

        
# --- Main PySide6 Application Window ---
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("ESP32 GUI Programmer")

        ports = ESP32Flasher.get_serial_ports()
        self.ui.comboBoxPorts.clear()
        self.ui.comboBoxPorts.addItems(ports)

        QWidget.setTabOrder(self.ui.comboBoxPorts, self.ui.lineEditSSID)
        QWidget.setTabOrder(self.ui.lineEditSSID, self.ui.lineEditPassword)
        QWidget.setTabOrder(self.ui.lineEditPassword, self.ui.lineEditServerAddress)
        QWidget.setTabOrder(self.ui.lineEditServerAddress, self.ui.lineEditServerPortNumber)
        QWidget.setTabOrder(self.ui.lineEditServerPortNumber, self.ui.lineEditDeviceID_DHT)

        self.serialMonitor = serial_monitor(parent=self)
        self.serialMonitor.inComming.connect(self.show_serial_monitor)
        self.ui.pushButtonStartSerialMonitor.clicked.connect(self.toggle_serial_monitor)

        self.ui.pushButtonUpload_DHT.clicked.connect(self.start_upload_DHT)
        self.ui.pushButtonUpload_VIB.clicked.connect(self.start_upload_VIB)
        self.ui.pushButtonUpload_WT.clicked.connect(self.start_upload_WT)

        self.ui.pushButtonAutoID_DHT.clicked.connect(self.autoID_DHT)
        self.ui.pushButtonAutoID_VIB.clicked.connect(self.autoID_VIB)
        self.ui.pushButtonAutoID_WT.clicked.connect(self.autoID_WT)

        self.flasher = ESP32Flasher(log_callback=self.gui_log_display)
        self.worker = None

        self.ui.actionExit.triggered.connect(self.close)

    def toggle_serial_monitor(self):
        if self.serialMonitor._running:
            self.serialMonitor.stop()
            self.serialMonitor.wait()
            # self.ui.pushButtonStartSerialMonitor.setText("모니터 시작")
        else:
            self.serialMonitor.port = self.ui.comboBoxPorts.currentText()
            self.serialMonitor.baudrate = 115200
            self.serialMonitor.start()
            # self.ui.pushButtonStartSerialMonitor.setText("모니터 중단")

    def show_serial_monitor(self, inMessage:bytearray):
        message = inMessage.decode('utf-8', errors='replace').strip()
        self.ui.textBrowserSerialMonitor.append(message)
        self.ui.textBrowserSerialMonitor.verticalScrollBar().setValue(self.ui.textBrowserSerialMonitor.verticalScrollBar().maximum())

    def autoID_DHT(self):
        stype = self.ui.comboBoxDHTType.currentText()
        current_time = datetime.datetime.now()
        log_format = current_time.strftime("%Y%m%d%H%M%S")

        autoID = f"KIOT/ESP32/{stype}/{log_format}"

        self.ui.lineEditDeviceID_DHT.setText(autoID)

    def autoID_VIB(self):
        stype = self.ui.comboBoxVIBType.currentText()
        current_time = datetime.datetime.now()
        log_format = current_time.strftime("%Y%m%d%H%M%S")

        autoID = f"KIOT/ESP32/{stype}/{log_format}"

        self.ui.lineEditDeviceID_VIB.setText(autoID)

    def autoID_WT(self):
        stype = self.ui.comboBoxWTType.currentText()
        current_time = datetime.datetime.now()
        log_format = current_time.strftime("%Y%m%d%H%M%S")

        autoID = f"KIOT/ESP32/{stype}/{log_format}"

        self.ui.lineEditDeviceID_WT.setText(autoID)

    def disable_action_buttons(self, enabled=False):
        self.ui.pushButtonUpload_DHT.setEnabled(enabled)
        self.ui.pushButtonUpload_VIB.setEnabled(enabled)
        self.ui.pushButtonUpload_WT.setEnabled(enabled)
        self.ui.pushButtonStartSerialMonitor.setEnabled(enabled)
        self.ui.pushButtonAutoID_DHT.setEnabled(enabled)
        self.ui.pushButtonAutoID_VIB.setEnabled(enabled)
        self.ui.pushButtonAutoID_WT.setEnabled(enabled)

    def start_upload_DHT(self):
        if self.serialMonitor._running:
            self.serialMonitor.stop()
            self.serialMonitor.wait()


        TARGET_PORT = self.ui.comboBoxPorts.currentText()

        # 1. Define a simple code to generate (user input in your GUI)
        SKETCH_NAME = "MQTT_DHT"
        stype = self.ui.comboBoxDHTType.currentText()
        if stype == "DHT11" or stype == "DHT22" or stype == "RHT05":
            fstype = "DHT"
        else:
            fstype = "BME280"

        EXAMPLE_CODE = self.read_code_file(f"codes/mqtt_{fstype}.ino")

        ssid = self.ui.lineEditSSID.text()
        password = self.ui.lineEditPassword.text()
        serverAddress = self.ui.lineEditServerAddress.text()
        portNumber = self.ui.lineEditServerPortNumber.text()
        deviceID = self.ui.lineEditDeviceID_DHT.text()

        modified_code = EXAMPLE_CODE.replace('const char* ssid = "MYSSID";', f'const char* ssid = "{ssid}";')
        modified_code = modified_code.replace('const char* password = "MYPASS";', f'const char* password = "{password}";')
        modified_code = modified_code.replace('const char* mqtt_server = "MYMQTTSERVER";', f'const char* mqtt_server = "{serverAddress}";')
        modified_code = modified_code.replace('  client.setServer(mqtt_server, portNumber);', f'  client.setServer(mqtt_server, {portNumber});')
        modified_code = modified_code.replace('    if (client.connect("esp32_htj"))', f'    if (client.connect("{deviceID}"))')
        modified_code = modified_code.replace('      client.subscribe("esp32_htj/output");', f'      client.subscribe("{deviceID}/output");')

        modified_code = modified_code.replace('    client.publish("esp32_htj/temperature", tempString);', f'    client.publish("{deviceID}/temperature", tempString);')
        modified_code = modified_code.replace('    client.publish("esp32_htj/humidity", humString);', f'    client.publish("{deviceID}/humidity", humString);')

        modified_code = modified_code.replace('  Serial.print("device ID: "); Serial.println("myID");', f'  Serial.print("device ID: "); Serial.println("{deviceID}");')
        

        # print(modified_code)
        # return

        self.worker = FlasherWorker(self.flasher, SKETCH_NAME, TARGET_PORT, modified_code)
        self.worker.sensorType = fstype
        self.worker.log_signal.connect(self.gui_log_display)
        self.worker.finished_signal.connect(self.on_upload_finished)
        self.worker.start()

        self.disable_action_buttons(enabled=False)

    def start_upload_VIB(self):
        if self.serialMonitor._running:
            self.serialMonitor.stop()
            self.serialMonitor.wait()


        TARGET_PORT = self.ui.comboBoxPorts.currentText()

        # 1. Define a simple code to generate (user input in your GUI)
        SKETCH_NAME = "MQTT_VIB"
        fstype = self.ui.comboBoxVIBType.currentText()
        EXAMPLE_CODE = self.read_code_file(f"codes/mqtt_{fstype}.ino")

        ssid = self.ui.lineEditSSID.text()
        password = self.ui.lineEditPassword.text()
        serverAddress = self.ui.lineEditServerAddress.text()
        portNumber = self.ui.lineEditServerPortNumber.text()
        deviceID = self.ui.lineEditDeviceID_VIB.text()

        modified_code = EXAMPLE_CODE.replace('const char* ssid = "MYSSID";', f'const char* ssid = "{ssid}";')
        modified_code = modified_code.replace('const char* password = "MYPASS";', f'const char* password = "{password}";')
        modified_code = modified_code.replace('const char* mqtt_server = "MYMQTTSERVER";', f'const char* mqtt_server = "{serverAddress}";')
        modified_code = modified_code.replace('  client.setServer(mqtt_server, portNumber);', f'  client.setServer(mqtt_server, {portNumber});')
        modified_code = modified_code.replace('    if (client.connect("esp32_htj"))', f'    if (client.connect("{deviceID}"))')
        modified_code = modified_code.replace('      client.subscribe("esp32_htj/output");', f'      client.subscribe("{deviceID}/output");')

        modified_code = modified_code.replace('    client.publish("esp32_htj/freq_x", tempString);', f'    client.publish("{deviceID}/freq_x", tempString);')
        modified_code = modified_code.replace('    client.publish("esp32_htj/freq_y", tempString);', f'    client.publish("{deviceID}/freq_y", tempString);')
        modified_code = modified_code.replace('    client.publish("esp32_htj/freq_z", tempString);', f'    client.publish("{deviceID}/freq_z", tempString);')
        modified_code = modified_code.replace('    client.publish("esp32_htj/rms_x", tempString);', f'    client.publish("{deviceID}/rms_x", tempString);')
        modified_code = modified_code.replace('    client.publish("esp32_htj/rms_y", tempString);', f'    client.publish("{deviceID}/rms_y", tempString);')
        modified_code = modified_code.replace('    client.publish("esp32_htj/rms_z", tempString);', f'    client.publish("{deviceID}/rms_z", tempString);')

        modified_code = modified_code.replace('  Serial.print("device ID: "); Serial.println("myID");', f'  Serial.print("device ID: "); Serial.println("{deviceID}");')
        

        # print(modified_code)
        # return

        self.worker = FlasherWorker(self.flasher, SKETCH_NAME, TARGET_PORT, modified_code)
        self.worker.sensorType = fstype
        self.worker.log_signal.connect(self.gui_log_display)
        self.worker.finished_signal.connect(self.on_upload_finished)
        self.worker.start()

        self.disable_action_buttons(enabled=False)

    def start_upload_WT(self):
        if self.serialMonitor._running:
            self.serialMonitor.stop()
            self.serialMonitor.wait()


        TARGET_PORT = self.ui.comboBoxPorts.currentText()

        # 1. Define a simple code to generate (user input in your GUI)
        SKETCH_NAME = "MQTT_WT"
        fstype = self.ui.comboBoxWTType.currentText()
        EXAMPLE_CODE = self.read_code_file(f"codes/mqtt_{fstype}.ino")

        ssid = self.ui.lineEditSSID.text()
        password = self.ui.lineEditPassword.text()
        serverAddress = self.ui.lineEditServerAddress.text()
        portNumber = self.ui.lineEditServerPortNumber.text()
        deviceID = self.ui.lineEditDeviceID_WT.text()

        modified_code = EXAMPLE_CODE.replace('const char* ssid = "MYSSID";', f'const char* ssid = "{ssid}";')
        modified_code = modified_code.replace('const char* password = "MYPASS";', f'const char* password = "{password}";')
        modified_code = modified_code.replace('const char* mqtt_server = "MYMQTTSERVER";', f'const char* mqtt_server = "{serverAddress}";')
        modified_code = modified_code.replace('  client.setServer(mqtt_server, portNumber);', f'  client.setServer(mqtt_server, {portNumber});')
        modified_code = modified_code.replace('    if (client.connect("esp32_htj"))', f'    if (client.connect("{deviceID}"))')
        modified_code = modified_code.replace('      client.subscribe("esp32_htj/output");', f'      client.subscribe("{deviceID}/output");')

        modified_code = modified_code.replace('    client.publish("esp32_htj/weight", tempString);', f'    client.publish("{deviceID}/weight", tempString);')

        modified_code = modified_code.replace('    Serial.print("device ID: "); Serial.println("myID");', f'    Serial.print("device ID: "); Serial.println("{deviceID}");')
        

        # print(modified_code)
        # return

        self.worker = FlasherWorker(self.flasher, SKETCH_NAME, TARGET_PORT, modified_code)
        self.worker.sensorType = fstype
        self.worker.log_signal.connect(self.gui_log_display)
        self.worker.finished_signal.connect(self.on_upload_finished)
        self.worker.start()

        self.disable_action_buttons(enabled=False)

    def read_code_file(self, file_path):
        """
        Reads the content of a text file and returns it as a string.

        Args:
            file_path (str): The full path to the text file (e.g., 'path/to/your/file.txt').

        Returns:
            str: The content of the file, or None if an error occurs.
        """
        try:
            # Open the file in read mode ('r')
            with open(file_path, 'r', encoding='utf-8') as file:
                # Read all the content and store it in the local variable 'EXAMPLE_CODE_content'
                EXAMPLE_CODE_content = file.read()
            
            # Return the content. In a real application, you would assign this
            # to a global or class-level variable named EXAMPLE_CODE if needed.
            return EXAMPLE_CODE_content
            
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def on_upload_finished(self):
        self.disable_action_buttons(enabled=True)

        self.serialMonitor.port = self.ui.comboBoxPorts.currentText()
        self.serialMonitor.baudrate = 115200
        self.serialMonitor.start()

    def gui_log_display(self, message):
        print(message)
        self.ui.textBrowserLogOutput.append(message)
        self.ui.textBrowserLogOutput.verticalScrollBar().setValue(self.ui.textBrowserLogOutput.verticalScrollBar().maximum())

    def closeEvent(self, event):
        if self.serialMonitor._running:
            self.serialMonitor.stop()
            self.serialMonitor.wait()
        return super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())