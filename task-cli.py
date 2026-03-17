import datetime
import json

ID = 0

class task:
  def __init__( self, description ):
    global ID
    self.id = ID
    self.description = description
    self.status = "todo"
    self.createdAt = datetime.datetime.now().isoformat()
    self.updatedAt = datetime.datetime.now().isoformat()

def addTask(description):
  global ID
  newTask = task(description)
  try:
    with open('tasks.json', 'r') as json_file:
      data = json.load(json_file)
  except (FileNotFoundError, json.decoder.JSONDecodeError):
    # If the file doesn't exist or is empty, start a new empty list
    data = []
  data.append(newTask.__dict__)
  with open('tasks.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
  print(f'Task added successfully (id: {newTask.id})')
  ID = ID + 1

def updateTask(id, description):
  try:
    with open('tasks.json', 'r') as json_file:
      data = json.load(json_file)
      for task in data:
        if (task['id'] == int(id)):
          task['description'] = description
          task['updatedAt'] = datetime.datetime.now().isoformat()
    with open('tasks.json', 'w') as json_file:
      json.dump(data, json_file, indent=4)
  except json.decoder.JSONDecodeError:
    print('No matching task found.')
    return

def deleteTask(id):
  try:
    with open('tasks.json', 'r') as json_file:
      data = json.load(json_file)
      for task in data:
        if (task['id'] == int(id)):
          data.remove(task)
          print(f'Task {id} deleted successfully.')
          break
    with open('tasks.json', 'w') as json_file:
      json.dump(data, json_file, indent=4)
  except json.decoder.JSONDecodeError:
    print('No tasks found.')
    return

def listTasks(status):
  try:
    with open('tasks.json', 'r') as json_file:
      data = json.load(json_file)
      for task in data:
        if (status == '' or task['status'] == status):
          print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
  except json.decoder.JSONDecodeError:
    print('No tasks found.')
    return

def markTask(id, status):
  try:
    with open('tasks.json', 'r') as json_file:
      data = json.load(json_file)
      found = False
      for task in data:
        if (task['id'] == int(id)):
          task['status'] = status
          task['updatedAt'] = datetime.datetime.now().isoformat()
          found = True
          break
      if not found:
        print('No matching task found.')
        return
    with open('tasks.json', 'w') as json_file:
      json.dump(data, json_file, indent=4) 
      print(f'Task {id} marked as {status}.')
  except json.decoder.JSONDecodeError:
    print('No matching task found.')
    return


while(True):
  print('Welcome to the task manager!')
  userinput = input('What would you like to do? (add, list, update, delete, exit) ')
  inputs = userinput.split(' ')
  if inputs[0] == 'add':
    if (len(inputs) < 2):
      print('Please provide a description for the task.')
    addTask(inputs[1])
  elif inputs[0] == 'list':
    if (len(inputs) < 2):
      listTasks('')
    else:
      match inputs[1]:
        case 'todo':
          listTasks('todo')
        case 'done':
          listTasks('done')
        case 'in-progress':
          listTasks('in-progress')
        case _:
          print('Invalid input, please try again.')
  elif inputs[0] == 'update':
    if (len(inputs) < 3):
      print('Please provide an id and a description for the task.')
    updateTask(inputs[1], inputs[2])
  elif inputs[0] == 'delete':
    if (len(inputs) < 2):
      print('Please provide an id for the task.')
    deleteTask(inputs[1])
  elif inputs[0] == 'mark-in-progress':
    if (len(inputs) < 2):
      print('Please provide an id for the task.')
    markTask(inputs[1], 'in-progress')
  elif inputs[0] == 'mark-done':
    if (len(inputs) < 2):
      print('Please provide an id for the task.')
    markTask(inputs[1], 'done')
  elif inputs[0] == 'exit':
    break
  else:
    print('Invalid input, please try again.')