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
import argparse
import shutil
import signal

# Constants for section names
CONSTANTS_SECTION = "Constants"
SWAPVAR_VARIABLE = "$swapvar"
KEYSWAP_SECTION = "KeySwap"
KEYSWAP_ALT_SECTION = "KeySwap_Alt"
PRESENT_SECTION = "Present"
CONDITION = "$active == 1 && $submerged == 0 && $underwaterOutfit == 1"
TEXTURE_OVERRIDE_HEAD_SECTION = None
TEXTURE_OVERRIDE_BODY_SECTION = None
TEXTURE_OVERRIDE_DRESS_SECTION = None
TEXTURE_OVERRIDE_EXTRA_SECTION = None

# Full path to and name of ini file being modified
def get_ini_files(script_directory):

    ini_files = [filename for filename in os.listdir(script_directory) if filename.endswith(".ini") and not filename.startswith("DISABLED")]

    if not ini_files:
        print(f"No INI files found at: {script_directory}.")
        exit(1)
    return ini_files

# Error checking for variables and sections in the ini
def check_ini_file(ini_path):
    try:
        with open(ini_path, "r") as ini_file:
            ini_contents = ini_file.read()

        required_variables = [
            SWAPVAR_VARIABLE,
        ]

        required_sections = [
            CONSTANTS_SECTION,
            KEYSWAP_SECTION,
        ]

        texture_override_head_section = find_texture_override_head_section(ini_contents)
        texture_override_body_section = find_texture_override_body_section(ini_contents)
        texture_override_dress_section = find_texture_override_dress_section(ini_contents)
        texture_override_extra_section = find_texture_override_extra_section(ini_contents)

        for variable in required_variables:
            if f"{variable}" not in ini_contents:
                raise ValueError(f"Error: The INI does not contain a {variable} section.")

        for section in required_sections:
            if f"[{section}]" not in ini_contents:
                raise ValueError(f"Error: The INI does not contain a [{section}] section.")

        return (
            texture_override_head_section,
            texture_override_body_section,
            texture_override_dress_section,
            texture_override_extra_section,
        )

    except ValueError as e:
        print(f"Error: {e}")
        return False

# Backing up the ini
def create_backup(ini_path):
    backup_path = f"{ini_path}.bak"
    shutil.copyfile(ini_path, backup_path)
    print(f"Created backup: {backup_path}")
    return backup_path

# Restoring the created backup
def restore_backup(ini_path, backup_path):
    try:
        shutil.copyfile(backup_path, ini_path)
        print(f"Restored backup: {ini_path}")
        os.remove(backup_path)
        print(f"Removed backup: {backup_path}")
    except FileNotFoundError:
        print(f"Backup not found: {backup_path}")

# Making sure the user input is the correct type (integer)
def get_user_integer_input(prompt):
    while True:
        try:
            integer_input = int(input(prompt))
            return integer_input
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Making sure the user input is the correct type (toggle key)
def get_user_key_input(prompt):
    while True:
        key_input = input(prompt).strip()
        if key_input:
            return key_input
        print("Invalid input. Please enter a valid key.")

# Making sure the user input is the correct type (yes/no)
def get_user_yes_or_no_input(prompt):
    while True:
        yes_or_no_input = input(prompt).strip()
        if yes_or_no_input:
            return yes_or_no_input
        print("Invalid input. Please enter y/n.")

# Making sure the ini still exists
def add_line_to_ini(ini_path, line_to_add):
    try:
        with open(ini_path, "a") as ini_file:
            ini_file.write("\n" + line_to_add)
    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

# finding the [TextureOverride**Head] section
def find_texture_override_head_section(ini_contents):
    for line in ini_contents.splitlines():
        if line.strip().startswith("[TextureOverride") and line.strip().endswith("Head]"):
            return line.strip()[1:-1]  # Remove brackets

# finding the [TextureOverride**Body] section
def find_texture_override_body_section(ini_contents):
    for line in ini_contents.splitlines():
        if line.strip().startswith("[TextureOverride") and line.strip().endswith("Body]"):
            return line.strip()[1:-1]  # Remove brackets

# finding the [TextureOverride**Dress] section
def find_texture_override_dress_section(ini_contents):
    for line in ini_contents.splitlines():
        if line.strip().startswith("[TextureOverride") and line.strip().endswith("Dress]"):
            return line.strip()[1:-1]  # Remove brackets

