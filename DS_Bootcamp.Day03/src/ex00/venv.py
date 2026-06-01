#!/usr/bin/env python3
import os


def main():
    venv_path = os.getenv('VIRTUAL_ENV')
    if venv_path:
        print(f"Your current virtual env is: {venv_path}")
    else:
        print("The virtual environment is not activated")


if __name__ == "__main__":
    main()


# sudo apt update && sudo apt install python3 python3-pip python3-venv
