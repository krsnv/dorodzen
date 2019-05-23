# Dorodzen - tiny pomodoro timer

Pomodoro Timer running with Dzen2. Best timer for tiling window managers.
Forked from and inspired by Pomodzen: https://github.com/wrl/pomodzen

![Dorodzen screenshot](https://raw.githubusercontent.com/krsnv/dorodzen/master/screenshot.gif)

![Dorodzen animated preview](https://raw.githubusercontent.com/krsnv/dorodzen/master/live-preview.gif)

## Installation

Dorodzen uses Dzen2 for drawing timer progress bar.

Ubuntu:
```
sudo apt install dzen2
```

Dorodzen is best with Terminus font:

```
sudo apt install xfonts-terminus
```

## Usage

### Basics

Simple example of usage is here:

```
python dorodzen.py
```

Or:

```
# Make it executable
chmod +x dorodzen.py

# And run
./dorodzen.py

```

You can also copy dorodzen to `/usr/sbin`:

```
chmod +x dorodzen.py
cp /usr/sbin/dorodzen
```

And anywhere from terminal:

```
dorodzen
```

Or using your dmenu.

### Notifications

You can add your voice record or music, or, maybe, alarm sound using command flag. It will be running after timer ends.

Also, you can add any kind of notification. 
