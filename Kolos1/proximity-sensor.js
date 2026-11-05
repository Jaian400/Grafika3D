// Compatibility node: X3DOM does not provide the standard ProximitySensor.
// Implements the enabled/center/size fields and entry/exit events used here.
(() => {
  if (x3dom.nodeTypes.ProximitySensor) return;
  x3dom.registerNodeType('ProximitySensor', 'EnvironmentalSensor',
    defineClass(x3dom.nodeTypes.X3DSensorNode, function (ctx) {
      x3dom.nodeTypes.ProximitySensor.superClass.call(this, ctx);
      this.addField_SFVec3f(ctx, 'center', 0, 0, 0);
      this.addField_SFVec3f(ctx, 'size', 0, 0, 0);
      this.addField_SFTime(ctx, 'enterTime', 0);
      this.addField_SFTime(ctx, 'exitTime', 0);
    }, {})
  );

  function check() {
    const canvas = document.querySelector('x3d');
    if (canvas && canvas.runtime && canvas.runtime.isReady) {
      const camera = canvas.runtime.viewMatrix().inverse().e3();
      document.querySelectorAll('proximitysensor').forEach(element => {
        const node = element._x3domNode;
        if (!node) return;
        const position = node.getCurrentTransform().inverse().multMatrixPnt(camera);
        const { center, size, enabled } = node._vf;
        const inside = enabled && size.x > 0 && size.y > 0 && size.z > 0
          && Math.abs(position.x - center.x) <= size.x / 2
          && Math.abs(position.y - center.y) <= size.y / 2
          && Math.abs(position.z - center.z) <= size.z / 2;
        if (inside !== node._vf.isActive) {
          node.postMessage('isActive', inside);
          node.postMessage(inside ? 'enterTime' : 'exitTime', Date.now() / 1000);
        }
      });
    }
    requestAnimationFrame(check);
  }
  requestAnimationFrame(check);
})();
