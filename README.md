# Smart Climate Controller (RTOS) 🌡️⚙️

**Course:** Real-Time Systems (RTOS)  
**Institution:** Vietnamese-German University (VGU)  

This repository contains the MicroPython implementation of a Real-Time Operating System (RTOS) based Smart Climate Control System. The project simulates a multi-tasking environment on an ESP32-S3 (YoloUNO) microcontroller, utilizing a producer-consumer architecture managed by asynchronous semaphores.

##  Live Simulation
You can view and run the fully wired 3D simulation of this project here:  


##  System Overview

## 🛠️ Hardware Setup (Simulated)
* **Microcontroller:** YoloUNO (ESP32-S3)
* **Sensors:** DHT20 (Temperature & Humidity) via I2C
* **Actuators:** 3x RGB LED Modules (representing a Heater, Cooler, and Humidifier)
* **Display:** LCD 1602 via I2C
* **Status:** Onboard LED (Pin 13)

##  Task Architecture
The system utilizes concurrent task scheduling to decouple sensor polling from long-running actuator state machines. 
* **`Task_ReadSensor` (Producer):** Polls the DHT20 every 5 seconds and releases execution tokens (Semaphores) when environmental thresholds are breached.
* **`Task_Heater` (Consumer):** Updates LED color based on safe (Green), warning (Orange), and critical (Red) temperature zones.
* **`Task_Cooler` (Consumer):** Activates a fixed 5-second cooling cycle when temperatures exceed 30°C.
* **`Task_Humidifier` (Consumer):** Executes a non-blocking 10-second multi-stage sequence (Green -> Yellow -> Red) when humidity drops below 40%.
* **`Task_Blinky`:** Independent 1-second system heartbeat.

## The Team
* **Nguyen Minh Triet (10423180)** - Lead Developer: System Architecture & RTOS Logic
* * **Nguyen Minh Triet (10423180)** - Hardware Mapping & Circuit Setup
* **Tran Quyen Anh (10423189)** - State Machine Design & Code Implementation
* **Tran Quyen Anh (10423189)** - Testing Validation & Report Documentation