# finding the [TextureOverride**Extra] section
def find_texture_override_extra_section(ini_contents):
    for line in ini_contents.splitlines():
        if line.strip().startswith("[TextureOverride") and line.strip().endswith("Extra]"):
            return line.strip()[1:-1]  # Remove brackets

def find_keyswap_values(ini_files, script_directory):
    keyswap_values = {}

    try:
        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)

            keyswap_section = {}
            current_section = None

            with open(ini_path, 'r') as ini_file:
                for line in ini_file:
                    line = line.strip()

                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]  # Remove brackets
                        continue

                    if current_section == KEYSWAP_SECTION:
                        parts = line.split('=')
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            keyswap_section[key] = value

            if keyswap_section:  # Check if keyswap_section is not empty
                keyswap_values[filename] = keyswap_section

        return keyswap_values

    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

# Writing to the ini main
def add_lines_to_ini_section(ini_path, section_name, lines_to_add):
    try:
        with open(ini_path, "r") as ini_file:
            ini_contents = ini_file.readlines()

        section_start = None
        section_end = None

        for i, line in enumerate(ini_contents):
            if line.strip() == f"[{section_name}]":
                section_start = i
                break

        if section_start is not None:
            for i in range(section_start + 1, len(ini_contents)):
                if ini_contents[i].strip().startswith("[") or i == len(ini_contents) - 1:
                    section_end = i
                    break

            if section_end is not None:
                # Find the index of the first comment line (;) or the end of the section
                comment_line_index = section_start + 1
                while comment_line_index < section_end:
                    if ini_contents[comment_line_index].strip().startswith(";"):
                        break
                    comment_line_index += 1

                # Insert the lines before the first comment line or the end of the section
                ini_contents = ini_contents[:comment_line_index] + [line + "\n" for line in lines_to_add] + ini_contents[comment_line_index:]

                with open(ini_path, "w") as ini_file:
                    ini_file.writelines(ini_contents)

    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

# Removing specified $swapvar values from [KeySwap_Alt] section]
def remove_swapvar_values(ini_path, swapvar_values):
    try:
        with open(ini_path, "r") as ini_file:
            ini_contents = ini_file.readlines()

        key_swap_alt_section_start = None
        key_swap_alt_section_end = None
        swapvar_line_index = None

        for i, line in enumerate(ini_contents):
            if line.strip() == f"[{KEYSWAP_ALT_SECTION}]":
                key_swap_alt_section_start = i + 1

            if key_swap_alt_section_start is not None and line.strip().startswith(SWAPVAR_VARIABLE):
                swapvar_line_index = i
                break

        if key_swap_alt_section_start is not None:
            for i in range(key_swap_alt_section_start, len(ini_contents)):
                if ini_contents[i].strip().startswith("[") or i == len(ini_contents) - 1:
                    key_swap_alt_section_end = i
                    break

        if swapvar_line_index is not None and key_swap_alt_section_start is not None and key_swap_alt_section_end is not None:
            swapvar_line = ini_contents[swapvar_line_index].strip()
            current_swapvar_values = swapvar_line.split('=')[1].strip().split(',')

            for value in swapvar_values:
                if str(value) in current_swapvar_values:
                    current_swapvar_values.remove(str(value))

            ini_contents[swapvar_line_index] = f"{SWAPVAR_VARIABLE} = {','.join(current_swapvar_values)}\n"

            with open(ini_path, "w") as ini_file:
                ini_file.writelines(ini_contents)

    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")


def modify_condition_value(ini_path, CONDITION):
    try:
        with open(ini_path, "r") as ini_file:
            ini_contents = ini_file.readlines()

        key_swap_section_start = None
        key_swap_section_end = None
        condition_line_index = None

        for i, line in enumerate(ini_contents):
            if line.strip() == f"[{KEYSWAP_SECTION}]":
                key_swap_section_start = i + 1

            if key_swap_section_start is not None and line.strip().startswith("condition"):
                condition_line_index = i
                break

        if key_swap_section_start is not None:
            for i in range(key_swap_section_start, len(ini_contents)):
                if ini_contents[i].strip().startswith("[") or i == len(ini_contents) - 1:
                    key_swap_section_end = i
                    break

        if condition_line_index is not None and key_swap_section_start is not None and key_swap_section_end is not None:
            ini_contents[condition_line_index] = f"condition = {CONDITION}\n"

            with open(ini_path, "w") as ini_file:
                ini_file.writelines(ini_contents)

    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")


