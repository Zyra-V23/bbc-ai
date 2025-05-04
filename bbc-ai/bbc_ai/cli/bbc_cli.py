import typer
import subprocess
import sys
from pathlib import Path

app = typer.Typer(no_args_is_help=False)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Smart Contract Audit Companion CLI.
    - 'bbc' launches the main interactive CLI (cli_runner.py)
    - 'bbc start' runs the setup
    """
    if ctx.invoked_subcommand is None:
        typer.echo("[bbc] Launching main CLI (cli_runner.py)...")
        subprocess.run([sys.executable, "../scripts/cli_runner.py"])

@app.command("start")
def start():
    """Initial setup for the BBC project."""
    docs = Path("docs")
    if not docs.exists():
        typer.echo("[bbc] Creating 'docs' folder...")
        docs.mkdir()
    else:
        typer.echo("[bbc] 'docs' folder already exists.")

    typer.echo("[bbc] Installing Python dependencies...")
    if not Path("requeriments.txt").exists():
        typer.echo("[bbc] 'requeriments.txt' not found!")
    else:
        subprocess.run(["pip", "install", "-r", "requeriments.txt"], check=True)

    env_example = Path(".env.example")
    if not env_example.exists():
        typer.echo("[bbc] Creating .env.example file...")
        env_example.write_text(
            """# Example environment variables for BBC\nDATABASE_URL=postgresql://bbc_user:bbc_password@localhost:5432/bbc_db\nANTHROPIC_API_KEY=your_anthropic_api_key_here\nSESSION_SECRET=your_session_secret_here\nADMIN_USERNAME=admin\nADMIN_PASSWORD=admin_password\n"""
        )
    else:
        typer.echo("[bbc] .env.example file already exists.")

    # Install PostgreSQL if not present and start the service
    typer.echo("[bbc] Installing PostgreSQL (if not present)...")
    subprocess.run(["sudo", "apt", "update"])  # Update package list
    subprocess.run(["sudo", "apt", "install", "-y", "postgresql", "postgresql-contrib"])
    typer.echo("[bbc] Starting PostgreSQL service...")
    subprocess.run(["sudo", "service", "postgresql", "start"])

    # Attempt to create the database and user automatically
    typer.echo("[bbc] Attempting to create PostgreSQL database and user...")
    try:
        subprocess.run(["sudo", "-u", "postgres", "psql", "-c", "CREATE DATABASE bbc_db;"], check=True)
        subprocess.run(["sudo", "-u", "postgres", "psql", "-c", "CREATE USER bbc_user WITH PASSWORD 'bbc_password';"], check=True)
        subprocess.run(["sudo", "-u", "postgres", "psql", "-c", "GRANT ALL PRIVILEGES ON DATABASE bbc_db TO bbc_user;"], check=True)
        typer.echo("[bbc] PostgreSQL database and user created successfully.")
    except Exception:
        typer.echo("[bbc] Could not automatically create the PostgreSQL database and user.")
        typer.echo("[bbc] If this is your first time setting up PostgreSQL, run the following commands:")
        typer.echo('  sudo -u postgres psql -c "CREATE DATABASE bbc_db;"')
        typer.echo('  sudo -u postgres psql -c "CREATE USER bbc_user WITH PASSWORD \'bbc_password\';"')
        typer.echo('  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE bbc_db TO bbc_user;"')

    typer.echo("[bbc] Setup complete. You can copy .env.example to .env and customize it.")

if __name__ == "__main__":
    app() 