import os
import sys
import bpy

# ==================== CONFIGURATION ====================
SOURCE_MESH = "YourBodyMeshName"      # Change to your avatar body mesh name
TARGET_MESH = "YourClothingName"      # Change to your clothing/hair mesh name
# =======================================================

def clear_console():
    """Clears the system console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write("\x1b[2J\x1b[H")
    print("--- Console Cleared. Commencing Shape Key Transfer Pipeline ---")

def create_and_bind_modifier(clothing, body, mod_name):
    """Helper to add, move to top, and bind the surface deform modifier safely."""
    if mod_name in clothing.modifiers:
        clothing.modifiers.remove(clothing.modifiers[mod_name])
        
    surf_mod = clothing.modifiers.new(name=mod_name, type='SURFACE_DEFORM')
    surf_mod.target = body
    
    bpy.context.view_layer.objects.active = clothing
    while clothing.modifiers.find(surf_mod.name) > 0:
        bpy.ops.object.modifier_move_up(modifier=surf_mod.name)
        
    with bpy.context.temp_override(object=clothing, active_object=clothing):
        bpy.ops.object.surfacedeform_bind(modifier=surf_mod.name)
        
    return surf_mod

def run_transfer():
    clear_console()
    
    body = bpy.data.objects.get(SOURCE_MESH)
    clothing = bpy.data.objects.get(TARGET_MESH)
    
    if not body or not clothing:
        print(f"❌ ERROR: Ensure '{SOURCE_MESH}' and '{TARGET_MESH}' exist.")
        return
        
    if not body.data.shape_keys:
        print(f"❌ ERROR: The source mesh '{SOURCE_MESH}' has no shape keys to transfer.")
        return

    print(f"🔹 Source Mesh: {body.name}")
    print(f"🔹 Target Mesh: {clothing.name}")

    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    for key_block in body.data.shape_keys.key_blocks:
        key_block.value = 0.0
    bpy.context.view_layer.update()

    mod_name = "Auto_Surface_Deform"
    key_blocks = body.data.shape_keys.key_blocks
    total_keys = len(key_blocks) - 1
    processed_count = 0
    
    print(f"⚡ Processing {total_keys} total potential shape keys...")

    for key_block in key_blocks:
        if key_block.name == 'Basis':
            continue
            
        try:
            surf_mod = create_and_bind_modifier(clothing, body, mod_name)
        except Exception as e:
            print(f"❌ BIND ERROR on '{key_block.name}': Could not bind mesh. Skipping key.\nDetails: {e}")
            if mod_name in clothing.modifiers:
                clothing.modifiers.remove(clothing.modifiers[mod_name])
            continue

        key_block.value = 1.0
        bpy.context.view_layer.update()
        
        has_deformation = False
        depsgraph = bpy.context.evaluated_depsgraph_get()
        clothing_eval = clothing.evaluated_get(depsgraph)
        
        for v in clothing.data.vertices:
            eval_vertex_co = clothing_eval.data.vertices[v.index].co
            if (v.co - eval_vertex_co).length > 0.0001: 
                has_deformation = True
                break
                
        if not has_deformation:
            print(f"   ⏩ Skipping: '{key_block.name}' (No deformation detected on target)")
            clothing.modifiers.remove(surf_mod)
            key_block.value = 0.0
            bpy.context.view_layer.update()
            continue

        print(f"   🚀 Baking Shape Key: '{key_block.name}'")
        
        with bpy.context.temp_override(object=clothing, active_object=clothing):
            bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier=surf_mod.name)
            
        new_clothing_key = clothing.data.shape_keys.key_blocks[-1]
        new_clothing_key.name = key_block.name 
        
        clothing.modifiers.remove(surf_mod)
        
        key_block.value = 0.0
        bpy.context.view_layer.update()
        
        processed_count += 1

    if mod_name in clothing.modifiers:
        clothing.modifiers.remove(clothing.modifiers[mod_name])
        
    for key_block in body.data.shape_keys.key_blocks:
        key_block.value = 0.0
    bpy.context.view_layer.update()

    print(f"\n🎉 SUCCESS! Transferred {processed_count} shape keys onto '{clothing.name}'. Source mesh reset to 0.")

run_transfer()
