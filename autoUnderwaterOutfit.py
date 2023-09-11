#----------------------------------------------------------------------------------------#
# Author: a4happy20----------------------------------------------------------------------#
#----------------------------------------------------------------------------------------#
# DESCRIPTION: Adds auto outfit change while under or in water---------------------------#
#----------------------------------------------------------------------------------------#
# USAGE: Run this script in a folder which contains the INI you want to adjust-----------#
#----------------------------------------------------------------------------------------#
# NOTE: This script will only function on mods generated using genshin_merge_mods.py-----#
#----------------------------------------------------------------------------------------#

import os
import shutil

def check_ini_file(ini_path):
    try:
        with open(ini_path, "r") as ini_file:
            ini_contents = ini_file.read()

        if "[Constants]" not in ini_contents:
            raise ValueError("Error: The INI does not contain a [Constants] section.")

        if "[KeySwap]" not in ini_contents:
            raise ValueError("Error: The INI does not contain a [KeySwap] section.")

        if "$swapvar" not in ini_contents:
            raise ValueError("Error: The INI does not contain a $swapvar variable.")

        return True

    except FileNotFoundError as e:
        print(f"INI file not found: {ini_path}")
        return False
    except ValueError as e:
        print(f"Error: {e}")
        return False

def get_ini_files(script_directory):
    return [filename for filename in os.listdir(script_directory) if filename.endswith(".ini")]

def create_backup(ini_path):
    backup_path = f"{ini_path}.bak"
    shutil.copyfile(ini_path, backup_path)
    print(f"Created backup: {backup_path}")
    return backup_path

def restore_backup(ini_path, backup_path):
    try:
        shutil.copyfile(backup_path, ini_path)
        print(f"Restored backup: {ini_path}")
        os.remove(backup_path)
        print(f"Removed backup: {backup_path}")
    except FileNotFoundError:
        print(f"Backup not found: {backup_path}")

def get_user_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_user_key_input(prompt):
    while True:
        key_input = input(prompt).strip()
        if key_input:
            return key_input
        print("Invalid input. Please enter a valid key.")

def add_line_to_ini(ini_path, line_to_add):
    try:
        with open(ini_path, "a") as ini_file:
            ini_file.write("\n" + line_to_add)
    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

def add_lines_to_ini_section(ini_path, section_name, lines_to_add):
    try:
        with open(ini_path, "r") as ini_file:
            ini_contents = ini_file.readlines()

        section_found = False
        for i, line in enumerate(ini_contents):
            if line.strip() == f"[{section_name}]":
                section_found = True
                break

        if section_found:
            while i < len(ini_contents):
                i += 1
                if i >= len(ini_contents) or ini_contents[i].strip().startswith("["):
                    break

            ini_contents[i:i] = [line + "\n" for line in lines_to_add]

            with open(ini_path, "w") as ini_file:
                ini_file.writelines(ini_contents)

    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

