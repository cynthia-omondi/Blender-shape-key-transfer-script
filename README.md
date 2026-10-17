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

## Troubleshooting

### Existing Surface Deform Modifiers
If your target clothing mesh already has an active, manually applied Surface Deform modifier targeting your source body mesh, **delete or disable it before running the script**. Leaving an active Surface Deform modifier on your mesh while the script builds its temporary iteration loop will stack the deformations, resulting in broken, double-scaled, or completely corrupted shape key bakes.

