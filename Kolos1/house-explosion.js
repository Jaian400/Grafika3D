(() => {
  const buildings = [
    { sensor: 'houseProximity', position: '180 10 -22', size: 14, proximity: true },
    { sensor: 'terminalTouch', position: '24 10 16', size: 20 },
    { sensor: 'towerTouch', position: '41 20 -9', size: 14 },
    { sensor: 'hangar9Touch', position: '9 8 -23', size: 14 },
    { sensor: 'hangar26Touch', position: '26 8 -23', size: 14 }
  ];
  buildings.forEach(building => {
  const sensor = document.getElementById(building.sensor);
  const size = building.size;
  const effect = document.createElement('switch');
  effect.setAttribute('whichChoice', '-1');
  effect.innerHTML = `
    <transform translation="${building.position}">
      <billboard axisOfRotation="0 0 0">
        <shape>
          <appearance><imageTexture url='"explosion.png"' repeatS="false" repeatT="false"></imageTexture></appearance>
          <indexedFaceSet coordIndex="0 1 2 3 -1" solid="false" lit="false">
            <coordinate point="${-size} ${-size} 0, ${size} ${-size} 0, ${size} ${size} 0, ${-size} ${size} 0"></coordinate>
            <textureCoordinate point="0 0, 1 0, 1 1, 0 1"></textureCoordinate>
          </indexedFaceSet>
        </shape>
      </billboard>
    </transform>`;
  document.querySelector('x3d scene').appendChild(effect);
  let timer;
  sensor.onoutputchange = event => {
    if (building.proximity) {
      if (event.fieldName !== 'isActive' || !(event.value === true || event.value === 'true')) return;
    } else if (event.fieldName !== 'touchTime') return;
    clearTimeout(timer);
    effect.setAttribute('whichChoice', '0');
    timer = setTimeout(() => effect.setAttribute('whichChoice', '-1'), 2800);
  };
  });
})();
