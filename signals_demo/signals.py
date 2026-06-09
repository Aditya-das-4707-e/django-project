import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SignalTest

@receiver(post_save, sender=SignalTest)
def signal_demo_receiver(sender, instance, created, **kwargs):
    current_thread = threading.current_thread()
    print("\n--- [SIGNAL RECEIVER START] ---")
    print(f"Receiver: Handling post_save for '{instance.name}'")
    print(f"Receiver Thread Name: {current_thread.name}, ID: {current_thread.ident}")
    
    # Proof 1 & 2: Synchronous execution & Thread identity
    print("Receiver: Simulating slow task (sleeping for 2 seconds)...")
    time.sleep(2)
    print("Receiver: Slow task completed.")
    
    # Proof 3: Same transaction (rolls back the database record if exception is raised)
    if "rollback" in instance.name.lower():
        print("Receiver: 'rollback' detected in name. Raising ValueError to test transaction rollback.")
        print("--- [SIGNAL RECEIVER ERROR RAISED] ---\n")
        raise ValueError("Forced error to test transaction rollback.")
        
    print("--- [SIGNAL RECEIVER END] ---\n")
