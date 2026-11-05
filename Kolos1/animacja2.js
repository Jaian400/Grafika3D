(() => {
  const plane = document.getElementById('animatedPlane');
  const passengers = document.getElementById('passengers');
  const roll = document.createElement('transform');
  roll.setAttribute('center', '0 2 0');
  while (plane.firstChild) roll.appendChild(plane.firstChild);
  plane.appendChild(roll);

  const explosion = document.createElement('switch');
  explosion.setAttribute('whichChoice', '-1');
  explosion.innerHTML = `
    <transform translation="-15 14 -5">
      <billboard axisOfRotation="0 0 0">
        <shape>
          <appearance>
            <imageTexture url='"explosion.png"' repeatS="false" repeatT="false"></imageTexture>
          </appearance>
          <indexedFaceSet coordIndex="0 1 2 3 -1" solid="false" lit="false">
            <coordinate point="-18 -18 0, 18 -18 0, 18 18 0, -18 18 0"></coordinate>
            <textureCoordinate point="0 0, 1 0, 1 1, 0 1"></textureCoordinate>
          </indexedFaceSet>
        </shape>
      </billboard>
    </transform>`;
  document.querySelector('x3d scene').appendChild(explosion);

  window.nightFlight = {
    render(progress) {
      const t = Math.max(0, Math.min(1, progress / 0.94));
      const hit = progress >= 0.94;
      explosion.setAttribute('whichChoice', hit ? '0' : '-1');
      const angle = (8 * Math.PI + 0.8) * t * t;
      const x = -15 + (hit ? 0 : Math.sin(t * Math.PI * 4) * 3 * Math.sin(t * Math.PI));
      const y = hit ? -0.3 : 32 * (1 - t * t);
      const z = 85 - 90 * t;
      plane.setAttribute('translation', `${x} ${y} ${z}`);
      plane.setAttribute('rotation', `0 1 0 ${Math.PI}`);
      roll.setAttribute('rotation', `0 0 1 ${angle}`);
      passengers.setAttribute('scale', '0 0 0');
    },
    reset() {
      explosion.setAttribute('whichChoice', '-1');
      roll.setAttribute('rotation', '0 0 1 0');
      passengers.setAttribute('scale', '1 1 1');
    }
  };
})();
