import random
import string
from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console)]
)

console.print("[bold cyan]Enter total energy to distribute among the dots:[/bold cyan]", end=" ")
total_energy = int(input())  

console.print("[bold cyan]Enter the number of dots:[/bold cyan]", end=" ")
n = int(input())  

console.print("[bold cyan]Enter a name for this universe (this will be the filename):[/bold cyan]", end=" ")
universe_name = input().strip()  

EXCESS_THRESHOLD = total_energy / n  
DEFICIT_THRESHOLD = 0  

dot_names = [''.join(random.choices(string.ascii_uppercase, k=n)) for _ in range(n)]

dots = {name: {'energy': total_energy / n} for name in dot_names}

def simulation(dots):
    steps = 0
    stagnant_dots = set()  
    simulation_log = []   

    while True:
        steps += 1
        step_log = [f"Step {steps}:"]
        any_exchange_happened = False   

        active_dots = [dot for dot in dots if dot not in stagnant_dots]
        if active_dots:
            selected_dot = random.choice(active_dots)
            lost_energy = 1   

            energy_destination = random.choice(['the void', 'another dot'])

            if energy_destination == 'the void':
                dots[selected_dot]['energy'] -= lost_energy
                step_log.append(f"[bold red]{selected_dot} lost {lost_energy} energy to the void (new: {dots[selected_dot]['energy']:.2f}).[/bold red]")
            else:
                potential_targets = [dot for dot in active_dots if dot != selected_dot]
                
                if potential_targets: 
                    target_dot = random.choice(potential_targets)
                    dots[selected_dot]['energy'] -= lost_energy
                    dots[target_dot]['energy'] += lost_energy
                    step_log.append(f"[bold green]{selected_dot} lost {lost_energy} energy to {target_dot} (new: {dots[selected_dot]['energy']:.2f}). {target_dot} gained {lost_energy} energy (new: {dots[target_dot]['energy']:.2f}).[/bold green]")
                else:
                    dots[selected_dot]['energy'] -= lost_energy
                    step_log.append(f"[bold red]{selected_dot} lost {lost_energy} energy to the void (new: {dots[selected_dot]['energy']:.2f}).[/bold red]")

            if dots[selected_dot]['energy'] <= DEFICIT_THRESHOLD:
                step_log.append(f"[bold yellow]{selected_dot} is now stagnant (energy: {dots[selected_dot]['energy']:.2f}).[/bold yellow]")
                stagnant_dots.add(selected_dot)

        
        simulation_log.append("\n".join(step_log))

        console.print(f"\n[bold blue]State after Step {steps}:[/bold blue]")
        for dot_name, energy in dots.items():
            status = "Stagnant" if dot_name in stagnant_dots else "Active"
            console.print(f"{dot_name}: {energy['energy']:.2f} - Status: {status}", style="bold white")

        if all(dot in stagnant_dots for dot in dots):
            break

    log_filename = f"{universe_name}.univ"
    with open(log_filename, "w") as log_file:
        log_file.write("\n".join(simulation_log))

    return steps, dots, stagnant_dots

total_steps, final_dots, stagnant_dots = simulation(dots)

console.print("\n[bold blue]Final State:[/bold blue]")
console.print(final_dots)
console.print("[bold yellow]Stagnant Dots:[/bold yellow]", stagnant_dots)