def add_underwater_outfit_lines_to_ini_sections(ini_files, script_directory, key_toggle, num_outfits, swapvar_values, outfit_select_values, key_swap, key_back, key_swap_type, value_swap, delay_in_frames):
    try:
        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)
            lines_to_add_constants, lines_to_add_present = generate_underwater_outfit_lines(key_toggle, num_outfits, swapvar_values, outfit_select_values, key_swap, key_back, key_swap_type, value_swap, delay_in_frames)
            
            add_lines_to_ini_section(ini_path, CONSTANTS_SECTION, lines_to_add_constants)
            # Check and create [Present] section if needed
            ensure_present_section_exists(ini_path, PRESENT_SECTION, lines_to_add_present)
            
    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

def generate_underwater_outfit_lines(key_toggle, num_outfits, swapvar_values, outfit_select_values, key_swap, key_back, key_swap_type, value_swap, delay_in_frames):

    lines_to_add_constants = [
        ";autoUnderwaterOutfit",
        "global persist $underwaterOutfit = 0",
        "global persist $underwaterOutfitSelect = 0",
        "global persist $submerged = 0",
        "global persist $submerged_start = 0",
        "global persist $swapvar_set = 0",
        "global persist $previousSwapvar = 0",
        f"global $delayInFrames = {delay_in_frames}",
        "global $delay = 0",
        "",
        "",
        "",
        ";Underwater Outfit On/Off",
        "[KeyUnderwaterOutfit]",
        "condition = $active == 1",
        f"key = {key_toggle}",
        "type = cycle",
        "$underwaterOutfit = 0,1",
        "",
    ]

    if num_outfits > 1:
        lines_to_add_constants.extend([
            ";Underwater Outfit Cycle",
            "[KeyUnderwaterOutfitSelect]",
            "condition = $active == 1 && $submerged == 1",
        ])
        if key_swap:
            lines_to_add_constants.append(f"key = {key_swap}")

        if key_back:
            lines_to_add_constants.append(f"back = {key_back}")
        
        if key_swap_type:
            lines_to_add_constants.append(f"type = {key_swap_type}")

        lines_to_add_constants.append(f"$underwaterOutfitSelect = {outfit_select_values}\n")

    lines_to_add_constants.extend([
    ";Key for switching variants when Underwater Outfit is ON",
    f"[{KEYSWAP_ALT_SECTION}]",
    "condition = $active == 1 && $submerged == 0 && $underwaterOutfit == 0",
    f"key = {key_swap}",
    f"back = {key_back}",
    f"type = {key_swap_type}",
    f"{SWAPVAR_VARIABLE} = {value_swap}",
    "",
    ])

    lines_to_add_present = [
        ";autoUnderwaterOutfit",
        "post $submerged_start = 0",
        "",
        ";autoUnderwater store outfit",
        "if $underwaterOutfit == 0",
        "    if $submerged_start == 1 && $submerged == 0 && $swapvar_set == 0",
        f"        $previousSwapvar = {SWAPVAR_VARIABLE}",
        "        $swapvar_set = 1",
        "        $submerged = 1",
        "",
        "    else if $submerged_start == 1 && $submerged == 0 && $swapvar_set == 1",
        "        $delay = 0",
        "    endif",
        "",
        "    ;autoUnderwater change outfit",
        "    if $submerged == 1",
    ]

    for i in range(num_outfits):
        if i == 0:
            lines_to_add_present.append(f"        if $underwaterOutfitSelect == {i}")
        else:
            lines_to_add_present.append(f"        elif $underwaterOutfitSelect == {i}")

        lines_to_add_present.append(f"            {SWAPVAR_VARIABLE} = {swapvar_values[i]}")

    lines_to_add_present.extend([
        "        endif",
        "    endif",
        "",
        "    ;autoUnderwater reset",
        "    if $submerged_start == 0",
        "        $submerged = 0",
        "    endif",
        "",
        "    if $submerged_start == 0 && $swapvar_set == 1",
        "        $delay = $delay+1",
        "",
        "    ;autoUnderwater restore outfit",
        "        if $submerged_start == 0 && $swapvar_set == 1 && $delay >= $delayInFrames",
        f"            {SWAPVAR_VARIABLE} = $previousSwapvar",
        "            $swapvar_set = 0",
        "            $delay = 0",
        "        endif",
        "    endif",
        "endif",
        "",
        "if $delay > $delayInFrames",
        "    $delay = 0",
        "endif",
        "",
        "",
        "",
        ";autoUnderwaterOutfit",
        "[TextureOverrideSwimIcon]",
        "hash = 45cbdd97",
        "$submerged_start = 1",
        "",
        ";autoUnderwaterOutfit",
        "[TextureOverrideSwimDownIcon]",
        "hash = 46d6aa04",
        "$submerged_start = 1",
        "",
        ";autoUnderwaterOutfit",
        "[ShaderOverrideWaterCensor3]",
        "hash = 2cb9fbd599d915ba",
        "allow_duplicate_hash = true",
        "if ps-t0 == 45",
        "    $submerged_start = 1",
        "endif",
        "",
        ";autoUnderwaterOutfit",
        "[TextureOverrideWaterCensor3]",
        "hash = 7c897a3a",
        "match_priority = 99",
        "filter_index = 45",
        "",
        "",
        "",
    ])
    
    return lines_to_add_constants, lines_to_add_present

