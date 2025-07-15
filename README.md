# USSD-Revenue-System-Simulator

This repository contains a mock USSD (Unstructured Supplementary Service Data) application simulating a component of an **Integrated County Revenue Management System (ICRMS)**.

---

## ✨ Features

- **Mock USSD Application:** Python Flask backend that simulates USSD menu navigation and input collection.
- **Session-Based Flow:** Maintains user state across multiple USSD requests using an in-memory dictionary.
- **Parking Services Flow:**
  - Users can select parking zones
  - Collects and validates vehicle plate numbers
  - Simulates payment confirmation (M-Pesa placeholder)
- **Navigation:**
  - `'0'` to go back
  - `'00'` to go home
- **Error Handling:** Graceful handling of unexpected inputs
- **QA Focused:** Designed for easy testing and test case development

---

## 🚀 Technologies Used

- **Python 3.x** – Core backend logic
- **Flask** – Micro web framework to handle POST requests from Africa's Talking
- **Africa's Talking Sandbox** – USSD gateway and simulator
- **Replit** – Cloud IDE and hosting (no Ngrok required)

---

## 💡 Understanding Session-Based USSD Flows (QA Perspective)

USSD is **session-based**, meaning it keeps track of a user's interaction in real-time (unlike SMS). This allows dynamic menus and stateful behavior during each session.

### ✅ How This Project Handles Sessions:

- **`sessions` Dictionary:** Stores active sessions keyed by `sessionId` (from Africa's Talking)
- **Menu State Tracking:** Each session contains:
  - `current_menu`: Tracks user position (e.g., `"parking_main"`)
  - `data`: Stores values entered like `vehicle_plate`
- **Input Parsing:** Africa’s Talking sends `text` like `1*2*ABC123`. The app extracts the **latest input** using:
  ```python
  user_input = text.split("*")[-1]


## 🎥 Demo: USSD Simulator in Action

This short demo showcases how the mock USSD flow works in real time using the [Africa's Talking USSD Simulator](https://account.africastalking.com). 

---

### 📸 Screenshot
https://github.com/Muthoni69/USSD-Revenue-System-Simulator/blob/main/USSD.png

---

### 📽️ Watch Demo Video

> 🔗 [Click here to watch the video demo](https://github.com/Muthoni69/USSD-Revenue-System-Simulator/blob/main/USSD.mp4)

---












