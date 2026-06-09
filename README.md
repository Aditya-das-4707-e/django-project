# Accuknox Django Signals & Python Assignment

This repository contains the completed tasks for the Accuknox backend developer assignment. It is organized into a single Django project called `accuknox_assignment` with an app called `signals_demo`, along with a custom Python class demonstration.

---

## 1. Project Folder Structure

```text
django project/ (Root Directory)
├── manage.py
├── README.md
├── accuknox_assignment/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── signals_demo/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── custom_classes.py
    ├── migrations/
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── signals.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

---

## 2. How to Run the Project

### Prerequisites
Make sure Python 3 and Django are installed in your environment.

### Setup and Migration
1. Open your terminal in the root directory:
   ```bash
   cd "django project"
   ```
2. Run database migrations to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```

### Start the Server
3. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
4. Access the web dashboard by navigating to:
   ```text
   http://127.0.0.1:8000/
   ```

---

## 3. Topic 1 - Django Signals

### Q1: Are Django signals synchronous or asynchronous by default?
**Answer:** Django signals are **synchronous** by default. The execution of the caller block pauses and waits for the connected signal receivers to finish executing before resuming.

#### Proof Code (Receiver - `signals_demo/signals.py`):
```python
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SignalTest

@receiver(post_save, sender=SignalTest)
def signal_demo_receiver(sender, instance, created, **kwargs):
    print("\n--- [SIGNAL RECEIVER START] ---")
    print(f"Receiver: Handling post_save for '{instance.name}'")
    
    # Simulating a 2-second delay
    print("Receiver: Simulating slow task (sleeping for 2 seconds)...")
    time.sleep(2)
    print("Receiver: Slow task completed.")
    print("--- [SIGNAL RECEIVER END] ---\n")
```

#### Verification Run (Django Shell):
```python
from signals_demo.models import SignalTest
print("Caller: About to create model instance...")
SignalTest.objects.create(name="Synchronous Test")
print("Caller: Model instance created.")
```

#### Expected Console Output:
```text
Caller: About to create model instance...

--- [SIGNAL RECEIVER START] ---
Receiver: Handling post_save for 'Synchronous Test'
Receiver: Simulating slow task (sleeping for 2 seconds)...
[2-second delay observed here]
Receiver: Slow task completed.
--- [SIGNAL RECEIVER END] ---

Caller: Model instance created.
```
*Note that the caller output `"Caller: Model instance created."` is printed only after the signal receiver completes its 2-second sleep.*

---

### Q2: Do Django signals run in the same thread as the caller?
**Answer:** Yes, by default, Django signals run in the **same thread** as the caller.

#### Proof Code (Receiver - `signals_demo/signals.py`):
```python
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SignalTest

@receiver(post_save, sender=SignalTest)
def signal_demo_receiver(sender, instance, created, **kwargs):
    current_thread = threading.current_thread()
    print(f"Receiver Thread Name: {current_thread.name}, ID: {current_thread.ident}")
```

#### Verification Run (Django Shell):
```python
import threading
from signals_demo.models import SignalTest

caller_thread = threading.current_thread()
print(f"Caller Thread Name : {caller_thread.name}, ID: {caller_thread.ident}")
SignalTest.objects.create(name="Thread Test")
```

#### Expected Console Output:
```text
Caller Thread Name : MainThread, ID: 130961963982976

--- [SIGNAL RECEIVER START] ---
Receiver: Handling post_save for 'Thread Test'
Receiver Thread Name: MainThread, ID: 130961963982976
...
```
*The Thread IDs and names match exactly, demonstrating that they share the identical call stack thread.*

---

### Q3: Do Django signals run in the same database transaction as the caller?
**Answer:** Yes, Django signals run in the **same database transaction** as the caller. If an exception occurs inside the receiver, the caller's transaction is aborted and rolled back.

#### Proof Code (Receiver - `signals_demo/signals.py`):
```python
@receiver(post_save, sender=SignalTest)
def signal_demo_receiver(sender, instance, created, **kwargs):
    if "rollback" in instance.name.lower():
        print("Receiver: Raising ValueError to force rollback.")
        raise ValueError("Forced error to test transaction rollback.")
```

#### Verification Run (Django Shell / Script):
```python
from django.db import transaction
from signals_demo.models import SignalTest

try:
    with transaction.atomic():
        print("Caller: Creating instance inside transaction...")
        SignalTest.objects.create(name="Transaction rollback test")
except ValueError as e:
    print(f"Caller: Caught exception: '{e}'")

# Check if the record exists in the database
exists = SignalTest.objects.filter(name="Transaction rollback test").exists()
print(f"Record exists in DB: {exists}")
```

#### Expected Console Output:
```text
Caller: Creating instance inside transaction...
>>> Receiver: Inside signal handler.
>>> Receiver: Raising ValueError to force rollback.

Caller: Caught exception: 'Forced error to test transaction rollback.'
Record exists in DB: False
```
*Because the signal raised an exception, the entire transaction block was rolled back, meaning the record was never saved in the database.*

---

## 4. Topic 2 - Rectangle Class

A custom python class `Rectangle` that requires `length: int` and `width: int` at instantiation and allows iterating over the instance to return its dimensions as dictionaries.

#### Class Code (`signals_demo/custom_classes.py`):
```python
class Rectangle:
    """
    A Rectangle class that yields its dimensions (length first, then width)
    in the form of dictionaries when iterated over.
    """
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}
```

#### Demonstration of Iteration:
```python
from signals_demo.custom_classes import Rectangle

rect = Rectangle(length=15, width=8)

for dimension in rect:
    print(dimension)
```

#### Output:
```text
{'length': 15}
{'width': 8}
```

#### How it works under the hood:
The class defines the magic method `__iter__()` which transforms the class instance into an iterable generator. When iterated over (e.g. using a `for` loop), the generator yields `{'length': self.length}` first, pauses execution, and then yields `{'width': self.width}` on the subsequent iteration step.
