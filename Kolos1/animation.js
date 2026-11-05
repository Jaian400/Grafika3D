(() => {
  const slider = document.getElementById('flightProgress');
  const button = document.getElementById('flightPlay');
  const plane = document.getElementById('animatedPlane');
  const passengers = document.getElementById('passengers');
  const nightMode = document.getElementById('nightMode');
  const dots = [];
  const passengerMaterials = [];
  const colorControl = document.getElementById('peopleColor');

  function updatePassengerColor() {
    const rgb = [1, 3, 5].map(offset => parseInt(colorControl.value.slice(offset, offset + 2), 16));
    const color = rgb.map(value => value / 255).join(' ');
    passengerMaterials.forEach(material => {
      material.setAttribute('diffuseColor', color);
      material.setAttribute('emissiveColor', rgb.map(value => value / 255 * 0.2).join(' '));
    });
  }
  let playing = false;
  let previousTime;
  const clamp = value => Math.max(0, Math.min(1, value));
  const mix = (a, b, t) => a + (b - a) * t;
  const smooth = t => t * t * (3 - 2 * t);

  for (let i = 0; i < 12; i++) {
    const dot = document.createElement('transform');
    dot.setAttribute('scale', '0 0 0');
    const shape = document.createElement('shape');
    shape.innerHTML = '<appearance><material diffuseColor="1 0.57 0.06" emissiveColor="0.2 0.07 0"></material></appearance><sphere radius="0.38"></sphere>';
    dot.appendChild(shape);
    passengerMaterials.push(shape.querySelector('material'));
    passengers.appendChild(dot);
    dots.push(dot);
  }
  colorControl.addEventListener('input', updatePassengerColor);
  updatePassengerColor();

  function update() {
    const p = Number(slider.value) / 100;
    slider.setAttribute('aria-valuetext', `${Math.round(p * 100)}%`);
    if (nightMode.checked) {
      window.nightFlight.render(p);
      return;
    }
    window.nightFlight.reset();
    // The model points along +Z; turn its nose toward the landing direction (-Z).
    let x = -15, y = 0, z, yaw = Math.PI;
    if (p < 0.4) {
      const t = p / 0.4;
      z = mix(85, 20, t);
      y = 26 * (1 - smooth(t));
    } else if (p < 0.6) {
      z = mix(20, -12, smooth((p - 0.4) / 0.2));
    } else if (p < 0.72) {
      const t = smooth((p - 0.6) / 0.12);
      x = mix(-15, -2, t);
      z = mix(-12, 0, t);
      yaw = mix(Math.PI, Math.PI / 2, t);
    } else {
      x = -2;
      z = 0;
      yaw = Math.PI / 2;
    }
    plane.setAttribute('translation', `${x} ${y} ${z}`);
    plane.setAttribute('rotation', `0 1 0 ${yaw}`);
    dots.forEach((dot, i) => {
      const t = (p - 0.73 - i * 0.009) / 0.16;
      const visible = t >= 0 && t < 1;
      dot.setAttribute('scale', visible ? '1 1 1' : '0 0 0');
      const u = clamp(t);
      const bend = clamp(u / 0.3);
      const walk = clamp((u - 0.3) / 0.7);
      dot.setAttribute('translation', `${mix(-1, 24, walk)} 1.6 ${mix(3.5, 7.5, bend)}`);
    });
  }

  slider.addEventListener('input', update);
  document.getElementById('planeTouch').onoutputchange = event => {
    if (event.fieldName !== 'touchTime') return;
    slider.value = '0';
    playing = true;
    previousTime = undefined;
    button.textContent = 'Pauza';
    update();
  };
  nightMode.addEventListener('change', () => {
    slider.value = '0';
    playing = nightMode.checked;
    previousTime = undefined;
    button.textContent = playing ? 'Pauza' : 'Odtwórz';
    update();
  });
  button.addEventListener('click', () => {
    if (Number(slider.value) >= 100) slider.value = '0';
    playing = !playing;
    button.textContent = playing ? 'Pauza' : 'Odtwórz';
    previousTime = undefined;
    update();
  });
  function tick(now) {
    if (playing && previousTime !== undefined) {
      slider.value = String(Math.min(100, Number(slider.value) + (now - previousTime) / 150));
      update();
      if (Number(slider.value) >= 100) {
        playing = false;
        button.textContent = 'Odtwórz ponownie';
      }
    }
    previousTime = now;
    requestAnimationFrame(tick);
  }
  update();
  requestAnimationFrame(tick);
})();
