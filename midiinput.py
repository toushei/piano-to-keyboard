import mido
import threading
import time
from pynput.keyboard import Controller, Key

# Define a mapping from MIDI notes to keyboard characters
midi_to_char = {

  # Notes at the very left
    # A0,   A0#,    B0
    21: '', 22: '', 23: '',

  # White Keys 
  # C        D        E        F        G        A        B
    24: '' , 26: '' , 28: '' , 29: '' , 31: '' , 33: '' , 35: '' , # C1-B1
    36:Key.ctrl_l,
             38:Key.cmd,
                      40:Key.alt_l,
                               41: ';', 43: 'q', 45: 'j', 47: 'k', # C2-B2

    48: 'x', 50: ' ', 52: '' , 
                               53: 'a', 55: 'o', 57: 'e', 59: 'u', # C3-B3
    60: 'i', 62: ' ', 64: 'd', 65: 'h', 67: 't', 69: 'n', 71: 's', # C4-B4
    
    72: '' , 74: ' ', 76: 'b', 77: 'm', 79: 'w', 81: 'v', 83: 'z', # C5-B5

    84: '' , 86:Key.enter,
                      88:Key.left,
                               89:Key.down,
                                        91:Key.right,
                                                 93:'',95:'', # C6-B6
    


  # Black Keys
  # C#       D#       F#       G#       A#
    25: '' , 27: '' , 30: '' , 32: '' , 34: '',    # C1-B1
    37:Key.shift_l,
             39:Key.tab,
                      42: 'a', 44: ',', 46: 'e',    # C2-B2, tetris

    49: ' ', 51: 'p', # tetris
                      54: ' ', 56: 'p', 58: 'y',    # C3-B3
    61: 'f', 63: 'g', 66: 'c', 68: 'r', 70: 'l',    # C4-B4
    
    73: '' , 75: '' , 78: '' , 80: '' , 82: '' ,    # C5-B5
    85:Key.backspace,
             87:Key.delete,
                      90:Key.up,
                               92: '' , 94: '' ,    # C6-B6



  # Notes at the very right
  # C       C#      D       D#      E                 F        F#       G        G#       A        A#       B
    96: '', 97: '', 98: '', 99: '', 100: '', 101: '', 102: '', 103: '', 104: '', 105: '', 106: '', 107: '', # C7-B7

    108: '' # C8

 }

# Dictionary to keep track of currently held notes
held_notes = {}
keyboard = Controller()

# notes without autorepeat delay
tetris_nodelay = [42, 44, 46, 49, 51,      88, 89, 90, 91]
                # spins don't hold,     arrow keys no delay
def repeat_key(action, note_num):
    keyboard.press(action)

    if note_num not in tetris_nodelay:
        time.sleep(0.5)
    
    while action in held_notes:
        keyboard.press(action)
        time.sleep(0.03)
    keyboard.release(action)

def midi_listener():
    with mido.open_input(mido.get_input_names()[0]) as port:
        try:
            for msg in port:
                if msg.type == 'note_on':
                    note = msg.note

                    if note == 22:  # Stop script if A0# is hit
                        raise SystemExit

                    action = midi_to_char[note]
                    
                    if action == '': # unbound notes
                        continue

                    if note not in [42, 44, 46] and action not in held_notes:  # Prevent starting multiple threads
                        held_notes[action] = True
                    threading.Thread(target=repeat_key, args=(action,note)).start()

                elif msg.type == 'note_off':
                    note = msg.note
                    action = midi_to_char[note]
                    if action in held_notes:
                        del held_notes[action]  # Remove from held notes to stop the thread

        except KeyboardInterrupt:
            print("Stopped listening.")
            # Release any keys that might still be held down
            for key in held_notes.keys():
                keyboard.release(key)

if __name__ == "__main__":
    midi_listener()

