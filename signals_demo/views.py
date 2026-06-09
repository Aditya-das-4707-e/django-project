import time
import threading
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from .models import SignalTest
from .custom_classes import Rectangle

def home_view(request):
    """
    Main dashboard view explaining the assignment tasks and providing endpoints to test them.
    """
    html_content = """
    <html>
    <head>
        <title>Accuknox Assignment Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; background-color: #f9f9f9; color: #333; }
            h1 { color: #2c3e50; }
            h2 { color: #2980b9; margin-top: 30px; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
            a.btn { display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold; margin-top: 10px; }
            a.btn:hover { background: #2980b9; }
            pre { background: #eee; padding: 10px; border-radius: 4px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Accuknox Backend Assignment Dashboard</h1>
        <p>This Django project demonstrates Django Signals behaviors (synchronicity, threading, transaction context) and a custom iterable Python class.</p>
        
        <div class="card">
            <h2>Question 1 & 2: Synchronous & Thread Identity Proof</h2>
            <p>Triggers a signal, sleeps for 2 seconds in the signal handler, and compares caller/receiver Thread IDs.</p>
            <a class="btn" href="/test-sync-thread/">Run Sync & Thread Test</a>
        </div>

        <div class="card">
            <h2>Question 3: Transaction Rollback Proof</h2>
            <p>Triggers a signal inside an atomic transaction block that raises an exception, proving the database save is rolled back.</p>
            <a class="btn" href="/test-transaction-rollback/">Run Transaction Rollback Test</a>
        </div>

        <div class="card">
            <h2>Rectangle Class Iteration Proof</h2>
            <p>Iterates over an instance of the custom <code>Rectangle</code> class to yield length and width as dictionaries.</p>
            <a class="btn" href="/test-rectangle/">Run Rectangle Iteration Test</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def test_sync_thread_view(request):
    """
    View to test synchronicity and thread identity.
    """
    caller_thread = threading.current_thread()
    print("\n" + "="*50)
    print("--- VIEW CALLER START ---")
    print(f"Caller Thread Name : {caller_thread.name}")
    print(f"Caller Thread ID   : {caller_thread.ident}")
    print("="*50)

    start_time = time.time()
    # Save a model instance to trigger post_save
    instance = SignalTest.objects.create(name="Sync & Thread Test Instance")
    end_time = time.time()
    
    elapsed = end_time - start_time
    print(f"--- VIEW CALLER END (Took {elapsed:.2f} seconds) ---")
    print("="*50 + "\n")

    return JsonResponse({
        "status": "Success",
        "message": "Signal triggered and completed synchronously.",
        "caller_thread_name": caller_thread.name,
        "caller_thread_id": caller_thread.ident,
        "time_taken_seconds": f"{elapsed:.4f}",
        "note": "Verify in console logs that the receiver Thread ID and caller Thread ID match exactly, and the caller waited for 2 seconds."
    })

def test_transaction_rollback_view(request):
    """
    View to test transaction rollback.
    """
    # Clean previous records
    SignalTest.objects.filter(name__icontains="rollback").delete()

    print("\n" + "="*50)
    print("--- VIEW CALLER: START TRANSACTION BLOCK ---")
    print("="*50)

    exception_caught = False
    error_message = ""
    try:
        with transaction.atomic():
            print("Caller: Creating instance with 'rollback' keyword in name...")
            instance = SignalTest.objects.create(name="Transaction rollback test instance")
    except ValueError as e:
        exception_caught = True
        error_message = str(e)
        print(f"Caller: Caught expected exception: '{e}'")

    # Verify if record exists in DB
    record_exists = SignalTest.objects.filter(name="Transaction rollback test instance").exists()
    print("="*50)
    print(f"Caller: Verification - Does record exist in database? {record_exists}")
    print("--- VIEW CALLER: END TRANSACTION BLOCK ---")
    print("="*50 + "\n")

    return JsonResponse({
        "status": "Verification Completed",
        "exception_caught": exception_caught,
        "error_message": error_message,
        "record_exists_in_database": record_exists,
        "conclusion": "Since the record exists check is FALSE, the database operation was rolled back together with the signal error."
    })

def test_rectangle_view(request):
    """
    View to demonstrate Rectangle iteration.
    """
    rect = Rectangle(length=15, width=8)
    items = list(rect)
    return JsonResponse({
        "class": "Rectangle",
        "input": {"length": rect.length, "width": rect.width},
        "iteration_results": items
    })
