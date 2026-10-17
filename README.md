# Blender Shape Key Transfer Script

An automated Python tool for **Blender** to perfectly project and transfer shape keys from a source avatar/body mesh onto target accessories like clothing, hair, or armor using a dynamic **Surface Deform** lifecycle.

Manually transferring shape keys to multi-layered clothing using Surface Deform modifiers often leads to mesh distortion. For clean deforms, the modifier must be bound when the source mesh is resting (`Basis` at 0.0), calculated at maximum delta (`Shape Key` at 1.0), baked, and completely torn down before cycling to the next frame state. 

This automation script eliminates this workflow bottleneck completely.


## How To Use

### 1. Mesh Preparation
1. Ensure both your **Source Mesh** (Body) and **Target Mesh** (Clothing/Hair) are perfectly aligned in the layout workspace.
2. Select your Source mesh and ensure all shape keys are set to `0.0` (resting position).

### 2. Configure & Execute Script
1. Open Blender's internal **Text Editor** viewport workspace panel.
2. Click **New** and paste the code from `shape_key_transfer.py`.
3. Locate the `CONFIGURATION` section at the top of the file:
   ```python
   SOURCE_MESH = "YourBodyMeshName"  # Replace with outliner name of body
   TARGET_MESH = "YourClothingName"  # Replace with outliner name of clothes/hair
   ```
4. Open the live log tracking terminal by selecting `Window > Toggle System Console` via the top header options.
5. Click the **Run Script** play icon button inside the text view window.

---

## Troubleshooting & Constraints
- **Target contains concave polygons:** If your source mesh causes a Surface Deform bind error, go into edit mode on your body mesh (`Tab`), select all elements (`A`), press `Ctrl + T` to triangulate the surface layout topology, and rerun the tool.
- **Modifier Stack Order:** The script automatically pushes the runtime binder to the very peak (index 0) of the modifier stack workspace array to process cleanly. Ensure active custom topological dependencies like `Armature` rigs sit below it during runtime.
