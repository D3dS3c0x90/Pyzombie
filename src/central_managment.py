from src.settings import *
import math


def debugger(message_type="", *args):
    global DEBUGGER, ALL_ZOMBIES, FRAME_NOW
    if FRAME_NOW % 10 == 0:
        p_p, m_p, z_t, z_z, z_c, b_z, b_d = False, False, False, False, False, False, False
        if message_type == "p_p":
            DEBUGGER["p_position_x"] = args[0]
            DEBUGGER["p_position_y"] = args[1]
            p_p = True
        elif message_type == "m_p":
            DEBUGGER["mouse_position_x"] = args[0]
            DEBUGGER["mouse_position_y"] = args[1]
            m_p = True
        elif message_type == "z_t":
            DEBUGGER["zombie_tree_collision"] = [args[0], args[1]]
            z_t = True
        elif message_type == "z_z":
            DEBUGGER["zombie_zombie_collision"] = [args[0], args[1]]
            z_z = True
        elif message_type == "b_z":
            DEBUGGER["bullet_zombie_collision"] = [args[0], args[1], args[2]]
            b_z = True
        elif message_type == "z_c":
            DEBUGGER["zombie_create"] = args[0]
            z_c = True
        elif message_type == "b_d":
            DEBUGGER["bullet_direction"] = args[0]
            b_d = True
        # \033[H resets the terminal cursor back to the top left corner (Line 1, Column 1)
        # \033[2J return cursur to top left of the terminal
        # This overwrites the old text in place instead of creating infinite scrolling lines!
        # Define a standard width for the text column before the arrow starts [W] character
        W = 80

        # PHASE A: Clear screen and draw the static blocks
        print(f"\033[2J\033[H" + 
f"""================= 🛠️  GAME ENGINE DIAGNOSTICS =================
[SYSTEM] Booting Engine Main Core...
[SYSTEM] Loading visual weapon arrays and survivor files...
[SYSTEM] Assets fully operational and armed.

{f"[+] Zombie {DEBUGGER['zombie_create']} has been created!":<{W}}{'<=='  if z_c else ''}           
{f"[!] Player Position : ({DEBUGGER['p_position_x']}, {DEBUGGER['p_position_y']})":<{W}}{'<=='  if p_p else ''}          
{f"[!] Mouse Position : ({DEBUGGER['mouse_position_x']}, {DEBUGGER['mouse_position_y']})":<{W}}{'<=='  if m_p else ''}
{f"[!] Mouse Direction : ({DEBUGGER['bullet_direction']})":<{W}}{'<=='  if b_d else ''}
{f"[!] Bullet - Zombie Collision Detection : ({DEBUGGER['bullet_zombie_collision'][0]}, {DEBUGGER['bullet_zombie_collision'][1]}, Damage = {DEBUGGER['bullet_zombie_collision'][2]})":<{W}}{'<=='  if b_z else ''}          
{f"[!] Zombie - Tree Collision Detection : ({DEBUGGER['zombie_tree_collision'][0]}, {DEBUGGER['zombie_tree_collision'][1]})":<{W}}{'<=='  if z_t else ''}          
{f"[!] Zombie - Zombie Collision Detection : ({DEBUGGER['zombie_zombie_collision'][0]}, {DEBUGGER['zombie_zombie_collision'][1]})":<{W}}{'<=='  if z_z else ''} \n""", end="")

        # PHASE B: The Dynamic Zombie Loop
        # for zombie in list(ALL_ZOMBIES.keys()):
        #     zombie_line = f"\n[!] Zombie : {zombie} | Health Case : {'Died' if ALL_ZOMBIES[zombie].health <= 0 else 'Alive'}"
        #     print(f"{zombie_line:<{W}}", end="")

        print("\n==============================================================")

def bullet_zombie_collision(bullet, zombies):
    for zombie in zombies:
        if zombie.rect.colliderect(bullet.rect) and zombie.is_dead == False:
            zombie.health -= bullet.damage
            return {
                "zombie_damage":True,
                "bullet_die":True,
                "bullet_damage":bullet.damage,
                "zombie_die":True,
                "zombie":zombie
            }
    return {
        "bullet_die":False,
    }
    
def bullet_tree_collision(bullet, trees):
    for tree in trees:
        if tree.rect.colliderect(bullet.rect):
            return {
                "bullet_die":True,
            }
    return {
        "bullet_die":False,
    }
    
def get_angle(dx, dy):
    # We invert dy because Pygame's Y axis goes down instead of up
    angle = math.atan2(-dy, dx)
    # Convert radians to degrees (0 to 360)
    degrees = math.degrees(angle)
    if degrees < 0:
        degrees += 360

    # 3. Compass Mapping: Map the 360° circle into 8 directional slices of 45° each
    if 22.5 <= degrees < 67.5:
        direction = "up_right"
    elif 67.5 <= degrees < 112.5:
        direction = "up"
    elif 112.5 <= degrees < 157.5:
        direction = "up_left"
    elif 157.5 <= degrees < 202.5:
        direction = "left"
    elif 202.5 <= degrees < 247.5:
        direction = "down_left"
    elif 247.5 <= degrees < 292.5:
        direction = "down"
    elif 292.5 <= degrees < 337.5:
        direction = "down_right"
    else:
        direction = "right"  # Covers 337.5 to 360 and 0 to 22.5
    return direction
    