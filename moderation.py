def moderate(command):
    # Block obvious harmful commands
    blocked = ["rm -rf", "shutdown", "format", "dd", "netsh"]
    return not any(x in command for x in blocked)
