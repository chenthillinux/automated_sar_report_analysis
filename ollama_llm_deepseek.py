import subprocess
import os

def install_ollama():
    """Install Ollama if not already installed."""
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Ollama is already installed.")
    except FileNotFoundError:
        print("Ollama not found. Installing Ollama...")
        subprocess.run(["curl", "-fsSL", "https://ollama.com/install.sh", "-o", "install_ollama.sh"], check=True)
        subprocess.run(["chmod", "+x", "install_ollama.sh"], check=True)
        subprocess.run(["./install_ollama.sh"], check=True)
        os.remove("install_ollama.sh")
        print("Ollama installed successfully.")

def pull_deepseek_model():
    """Pull the DeepSeek R1 8B model using Ollama."""
    print("Pulling DeepSeek R1 8B model...")
    subprocess.run(["ollama", "pull", "deepseek-r1:8b"], check=True)
    print("DeepSeek R1 8B model pulled successfully.")

def read_file():
    """Prompt the user for a file path and read its content."""
    file_path = input("Enter the path to the log file: ").strip()
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

def analyze_log_with_deepseek(log_content):
    """Send the log content to the DeepSeek model for analysis."""
    if not log_content:
        print("No log content to analyze.")
        return

    # Construct the prompt
    prompt = f"""
    Analyze the following log file and provide a summary of key events, errors, and warnings:
    
    {log_content}
    
    Provide a detailed analysis, including:
    1. Any critical errors or warnings.
    2. Patterns or trends in the log data.
    3. Suggestions for troubleshooting or improving the system.
    """

    # Run the DeepSeek model with the prompt
    print("Sending log content to DeepSeek model for analysis...")
    result = subprocess.run(
        ["ollama", "run", "deepseek-r1:8b"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Print the model's response
    if result.returncode == 0:
        print("DeepSeek Model Analysis:")
        print(result.stdout.decode())
    else:
        print("Error running the DeepSeek model:")
        print(result.stderr.decode())

if __name__ == "__main__":
    # Step 1: Install Ollama (if not already installed)
    install_ollama()

    # Step 2: Pull the DeepSeek R1 8B model
    pull_deepseek_model()

    # Step 3: Prompt the user for the log file path and analyze it
    log_content = read_file()

    # Step 4: Analyze the log content using the DeepSeek model
    if log_content:
        analyze_log_with_deepseek(log_content)
