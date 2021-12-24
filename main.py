import typer
import git
from InquirerPy import inquirer

try:
    repo = git.Repo('.')
except git.exc.InvalidGitRepositoryError as err:
    typer.echo("This is not a Git repository")
    exit()

def get_branches():
    """Return the list of local branches except the active."""
    branches = []
    for ref in repo.heads:
        if ref != repo.active_branch:
            branches.append(ref)
    return branches

app = typer.Typer()

@app.command()
def list():
    branch = inquirer.select(
        message="Select a branch:",
        choices=get_branches(),
    ).execute()

    repo.git.checkout(branch)

@app.command()
def delete():
    branches = inquirer.checkbox(
        message="Select the branches:",
        choices=get_branches(),
        cycle=False,
    ).execute()

    for branch in branches:
        repo.delete_head(branch, force = True)
        typer.echo(f"Branch {branch} deleted")

@app.command()
def install():
    import os
    file_path = os.path.realpath(__file__)

    os.system(f"git config --global alias.list '!python3 {file_path} list'")
    os.system(f"git config --global alias.del '!python3 {file_path} delete'")

if __name__ == "__main__":
    app()