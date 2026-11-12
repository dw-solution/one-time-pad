# One-Time Pad Generator

A small desktop app that generates one-time pad key material. Start it, select **Generate**, and it fills the window with cryptographically random numbers in five-digit groups, the classic pad format. It runs on Windows, macOS, and Linux.

![The generator after selecting Generate, showing a pad of 50 five-digit groups](screenshot.png)

## Where the randomness comes from

Every symbol comes from Python's `secrets` module, which reads the operating system's cryptographically secure random number generator: `getrandom()` on Linux, `BCryptGenRandom` on Windows, and the kernel CSPRNG on macOS. `secrets.choice` uses rejection sampling, so each digit or letter is equally likely and the pad carries no modulo bias. The test suite includes a chi-square check on 100,000 digits as a sanity test of that uniformity.

## Using it

| Control | What it does |
|---|---|
| Symbols | Digits (0-9), Letters (A-Z), or Hex (0-9, A-F) |
| Groups | How many groups to generate, 1 to 1000 (default 50) |
| Group size | Symbols per group, 1 to 20 (default 5) |
| Generate | Creates a new pad. `Enter` does the same |
| Copy | Puts the pad on the clipboard |
| Save... | Writes the pad to a text file. `Ctrl+S` does the same |
| Clear | Wipes the pad from the window |

Each pad gets a random 8-character ID and a UTC timestamp in its header, so the two parties holding copies can confirm they are on the same sheet.

A one-time pad is only secure when the key is truly random, at least as long as the message, kept secret, and **never reused**. Use a pad once, then destroy every copy, including saved files and anything left on the clipboard.

## Running it

### Download a build (no Python needed)

Tagged releases on GitHub carry prebuilt binaries for each platform under **Releases**:

- `OneTimePad-windows.exe` runs directly. SmartScreen may warn because the binary is unsigned; choose **More info**, then **Run anyway**.
- `OneTimePad-macos.zip` unzips to `OneTimePad.app`. The app is unsigned, so the first launch needs right-click, **Open**.
- `OneTimePad-linux` is for 64-bit Intel and AMD PCs. It needs `chmod +x OneTimePad-linux` before it runs.
- `OneTimePad-linux-arm64` is for 64-bit ARM Linux, including a Raspberry Pi 3, 4, 5, or Zero 2 W running the 64-bit Raspberry Pi OS (Bookworm or newer) with the desktop. It also needs `chmod +x` first.

The Linux builds are made on Ubuntu 22.04, so they run on that release and anything newer. A 32-bit Raspberry Pi OS can't run either binary; use the source instructions below instead.

### Run from source

Requires Python 3.9 or newer with Tkinter. The python.org installers for Windows and macOS include Tkinter. On Ubuntu or Debian, install it with `sudo apt install python3-tk`. Raspberry Pi OS with the desktop already includes it.

```
git clone <this repo>
cd one-time-pad
python3 onetimepad.py
```

`python3 -m otp` works too. There are no third-party dependencies.

### Run the tests

```
python3 -m unittest discover -s tests -v
```

## Building binaries yourself

```
pip install pyinstaller
pyinstaller --onefile --windowed --name OneTimePad onetimepad.py
```

The result lands in `dist/`. PyInstaller builds for the platform it runs on, so a Windows binary has to be built on Windows, and so on. The GitHub Actions workflow in `.github/workflows/build.yml` does this on all three platforms for every push, and attaches the binaries to a release when a `v*` tag is pushed.

## Layout

```
onetimepad.py      entry point (also the PyInstaller target)
otp/pad.py         pad generation and formatting
otp/gui.py         Tkinter interface
tests/test_pad.py  unit tests
```
