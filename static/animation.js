// Three.js Particle Background Animation

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x000000, 0); // Transparent background
document.body.appendChild(renderer.domElement);
renderer.domElement.id = 'three-canvas';

// Particles
const particleCount = 1000;
const particles = new THREE.BufferGeometry();
const positions = new Float32Array(particleCount * 3);

for (let i = 0; i < particleCount; i++) {
    const i3 = i * 3;
    positions[i3] = (Math.random() - 0.5) * 10; // x
    positions[i3 + 1] = (Math.random() - 0.5) * 10; // y
    positions[i3 + 2] = (Math.random() - 0.5) * 10; // z
}

particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));

const particleMaterial = new THREE.PointsMaterial({
    color: 0x888888,
    size: 0.05,
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false
});

const particleSystem = new THREE.Points(particles, particleMaterial);
scene.add(particleSystem);

camera.position.z = 5;

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    particleSystem.rotation.x += 0.0005;
    particleSystem.rotation.y += 0.0008;

    renderer.render(scene, camera);
}
animate();

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// GSAP animation for dynamic elements (optional, can be removed if not needed for specific elements)
// Example: Animate camera position slightly
gsap.to(camera.position, { duration: 10, z: 6, repeat: -1, yoyo: true, ease: "power1.inOut" });