import os
import subprocess


def main():
    figgy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'main.py')
    subprocess.call(f"pgzrun {figgy_path}", shell=True)


if __name__ == "__main__":
    main()