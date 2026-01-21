import os


def roll_call():
    print("\n📋 JUST-IN-SITE SYSTEM ROLL CALL")
    print("=" * 50)

    files = [f for f in os.listdir('.') if f.endswith('.py')]
    files.sort()

    count = 0
    for filename in files:
        if filename == "inventory.py": continue  # Skip self

        role = "Unknown Role"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                # Read the first 20 lines to find the "Role" or "Description"
                head = [next(f) for _ in range(20)]
                for line in head:
                    if "**Role:**" in line:
                        role = line.split("**Role:**")[1].strip()
                        break
                    elif "**File:**" in line and role == "Unknown Role":
                        # sometimes we put file name first
                        pass
        except:
            role = "Error reading file"

        print(f"{filename:<25} | {role}")
        count += 1

    print("=" * 50)
    print(f"Total Modules Found: {count}\n")


if __name__ == "__main__":
    roll_call()