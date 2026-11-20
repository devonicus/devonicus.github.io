"""Text-free store event art from one hero model: 16:9 event card (App Store card and Google Play promo image),
9:16 App Store details page and 1024x500 Play feature graphic. Blender Cycles, CC0 HDRI plus a key light from the
upper left. The subject is framed inside Google Play's promo safe zone (margins 15% top, 20% left/right/bottom).

usage: python3 event_art.py OUT_PREFIX HERO.glb|demo HDRI.hdr BG_HEX SAMPLES [SCALE=1.0]
  writes OUT_PREFIX-card-1920x1080.png, -details-1080x1920.png, -feature-1024x500.png (no text, no logos)
  SCALE < 1 renders a quick low-resolution preview."""
import sys, math, bpy
from mathutils import Vector

out, hero, hdri, bg_hex, samples = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
scale = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [(x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = samples; sc.cycles.use_denoising = True
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'

# hero: an imported model, or the Devonicus mark as a demo subject
if hero == 'demo':
    bpy.ops.object.text_add(); t = bpy.context.object; t.data.body = 'D'
    t.data.font = bpy.data.fonts.load('/home/claude/brand/fredoka-700.ttf')
    t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.size = 2.4
    t.data.extrude = 0.35; t.data.bevel_depth = 0.07; t.data.bevel_resolution = 6
    bpy.ops.object.convert(target='MESH'); bpy.ops.object.shade_smooth()
    m = bpy.data.materials.new('brass'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin('#f2b33d'), 1); b.inputs['Metallic'].default_value = 1; b.inputs['Roughness'].default_value = 0.25
    t.data.materials.append(m); t.rotation_euler = (math.radians(90), 0, math.radians(-18))
    objs = [t]
else:
    bpy.ops.import_scene.gltf(filepath=hero)
    objs = [o for o in bpy.context.selected_objects if o.type == 'MESH']

# fit the hero: base on the floor, centred, 2 units tall
bpy.context.view_layer.update()
pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
k = 2.0 / max(hi.z - lo.z, 1e-6)
root = bpy.data.objects.new('hero', None); sc.collection.objects.link(root)
for o in objs:
    if o.parent is None: o.parent = root
root.scale = (k, k, k)
root.location = (-(lo.x + hi.x) / 2 * k, -(lo.y + hi.y) / 2 * k, -lo.z * k)
W = (hi.x - lo.x) * k   # hero width after fitting

# cyclorama backdrop in the game's colour, with a soft warm floor bounce
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 8, 0)); floor = bpy.context.object
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.subdivide(number_cuts=40); bpy.ops.object.mode_set(mode='OBJECT')
for v in floor.data.vertices:               # curve the back half up into a wall
    if v.co.y > 0: v.co.z = (v.co.y ** 2) / 14
bpy.ops.object.shade_smooth()
bm = bpy.data.materials.new('backdrop'); bm.use_nodes = True; bn = bm.node_tree.nodes['Principled BSDF']
bn.inputs['Base Color'].default_value = (*lin(bg_hex), 1); bn.inputs['Roughness'].default_value = 0.8
floor.data.materials.append(bm)

# lighting: CC0 studio HDRI for reflections and fill, a big key from the upper left, a warm rim from behind
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
env = w.node_tree.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(hdri)
w.node_tree.links.new(env.outputs['Color'], w.node_tree.nodes['Background'].inputs['Color'])
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.8


def area(loc, energy, size, col):
    bpy.ops.object.light_add(type='AREA', location=loc); l = bpy.context.object
    l.data.energy, l.data.size, l.data.color = energy, size, col
    l.rotation_euler = (Vector((0, 0, 1)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


area((-5, -4, 6), 1800, 5, (1, .96, .9)); area((4, 4, 3), 900, 3, (1, .85, .65))

cam_data = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cam_data); sc.collection.objects.link(cam); sc.camera = cam
cam_data.lens = 70; cam_data.sensor_fit = 'VERTICAL'; cam_data.sensor_height = 24


def shoot(name, rw, rh, fill_h, centre_y):
    """Frame the hero so it fills fill_h of the frame height, centred at centre_y (0 top..1 bottom)."""
    sc.render.resolution_x, sc.render.resolution_y = int(rw * scale), int(rh * scale)
    target = Vector((0, 0, 1.0))
    vis_h = 2.0 / fill_h                          # world height visible at the hero
    d = vis_h * cam_data.lens / cam_data.sensor_height
    d = max(d, (W / 0.5) * cam_data.lens / (cam_data.sensor_height * rw / rh))   # keep it inside half the width
    tilt = math.radians(8)
    cam.location = target + Vector((0, -d * math.cos(tilt), d * math.sin(tilt)))
    cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = f'{out}-{name}.png'; bpy.ops.render.render(write_still=True)


# Play safe box on 16:9 is y 15%..80%, x 20%..80% -> centre at 47.5% height, about 65% tall; aim the hero at 52% of the height
shoot('card-1920x1080', 1920, 1080, 0.48, 0.475)
shoot('details-1080x1920', 1080, 1920, 0.36, 0.5)
shoot('feature-1024x500', 1024, 500, 0.58, 0.5)
print('done', round(W, 2))
