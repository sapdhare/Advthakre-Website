
const canvas = document.getElementById("bg-canvas");

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });

renderer.setSize(window.innerWidth, window.innerHeight);

const geometry = new THREE.BufferGeometry();
const vertices = [];

for (let i = 0; i < 5000; i++) {
  vertices.push(
    (Math.random() - 0.5) * 2000,
    (Math.random() - 0.5) * 2000,
    (Math.random() - 0.5) * 2000
  );
}

geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));

const material = new THREE.PointsMaterial({
  color: 0xd4af37,
  size: 2
});

const points = new THREE.Points(geometry, material);
scene.add(points);

camera.position.z = 500;

function animate() {
  requestAnimationFrame(animate);
  points.rotation.y += 0.0005;
  renderer.render(scene, camera);
}

animate();