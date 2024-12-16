# Interactive Graphical System

## About

Project developed for the Computer Graphics class at UFSC

## Dependencies

- Running Linux
- GTK 3 installed
- Numpy Python library installed

## How to run

You only need to run the following command in the root directory
```
python3 main.py
```

When adding a new object, use a pattern like this (it draws a square):

```
(500.0, 500.0), (500.0, 200.0), (200.0, 200.0), (200.0, 500.0)
```

Or something like this for a curve:

```
(500.0, 500.0, 0.0), (500.0, 200.0, 0.0), (200.0, 200.0, 0.0), (200.0, 500.0, 0.0), (200.0, 800.0, 0.0), (-100.0, 800.0, 0.0), (-100.0, 500.0, 0.0)
(633.0, 600.0, 0.0), (829.0, 260.0, 0.0), (200.0, 200.0, 0.0), (200.0, 500.0, 0.0), (200.0, 800.0, 0.0), (609.0, 257.0, 0.0), (298.0, 268.0, 0.0)
(15.0, 791.0, 0.0), (666.0, 327.0, 0.0), (200.0, 200.0, 0.0), (200.0, 500.0, 0.0), (200.0, 800.0, 0.0), (609.0, 257.0, 0.0), (298.0, 268.0, 0.0)
```

Cube:
```
(100, 400, 100), (100, 600, 100), (300, 600, 100), (300, 400, 100), (100, 400, 100), (100, 400, 300), (100, 600, 300), (100, 600, 100), (300, 600, 100), 
(300, 600, 300), (300, 400, 300), (300, 400, 100), (300, 400, 300), (100, 400, 300), (100, 600, 300), (300, 600, 300)
```

```
(100, 400, -200), (100, 600, -200), (300, 600, -200), (300, 400, -200), (100, 400, -200), (100, 400, 300), (100, 600, 300), (100, 600, -200), (300, 600, -200), (300, 600, 300), (300, 400, 300), (300, 400, -200), (300, 400, 300), (100, 400, 300), (100, 600, 300), (300, 600, 300)
```