def ensure_present_section_exists(ini_path, section_name, lines_to_add_present):
    try:
        with open(ini_path, "r") as ini_file:
            ini_contents = ini_file.readlines()

        present_section_found = False
        shader_line_index = None

        for i, line in enumerate(ini_contents):
            if line.strip() == f"[{section_name}]":
                present_section_found = True
                break
            elif line.strip().startswith("; Shader"):
                shader_line_index = i

        if not present_section_found:
            if shader_line_index is not None:
                ini_contents.insert(shader_line_index, f"[{section_name}]\n")
            else:
                ini_contents.append(f"\n\n[{section_name}]\n")
                ini_contents.extend([f"{line}\n" for line in lines_to_add_present])

        present_section_found = False  # Reset the flag

        for i, line in enumerate(ini_contents):
            if line.strip() == f"[{section_name}]":
                present_section_found = True
                continue  # Skip adding the lines if the section is found

            if present_section_found and line.strip().startswith("; Shader"):
                # Insert the lines before the `; Shader` line
                ini_contents = (
                    ini_contents[:i] +
                    [line + "\n" for line in lines_to_add_present] +
                    ini_contents[i:]
                )
                break

        with open(ini_path, "w") as ini_file:
            ini_file.writelines(ini_contents)

    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")


# Adding AGMG3ShaderFix lines to relevant sections
def add_lines_to_ini_sections(ini_files, script_directory):
    try:
        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)
            TEXTURE_OVERRIDE_HEAD_SECTION, TEXTURE_OVERRIDE_BODY_SECTION, TEXTURE_OVERRIDE_DRESS_SECTION, TEXTURE_OVERRIDE_EXTRA_SECTION = check_ini_file(filename)
            
            # Lines to add to [Constants] section
            lines_to_add_constants = [
                ";AGMG3ShaderFix",
                "global $CharacterIB",
                ";0=none, 1=head, 2=body, 3=dress, 4=extra",
                "",
            ]

            # Lines to add to [Present] section
            lines_to_add_present = [
                ";AGMG3ShaderFix",
                "post $CharacterIB = 0",
                "",
            ]

            if TEXTURE_OVERRIDE_HEAD_SECTION:
            # Lines to add to [TextureOverride* *Head] section
                lines_to_add_head = [
                    ";AGMG3ShaderFix",
                    "$CharacterIB = 1",
                    "ResourceRefHeadDiffuse = reference ps-t1",
                    "ResourceRefHeadLightMap = reference ps-t2",
                    "",
            ]

            if TEXTURE_OVERRIDE_BODY_SECTION:
            # Lines to add to [TextureOverride* *Body] section
                lines_to_add_body = [
                    ";AGMG3ShaderFix",
                    "$CharacterIB = 2",
                    "ResourceRefBodyDiffuse = reference ps-t1",
                    "ResourceRefBodyLightMap = reference ps-t2",
                    "",
                ]

            if TEXTURE_OVERRIDE_BODY_SECTION:
            # Lines to add to [TextureOverride* *Dress] section
                lines_to_add_dress = [
                    ";AGMG3ShaderFix",
                    "$CharacterIB = 3",
                    "ResourceRefDressDiffuse = reference ps-t1",
                    "ResourceRefDressLightMap = reference ps-t2",
                    "",
                ]

            if TEXTURE_OVERRIDE_BODY_SECTION:
            # Lines to add to [TextureOverride* *Extra] section
                lines_to_add_extra = [
                    ";AGMG3ShaderFix",
                    "$CharacterIB = 4",
                    "ResourceRefExtraDiffuse = reference ps-t1",
                    "ResourceRefExtraLightMap = reference ps-t2",
                    "",
                ]

            # Add lines to INI file under specific section headers
            add_lines_to_ini_section(ini_path, CONSTANTS_SECTION, lines_to_add_constants)
            add_lines_to_ini_section(ini_path, PRESENT_SECTION, lines_to_add_present)
            add_lines_to_ini_section(ini_path, TEXTURE_OVERRIDE_HEAD_SECTION, lines_to_add_head)
            add_lines_to_ini_section(ini_path, TEXTURE_OVERRIDE_BODY_SECTION, lines_to_add_body)
            add_lines_to_ini_section(ini_path, TEXTURE_OVERRIDE_DRESS_SECTION, lines_to_add_dress)
            add_lines_to_ini_section(ini_path, TEXTURE_OVERRIDE_EXTRA_SECTION, lines_to_add_extra)

    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

