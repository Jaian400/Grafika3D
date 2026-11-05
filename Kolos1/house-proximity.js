(() => {
  const scene = document.querySelector('x3d scene');
  const caption = document.createElement('transform');
  caption.setAttribute('translation', '180 3.5 -16.88');
  caption.innerHTML = `<shape>
      <appearance><material diffuseColor="0.04 0.04 0.04"></material></appearance>
      <text string='"dom terrorystow"' solid="false">
        <fontStyle size="0.85" justify='"MIDDLE" "MIDDLE"' family='"SANS"'></fontStyle>
      </text>
    </shape>`;
  scene.appendChild(caption);
  const airportView = scene.querySelector('viewpoint');
  const houseView = document.createElement('viewpoint');
  houseView.setAttribute('position', '180 18 55');
  houseView.setAttribute('orientation', '1 0 0 -0.19');
  houseView.setAttribute('centerOfRotation', '180 3 -22');
  houseView.setAttribute('description', 'Domek');
  scene.appendChild(houseView);
  const controls = document.createElement('section');
  controls.className = 'control-section';
  const visit = document.createElement('button');
  visit.textContent = 'Widok domku';
  visit.addEventListener('click', () => houseView.setAttribute('set_bind', 'true'));
  const back = document.createElement('button');
  back.textContent = 'Widok lotniska';
  back.style.marginLeft = '8px';
  back.addEventListener('click', () => airportView.setAttribute('set_bind', 'true'));
  controls.appendChild(visit);
  controls.appendChild(back);
  document.querySelector('.control-panel').appendChild(controls);
})();
