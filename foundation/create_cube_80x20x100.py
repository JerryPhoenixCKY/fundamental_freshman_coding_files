import bpy
import bmesh

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create a new cube
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))

# Get the active object (the cube we just created)
cube = bpy.context.active_object

# Set the dimensions
# Blender uses (width, depth, height) which corresponds to (X, Y, Z)
cube.dimensions = (80, 20, 100)

# Apply the scale to make the dimensions permanent
bpy.ops.object.transform_apply(scale=True)

# Optional: Add some visual enhancements
# Set smooth shading
bpy.ops.object.shade_smooth()

# Add a material
material = bpy.data.materials.new(name="Cube_Material")
material.use_nodes = True
material.node_tree.clear()

# Create a simple material with principled BSDF
bsdf = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (0.8, 0.3, 0.1, 1.0)  # Orange color
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.5

output = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
material.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign material to cube
cube.data.materials.append(material)

# Set camera to view the cube
bpy.ops.object.camera_add(location=(120, -120, 80))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)

# Set camera as active camera
bpy.context.scene.camera = camera

# Add a light
bpy.ops.object.light_add(type='SUN', location=(50, 50, 100))
light = bpy.context.active_object
light.data.energy = 2.0

print("Cube created successfully!")
print(f"Dimensions: {cube.dimensions}")
print("You can now save the file or continue editing in Blender.")