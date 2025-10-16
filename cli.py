import click
from models.user import User
from models.glucose_entry import GlucoseEntry

@click.group()
def main():
    """Blood Glucose Tracker CLI"""
    pass

# ------------------ User Commands ------------------

@main.group()
def user():
    """Manage Users"""
    pass

@user.command()
@click.option("--name", prompt="Name", help="User's name")
@click.option("--age", prompt="Age", type=int, help="User's age")
@click.option("--email", prompt="Email", help="User's email")
def create(name, age, email):
    """Create a new user"""
    try:
        u = User.create(name, age, email)
        click.echo(f"✅ User created: {u.id} | {u.name} | {u.email}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@user.command()
def list():
    """List all users"""
    users = User.get_all()
    for u in users:
        click.echo(f"{u.id} | {u.name} | {u.age} | {u.email}")

@user.command()
@click.argument("user_id", type=int)
@click.option("--name", help="New name")
@click.option("--age", type=int, help="New age")
@click.option("--email", help="New email")
def update(user_id, name, age, email):
    """Update user details"""
    u = User.find_by_id(user_id)
    if not u:
        click.echo("❌ User not found.")
        return
    updated = User.update(user_id, name, age, email)
    click.echo(f"✅ Updated user: {updated.id} | {updated.name} | {updated.age} | {updated.email}")

@user.command()
@click.argument("user_id", type=int)
def delete(user_id):
    """Delete a user and their glucose entries"""
    u = User.find_by_id(user_id)
    if not u:
        click.echo("❌ User not found.")
        return
    for entry in u.glucose_entries():
        GlucoseEntry.delete(entry.id)
    User.delete(user_id)
    click.echo(f"✅ User {user_id} and related entries deleted.")

@user.command()
@click.argument("name")
def find(name):
    """Find user by name"""
    users = User.get_all()
    found = [u for u in users if u.name.lower() == name.lower()]
    if not found:
        click.echo("No users found with that name.")
        return
    for u in found:
        click.echo(f"{u.id} | {u.name} | {u.age} | {u.email}")

# ------------------ Glucose Entry Commands ------------------

@main.group()
def glucose():
    """Manage Glucose Entries"""
    pass

@glucose.command()
@click.argument("user_id", type=int)
@click.option("--value", prompt="Glucose value (mmol/L)", type=float)
@click.option("--notes", default="", help="Optional notes")
def add(user_id, value, notes):
    """Add glucose entry for a user"""
    u = User.find_by_id(user_id)
    if not u:
        click.echo("❌ User not found.")
        return
    entry = GlucoseEntry.create(user_id, value, notes)
    click.echo(f"✅ Entry added: {entry.id} | {entry.value_mmol} mmol/L | {entry.notes}")

@glucose.command()
@click.argument("user_id", type=int)
def list(user_id):
    """List glucose entries for a user"""
    u = User.find_by_id(user_id)
    if not u:
        click.echo("❌ User not found.")
        return
    entries = u.glucose_entries()
    if not entries:
        click.echo("No entries found.")
        return
    for e in entries:
        click.echo(f"{e.id} | {e.value_mmol} mmol/L | {e.timestamp} | {e.notes}")

@glucose.command()
@click.argument("entry_id", type=int)
@click.option("--value", type=float, help="New glucose value")
@click.option("--notes", help="New notes")
def update(entry_id, value, notes):
    """Update a glucose entry"""
    e = GlucoseEntry.find_by_id(entry_id)
    if not e:
        click.echo("❌ Entry not found.")
        return
    updated = GlucoseEntry.update(entry_id, value, notes)
    click.echo(f"✅ Updated entry: {updated.id} | {updated.value_mmol} mmol/L | {updated.notes}")

@glucose.command()
@click.argument("entry_id", type=int)
def delete(entry_id):
    """Delete a glucose entry"""
    success = GlucoseEntry.delete(entry_id)
    if success:
        click.echo(f"✅ Entry {entry_id} deleted.")
    else:
        click.echo("❌ Failed to delete entry.")

@glucose.command()
@click.argument("value", type=float)
def find(value):
    """Find glucose entries by value"""
    entries = GlucoseEntry.get_all()
    found = [e for e in entries if e.value_mmol == value]
    if not found:
        click.echo("No entries found with that value.")
        return
    for e in found:
        click.echo(f"{e.id} | {e.user_id} | {e.value_mmol} mmol/L | {e.timestamp} | {e.notes}")

if __name__ == "__main__":
    main()
