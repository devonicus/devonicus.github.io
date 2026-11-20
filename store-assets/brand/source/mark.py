"""Devonicus mark: a brass D with a cranberry tile in its counter, on a teal tile.
usage: python3 mark.py OUT.png SIZE SAMPLES [tile|bare]"""
import sys, math, bpy, bmesh
from mathutils import Vector

out, size, samples, mode = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
GEM_X = float(sys.argv[5]) if len(sys.argv) > 5 else 0.06
GEM_Y = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
FONT = "/home/claude/brand/fredoka-700.ttf"

def hexrgb(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [(x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*lin, a)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = samples
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 12
sc.cycles.glossy_bounces = 6
sc.render.resolution_x = sc.render.resolution_y = size
sc.render.film_transparent = True
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Punchy'
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.render.image_settings.color_depth = '16'

def mat(name, base, metallic=0.0, rough=0.4, coat=0.0, sheen=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexrgb(base)
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Roughness'].default_value = rough
    b.inputs['Coat Weight'].default_value = coat
    b.inputs['Coat Roughness'].default_value = 0.08
    return m

brass = mat('brass', '#f7c552', metallic=1.0, rough=0.22)
# a gentle brushed variation so the brass doesn't read flat
nt = brass.node_tree; bsdf = nt.nodes['Principled BSDF']
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 400; noise.inputs['Detail'].default_value = 6
ramp = nt.nodes.new('ShaderNodeMapRange'); ramp.inputs['To Min'].default_value = 0.17; ramp.inputs['To Max'].default_value = 0.23
nt.links.new(noise.outputs['Fac'], ramp.inputs['Value']); nt.links.new(ramp.outputs['Result'], bsdf.inputs['Roughness'])
cran = mat('cranberry', '#9c1f3c', rough=0.16, coat=1.0)
teal = mat('teal', '#124650', rough=0.45, coat=0.5)

# letter
bpy.ops.object.text_add(location=(0, 0, 0))
t = bpy.context.object; t.data.body = 'Devonicus' if mode == 'word' else 'D'
t.data.font = bpy.data.fonts.load(FONT)
t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
t.data.size = 2.85; t.data.extrude = 0.18
t.data.bevel_depth = 0.06; t.data.bevel_resolution = 6
t.data.resolution_u = 24
if mode == 'word': t.data.space_character = 1.07
bpy.ops.object.convert(target='MESH')
d = bpy.context.object; d.data.materials.append(brass)
bpy.ops.object.shade_smooth()
# centre the glyph optically
bb = [d.matrix_world @ Vector(c) for c in d.bound_box]
cx = (min(v.x for v in bb) + max(v.x for v in bb)) / 2; cy = (min(v.y for v in bb) + max(v.y for v in bb)) / 2
d.location.x -= cx; d.location.y -= cy
w = max(v.x for v in bb) - min(v.x for v in bb); h = max(v.y for v in bb) - min(v.y for v in bb)
d.location.z = 0.20
# counter tile: a small rounded cranberry square set in the D's bowl, a little proud of the face
if mode != 'word':
    bpy.ops.mesh.primitive_cube_add(size=1)
    g = bpy.context.object
    g.scale = (0.30, 0.30, 0.12); bpy.ops.object.transform_apply(scale=True)
    g.location = (GEM_X, GEM_Y, 0.36)
    bev = g.modifiers.new('bev', 'BEVEL'); bev.width = 0.08; bev.segments = 10; bev.limit_method = 'NONE'
    g.data.materials.append(cran); bpy.ops.object.shade_smooth()

if mode == 'tile':
    me = bpy.data.meshes.new('tile'); bm = bmesh.new()
    s, rad, n = 1.45, 0.46, 20
    pts = []
    for cx_, cy_, a0 in ((s - rad, s - rad, 0), (-s + rad, s - rad, 90), (-s + rad, -s + rad, 180), (s - rad, -s + rad, 270)):
        for i in range(n + 1):
            ang = math.radians(a0 + 90 * i / n)
            pts.append((cx_ + rad * math.cos(ang), cy_ + rad * math.sin(ang), 0))
    vs = [bm.verts.new(v) for v in pts]
    bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    for v in [e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)]: v.co.z += 0.28
    bm.to_mesh(me); bm.free()
    tile = bpy.data.objects.new('tile', me); sc.collection.objects.link(tile)
    tile.location.z = -0.2
    tb = tile.modifiers.new('bev', 'BEVEL'); tb.width = 0.07; tb.segments = 8; tb.limit_method = 'ANGLE'
    tile.data.materials.append(teal)
    for p_ in tile.data.polygons: p_.use_smooth = True

# lights: key from the upper left (the games' light direction), cool fill, warm rim
def area(name, loc, energy, size, color):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.object; l.data.energy = energy; l.data.size = size; l.data.color = color
    direction = Vector((0, 0, 0)) - Vector(loc); l.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
area('key', (-4.5, 4.0, 6.5), 2200, 4.0, (1.0, 0.96, 0.90))
area('fill', (5.0, -2.0, 4.0), 500, 6.0, (0.80, 0.90, 1.0))
area('rim', (3.0, 5.0, 1.8), 900, 2.0, (1.0, 0.85, 0.65))

# big warm softbox overhead: the flat brass face reflects it, so the letter reads bright gold
bpy.ops.mesh.primitive_plane_add(size=1, location=(-2.0, 2.0, 22.0))
sb = bpy.context.object; sb.scale = (16, 16, 1)
sb.rotation_euler = (Vector((0, 0, 0)) - sb.location).to_track_quat('-Z', 'Y').to_euler(); sb.rotation_euler.z += math.radians(-35)
em = bpy.data.materials.new('soft'); em.use_nodes = True
en = em.node_tree.nodes; en.remove(en['Principled BSDF'])
e = en.new('ShaderNodeEmission'); e.inputs['Strength'].default_value = 2.6
tc = en.new('ShaderNodeTexCoord'); gr = en.new('ShaderNodeTexGradient'); cr = en.new('ShaderNodeValToRGB')
cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[0].color = (0.42, 0.33, 0.22, 1)
cr.color_ramp.elements[1].position = 0.62; cr.color_ramp.elements[1].color = (1.0, 0.93, 0.80, 1)
em.node_tree.links.new(tc.outputs['Generated'], gr.inputs['Vector']); em.node_tree.links.new(gr.outputs['Fac'], cr.inputs['Fac'])
em.node_tree.links.new(cr.outputs['Color'], e.inputs['Color'])
em.node_tree.links.new(e.outputs['Emission'], en['Material Output'].inputs['Surface'])
sb.data.materials.append(em); sb.visible_camera = False; sb.visible_shadow = False
# soft studio world for reflections in the brass
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']
grad = world.node_tree.nodes.new('ShaderNodeTexGradient'); grad.gradient_type = 'SPHERICAL'
ramp2 = world.node_tree.nodes.new('ShaderNodeValToRGB')
ramp2.color_ramp.elements[0].color = hexrgb('#0e2328'); ramp2.color_ramp.elements[1].color = hexrgb('#f6eedc')
world.node_tree.links.new(grad.outputs['Fac'], ramp2.inputs['Fac']); world.node_tree.links.new(ramp2.outputs['Color'], bg.inputs['Color'])
bg.inputs['Strength'].default_value = 0.45

# camera: near-orthographic, slight tilt so the bevels catch light
bpy.ops.object.camera_add(location=(0.0, -1.3, 14.0))
cam = bpy.context.object; sc.camera = cam
cam.data.lens = 120
cam.rotation_euler = (Vector((0, 0, 0.1)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.sensor_width = 36
fit = 3.08 if mode == 'tile' else 2.1
if mode == 'word':
    fit = w * 1.04
    sc.render.resolution_y = int(size * (h * 1.25) / fit)
cam.data.type = 'ORTHO'; cam.data.ortho_scale = fit

sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print('dims', round(w, 3), round(h, 3))
