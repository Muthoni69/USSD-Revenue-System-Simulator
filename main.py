from flask import Flask, request, make_response

app = Flask(__name__)

# This dictionary will simulate user sessions.
# In a real application, you would replace this with a persistent storage
# like a database (e.g., Firestore, Redis) to handle multiple users
# and ensure session data isn't lost if the server restarts.
sessions = {}

# Home route for browser testing and health check
@app.route('/', methods=['GET'])
def home():
    return '''
    <h2>✅ K County USSD Simulation is Running</h2>
    <p>To test the USSD app, send a POST request to <code>/ussd</code> from Africa's Talking simulator or Postman.</p>
    '''

# USSD logic route
@app.route('/ussd', methods=['POST'])
def ussd_callback():
    """
    Handles incoming USSD requests from Africa's Talking, managing session state.
    """
    global sessions # Access the global sessions dictionary


    session_id = request.values.get("sessionId", None)
    phone_number = request.values.get("phoneNumber", None)
   
    # For the first request, it's typically empty or "default".
    text = request.values.get("text", "default")

    # Determine the user's current input for this step
    # If text is "default" or empty, it's the initial dial.
    # Otherwise, get the last part after splitting by '*'
    user_input = "" if text == "default" or text == "" else text.split("*")[-1] # Get only the *last* input from the user

    # Initialize session if it's a new one
    if session_id not in sessions:
        sessions[session_id] = {
            "current_menu": "main", # Start at the main menu
            "data": {} # To store any data collected from the user during the session
        }
        print(f"New session started for {phone_number} with ID: {session_id}")
    else:
        print(f"Existing session for {phone_number} (ID: {session_id}), "
              f"full text: '{text}', user_input: '{user_input}'")

    # Get the current menu state for this session
    current_menu = sessions[session_id]["current_menu"]
    response_message = "" # This will hold the USSD response string

    # --- USSD Logic based on current menu and user's last input ---

    # Main Menu
    if current_menu == "main":
        if user_input == "": # Initial dial
            response_message = "CON Welcome to K County\n" \
                               "1. Parking Services\n" \
                               "2. Fees and Charges\n" \
                               "3. Permits\n" \
                               "4. Emergency Contacts"
        elif user_input == "1":
            sessions[session_id]["current_menu"] = "parking_main"
            response_message = "CON Daily Parking Zones:\n" \
                               "1. TOWN1\n" \
                               "2. TOWN2\n" \
                               "0. Back to Main Menu"
        elif user_input == "2":
            sessions[session_id]["current_menu"] = "fees_charges_menu"
            response_message = "CON Fees and Charges:\n" \
                               "1. Market Fees\n" \
                               "2. Business Licenses\n" \
                               "0. Back to Main Menu"
        elif user_input == "3":
            sessions[session_id]["current_menu"] = "permits_menu"
            response_message = "CON Permits:\n" \
                               "1. Building Permits\n" \
                               "2. Health Permits\n" \
                               "0. Back to Main Menu"
        elif user_input == "4":
            sessions[session_id]["current_menu"] = "emergency_contacts"
            response_message = "CON Emergency Contacts:\n" \
                               "Police: 999\n" \
                               "Ambulance: 112\n" \
                               "Fire: 113\n" \
                               "0. Back to Main Menu"
        else:
            response_message = "CON Invalid option. Please try again.\n" \
                               "1. Parking Services\n" \
                               "2. Fees and Charges\n" \
                               "3. Permits\n" \
                               "4. Emergency Contacts"

    # Parking Services Menu
    elif current_menu == "parking_main":
        if user_input == "1":
            sessions[session_id]["current_menu"] = "parking_town1_plate"
            response_message = "CON Enter your vehicle plate number for TOWN1 zone:"
        elif user_input == "2":
            sessions[session_id]["current_menu"] = "parking_town2_plate"
            response_message = "CON Enter your vehicle plate number for TOWN2 zone:"
        elif user_input == "0": # Back to Main Menu
            sessions[session_id]["current_menu"] = "main"
            response_message = "CON Welcome to K County\n" \
                               "1. Parking Services\n" \
                               "2. Fees and Charges\n" \
                               "3. Permits\n" \
                               "4. Emergency Contacts"
        else:
            response_message = "CON Invalid option. Please select a zone or 0 to go back.\n" \
                               "1. Town1\n" \
                               "2. Town2\n" \
                               "0. Back to Main Menu"

    # TOWN1 Parking Plate Input
    elif current_menu == "parking_town1_plate":
        if user_input == "0": # Back to Parking Services Menu
            sessions[session_id]["current_menu"] = "parking_main"
            response_message = "CON Daily Parking Zones:\n" \
                               "1. Town1\n" \
                               "2. Town2\n" \
                               "0. Back to Main Menu"
        elif user_input != "": # Assuming user entered a plate number
            plate = user_input
            sessions[session_id]["data"]["parking_zone"] = "Town1"
            sessions[session_id]["data"]["vehicle_plate"] = plate
            sessions[session_id]["current_menu"] = "parking_confirm"
            # Simulate fetching amount (in a real app, this would be a lookup)
            amount = "100 KES"
            response_message = f"CON Confirm payment for {plate} in Town1: {amount}\n" \
                               "1. Confirm\n" \
                               "0. Back"
        else:
            response_message = "CON Please enter your vehicle plate number (e.g., KBC123A):\n" \
                               "0. Back"

    # TOWN2 Parking Plate Input (similar to TOWN1, but distinct state)
    elif current_menu == "parking_town2_plate":
        if user_input == "0": # Back to Parking Services Menu
            sessions[session_id]["current_menu"] = "parking_main"
            response_message = "CON Daily Parking Zones:\n" \
                               "1. Town1\n" \
                               "2. Town2\n" \
                               "0. Back to Main Menu"
        elif user_input != "": # Assuming user entered a plate number
            plate = user_input
            sessions[session_id]["data"]["parking_zone"] = "TOWN2"
            sessions[session_id]["data"]["vehicle_plate"] = plate
            sessions[session_id]["current_menu"] = "parking_confirm"
            # Simulate fetching amount
            amount = "80 KES" # Different amount for TOWN2
            response_message = f"CON Confirm payment for {plate} in TOWN2: {amount}\n" \
                               "1. Confirm\n" \
                               "0. Back"
        else:
            response_message = "CON Please enter your vehicle plate number for TOWN2 zone:\n" \
                               "0. Back"

    # Parking Confirmation
    elif current_menu == "parking_confirm":
        if user_input == "1":
            # Here, you would integrate with a payment gateway (e.g., M-Pesa Daraja API)
            # using sessions[session_id]["data"]["vehicle_plate"] and sessions[session_id]["data"]["parking_zone"]
            # For this simulation, we just end the session.
            response_message = "END Payment initiated. You will receive an M-Pesa prompt shortly. Thank you!"
            del sessions[session_id] # End session and clear data
        elif user_input == "0": # Go back to plate input
            # Determine which plate input menu to go back to based on stored data
            if sessions[session_id]["data"].get("parking_zone") == "TOWN1":
                sessions[session_id]["current_menu"] = "parking_town1_plate"
                response_message = "CON Enter your vehicle plate number for TOWN1 zone:"
            elif sessions[session_id]["data"].get("parking_zone") == "TOWN2":
                sessions[session_id]["current_menu"] = "parking_town2_plate"
                response_message = "CON Enter your vehicle plate number for TOWN2 zone:"
            else: # Fallback if zone not set (shouldn't happen with proper flow)
                sessions[session_id]["current_menu"] = "parking_main"
                response_message = "CON Daily Parking Zones:\n1. TOWN1\n2. TOWN2\n0. Back to Main Menu"
        else:
            response_message = "CON Invalid option. Please select 1 to confirm or 0 to go back.\n" \
                               "1. Confirm\n" \
                               "0. Back"

    # Fees and Charges Menu (Placeholder)
    elif current_menu == "fees_charges_menu":
        if user_input == "1":
            response_message = "END Market Fees information coming soon. Thank you!"
            del sessions[session_id]
        elif user_input == "2":
            response_message = "END Business Licenses information coming soon. Thank you!"
            del sessions[session_id]
        elif user_input == "0":
            sessions[session_id]["current_menu"] = "main"
            response_message = "CON Welcome to K County\n" \
                               "1. Parking Services\n" \
                               "2. Fees and Charges\n" \
                               "3. Permits\n" \
                               "4. Emergency Contacts"
        else:
            response_message = "CON Invalid option. Please select an option or 0 to go back.\n" \
                               "1. Market Fees\n" \
                               "2. Business Licenses\n" \
                               "0. Back to Main Menu"

    # Permits Menu (Placeholder)
    elif current_menu == "permits_menu":
        if user_input == "1":
            response_message = "END Building Permits details coming soon. Thank you!"
            del sessions[session_id]
        elif user_input == "2":
            response_message = "END Health Permits details coming soon. Thank you!"
            del sessions[session_id]
        elif user_input == "0":
            sessions[session_id]["current_menu"] = "main"
            response_message = "CON Welcome to K County\n" \
                               "1. Parking Services\n" \
                               "2. Fees and Charges\n" \
                               "3. Permits\n" \
                               "4. Emergency Contacts"
        else:
            response_message = "CON Invalid option. Please select an option or 0 to go back.\n" \
                               "1. Building Permits\n" \
                               "2. Health Permits\n" \
                               "0. Back to Main Menu"

    # Emergency Contacts (Ends session after displaying info)
    elif current_menu == "emergency_contacts":
        if user_input == "0": # Back to Main Menu
            sessions[session_id]["current_menu"] = "main"
            response_message = "CON Welcome to K County\n" \
                               "1. Parking Services\n" \
                               "2. Fees and Charges\n" \
                               "3. Permits\n" \
                               "4. Emergency Contacts"
        else: # Any other input just re-displays or ends
            response_message = "CON Emergency Contacts:\n" \
                               "Police: 999\n" \
                               "Ambulance: 112\n" \
                               "Fire: 113\n" \
                               "0. Back to Main Menu"


    # Create the Flask response
    resp = make_response(response_message, 200)
    resp.headers['Content-Type'] = 'text/plain' # Important for Africa's Talking
    return resp

if __name__ == '__main__':
    # Run the Flask app on port 5000 (standard for development)
    # Use debug=True for development to auto-reload on code changes
    app.run(host='0.0.0.0', port=5000, debug=True)
