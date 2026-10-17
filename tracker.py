import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"


def load_data():
	"""Load expense data and budget from the JSON file."""
	if not os.path.exists(DATA_FILE):
		return {"budget": 0.0, "expenses": []}
	try:
		with open(DATA_FILE, "r") as file:
			return json.load(file)
	except json.JSONDecodeError:
		return {"budget": 0.0, "expenses": []}


def save_data(data):
	"""Save expense data and budget to the JSON file."""
	with open(DATA_FILE, "w") as file:
		json.dump(data, file, indent=4)


def set_monthly_budget(data):
	"""Set or update the family's monthly budget."""
	try:
		budget = float(input("\nEnter monthly budget amount ($): "))
		if budget < 0:
			print("Budget cannot be negative.")
			return
		data["budget"] = budget
		save_data(data)
		print(f"✅ Monthly budget successfully set to ${budget:.2f}!")
	except ValueError:
		print("❌ Invalid input. Please enter a valid number.")


def add_expense(data):
	"""Add a new family expense."""
	print("\n--- Add New Expense ---")

	try:
		amount = float(input("Enter amount ($): "))
		if amount <= 0:
			print("Amount must be greater than zero.")
			return
	except ValueError:
		print("❌ Invalid amount. Please enter a number.")
		return

	print("Categories: Food, Utilities, Rent, Entertainment, Healthcare, Education, Other")
	category = input("Enter category: ").strip().capitalize()
	if not category:
		category = "Other"

	description = input("Enter description or family member name (e.g., Mom - Grocery): ").strip()
	if not description:
		description = "General Expense"

	expense = {
		"date": datetime.now().strftime("%Y-%m-%d %H:%M"),
		"amount": amount,
		"category": category,
		"description": description,
	}

	data["expenses"].append(expense)
	save_data(data)
	print(f"✅ Successfully added ${amount:.2f} under '{category}'.")


def view_expenses(data):
	"""View all recorded expenses."""
	expenses = data["expenses"]
	if not expenses:
		print("\nNo expenses recorded yet.")
		return

	print("\n--- Family Expense History ---")
	print(f"{'Date & Time':<20} | {'Category':<15} | {'Amount ($)':<10} | {'Description':<25}")
	print("-" * 75)
	for exp in expenses:
		print(
			f"{exp['date']:<20} | {exp['category']:<15} | "
			f"${exp['amount']:<9.2f} | {exp['description']:<25}"
		)


def check_budget_and_summary(data):
	"""Display category-wise totals, total spent, and budget status."""
	expenses = data["expenses"]
	budget = data["budget"]
	total_spent = sum(exp["amount"] for exp in expenses)

	print("\n--- Expense Summary & Budget ---")
	print(f"Total Monthly Budget: ${budget:.2f}")
	print(f"Total Spent So Far:   ${total_spent:.2f}")

	if budget > 0:
		remaining = budget - total_spent
		if remaining >= 0:
			print(f"Remaining Budget:     ${remaining:.2f} (You're on track!)")
		else:
			print(f"⚠️ Budget Exceeded by: ${abs(remaining):.2f}!")
	else:
		print("Tip: Set a monthly budget to track your savings goals.")

	if not expenses:
		return

	print("\n--- Breakdown by Category ---")
	category_totals = {}
	for exp in expenses:
		category = exp["category"]
		category_totals[category] = category_totals.get(category, 0.0) + exp["amount"]

	print(f"{'Category':<15} | {'Total Spent ($)'}")
	print("-" * 30)
	for category, total in category_totals.items():
		print(f"{category:<15} | ${total:.2f}")


def main():
	data = load_data()

	while True:
		print("\n==============================")
		print("   FAMILY EXPENSE TRACKER     ")
		print("==============================")
		print("1. Set/Update Monthly Budget")
		print("2. Add Expense")
		print("3. View All Expenses")
		print("4. View Summary & Budget Status")
		print("5. Exit")

		choice = input("\nChoose an option (1-5): ").strip()

		if choice == "1":
			set_monthly_budget(data)
		elif choice == "2":
			add_expense(data)
		elif choice == "3":
			view_expenses(data)
		elif choice == "4":
			check_budget_and_summary(data)
		elif choice == "5":
			print("\nThank you for using Family Expense Tracker. Goodbye!")
			break
		else:
			print("❌ Invalid choice. Please select a number between 1 and 5.")


if __name__ == "__main__":
	main()
