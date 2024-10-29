from rich.console import Console

console = Console()

console.print("[cyan]Universe Name: ", end="")
universe = input("")

with open(f"{universe}.univ", 'r') as f:
    lines = f.readlines()

for line in lines:
    console.print(line.strip())
