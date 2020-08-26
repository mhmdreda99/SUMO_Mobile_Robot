import sumo_joystick
import sumo_arrowkeys

# Prompt for input device
continue_prompting = True
while continue_prompting:
  print('Input methods:')
  print('1: Arrow Keys')
  print('2: Controller')
  choice = input('Please select an input method (enter either 1 or 2): ')
  try:
    choice = int(choice)
    if choice < 1 or choice > 2:
      print('\nNumber not in range (please enter 1 or 2)\n')
    else:
      continue_prompting = False
  except ValueError:
    print('\nValue must be a number, try again\n')
  
if choice == 1:
  sumo_arrowkeys.main()
elif choice == 2:
  sumo_joystick.main()