# Adding AGMG3ShaderFix lines to the end of the ini
def add_lines_to_end_of_ini(ini_path):
    try:
        with open(ini_path, "a") as ini_file:
            # Add the lines you want to append to the end of the INI file
            lines_to_add = [
                "",
                ";AGMG3ShaderFix",
                "[ResourceRefHeadDiffuse]",
                "[ResourceRefHeadLightMap]",
                "[ResourceRefBodyDiffuse]",
                "[ResourceRefBodyLightMap]",
                "[ResourceRefDressDiffuse]",
                "[ResourceRefDressLightMap]",
                "[ResourceRefExtraDiffuse]",
                "[ResourceRefExtraLightMap]",
                "",
                "[ShaderRegexCharReflection]",
                "shader_model = ps_5_0",
                "run = CommandListReflectionTexture",
                "",
                "[ShaderRegexCharReflection.pattern]",
                "mul r\\d+\\.\\w+, r\\d+\\.\\w+,[^.]*\\.\\w+\\n",
                "mad o\\d+\\.\\w+, r\\d+\\.\\w+, cb\\d+\\[\\d+\\]\\.\\w+, r\\d+\\.\\w+\\n",
                "mov o\\d+\\.\\w+, l\\(\\d+\\.\\d+\\)\\n",
                "",
                "[ShaderOverrideOutline]",
                "hash=6ce92f3bcc9c03d0",
                "run = CommandListOutline",
                "allow_duplicate_hash=overrule",
                "",
                "[CommandListReflectionTexture]",
                "if $CharacterIB != 0",
                "    if $CharacterIB == 1",
                "        ps-t0 = copy ResourceRefHeadDiffuse",
                "    else if $CharacterIB == 2",
                "        ps-t0 = copy ResourceRefBodyDiffuse",
                "    else if $CharacterIB == 3",
                "        ps-t0 = copy ResourceRefDressDiffuse",
                "    else if $CharacterIB == 4",
                "        ps-t0 = copy ResourceRefExtraDiffuse",
                "    endif",
                "drawindexed=auto",
                "$CharacterIB = 0",
                "endif",
                "",
                "[CommandListOutline]",
                "if $CharacterIB != 0",
                "    if $CharacterIB == 1",
                "        ps-t1 = copy ResourceRefHeadLightMap",
                "    else if $CharacterIB == 2",
                "        ps-t1 = copy ResourceRefBodyLightMap",
                "    else if $CharacterIB == 3",
                "        ps-t1 = copy ResourceRefDressLightMap",
                "    else if $CharacterIB == 4",
                "        ps-t1 = copy ResourceRefExtraLightMap",
                "    endif",
                "drawindexed=auto",
                "$CharacterIB = 0",
                "endif",
                "",
            ]
            ini_file.write("\n" + "\n".join(lines_to_add))
    except FileNotFoundError:
        print(f"INI file not found: {ini_path}")

