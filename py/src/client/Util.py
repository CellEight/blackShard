def choice(question, choices):
    selection = None 
    while selection not in choices:
        selection = input(f"[?] {question} [ ",".join(choices)}]: ").lower()
    return selection 
