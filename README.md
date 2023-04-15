

1. Python Environment Setup
### Check if your Python environment is already configured:
```
    python3 --version
    pip3 --version
```

2. Virtual Environment Setup#
Create a new virtual environment by choosing a Python interpreter and making a ./venv directory to hold it:
Ubuntu
```
    python3 -m venv ./venv
```
    - Activate the environment:
```
    source ./venv/bin/activate
```
macOS
```
    python3 -m venv ./venv
```
    - Activate the environment:
```
    source ./venv/bin/activate
```
Windows
```
    C:\> python3 -m venv ./venv
```
    - Activate the environment:
```
    C:\> .\venv\Scripts\activate
```

3. Install Rasa Open Source
First make sure your pip version is up to date:
```
    pip3 install -U pip
```
To install Rasa Open Source:
```
    pip3 install rasa
```
You can now create a new project with:
```
    rasa init
```
