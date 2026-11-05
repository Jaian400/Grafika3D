"""Add terminal architecture and a lake below the landing approach."""
from pathlib import Path
import math
import re
import xml.etree.ElementTree as ET


def box(position, size, color, extra=''):
    return (f'<transform translation="{position}"><shape><appearance>'
            f'<material diffuseColor="{color}" {extra}></material></appearance>'
            f'<box size="{size}"></box></shape></transform>')


def build():
    path = Path(__file__).with_name('lotnisko.html')
    html = path.read_text(encoding='utf-8')
    terrain = ET.fromstring(re.search(r'<elevationGrid\b.*?</elevationGrid>', html, re.S).group())
    heights = list(map(float, terrain.get('height').split()))
    nx, nz = int(terrain.get('xDimension')), int(terrain.get('zDimension'))

    def ground(x, z):
        u, v = (x + 200) / 5, (z + 175) / 5
        i, j = min(nx - 2, max(0, int(u))), min(nz - 2, max(0, int(v)))
        a, b = max(0, min(1, u - i)), max(0, min(1, v - j))
        return -0.99 + ((1 - b) * ((1 - a) * heights[j * nx + i] + a * heights[j * nx + i + 1])
                        + b * ((1 - a) * heights[(j + 1) * nx + i] + a * heights[(j + 1) * nx + i + 1]))

    tower_proto = '''<ProtoDeclare name="Wieza">
  <ProtoInterface>
    <field name="position" type="SFVec3f" accessType="inputOutput" value="0 0 0"></field>
    <field name="sizeScale" type="SFVec3f" accessType="inputOutput" value="1 1 1"></field>
    <field name="bodyColor" type="SFColor" accessType="inputOutput" value="0.80 0.81 0.75"></field>
    <field name="glassColor" type="SFColor" accessType="inputOutput" value="0.13 0.33 0.40"></field>
    <field name="windowGlow" type="SFColor" accessType="inputOutput" value="0 0 0"></field>
  </ProtoInterface>
  <ProtoBody>
    <Transform>
      <IS>
        <connect nodeField="translation" protoField="position"></connect>
        <connect nodeField="scale" protoField="sizeScale"></connect>
      </IS>
      <Transform translation="0 10 0">
        <Shape><Appearance><Material>
          <IS><connect nodeField="diffuseColor" protoField="bodyColor"></connect></IS>
        </Material></Appearance><Box size="3.5 16 3.5"></Box></Shape>
      </Transform>
      <Transform translation="0 20 0">
        <Shape><Appearance><Material specularColor="0.8 0.9 1" shininess="0.7">
          <IS>
            <connect nodeField="diffuseColor" protoField="glassColor"></connect>
            <connect nodeField="emissiveColor" protoField="windowGlow"></connect>
          </IS>
        </Material></Appearance><Box size="6.5 3.5 5.5"></Box></Shape>
      </Transform>
      <Transform translation="0 22 0">
        <Shape><Appearance><Material diffuseColor="0.75 0.77 0.72"></Material></Appearance>
          <Box size="8 0.5 7"></Box></Shape>
      </Transform>
    </Transform>
  </ProtoBody>
</ProtoDeclare>'''
    tree_proto = '''<ProtoDeclare name="Drzewo">
  <ProtoInterface>
    <field name="position" type="SFVec3f" accessType="inputOutput" value="0 0 0"></field>
    <field name="sizeScale" type="SFVec3f" accessType="inputOutput" value="1 1 1"></field>
    <field name="crownColor" type="SFColor" accessType="inputOutput" value="0.12 0.38 0.13"></field>
  </ProtoInterface>
  <ProtoBody>
    <Transform>
      <IS>
        <connect nodeField="translation" protoField="position"></connect>
        <connect nodeField="scale" protoField="sizeScale"></connect>
      </IS>
      <Transform translation="0 2 0">
        <Shape><Appearance><Material diffuseColor="0.32 0.19 0.09"></Material></Appearance>
          <Cylinder radius="0.45" height="4"></Cylinder></Shape>
      </Transform>
      <Transform translation="0 5 0">
        <Shape><Appearance><Material>
          <IS><connect nodeField="diffuseColor" protoField="crownColor"></connect></IS>
        </Material></Appearance><Sphere radius="2.4"></Sphere></Shape>
      </Transform>
    </Transform>
  </ProtoBody>
</ProtoDeclare>'''
    parts = ['<!-- AIRPORT DETAILS START -->', tower_proto, tree_proto, '<group id="airportObjects">',
             '<group id="airportBuildings">', '<group id="terminal">']
    parts.append('<TouchSensor id="terminalTouch" description="Wybuch terminala"></TouchSensor>')
    # Keep the entrance at x=24,z=8 so the passenger animation reaches the door.
    parts.append(box('24 4.5 16', '24 7 16', '0.76 0.78 0.75'))
    parts.append(box('24 5 7.94', '23 5.6 0.12', '0.15 0.36 0.44', 'specularColor="0.8 0.9 1" shininess="0.65"'))
    parts.append(box('24 2.7 7.65', '2.8 3.4 0.2', '0.07 0.17 0.21'))
    parts.append(box('24 6.2 5.7', '9 0.35 5', '0.86 0.87 0.80'))
    parts.append(box('24 8.25 16', '26 0.5 18', '0.32 0.37 0.39'))
    for x in (9, 39):
        parts.append(f'<group id="terminalWing{x}">')
        parts.append(box(f'{x} 3 19', '6 4 22', '0.68 0.71 0.70'))
        parts.append(box(f'{x} 5.2 19', '6.8 0.4 22.8', '0.32 0.37 0.39'))
        parts.append(box(f'{x} 3.3 7.94', '5 2.1 0.15', '0.15 0.36 0.44'))
        parts.append('</group>')
    parts.extend(['</group>', '<group id="controlTower">'])
    parts.append('<TouchSensor id="towerTouch" description="Wybuch wieży"></TouchSensor>')
    parts.append('''<ProtoInstance name="Wieza" DEF="AirportTower">
      <fieldValue name="position" value="41 0 -9"></fieldValue>
      <fieldValue name="sizeScale" value="1 1 1"></fieldValue>
      <fieldValue name="bodyColor" value="0.80 0.81 0.75"></fieldValue>
      <fieldValue name="glassColor" value="0.13 0.33 0.40"></fieldValue>
      <fieldValue name="windowGlow" value="0 0 0"></fieldValue>
    </ProtoInstance>''')
    parts.extend(['</group>', '<group id="hangars">'])
    for x in (9, 26):
        parts.append(f'<group id="hangar{x}">')
        parts.append(f'<TouchSensor id="hangar{x}Touch" description="Wybuch hangaru"></TouchSensor>')
        parts.append(box(f'{x} 4 -23', '14 6 16', '0.64 0.69 0.70'))
        parts.append(box(f'{x} 7.3 -23', '15 0.6 17', '0.33 0.39 0.43'))
        parts.append(box(f'{x} 3.4 -14.9', '10 4.8 0.2', '0.29 0.37 0.40'))
        parts.append('</group>')
    parts.extend(['</group>', '</group>', '<group id="airportApron">'])
    parts.append(box('0 0 0', '100 2 70', '0.48 0.5 0.52'))
    parts.extend(['</group>', '<group id="runway">'])
    parts.append(box('-15 1.1 0', '18 0.2 58', '0.22 0.23 0.24'))
    parts.append('<group id="runwayMarkings">')
    # Runway centre markings and threshold stripes.
    for z in range(-23, 25, 8):
        parts.append(box(f'-15 1.215 {z}', '0.45 0.03 3.8', '0.94 0.94 0.85'))
    for x in (-21, -19, -17, -13, -11, -9):
        parts.append(box(f'{x} 1.215 25', '0.8 0.03 3', '0.94 0.94 0.85'))
    parts.extend(['</group>', '</group>', '<group id="accessRoad">'])
    # Five straight strips; diagonal strips split each corner into 45-degree turns.
    parts.append(box('28 -0.8 71.5', '7 0.3 73', '0.035 0.035 0.035'))
    parts.append('<transform translation="38 -0.8 115" rotation="0 1 0 0.785398">'
                 + box('0 0 0', '7 0.3 34.2843', '0.035 0.035 0.035') + '</transform>')
    parts.append(box('104 -0.8 125', '118 0.3 7', '0.035 0.035 0.035'))
    parts.append('<transform translation="170 -0.8 115" rotation="0 1 0 -0.785398">'
                 + box('0 0 0', '7 0.3 34.2843', '0.035 0.035 0.035') + '</transform>')
    parts.append(box('180 -0.8 46', '7 0.3 124', '0.035 0.035 0.035'))
    parts.extend(['</group>', '<group id="mountainHouse">'])
    parts.append('<ProximitySensor id="houseProximity" center="180 20 -22" size="90 100 90"></ProximitySensor>')
    base = ground(180, -22)
    parts.append(box(f'180 {base + 2.8} -22', '12 5.6 10', '0.86 0.77 0.59'))
    roof = ' '.join(f'{x} {base+y:.3f} {z}' for x,y,z in [(173,5.3,-28),(187,5.3,-28),(180,8.5,-28),(173,5.3,-16),(187,5.3,-16),(180,8.5,-16)])
    parts.append(f'''<shape><appearance><material diffuseColor="0.43 0.16 0.10"></material></appearance>
      <indexedFaceSet coordIndex="0 2 1 -1 3 4 5 -1 0 3 5 2 -1 1 2 5 4 -1 0 1 4 3 -1" solid="false">
        <coordinate point="{roof}"></coordinate></indexedFaceSet></shape>''')
    parts.extend(['</group>', '</group>', '<group id="roadsideTrees">'])
    for index, (x, z) in enumerate(( (x, z) for z in (45, 60, 75, 90) for x in (20, 36) )):
        scale = (0.9, 1.05, 1.15)[index % 3]
        parts.append(f'''<ProtoInstance name="Drzewo" DEF="RoadTree{index + 1}">
          <fieldValue name="position" value="{x} -1 {z}"></fieldValue>
          <fieldValue name="sizeScale" value="{scale} {scale} {scale}"></fieldValue>
        </ProtoInstance>''')
    parts.append('</group>')
    # The lake is scenery, separate from the airport object hierarchy.
    parts.append('<transform id="approachLake" translation="-15 0 75">')
    # Same egg outline twice: larger grey shore underneath the blue water.
    for scale, y, color in [(1.09, -0.88, '0.49 0.50 0.47'), (1, -0.78, '0.08 0.40 0.55')]:
        points = ['0 0 0']
        for i in range(32):
            angle = 2 * math.pi * i / 32
            x = 22 * math.cos(angle) * (1 - 0.24 * math.sin(angle))
            z = 25 * math.sin(angle)
            points.append(f'{x:.3f} 0 {z:.3f}')
        indices = ' '.join(f'0 {(i + 1) % 32 + 1} {i + 1} -1' for i in range(32))
        parts.append(f'''<transform translation="0 {y} 0" scale="{scale} 1 {scale}">
          <shape><appearance><material diffuseColor="{color}"></material></appearance>
            <indexedFaceSet coordIndex="{indices}" solid="false">
              <coordinate point="{' '.join(points)}"></coordinate>
            </indexedFaceSet>
          </shape>
        </transform>''')
    parts.append('</transform>')
    parts.append('<!-- AIRPORT DETAILS END -->')
    fragment = '\n'.join(parts)
    ET.fromstring('<scene>' + fragment + '</scene>')
    path = Path(__file__).with_name('lotnisko.html')
    html = path.read_text(encoding='utf-8')
    html = re.sub(r'      <!-- Szara płyta lotniska -->.*?(?=<!-- AIRPORT DETAILS START -->)', '', html, count=1, flags=re.S)
    if '<!-- AIRPORT DETAILS START -->' in html:
        html = re.sub(r'<!-- AIRPORT DETAILS START -->.*?<!-- AIRPORT DETAILS END -->', fragment, html, flags=re.S)
    else:
        start = html.index('      <!-- Element 2: terminal -->')
        end = html.index('    </scene>', start)
        html = html[:start] + fragment + '\n' + html[end:]
    path.write_text(html, encoding='utf-8')
    print('OK: grouped airport objects; simplified terminal, tower and hangars; lake preserved.')


if __name__ == '__main__':
    build()