def main():
    parser = argparse.ArgumentParser(description="Add autoUnderwaterOutfit Lines to your ini file.")
    parser.add_argument("--num_outfits", type=int, help="Number of Underwater Outfits.")
    parser.add_argument("--swapvar_values", nargs='+', type=int, help=f"Values of {SWAPVAR_VARIABLE} for each Underwater Outfit.")
    parser.add_argument("--toggle_key", type=str, help="Key for toggling auto underwater outfit on/off.")
    parser.add_argument("--delay", type=int, help="Set the delayInFrames for switching the outfit after leaving water.")
    parser.add_argument("--aks", type=str, choices=["y", "n"], help="Do you want the Underwater Outfits to only be available when you are underwater or if functionality is toggled off.")
    parser.add_argument("--v3", type=str, choices=["y", "n"], help="Is the character from game version 3.0 or above?")
    
    args = parser.parse_args()

    # Error checking
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
        # User inputs
        if args.num_outfits is None:
            num_outfits = get_user_integer_input("How many Underwater Outfits do you have? (e.g., 'Number'):\n")
        else:
            num_outfits = args.num_outfits

        if args.swapvar_values is None:
            swapvar_values = []
            for i in range(num_outfits):
                swapvar_value = get_user_integer_input(f"Enter the value of {SWAPVAR_VARIABLE} for Underwater Outfit {i + 1} (e.g., 'Number'):\n")
                swapvar_values.append(swapvar_value)
        else:
            swapvar_values = args.swapvar_values

        if args.toggle_key is None:
            key_toggle = get_user_key_input("Enter a key for toggling auto underwater outfit (e.g., 'Number, Letter, or Special Key (VK_RIGHT)'):\n")
        else:
            key_toggle = args.toggle_key

        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)
            find_keyswap_values(ini_files, script_directory)

            # Extract values from the KeySwap section
            ini_files = get_ini_files(script_directory)
            keyswap_values = find_keyswap_values(ini_files, script_directory)

            for filename, keyswap_section in keyswap_values.items():
                key_swap = keyswap_section.get('key', '')  # Default to empty string if key is not found
                key_back = keyswap_section.get('back', '')
                key_swap_type = keyswap_section.get('type', '')
                value_swap = keyswap_section.get(SWAPVAR_VARIABLE, '')

        if args.delay is None:
            delay_in_frames = 480
        else:
            delay_in_frames = args.delay

        if args.num_outfits is None:
            outfit_select_values = ",".join(map(str, range(num_outfits)))
        else:
            outfit_select_values = ",".join(map(str, range(args.num_outfits)))

        if args.aks is None:
            adjust_key_swap = get_user_yes_or_no_input("Do you want the Underwater Outfits to only be available when you are underwater or if functionality is toggled off? (yes/no):\n").strip().lower()
        else:
            adjust_key_swap = args.aks

        if args.v3 is None:
            is_version_3_or_above = get_user_yes_or_no_input("Is the character from game version 3.0 and above? (yes/no):\n")
        else:
            is_version_3_or_above = args.v3

        # Create backups before making any changes
        backup_paths = []
        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)
            backup_path = create_backup(ini_path)
            backup_paths.append(backup_path)

        # Adds autoUnderwaterOutfit
        add_underwater_outfit_lines_to_ini_sections(ini_files, script_directory, key_toggle, num_outfits, swapvar_values, outfit_select_values, key_swap, key_back, key_swap_type, value_swap, delay_in_frames)

        # Removing $swapvar variables if only available underwater
        if adjust_key_swap in ["yes", "y"]:
            for filename in ini_files:
                ini_path = os.path.join(script_directory, filename)
                remove_swapvar_values(ini_path, swapvar_values)

        # Adds AGMG3ShaderFix
        line_to_add_agmg3shaderfix = "; Generated shader fix for 3.0+ GIMI importer characters. Please contact the tool developers at https://discord.gg/agmg if you have any questions."
        if is_version_3_or_above in ["yes", "y"]:
            add_lines_to_ini_sections(ini_files, script_directory)

            for filename in ini_files:
                ini_path = os.path.join(script_directory, filename)
                add_lines_to_end_of_ini(ini_path)
                add_line_to_ini(ini_path, line_to_add_agmg3shaderfix)

        # Signing and adding the new condition value for [KeySwap]
        line_to_add = "; .ini modified by autoUnderwaterOutfit.py - Created by a4happy20 - https://github.com/a4happy20/autoUnderwaterOutfit"
        for filename in ini_files:
            ini_path = os.path.join(script_directory, filename)
            add_line_to_ini(ini_path, line_to_add)
            modify_condition_value(ini_path, CONDITION)

        print(f"Successfully added {num_outfits} Underwater Outfits")

        # Offer the option to revert changes and restore backups
        revert_changes = input("Do you want to revert changes and restore backups? (yes/no):\n").strip().lower()
        if revert_changes in ["yes", "y"]:
            for filename, backup_path in zip(ini_files, backup_paths):
                ini_path = os.path.join(script_directory, filename)
                restore_backup(ini_path, backup_path)

    except KeyboardInterrupt:
        print("Script interrupted by user.")

    except ValueError:
        print("Invalid input. Please enter a valid number or key.\n")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)
    main()