import pickle
import base64
import pyperclip

def serialize_to_clipboard(obj):
    """
    Serialize an arbitrary object using pickle, encode the bytes to base64,
    and copy the result to the clipboard.

    Parameters:
    - obj: The object to be serialized.

    Returns:
    None
    """
    try:
        serialized_data = pickle.dumps(obj)
        encoded_data = base64.b64encode(serialized_data).decode('utf-8')
        pyperclip.copy(encoded_data)
        print("Object serialized and copied to clipboard.")
    except Exception as e:
        print(f"Serialization error: {e}")

def deserialize_from_clipboard():
    """
    Read base64-encoded string from the clipboard, decode it, and
    de-serialize the bytes into an object instance.

    Returns:
    - The de-serialized object.
    """
    try:
        clipboard_data = pyperclip.paste()
        if clipboard_data:
            decoded_data = base64.b64decode(clipboard_data.encode('utf-8'))
            obj = pickle.loads(decoded_data)
            print("Object de-serialized successfully.")
            return obj
        else:
            print("Clipboard is empty. Nothing to de-serialize.")
            return None
    except Exception as e:
        print(f"De-serialization error: {e}")
        return None