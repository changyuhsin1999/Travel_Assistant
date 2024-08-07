import os
import platform
import subprocess
import sys


def run_llamafile(model_name):
    # Get the current operating system
    current_os = platform.system()

    # Define the model file based on the OS

    model_file = model_name

    # Perform OS-specific actions
    if current_os == "Windows":

        # Rename the file to .exe if not already done
        if not model_file.endswith(".exe"):
            new_model_file = f"{model_name}.exe"
            # check if new_model_file already exists
            if not os.path.exists(new_model_file):
                if os.path.exists(model_name):
                    os.rename(model_name, new_model_file)
                else:
                    print(f"Model file not found: {model_name}")
                    sys.exit(1)

            model_file = new_model_file

        # Run the executable
        try:
            subprocess.run([model_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run the model: {e}")

    elif current_os in ["Linux", "Darwin", "FreeBSD"]:
        # Make the file executable
        try:
            subprocess.run(["chmod", "+x", model_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to make the file executable: {e}")
            sys.exit(1)

        # Run the executable
        try:
            subprocess.run([f"./{model_file}"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run the model: {e}")
            sys.exit(1)

    else:
        print(f"Unsupported operating system: {current_os}")
        sys.exit(1)


if __name__ == "__main__":
    # Replace with your actual model filename without extension
    model_filename = "mistral-7b-instruct-v0.2.Q4_0.llamafile"
    if sys.argv[1:]:
        model_filename = sys.argv[1]
    run_llamafile(model_filename)
