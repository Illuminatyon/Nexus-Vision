"""
Library Check Utility for Reconnaissance Vidéo Python v1

This script checks if all required libraries for the Reconnaissance Vidéo Python v1
program are installed correctly and provides information about their versions.
"""

import sys
import importlib.util
import subprocess
import platform

# List of required libraries
required_libraries = [
    {"name": "opencv-python", "import_name": "cv2", "min_version": "4.5.0"},
    {"name": "mediapipe", "import_name": "mediapipe", "min_version": "0.8.9"},
    {"name": "numpy", "import_name": "numpy", "min_version": "1.19.0"}
]

def check_library(library):
    """Check if a library is installed and get its version."""
    try:
        # Check if the library is installed
        spec = importlib.util.find_spec(library["import_name"])
        if spec is None:
            return False, None

        # Import the library to get its version
        module = importlib.import_module(library["import_name"])
        version = getattr(module, "__version__", "unknown")

        return True, version
    except Exception as e:
        return False, str(e)

def main():
    print("\n=== Library Check for Reconnaissance Vidéo Python v1 ===\n")

    # Print Python version
    print(f"Python version: {platform.python_version()}")
    print(f"System: {platform.system()} {platform.release()}\n")

    all_installed = True

    # Check each required library
    for library in required_libraries:
        installed, version = check_library(library)

        if installed:
            status = "✓ Installed"
            if version != "unknown":
                if library["min_version"] and version < library["min_version"]:
                    status = f"⚠ Installed (version {version}, recommended: {library['min_version']}+)"
                    all_installed = False
            else:
                status = "✓ Installed (version unknown)"
        else:
            status = "✗ Not installed"
            all_installed = False

        print(f"{library['name']}: {status}")
        if not installed:
            print(f"  - Install with: pip install {library['name']}")

    print("\n=== Summary ===")
    if all_installed:
        print("All required libraries are installed correctly! ✓")
        print("You can run the main program with: python main.py")
    else:
        print("Some libraries are missing or need to be updated. ✗")
        print("Please install the missing libraries using:")
        print("  pip install -r requirements.txt")

    print("\n=== Troubleshooting ===")
    print("If you encounter issues with MediaPipe:")
    print("  - Try: pip install --upgrade mediapipe")
    print("  - For Windows users: Make sure Visual C++ build tools are installed")
    print("\nIf you encounter issues with OpenCV:")
    print("  - Make sure your webcam is properly connected")
    print("  - Check if other applications are using the camera")

if __name__ == "__main__":
    main()
