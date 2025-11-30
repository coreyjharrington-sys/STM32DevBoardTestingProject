# Test_Serial – Firmware + HITL Simulation in CI

*A combined hardware + firmware + automated test demonstration project*

This project demonstrates a **Hardware-In-The-Loop (HITL)-style automated test pipeline** using a **custom STM32F103C8T6 development board that I designed in KiCad**, combined with firmware validation using **Pytest** and **GitHub Actions**.

When code is pushed or a pull request is opened, the CI workflow automatically:

1. **Builds the firmware**
2. **Flashes the STM32F103C8T6 board** connected to the GitHub Actions runner
3. **Runs Pytest-based functional tests** against the physical device
4. **Reports pass/fail status** back to GitHub

This pipeline simulates a professional HITL test system, showing how real hardware can be validated automatically using continuous integration.

---

## 📦 Project Structure

```
Test_Serial/
│
├── firmware/              # Embedded C firmware for STM32F103C8T6
│   ├── src/
│   ├── include/
│   └── (build artifacts ignored via .gitignore)
│
├── tests/                 # Pytest functional tests for HITL validation
│   ├── test_commands.py
│   ├── test_math_ops.py
│   ├── dut_config.json    # PID/VID → auto-detect COM port
│   └── helpers/
│
├── hardware/              # Full KiCad project for the custom STM32 board
│   ├── *.kicad_pro
│   ├── *.kicad_sch
│   ├── *.kicad_pcb
│   ├── symbols/
│   └── footprints/
│
├── scripts/               # Optional Python helper scripts
│
├── requirements.txt       # Python dependencies for Pytest HITL tests
├── .gitignore
└── README.md
```

The KiCad project is intentionally included to showcase the board design to recruiters/employers.
Only temporary, generated, and fabrication files are ignored via `.gitignore`.

---

## 🔧 Hardware Overview (Custom STM32F103C8T6 Board)

The DUT is a custom development board designed in **KiCad**. The design includes:

* STM32F103C8T6 microcontroller
* USB-to-UART for firmware testing
* SWD debug header
* Power regulation and filtering
* Breakouts for serial, GPIO, and test pins

The PCB and schematic files are included so reviewers can inspect routing, component selection, layout style, and design organization.

This hardware is used directly in the HITL CI workflow.

---

## 🧩 Firmware Overview

The embedded firmware is intentionally minimal and built for testing.
It implements a UART command interface supporting:

* A **command/response** handshake
* Four arithmetic operations:

  * **Add**
  * **Subtract**
  * **Multiply**
  * **Divide**
* A small set of additional commands used by the test suite

This makes the board ideal for CI-driven firmware verification.

---

## 🧪 HITL Test Flow (Pytest)

After flashing the firmware, GitHub Actions triggers **Pytest** to validate real hardware behavior:

* A Python script scans the system’s USB devices
* It loads the `dut_config.json` file to locate the board based on:

  * **PID**
  * **VID**
  * **Baudrate**
* The test suite opens the serial port and sends each supported command
* Responses are parsed and validated

Example Pytest coverage:

* Handshake / ping test
* Add / subtract / multiply / divide
* Error format tests
* Command framing validation

Test artifacts (logs, HTML output, temp files) are fully ignored via `.gitignore`.

---

## ⚙️ GitHub Actions CI

The automated pipeline runs on every:

* **Push**
* **Pull request**

Workflow steps:

1. Install ARM toolchain & Python dependencies
2. Build firmware
3. Flash firmware onto the STM32F103C8T6
4. Run Pytest HITL tests on the physical device
5. Upload logs, artifacts, and test summaries

This creates a fully automated feedback loop for both firmware and hardware behavior.

---

## 🐍 Python Environment

Install local dependencies:

```bash
pip install -r requirements.txt
```

Key libraries include:

* `pytest`
* `pyserial`
* Utility modules for device enumeration and communications

---

## 🔌 DUT Configuration File (`dut_config.json`)

This file determines which device to test against:

```json
{
    "pid": "0x1234",
    "vid": "0x5678",
    "baudrate": 115200
}
```

Pytest uses these identifiers to automatically determine the correct COM port.

This avoids any hard-coding and ensures the CI system always targets the correct board.

---

## 📝 License

This project is licensed under the **GNU General Public License (GPL)**.
See the `LICENSE` file for details.

---

## 🛠️ Future Improvements

* SQL logging of test metrics
* Mock serial interface for Pytest-only simulations
* More extensive command set
* Automated hardware reset between test cycles
* Multi-device testing support
* Hardware fault injection
* Coverage reporting and test data visualization
