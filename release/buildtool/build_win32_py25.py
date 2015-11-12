import subprocess


def main():
    subprocess.check_call(["python", "build.py", "win32py25"])


if __name__ == "__main__":
    main()
