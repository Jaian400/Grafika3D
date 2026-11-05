(() => {
  const toggle = document.getElementById('nightMode');
  const status = document.getElementById('dayNightStatus');
  const scene = document.querySelector('x3d scene');
  const sky = scene.querySelector('background');
  const fog = scene.querySelector('fog');
  const sun = scene.querySelector('directionallight');
  const navigation = document.createElement('navigationinfo');
  navigation.setAttribute('headlight', 'false');
  scene.appendChild(navigation);

  const skyBall = document.createElement('transform');
  skyBall.setAttribute('translation', '-60 85 -100');
  const ballShape = document.createElement('shape');
  const ballAppearance = document.createElement('appearance');
  const ballMaterial = document.createElement('material');
  ballMaterial.setAttribute('specularColor', '1 1 1');
  ballMaterial.setAttribute('shininess', '0.8');
  const ballGeometry = document.createElement('sphere');
  ballGeometry.setAttribute('radius', '7');
  ballAppearance.appendChild(ballMaterial);
  ballShape.appendChild(ballAppearance);
  ballShape.appendChild(ballGeometry);
  skyBall.appendChild(ballShape);
  scene.appendChild(skyBall);
  const ballLight = document.createElement('pointlight');
  ballLight.setAttribute('location', '-60 85 -100');
  ballLight.setAttribute('radius', '400');
  ballLight.setAttribute('attenuation', '1 0.002 0.00001');
  scene.appendChild(ballLight);

  const runwayLight = document.createElement('pointlight');
  runwayLight.setAttribute('location', '-15 8 0');
  runwayLight.setAttribute('color', '1 0.88 0.66');
  runwayLight.setAttribute('intensity', '0.9');
  runwayLight.setAttribute('radius', '45');
  runwayLight.setAttribute('attenuation', '1 0.02 0.002');
  runwayLight.setAttribute('on', 'false');
  scene.appendChild(runwayLight);

  function updateLighting() {
    const night = toggle.checked;
    ballMaterial.setAttribute('diffuseColor', night ? '0.78 0.81 0.85' : '1 0.85 0.05');
    ballMaterial.setAttribute('emissiveColor', night ? '0.32 0.35 0.40' : '0.65 0.48 0.02');
    ballLight.setAttribute('color', night ? '0.65 0.76 1' : '1 0.90 0.60');
    ballLight.setAttribute('intensity', night ? '0.55' : '0.9');
    runwayLight.setAttribute('on', String(night));
    sky.setAttribute('skyColor', night
      ? '0.008 0.015 0.045, 0.025 0.045 0.10, 0.10 0.14 0.22'
      : '0.28 0.52 0.79, 0.65 0.79 0.90, 0.84 0.88 0.90');
    sky.setAttribute('groundColor', night
      ? '0.015 0.035 0.02, 0.04 0.07 0.06, 0.10 0.14 0.22'
      : '0.22 0.46 0.16, 0.43 0.58 0.37, 0.84 0.88 0.90');
    fog.setAttribute('color', night ? '0.10 0.14 0.22' : '0.84 0.88 0.90');
    sun.setAttribute('intensity', night ? '0.22' : '0.8');
    sun.setAttribute('ambientIntensity', night ? '0.12' : '0.3');
    sun.setAttribute('color', night ? '0.50 0.65 1' : '1 1 1');
    const tower = document.querySelector('#controlTower wieza');
    if (tower) tower.setAttribute('windowGlow', night ? '0.55 0.37 0.13' : '0 0 0');
    status.textContent = night ? 'Noc' : 'Dzień';
  }
  toggle.addEventListener('change', updateLighting);
  document.querySelector('x3d').addEventListener('load', updateLighting);
  updateLighting();
})();
