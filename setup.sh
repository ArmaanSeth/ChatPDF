#!/bin/bash

echo "Starting script..."

ENV_DIR=".venv"
PYTHON_VERSION="3.9.18"

# Function to check if the virtual environment exists and create it if it doesn't
check_and_create_venv() {
    if [ -d "$ENV_DIR" ]; then
        echo "Virtual environment '$ENV_DIR' already exists. Activating..."
    else
        echo "Creating new virtual environment in '$ENV_DIR' with Python $PYTHON_VERSION..."
        python -m venv "$ENV_DIR" --python "$PYTHON_VERSION"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to create virtual environment in '$ENV_DIR'."
            exit 1
        fi
    fi
}

# Check/create the virtual environment
check_and_create_venv

# Activate the virtual environment
if [ -f "$ENV_DIR/Scripts/activate" ]; then
    source "$ENV_DIR/Scripts/activate"
else
    echo "Error: Activation script not found."
    exit 1
fi

# Verify activation
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
else
    echo "Virtual environment '$ENV_DIR' activated successfully."
fi

echo "Setup completed successfully."

# Sync dependencies using uv
sync_dependencies() {
    echo "Syncing dependencies using uv..."
    uv sync
    if [ $? -ne 0 ]; then
        echo "Error: Failed to sync dependencies."
        exit 1
    fi
    echo "Dependencies synced successfully."
}

# Main menu
menu() {
    while true; do
        echo "Document Chatbot Tool"
        echo "======================="
        echo "1. Run with Streamlit interface"
        echo "2. Sync dependencies"
        echo "3. Exit"
        read -p "Enter your choice (1-3): " choice

        case $choice in
            1)
                echo "Running the application with Streamlit interface..."
                streamlit run src/app.py
                echo "Press Enter to return to the menu."
                read
                ;;
            2)
                sync_dependencies
                ;;
            3)
                echo "Exiting..."
                deactivate
                exit 0
                ;;
            *)
                echo "Invalid choice. Please try again."
                ;;
        esac
    done
}

# Show the menu
menu
