import typer

from src.train import train_model as train_main
from src.predict import main as predict_main
from scripts.validate_historical_matches import validate_historical_matches as validate_main


def version_callback(value: bool):
    if value:
        typer.echo("Football Prediction CLI v1.0")
        raise typer.Exit()


app = typer.Typer(help="Football Prediction Project CLI")


@app.command()
def train():
    """Train the models and save artifacts."""
    train_main()


@app.command()
def predict():
    """Make predictions on upcoming matches."""
    predict_main()


@app.command()
def validate():
    """Validate historical match data for consistency."""
    validate_main()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Mostra a versão do CLI"
    )
):
    pass


if __name__ == "__main__":
    app()