def remove_swapvar_values(ini_path, swapvar_values):
    try:
        with open(ini_path, "r") as ini_file:
            ini_contents = ini_file.readlines()

        key_swap_section_start = None
        key_swap_section_end = None
        swapvar_line_index = None

        for i, line in enumerate(ini_contents):
            if line.strip() == "[KeySwap]":
                key_swap_section_start = i + 1

            if key_swap_section_start is not None and line.strip().startswith("$swapvar"):
                swapvar_line_index = i
                break

        if swapvar_line_index is not None:
            swapvar_line = ini_contents[swapvar_line_index].strip()
            current_swapvar_values = swapvar_line.split('=')[1].strip().split(',')

            for value in swapvar_values:
                if str(value) in current_swapvar_values:
                    current_swapvar_values.remove(str(value))

            ini_contents[swapvar_line_index] = f"$swapvar = {','.join(current_swapvar_values)}\n"

            with open(ini_path, "w") as ini_file:
                ini_file.writelines(ini_contents)

    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    ini_files = get_ini_files(script_directory)

    invalid_ini_files = [filename for filename in ini_files if not check_ini_file(os.path.join(script_directory, filename))]

    if invalid_ini_files:
        print("INFO: This script will only work on INI files generated by genshin_merge_mods.py")
        print("Invalid INI files:")
        for invalid_file in invalid_ini_files:
            print(invalid_file)
        return

    try:
        num_outfits = get_user_integer_input("How many Underwater Outfits do you have? (e.g., 'Number'):\n")
        swapvar_values = []

        for i in range(num_outfits):
            swapvar_value = get_user_integer_input(f"Enter the value of $swapvar for Underwater Outfit {i + 1} (e.g., 'Number'):\n")
            swapvar_values.append(swapvar_value)

        key_toggle = get_user_key_input("Enter a key for toggling auto underwater outfit (e.g., 'Number, Letter, or Special Key (VK_RIGHT)'):\n")

        if num_outfits > 1:
            key_cycle = get_user_key_input("Enter a key for switching your underwater outfits (e.g., 'Number, Letter, or Special Key (VK_RIGHT)'):\n")

        outfit_select_values = ",".join(map(str, range(num_outfits)))

        lines_to_add_constants = [
            ";Underwater Outfit Changer",
            "global persist $underwaterOutfit = 0",
            "global persist $underwaterOutfitSelect = 0",
            "global persist $submerged = 0",
            "global persist $submerged_start = 0",
            "global persist $swapvar_set = 0",
            "global persist $previousSwapvar = 0",
            "",
            "",
            "[KeyUnderwaterOutfit]",
            "condition = $active == 1",
            f"key = {key_toggle}",
            "type = cycle",
            "$underwaterOutfit = 0,1",
            "",
        ]

        if num_outfits > 1:
            lines_to_add_constants.extend([
                "[KeyUnderwaterOutfitSelect]",
                "condition = $active == 1",
                f"key = {key_cycle}",
                "type = cycle",
                f"$underwaterOutfitSelect = {outfit_select_values}",
                "",
                "",
                "",
            ])

        lines_to_add_present = [
            "post $submerged_start = 0",
            "",
            "",
            ";underwater store outfit",
            "if $underwaterOutfit == 0",
            "    if $submerged_start == 1 && $submerged == 0",
            "        $previousSwapvar = $swapvar",
            "        $swapvar_set = 1",
            "        $submerged = 1",
            "    endif",
            "",
            "    ;underwater change outfit",
            "    if $submerged == 1",
        ]

        for i in range(num_outfits):
            if i == 0:
                lines_to_add_present.append(f"        if $underwaterOutfitSelect == {i}")
            else:
                lines_to_add_present.append(f"        elif $underwaterOutfitSelect == {i}")

            lines_to_add_present.append(f"            $swapvar = {swapvar_values[i]}")

        lines_to_add_present.extend([
            "        endif",
            "    endif",
            "",
            "    ;underwater reset",
            "    if $submerged_start == 0",
            "        $submerged = 0",
            "    endif",
            "",
            "    ;underwater restore outfit",
            "    if $submerged_start == 0 && $swapvar_set == 1",
            "        $swapvar = $previousSwapvar",
            "        $swapvar_set = 0",
            "    endif",
            "endif",
            "",
            "",
            "",
            "[TextureOverrideSwimIcon]",
            "hash = 45cbdd97",
            "$submerged_start = 1",
            "",
            "[TextureOverrideSwimDownIcon]",
            "hash = 46d6aa04",
            "$submerged_start = 1",
            "",
            "[ShaderOverrideWaterCensor3]",
            "hash = 2cb9fbd599d915ba",
            "allow_duplicate_hash = true",
            "if ps-t0 == 45",
            "    $submerged_start = 1",
            "endif",
            "",
            "[TextureOverrideWaterCensor3]",
            "hash = 7c897a3a",
            "match_priority = 99",
            "filter_index = 45",
            "",
            "",
            "",
        ])

        adjust_key_swap = input("Do you want the Underwater Outfits to only be available when you are underwater? (yes/no):\n").strip().lower()

        # Create backups before making any changes
        backup_paths = []

        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)
            backup_path = create_backup(ini_path)
            backup_paths.append(backup_path)

        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)
            add_lines_to_ini_section(ini_path, "Constants", lines_to_add_constants)
            add_lines_to_ini_section(ini_path, "Present", lines_to_add_present)

        # Adjust the [KeySwap] $swapvar variable
        if adjust_key_swap in ["yes", "y"]:
            for filename in ini_files:
                ini_path = os.path.join(script_directory, filename)
                remove_swapvar_values(ini_path, swapvar_values)

        line_to_add = "; .ini modified by autoUnderwaterOutfit.py - Created by a4happy20"
        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)
            add_line_to_ini(ini_path, line_to_add)

        print(f"Successfully added {num_outfits} Underwater Outfits")

        # Offer the option to revert changes and restore backups
        revert_changes = input("Do you want to revert changes and restore backups? (yes/no):\n").strip().lower()
        if revert_changes in ["yes", "y"]:
            for filename, backup_path in zip(ini_files, backup_paths):
                ini_path = os.path.join(script_directory, filename)
                restore_backup(ini_path, backup_path)

    except ValueError:
        print("Invalid input. Please enter a valid number or key.\n")

if __name__ == "__main__":
    main()
