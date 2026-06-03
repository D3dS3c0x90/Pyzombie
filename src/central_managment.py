from src.settings import DEBUGGER


def debugger(message_type="", *args):
    global DEBUGGER
    p_p, m_p, z_t, z_z, z_c, b_z = False, False, False, False, False, False
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
    # \033[H resets the terminal cursor back to the top left corner (Line 1, Column 1)
    # \033[2J return cursur to top left of the terminal
    # This overwrites the old text in place instead of creating infinite scrolling lines!
    print(f"\033[2J\033[H" + f"""
================= 🛠️  GAME ENGINE DIAGNOSTICS =================
[SYSTEM] Booting Engine Main Core...
[SYSTEM] Loading visual weapon arrays and survivor files...
[SYSTEM] Assets fully operational and armed.
[+] Zombie {DEBUGGER["zombie_create"]} has been created!"                   {'<==' if z_c else ''}           
[!] Player Position : ({DEBUGGER['p_position_x']}, {DEBUGGER['p_position_y']})                  {'<==' if p_p else ''}          
[!] Mouse Position : ({DEBUGGER['mouse_position_x']}, {DEBUGGER['mouse_position_y']})                   {'<==' if m_p else ''}
[!] Bullet - Zombie Collision Detection : ({DEBUGGER['bullet_zombie_collision'][0]}, {DEBUGGER['bullet_zombie_collision'][1]}, Damage = {DEBUGGER['bullet_zombie_collision'][2]})   {'<==' if b_z else ''}          
[!] Zombie - Tree Collision Detection : ({DEBUGGER['zombie_tree_collision'][0]}, {DEBUGGER['zombie_tree_collision'][1]})        {'<==' if z_t else ''}          
[!] Zombie - Zombie Collision Detection : ({DEBUGGER['zombie_zombie_collision'][0]}, {DEBUGGER['zombie_zombie_collision'][1]})     {'<==' if z_z else ''}          
==============================================================
""")


def bullet_zombie_collision(bullet, zombies):
    for zombie in zombies:
        if zombie.rect.colliderect(bullet.rect):
            return {
                "zombie_damage":True,
                "bullet_die":True,
                "bullet_damage":bullet.damage
            }
    return {
        "bullet_die":False,
    }