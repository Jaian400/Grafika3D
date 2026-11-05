"""Embed the local Blender OBJ/MTL aircraft directly in lotnisko.html."""
from pathlib import Path
import xml.etree.ElementTree as ET


def convert():
    folder = Path(__file__).resolve().parent
    materials = {}
    current = None
    for line in (folder / 'PLANE2.mtl').read_text().splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == 'newmtl':
            current = materials.setdefault(parts[1], {})
        elif current is not None:
            current[parts[0]] = parts[1:]

    vertices, normals, groups = [], [], {}
    material = None
    for line in (folder / 'PLANE2.obj').read_text().splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == 'v':
            vertices.append(parts[1:4])
        elif parts[0] == 'vn':
            normals.append(parts[1:4])
        elif parts[0] == 'usemtl':
            material = parts[1]
        elif parts[0] == 'f':
            face = []
            for token in parts[1:]:
                indices = token.split('/')
                v = int(indices[0])
                n = int(indices[2]) if len(indices) > 2 and indices[2] else None
                face.append((v - 1 if v > 0 else len(vertices) + v,
                             (n - 1 if n > 0 else len(normals) + n) if n else None))
            groups.setdefault(material, []).append(face)

    root = ET.Element('X3D', profile='Interchange', version='3.3')
    scene = ET.SubElement(root, 'Scene')
    face_count = 0
    for name, faces in groups.items():
        shape = ET.SubElement(scene, 'Shape')
        appearance = ET.SubElement(shape, 'Appearance')
        props = materials.get(name, {})
        ET.SubElement(appearance, 'Material',
                      diffuseColor=' '.join(props.get('Kd', ['0.8'] * 3)),
                      specularColor=' '.join(props.get('Ks', ['0'] * 3)),
                      shininess=str(min(float(props.get('Ns', ['0'])[0]) / 1000, 1)),
                      transparency=str(1 - float(props.get('d', ['1'])[0])))
        vertex_map, normal_map = {}, {}
        coord_indices, normal_indices = [], []
        has_normals = all(n is not None for face in faces for _, n in face)
        for face in faces:
            for v, n in face:
                coord_indices.append(str(vertex_map.setdefault(v, len(vertex_map))))
                if has_normals:
                    normal_indices.append(str(normal_map.setdefault(n, len(normal_map))))
            coord_indices.append('-1')
            if has_normals:
                normal_indices.append('-1')
        mesh = ET.SubElement(shape, 'IndexedFaceSet',
                             coordIndex=' '.join(coord_indices), solid='false')
        ET.SubElement(mesh, 'Coordinate', point=' '.join(' '.join(vertices[v]) for v in vertex_map))
        if has_normals:
            mesh.set('normalIndex', ' '.join(normal_indices))
            ET.SubElement(mesh, 'Normal', vector=' '.join(' '.join(normals[n]) for n in normal_map))
        face_count += len(faces)
    # HTML requires explicit closing tags, including Coordinate and Material.
    geometry = '\n'.join(ET.tostring(shape, encoding='unicode', short_empty_elements=False)
                         for shape in scene)
    start = '<!-- PLANE2 START -->'
    end = '<!-- PLANE2 END -->'
    model = (start + '\n<transform id="animatedPlane" translation="-15 26 85" rotation="0 1 0 3.141593">'
             + '\n<TouchSensor id="planeTouch" description="Uruchom animację samolotu"></TouchSensor>'
             + '\n<transform translation="-2.13 1.21 1.64" scale="0.3 0.3 0.3">\n'
             + geometry + '\n</transform>\n</transform>\n' + end)
    output = folder / 'lotnisko.html'
    html = output.read_text(encoding='utf-8')
    if start in html and end in html:
        before, rest = html.split(start, 1)
        _, after = rest.split(end, 1)
        html = before + model + after
    else:
        target = '<inline url="PLANE2.obj"></inline>'
        if target not in html:
            raise ValueError('Cannot find aircraft insertion point')
        html = html.replace(target, model, 1)
    output.write_text(html, encoding='utf-8')
    print(f'{output.name}: {len(vertices)} vertices, {face_count} faces, {len(groups)} materials')
    print('Bounds:', [(min(float(v[i]) for v in vertices), max(float(v[i]) for v in vertices)) for i in range(3)])


if __name__ == '__main__':
    convert()
