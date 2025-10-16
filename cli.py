import click
from datetime import datetime
from models.user import User
from models.glucose_entry import GlucoseEntry

def format_timestamp(ts):
    """Convert ISO timestamp to 12-hour format with AM/PM"""
    dt = datetime.fromisoformat(ts)
    return dt.strftime("%Y-%m-%d %I:%M:%S %p")

@click.group()
def cli():
    """Blood Glucose Tracker CLI"""
    pass

@cli.command()
def menu():
    """Interactive menu for the tracker"""
    while True:
        click.echo("\n=== Blood Glucose Tracker CLI ===")
        click.echo("1. Create User")
        click.echo("2. View All Users")
        click.echo("3. Add Glucose Entry")
        click.echo("4. View Glucose Entries for a User")
        click.echo("5. Delete User")
        click.echo("0. Exit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            name = click.prompt("Enter name")
            age = click.prompt("Enter age", type=int)
            email = click.prompt("Enter email")
            try:
                user = User.create(name, age, email)
                click.echo(f"✅ User created: {user.id} | {user.name} | {user.email}")
            except Exception as e:
                click.echo(f"❌ Error creating user: {e}")

        elif choice == 2:
            users = User.get_all()
            if not users:
                click.echo("No users found.")
            for u in users:
                click.echo(f"{u.id} | {u.name} | {u.age} | {u.email}")

        elif choice == 3:
            user_id = click.prompt("Enter user ID", type=int)
            value = click.prompt("Enter glucose value (mmol/L)", type=float)
            notes = click.prompt("Enter notes (optional)", default="")
            user_obj = User.find_by_id(user_id)
            if not user_obj:
                click.echo("User not found.")
                continue
            entry = GlucoseEntry.create(user_id, value, notes)
            click.echo(f"✅ Entry added: {entry.id} | {entry.value_mmol} mmol/L | {format_timestamp(entry.timestamp)} | {entry.notes}")

        elif choice == 4:
            user_id = click.prompt("Enter user ID", type=int)
            user_obj = User.find_by_id(user_id)
            if not user_obj:
                click.echo("User not found.")
                continue
            entries = user_obj.glucose_entries()
            if not entries:
                click.echo("No glucose entries found for this user.")
                continue
            for e in entries:
                click.echo(f"{e.id} | {e.value_mmol} mmol/L | {format_timestamp(e.timestamp)} | {e.notes}")

        elif choice == 5:
            user_id = click.prompt("Enter user ID to delete", type=int)
            user_obj = User.find_by_id(user_id)
            if not user_obj:
                click.echo("User not found.")
                continue
            for e in user_obj.glucose_entries():
                GlucoseEntry.delete(e.id)
            User.delete(user_id)
            click.echo(f"User {user_id} and related entries deleted.")

        elif choice == 0:
            click.echo("Goodbye!")
            break

        else:
            click.echo("Invalid option. Try again.")

if __name__ == "__main__":
    cli()
