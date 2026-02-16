import typer
from daimon.commands.run import run_command
from daimon.commands.init import init_command

app = typer.Typer()

app.command()(run_command)
app.command()(init_command)

if __name__ == "__main__":
    app()