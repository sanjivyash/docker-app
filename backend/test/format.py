class Format:
  styles =  {
    "blue" : '\033[94m',
    "cyan" : '\033[96m',
    "green" : '\033[92m',
    "yellow" : '\033[93m',
    "red" : '\033[91m',
    
    "header" : '\033[95m',
    "success" : '\033[92m',
    "warning" : '\033[93m',
    "error" : '\033[91m',
    
    "bold" : '\033[1m',
    "underline" : '\033[4m',
    "endc" : '\033[0m',
  }


def formatter(text: str, *args):
  start = "".join(map(lambda x: Format.styles[x], args))
  return f'{start}{text}{Format.styles["endc"]}'
