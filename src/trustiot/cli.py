import click
import importlib.util
from trustiot.simulation import run_simulation
from trustiot.visualize import display_enhanced_results

@click.command()
@click.argument('setup_script', type=click.Path(exists=True))
@click.option('--num-runs', default=5, help='Number of benchmark runs.')
@click.option('--show-plots/--no-plots', default=True, help='Display plots.')
def cli(setup_script, num_runs, show_plots):
    """A simulation framework for task allocation in edge computing environments."""

    # Dynamically import the user-defined setup script
    spec = importlib.util.spec_from_file_location("setup", setup_script)
    setup_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup_module)

    # Check if the setup script has a 'setup' function
    if not hasattr(setup_module, 'setup'):
        raise click.UsageError("The setup script must have a 'setup' function.")

    # Run the simulation
    results = run_simulation(setup_module.setup, num_runs=num_runs)

    # Display the results
    if show_plots:
        display_enhanced_results(results, "Custom Simulation", setup_module.setup)

if __name__ == '__main__':
    cli()