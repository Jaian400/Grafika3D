"""Build a continuous mountain range behind the airport, without random spikes."""
from pathlib import Path
import math
import re
import xml.etree.ElementTree as ET


def build():
    path = Path(__file__).with_name('lotnisko.html')
    html = path.read_text(encoding='utf-8')
    # The core build silently omits the Geometry3DExt / ElevationGrid node.
    html = html.replace('/download/dev/x3dom.js', '/download/dev/x3dom-full.js')
    nx, nz, step = 81, 71, 5
    heights, colors = [], []
    for row in range(nz):
        z = -175 + row * step
        for col in range(nx):
            x = -200 + col * step
            # A U-shaped valley: nearby rear ridge and two side walls.
            ridge_z = -88 + 8 * math.sin(x / 26)
            rear = (62 + 15 * math.sin(x / 17) + 10 * math.cos(x / 31)) * math.exp(-((z - ridge_z) / 30) ** 2)
            left = (58 + 12 * math.sin(z / 19)) * math.exp(-((x + 96 + 6 * math.sin(z / 25)) / 28) ** 2)
            right = (64 + 14 * math.cos(z / 21)) * math.exp(-((x - 100 - 7 * math.sin(z / 28)) / 30) ** 2)
            # Side walls end before the camera; the slab has a flat grass margin.
            side_fade = max(0, min(1, (100 - z) / 50))
            clearance = max(abs(x) - 58, -z - 43, 0)
            edge = max(0, min(1, (200 - abs(x)) / 45, (z + 175) / 40))
            h = max(rear, left * side_fade, right * side_fade) * min(clearance / 22, 1) * edge
            h *= 0.8
            heights.append(round(h, 3))
            # Warm stone above muted green foothills, with pale summit rock.
            palette = [(0, (0.22, 0.46, 0.16)),
                       (12, (0.32, 0.43, 0.25)),
                       (32, (0.46, 0.43, 0.36)),
                       (55, (0.59, 0.56, 0.49)),
                       (85, (0.76, 0.74, 0.67))]
            for (low, a), (high, b) in zip(palette, palette[1:]):
                if h <= high:
                    t = max(0, min(1, (h - low) / (high - low)))
                    colors.extend(round(v * (1 - t) + w * t, 3) for v, w in zip(a, b))
                    break
            else:
                colors.extend(palette[-1][1])

    terrain = '''      <!-- TERRAIN START -->
      <!-- Lotnisko w dolinie: bliskie góry z tyłu i po obu bokach. -->
      <transform translation="0 -1.5 0">
        <shape>
          <appearance>
            <material diffuseColor="1 1 1"></material>
            <imageTexture url='"grass.png"' repeatS="true" repeatT="true"></imageTexture>
            <textureTransform scale="36 32"></textureTransform>
          </appearance>
          <box size="440 1 380"></box>
        </shape>
      </transform>
      <transform translation="-200 -0.99 -175">
        <shape>
          <appearance><material diffuseColor="1 1 1" ambientIntensity="0.35"></material></appearance>
          <elevationGrid id="backgroundMountains" xDimension="81" zDimension="71"
                         xSpacing="5" zSpacing="5" solid="false"
                         creaseAngle="0.6" colorPerVertex="true" height="HEIGHTS">
            <color color="COLORS"></color>
          </elevationGrid>
        </shape>
      </transform>
      <!-- TERRAIN END -->

'''.replace('HEIGHTS', ' '.join(map(str, heights))).replace('COLORS', ' '.join(map(str, colors)))
    # The mountain grid also covers the flat valley. Put textured grass just
    # above its zero-height cells so the grid cannot hide the base texture.
    points = ' '.join(f'{-200 + col * step} -0.97 {-175 + row * step}'
                      for row in range(nz) for col in range(nx))
    uv = ' '.join(f'{col * step / 12:.3f} {row * step / 12:.3f}'
                  for row in range(nz) for col in range(nx))
    faces = []
    for row in range(nz - 1):
        for col in range(nx - 1):
            a = row * nx + col
            corners = (a, a + nx, a + nx + 1, a + 1)
            if all(heights[i] == 0 for i in corners):
                faces.append(' '.join(map(str, corners)) + ' -1')
    grass = f'''<shape id="valleyGrass">
      <appearance><material diffuseColor="1 1 1"></material>
        <imageTexture url='"grass.png"' repeatS="true" repeatT="true"></imageTexture>
      </appearance>
      <indexedFaceSet coordIndex="{' '.join(faces)}" solid="false">
        <coordinate point="{points}"></coordinate>
        <textureCoordinate point="{uv}"></textureCoordinate>
      </indexedFaceSet>
    </shape>
'''
    terrain = terrain.replace('      <!-- TERRAIN END -->', grass + '      <!-- TERRAIN END -->')
    if '<!-- TERRAIN START -->' in html:
        html = re.sub(r'      <!-- TERRAIN START -->.*?<!-- TERRAIN END -->\s*', terrain, html, count=1, flags=re.S)
    else:
        start = html.index('      <!-- Zielona')
        end = html.index('      <!-- PLANE2 START -->', start)
        html = html[:start] + terrain + html[end:]
    html = re.sub(r'<background\b.*?</background>', '''<background skyAngle="1.1 1.570796"
                  skyColor="0.28 0.52 0.79, 0.65 0.79 0.90, 0.84 0.88 0.90"
                  groundAngle="1.3 1.570796"
                  groundColor="0.22 0.46 0.16, 0.43 0.58 0.37, 0.84 0.88 0.90"></background>''', html, count=1, flags=re.S)
    html = re.sub(r'\s*<fog\b.*?</fog>', '', html, flags=re.S)
    html = html.replace('</background>', '</background>\n      <fog color="0.84 0.88 0.90" fogType="LINEAR" visibilityRange="550"></fog>', 1)
    html = re.sub(r'<viewpoint\b.*?</viewpoint>', '<viewpoint description="Lotnisko w dolinie" position="0 58 135" orientation="1 0 0 -0.32" centerOfRotation="0 0 0" fieldOfView="1.05" zFar="10000"></viewpoint>', html, count=1, flags=re.S)

    grid = ET.fromstring('<Scene>' + terrain + '</Scene>').find('.//elevationGrid')
    assert len(grid.get('height').split()) == nx * nz
    assert len(grid.find('color').get('color').split()) == nx * nz * 3
    assert all(heights[row * nx + col] == 0
               for row in range(nz) for col in range(nx)
               if abs(-200 + col * step) <= 58 and abs(-175 + row * step) <= 43)
    path.write_text(html, encoding='utf-8')
    print(f'OK: {nx} x {nz} vertices; flat airport; nearby valley walls; max height {max(heights)}')


if __name__ == '__main__':
    build()
