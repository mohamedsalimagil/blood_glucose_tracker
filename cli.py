import click
from datetime import datetime
from models.user import User
from models.glucose_entry import GlucoseEntry

# Helper function to display timestamps in a 12-hour readable format (e.g., 02:30 PM)
def format_timestamp(ts):
    """Convert ISO timestamp to 12-hour format with AM/PM"""
    dt = datetime.fromisoformat(ts)
    return dt.strftime("%Y-%m-%d %I:%M:%S %p")

@click.group()
def cli():
    """Main group for Click commands (only used because Click needs it)."""
    pass

@cli.command()
def menu():
    """Runs the interactive menu-based version of the tracker."""
    
    # This while loop keeps the app running until the user chooses to exit
    while True:
        click.echo("\n=== Blood Glucose Tracker CLI ===")
        click.echo("1. Create User")
        click.echo("2. View All Users")
        click.echo("3. Add Glucose Entry")
        click.echo("4. View Glucose Entries for a User")
        click.echo("5. Delete User")
        click.echo("6. Edit Glucose Entry")
        click.echo("0. Exit")

        # Ask the user to choose an option (must be a number)
        choice = click.prompt("Enter your choice", type=int)

        # ✅ OPTION 1: Create a new user
        if choice == 1:
            # Get and validate name (must be only letters and spaces)
            name = click.prompt("Enter name").strip()
            if not all(part.isalpha() for part in name.split()) or len(name) < 2:
                click.echo(" Name must contain only letters and spaces, with at least 2 characters.")
                continue

            # Get and validate age (must be a positive number)
            age = click.prompt("Enter age", type=int)
            if age <= 0:
                click.echo(" Age must be a positive integer.")
                continue

            # Get and validate email (basic check for @ and .)
            email = click.prompt("Enter email")
            if "@" not in email or "." not in email:
                click.echo(" Invalid email format.")
                continue

            # Try to create the user and handle any database errors
            try:
                user = User.create(name, age, email)
                click.echo(f" User created: {user.id} | {user.name} | {user.email}")
            except Exception as e:
                click.echo(f"Error creating user: {e}")

        # OPTION 2: List all users in the system
        elif choice == 2:
            users = User.get_all()
            if not users:
                click.echo("No users found.")
            for u in users:
                click.echo(f"{u.id} | {u.name} | {u.age} | {u.email}")

        # OPTION 3: Add a glucose reading for a specific user
        elif choice == 3:
            user_id = click.prompt("Enter user ID", type=int)
            value = click.prompt("Enter glucose value (mmol/L)", type=float)
            notes = click.prompt("Enter notes (optional)", default="")

            # Check if the user exists before adding an entry
            user_obj = User.find_by_id(user_id)
            if not user_obj:
                click.echo("User not found.")
                continue

            entry = GlucoseEntry.create(user_id, value, notes)
            click.echo(f" Entry added: {entry.id} | {entry.value_mmol} mmol/L | {format_timestamp(entry.timestamp)} | {entry.notes}")

        # OPTION 4: View all glucose entries for a given user
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

        #  OPTION 5: Delete a user AND all their related entries
        elif choice == 5:
            user_id = click.prompt("Enter user ID to delete", type=int)
            user_obj = User.find_by_id(user_id)
            if not user_obj:
                click.echo("User not found.")
                continue

            # Delete all their entries first, then delete user
            for e in user_obj.glucose_entries():
                GlucoseEntry.delete(e.id)

            User.delete(user_id)
            click.echo(f"User {user_id} and related entries deleted.")

        #  OPTION 6: Edit an existing glucose entry (value or notes)
        elif choice == 6: 
            entry_id = click.prompt("Enter Entry ID to edit", type=int)
            entry = GlucoseEntry.find_by_id(entry_id)

            if not entry:
                click.echo("Entry not found.")
                continue

            # Ask user for new values — pressing Enter keeps old data
            new_value = click.prompt(
                f"Current value is {entry.value_mmol}. Enter new value or press Enter to keep",
                default="",
                show_default=False
            )
            new_notes = click.prompt(
                f"Current notes are '{entry.notes}'. Enter new notes or press Enter to keep",
                default="",
                show_default=False
            )

            # If the user leaves a field blank, we don't update that part
            value_to_update = float(new_value) if new_value else None
            notes_to_update = new_notes if new_notes else None

            updated = GlucoseEntry.update(entry_id, value_to_update, notes_to_update)
            if updated:
                click.echo(
                    f" Updated: {updated.id} | {updated.value_mmol} mmol/L | "
                    f"{format_timestamp(updated.timestamp)} | {updated.notes}"
                )
            else:
                click.echo(" Update failed.")

        #  OPTION 0: Exit the program cleanly
        elif choice == 0:
            click.echo("Goodbye!")
            break

        # Handle invalid menu input
        else:
            click.echo("Invalid option. Try again.")

if __name__ == "__main__":
    cli()
