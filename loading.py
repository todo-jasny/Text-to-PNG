# Code authored by Anthony Albright
# albright.anthony21@gmail.com
import sys
import time
import threading

def circle(stop_event, message="Loading", interval=0.1):
    """Display a spinning loading animation."""
    loading_chars = [' /', ' |', ' \\', ' -']
    while not stop_event.is_set():
        for char in loading_chars:
            if stop_event.is_set():
                break
            with threading.Lock():
                sys.stdout.write(f'\r{message} {char}')
                sys.stdout.flush()
            time.sleep(interval)
    with threading.Lock():
        sys.stdout.write(f'\r{message} done!{" " * 10}\n')  # Clear the line after done

def dots(stop_event, message="Loading", interval=0.1):
    """Display a dot-based loading animation."""
    loading_chars = [' ', ' .', ' ..', ' ...']
    while not stop_event.is_set():
        for char in loading_chars:
            if stop_event.is_set():
                break
            with threading.Lock():
                sys.stdout.write(f'\r{message} {char}')
                sys.stdout.flush()
            time.sleep(interval)
    with threading.Lock():
        sys.stdout.write(f'\r{message} done!{" " * 10}\n')  # Clear the line after done

def run(task_function, message="Loading", interval=0.1, animation_type=circle):
    """Run a task with a loading animation and return the result.

    Args:
        task_function (callable): The task to run.
        message (str): Message to display during loading.
        interval (float): Time interval for the animation.
        animation_type (function): The type of loading animation (circle or dots).

    Returns:
        The result of the task_function, or None if there was an error.
    """
    if animation_type not in (circle, dots):
        raise ValueError("Invalid animation type. Choose 'circle' or 'dots'.")
    
    stop_event = threading.Event()
    animation_thread = threading.Thread(target=animation_type, args=(stop_event, message, interval))
    animation_thread.start()

    result = None
    try:
        result = task_function()  # Capture the result of the task_function
    except Exception as e:
        with threading.Lock():
            sys.stdout.write(f'\r{message} failed: {e}{" " * 10}\n')  # Clear the line after failure
    finally:
        stop_event.set()
        animation_thread.join()
    
    return result  # Return the result of the task_function
