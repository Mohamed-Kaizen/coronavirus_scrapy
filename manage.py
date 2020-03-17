import typer
import uvicorn

app = typer.Typer()


@app.command()
def serve():
    typer.echo(f"Running the server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")


if __name__ == "__main__":
    app()

