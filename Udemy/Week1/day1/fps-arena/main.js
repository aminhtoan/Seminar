import * as THREE from "https://unpkg.com/three@0.161.0/build/three.module.js";

const UI = {
  playerHp: document.getElementById("playerHp"),
  enemyHp: document.getElementById("enemyHp"),
  score: document.getElementById("score"),
  overlay: document.getElementById("overlay"),
  startBtn: document.getElementById("startBtn"),
};

const SETTINGS = {
  arenaHalfSize: 18,
  wallHeight: 4,
  playerHeight: 1.6,
  playerRadius: 0.5,
  moveSpeed: 6.0,
  turnSpeed: 3.2, // radians/sec
  mouseSensitivity: 0.0022,
  maxPitch: 1.2,
  shootCooldownMs: 250,
  bulletSpeed: 38,
  bulletRange: 35,
  bulletRadius: 0.09,
  enemyMoveSpeed: 3.8,
  enemyShootIntervalMs: 1200,
  enemyBulletRange: 28,
  enemyBulletSpeed: 28,
};

const clamp = (v, min, max) => Math.max(min, Math.min(max, v));

function nowMs() {
  return performance.now();
}

function setOverlayVisible(visible) {
  UI.overlay.classList.toggle("hidden", !visible);
}

function makeRenderer() {
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  document.body.appendChild(renderer.domElement);
  return renderer;
}

function makeScene() {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0b0f17);

  const ambient = new THREE.AmbientLight(0xffffff, 0.35);
  scene.add(ambient);

  const dir = new THREE.DirectionalLight(0xffffff, 1.0);
  dir.position.set(10, 18, 6);
  dir.castShadow = true;
  dir.shadow.mapSize.set(1024, 1024);
  dir.shadow.camera.near = 1;
  dir.shadow.camera.far = 60;
  dir.shadow.camera.left = -25;
  dir.shadow.camera.right = 25;
  dir.shadow.camera.top = 25;
  dir.shadow.camera.bottom = -25;
  scene.add(dir);

  const hemi = new THREE.HemisphereLight(0x88aaff, 0x223344, 0.45);
  hemi.position.set(0, 10, 0);
  scene.add(hemi);

  return scene;
}

function makeCamera() {
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    200
  );
  return camera;
}

function makeArena(scene) {
  const group = new THREE.Group();

  const floorGeo = new THREE.PlaneGeometry(
    SETTINGS.arenaHalfSize * 2,
    SETTINGS.arenaHalfSize * 2
  );
  const floorMat = new THREE.MeshStandardMaterial({
    color: 0x1a2331,
    roughness: 0.95,
    metalness: 0.0,
  });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  group.add(floor);

  const grid = new THREE.GridHelper(
    SETTINGS.arenaHalfSize * 2,
    SETTINGS.arenaHalfSize * 2,
    0x2b3b55,
    0x1b2636
  );
  grid.material.transparent = true;
  grid.material.opacity = 0.35;
  group.add(grid);

  const wallMat = new THREE.MeshStandardMaterial({
    color: 0x2a3242,
    roughness: 0.85,
    metalness: 0.05,
  });

  const wallThickness = 1;
  const size = SETTINGS.arenaHalfSize * 2;
  const h = SETTINGS.wallHeight;

  const north = new THREE.Mesh(
    new THREE.BoxGeometry(size + wallThickness * 2, h, wallThickness),
    wallMat
  );
  north.position.set(0, h / 2, -SETTINGS.arenaHalfSize - wallThickness / 2);
  north.castShadow = true;
  north.receiveShadow = true;

  const south = north.clone();
  south.position.z = SETTINGS.arenaHalfSize + wallThickness / 2;

  const west = new THREE.Mesh(
    new THREE.BoxGeometry(wallThickness, h, size + wallThickness * 2),
    wallMat
  );
  west.position.set(-SETTINGS.arenaHalfSize - wallThickness / 2, h / 2, 0);
  west.castShadow = true;
  west.receiveShadow = true;

  const east = west.clone();
  east.position.x = SETTINGS.arenaHalfSize + wallThickness / 2;

  group.add(north, south, west, east);

  // A couple of cover pillars
  const pillarGeo = new THREE.CylinderGeometry(0.7, 0.7, 3.2, 18);
  const pillarMat = new THREE.MeshStandardMaterial({
    color: 0x2c3c58,
    roughness: 0.8,
  });
  const pillarPositions = [
    new THREE.Vector3(-6, 1.6, -4),
    new THREE.Vector3(6, 1.6, 5),
    new THREE.Vector3(0, 1.6, 9),
  ];
  for (const pos of pillarPositions) {
    const p = new THREE.Mesh(pillarGeo, pillarMat);
    p.position.copy(pos);
    p.castShadow = true;
    p.receiveShadow = true;
    group.add(p);
  }

  scene.add(group);
  return { group };
}

function makeEnemy(scene) {
  // Boss: red capsule (different from a cube)
  const geo = new THREE.CapsuleGeometry(0.55, 0.9, 8, 16);
  const mat = new THREE.MeshStandardMaterial({ color: 0xff2d2d, roughness: 0.55 });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.position.set(8, 1.0, -8);
  scene.add(mesh);
  return mesh;
}

function makeMuzzleFlash(scene) {
  const geo = new THREE.SphereGeometry(0.08, 12, 10);
  const mat = new THREE.MeshBasicMaterial({ color: 0xfff3b0 });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.visible = false;
  scene.add(mesh);
  return mesh;
}

function yawToForward(yaw) {
  // yaw=0 faces -Z (Three.js camera default). Positive yaw turns LEFT.
  return new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
}

function integratePlayerMovement(player, input, dt) {
  const forward = yawToForward(player.yaw);
  const right = new THREE.Vector3(-forward.z, 0, forward.x).normalize();

  let moveZ = 0;
  if (input.ArrowUp) moveZ += 1;
  if (input.ArrowDown) moveZ -= 1;

  let moveX = 0;
  if (input.ArrowRight) moveX += 1;
  if (input.ArrowLeft) moveX -= 1;

  const stepZ = SETTINGS.moveSpeed * dt * moveZ;
  const stepX = SETTINGS.moveSpeed * dt * moveX;
  player.position.addScaledVector(forward, stepZ);
  player.position.addScaledVector(right, stepX);

  // Clamp inside arena (simple radius-based bounds)
  const max = SETTINGS.arenaHalfSize - SETTINGS.playerRadius;
  player.position.x = clamp(player.position.x, -max, max);
  player.position.z = clamp(player.position.z, -max, max);
}

function updateCamera(camera, player) {
  camera.position.set(player.position.x, SETTINGS.playerHeight, player.position.z);
  camera.rotation.order = "YXZ";
  camera.rotation.y = player.yaw;
  camera.rotation.x = player.pitch;
}

function raycastShot({ origin, direction, range, targetMesh }) {
  const raycaster = new THREE.Raycaster(origin, direction, 0, range);
  const hits = raycaster.intersectObject(targetMesh, false);
  return hits.length > 0;
}

function makeBulletMesh(color) {
  const geo = new THREE.SphereGeometry(SETTINGS.bulletRadius, 10, 10);
  const mat = new THREE.MeshStandardMaterial({
    color,
    roughness: 0.25,
    metalness: 0.1,
    emissive: new THREE.Color(color),
    emissiveIntensity: 0.55,
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.castShadow = true;
  return mesh;
}

function spawnBullet(state, { owner, origin, direction, speed, range, color, damage }) {
  const mesh = makeBulletMesh(color);
  mesh.position.copy(origin);
  state.scene.add(mesh);

  state.projectiles.push({
    owner,
    mesh,
    prevPos: origin.clone(),
    velocity: direction.clone().normalize().multiplyScalar(speed),
    traveled: 0,
    maxDistance: range,
    damage,
  });
}

function removeProjectile(state, p) {
  state.scene.remove(p.mesh);
  p.mesh.geometry?.dispose?.();
  p.mesh.material?.dispose?.();
}

function clampInsideArenaXZ(pos) {
  const max = SETTINGS.arenaHalfSize - SETTINGS.playerRadius;
  pos.x = clamp(pos.x, -max, max);
  pos.z = clamp(pos.z, -max, max);
}

function updateProjectiles(state, dt) {
  if (state.projectiles.length === 0) return;

  const arenaLimit = SETTINGS.arenaHalfSize + 2;
  const playerCenter = new THREE.Vector3(state.player.position.x, SETTINGS.playerHeight, state.player.position.z);

  for (let i = state.projectiles.length - 1; i >= 0; i--) {
    const p = state.projectiles[i];

    p.prevPos.copy(p.mesh.position);
    const step = p.velocity.clone().multiplyScalar(dt);
    p.mesh.position.add(step);
    p.traveled += step.length();

    // Remove if out of range or outside arena bounds
    if (
      p.traveled > p.maxDistance ||
      Math.abs(p.mesh.position.x) > arenaLimit ||
      Math.abs(p.mesh.position.z) > arenaLimit
    ) {
      removeProjectile(state, p);
      state.projectiles.splice(i, 1);
      continue;
    }

    // Collision checks
    if (state.game.over) {
      removeProjectile(state, p);
      state.projectiles.splice(i, 1);
      continue;
    }

    if (p.owner === "player") {
      // Check against enemy mesh using ray segment to avoid tunneling
      const segDir = p.mesh.position.clone().sub(p.prevPos);
      const segLen = segDir.length();
      if (segLen > 0.0001) {
        const raycaster = new THREE.Raycaster(p.prevPos, segDir.normalize(), 0, segLen + SETTINGS.bulletRadius);
        const hits = raycaster.intersectObject(state.enemy.mesh, false);
        if (hits.length > 0) {
          state.enemy.hp = Math.max(0, state.enemy.hp - p.damage);
          state.game.score += 1;
          syncHud(state);
          removeProjectile(state, p);
          state.projectiles.splice(i, 1);
          if (state.enemy.hp <= 0) {
            state.game.over = true;
            state.game.message = "You win! Press R to restart.";
            showGameOver(state);
          }
          continue;
        }
      }
    } else {
      // Enemy bullet vs player (player is a cylinder-ish point)
      const dx = p.mesh.position.x - playerCenter.x;
      const dz = p.mesh.position.z - playerCenter.z;
      const distXZ = Math.hypot(dx, dz);
      if (distXZ < SETTINGS.playerRadius + SETTINGS.bulletRadius) {
        state.player.hp = Math.max(0, state.player.hp - p.damage);
        syncHud(state);
        removeProjectile(state, p);
        state.projectiles.splice(i, 1);
        if (state.player.hp <= 0) {
          state.game.over = true;
          state.game.message = "You lose! Press R to restart.";
          showGameOver(state);
        }
        continue;
      }
    }

    // Very simple cover collision: if bullet intersects a pillar, remove it
    const raycaster = new THREE.Raycaster(p.prevPos, p.mesh.position.clone().sub(p.prevPos).normalize(), 0, p.mesh.position.distanceTo(p.prevPos) + SETTINGS.bulletRadius);
    const coverHits = raycaster.intersectObjects(state.world.coverMeshes, false);
    if (coverHits.length > 0) {
      removeProjectile(state, p);
      state.projectiles.splice(i, 1);
      continue;
    }
  }
}

function tryPlayerShoot(state) {
  const t = nowMs();
  if (t - state.player.lastShotAt < SETTINGS.shootCooldownMs) return;
  state.player.lastShotAt = t;

  const origin = new THREE.Vector3(
    state.player.position.x,
    SETTINGS.playerHeight,
    state.player.position.z
  );
  const dir = new THREE.Vector3();
  state.camera.getWorldDirection(dir);

  // flash
  state.effects.muzzleFlash.position.copy(origin).addScaledVector(dir, 0.6);
  state.effects.muzzleFlash.visible = true;
  state.effects.muzzleFlashOffAt = t + 55;

  if (state.game.over) return;

  spawnBullet(state, {
    owner: "player",
    origin: origin.addScaledVector(dir, 0.6),
    direction: dir,
    speed: SETTINGS.bulletSpeed,
    range: SETTINGS.bulletRange,
    color: 0xfff3b0,
    damage: 18,
  });
}

function enemyLineOfSight(state) {
  const origin = state.enemy.mesh.position.clone();
  origin.y = 0.7;
  const toPlayer = new THREE.Vector3(
    state.player.position.x - state.enemy.mesh.position.x,
    0,
    state.player.position.z - state.enemy.mesh.position.z
  );

  const dist = toPlayer.length();
  if (dist < 0.001) return { canSee: true, direction: new THREE.Vector3(0, 0, -1), dist: 0 };

  const direction = toPlayer.clone().normalize();

  // If any pillar blocks, treat as no LOS.
  const raycaster = new THREE.Raycaster(origin, direction, 0, dist);
  const hits = raycaster.intersectObjects(state.world.coverMeshes, false);
  if (hits.length > 0) return { canSee: false, direction, dist };

  return { canSee: true, direction, dist };
}

function stepEnemyAI(state, dt) {
  if (state.game.over) return;

  // Chase player (simple seek) with mild orbiting
  const toPlayer = new THREE.Vector3(
    state.player.position.x - state.enemy.mesh.position.x,
    0,
    state.player.position.z - state.enemy.mesh.position.z
  );

  const dist = toPlayer.length();
  const desired = dist > 0.001 ? toPlayer.normalize() : new THREE.Vector3(0, 0, -1);

  // orbit a bit so it isn't perfectly linear
  const orbit = new THREE.Vector3(-desired.z, 0, desired.x).multiplyScalar(0.35);
  const moveDir = desired.clone().add(orbit).normalize();

  const speed = SETTINGS.enemyMoveSpeed * (dist > 3 ? 1 : 0.35);
  state.enemy.mesh.position.addScaledVector(moveDir, speed * dt);

  const max = SETTINGS.arenaHalfSize - 0.7;
  state.enemy.mesh.position.x = clamp(state.enemy.mesh.position.x, -max, max);
  state.enemy.mesh.position.z = clamp(state.enemy.mesh.position.z, -max, max);

  // Face the player
  const face = new THREE.Vector3(
    state.player.position.x - state.enemy.mesh.position.x,
    0,
    state.player.position.z - state.enemy.mesh.position.z
  );
  state.enemy.mesh.rotation.y = Math.atan2(face.x, -face.z);

  // Shoot at interval if in LOS
  const t = nowMs();
  if (t - state.enemy.lastShotAt < SETTINGS.enemyShootIntervalMs) return;
  if (dist > SETTINGS.enemyBulletRange) return;

  const { canSee, direction } = enemyLineOfSight(state);
  if (!canSee) return;

  state.enemy.lastShotAt = t;

  state.effects.enemyFlash.position
    .copy(state.enemy.mesh.position)
    .add(new THREE.Vector3(0, 0.7, 0))
    .addScaledVector(direction, 0.8);
  state.effects.enemyFlash.visible = true;
  state.effects.enemyFlashOffAt = t + 55;

  // Enemy hitscan: small aim wobble
  const wobble = new THREE.Vector3(
    (Math.random() - 0.5) * 0.07,
    0,
    (Math.random() - 0.5) * 0.07
  );
  const shotDir = direction.clone().add(wobble).normalize();

  const enemyOrigin = state.enemy.mesh.position.clone().add(new THREE.Vector3(0, 0.7, 0));
  spawnBullet(state, {
    owner: "enemy",
    origin: enemyOrigin.addScaledVector(shotDir, 0.9),
    direction: shotDir,
    speed: SETTINGS.enemyBulletSpeed,
    range: SETTINGS.enemyBulletRange,
    color: 0xb0fffe,
    damage: 9,
  });
}

function syncHud(state) {
  UI.playerHp.textContent = String(state.player.hp);
  UI.enemyHp.textContent = String(state.enemy.hp);
  UI.score.textContent = String(state.game.score);
}

function showGameOver(state) {
  setOverlayVisible(true);
  UI.overlay.querySelector("#title").textContent = "Game Over";
  UI.overlay.querySelector("#desc").textContent = state.game.message;
  UI.startBtn.textContent = "Restart";
}

function resetGame(state) {
  state.player.position.set(0, 0, 12);
  state.player.yaw = 0;
  state.player.pitch = 0;
  state.player.hp = 100;
  state.player.lastShotAt = -99999;

  state.enemy.mesh.position.set(0, 1.0, -10);
  state.enemy.hp = 100;
  state.enemy.lastShotAt = -99999;

  state.game.score = 0;
  state.game.over = false;
  state.game.message = "";

  // Clear bullets
  for (const p of state.projectiles) {
    removeProjectile(state, p);
  }
  state.projectiles.length = 0;

  // Restore overlay text
  UI.overlay.querySelector("#title").textContent = "FPS Arena";
  UI.overlay.querySelector("#desc").textContent =
    "Use the mouse to aim. Arrow keys to move (←/→ strafe). Space to shoot.";
  UI.startBtn.textContent = "Start";

  syncHud(state);
}

function makeCoverMeshes(arenaGroup) {
  // Cover meshes are the pillars.
  return arenaGroup.children.filter((o) => o.isMesh && o.geometry?.type === "CylinderGeometry");
}

function main() {
  const renderer = makeRenderer();
  const scene = makeScene();
  const camera = makeCamera();

  const arena = makeArena(scene);
  const enemyMesh = makeEnemy(scene);

  const muzzleFlash = makeMuzzleFlash(scene);
  const enemyFlash = makeMuzzleFlash(scene);
  enemyFlash.material = enemyFlash.material.clone();
  enemyFlash.material.color = new THREE.Color(0xb0fffe);

  const state = {
    renderer,
    scene,
    camera,
    input: {
      ArrowUp: false,
      ArrowDown: false,
      ArrowLeft: false,
      ArrowRight: false,
      Space: false,
    },
    player: {
      position: new THREE.Vector3(0, 0, 10),
      yaw: Math.PI,
      pitch: 0,
      hp: 100,
      lastShotAt: -99999,
    },
    enemy: {
      mesh: enemyMesh,
      hp: 100,
      lastShotAt: -99999,
    },
    world: {
      coverMeshes: makeCoverMeshes(arena.group),
    },
    effects: {
      muzzleFlash,
      muzzleFlashOffAt: 0,
      enemyFlash,
      enemyFlashOffAt: 0,
    },
    projectiles: [],
    game: {
      score: 0,
      over: false,
      message: "",
      started: false,
    },
  };

  syncHud(state);
  updateCamera(camera, state.player);

  function onResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }
  window.addEventListener("resize", onResize);

  function setKey(e, down) {
    if (e.code === "Space") {
      state.input.Space = down;
      return;
    }
    if (e.code in state.input) {
      state.input[e.code] = down;
    }
  }

  window.addEventListener("keydown", (e) => {
    // Prevent page scrolling with arrow keys / space.
    if (
      e.code === "ArrowUp" ||
      e.code === "ArrowDown" ||
      e.code === "ArrowLeft" ||
      e.code === "ArrowRight" ||
      e.code === "Space"
    ) {
      e.preventDefault();
    }

    if (e.code === "KeyR") {
      resetGame(state);
      setOverlayVisible(false);
      state.game.started = true;
      return;
    }

    setKey(e, true);
  });

  window.addEventListener("keyup", (e) => setKey(e, false));

  function requestAimLock() {
    // Pointer Lock enables mouse-look.
    const el = renderer.domElement;
    if (document.pointerLockElement !== el) {
      el.requestPointerLock?.();
    }
  }

  document.addEventListener("pointerlockchange", () => {
    // If user presses Esc, pointer lock ends.
    const locked = document.pointerLockElement === renderer.domElement;
    if (!locked && state.game.started && !state.game.over) {
      setOverlayVisible(true);
      UI.overlay.querySelector("#title").textContent = "Paused";
      UI.overlay.querySelector("#desc").textContent =
        "Click Start to resume and re-lock the mouse.";
      UI.startBtn.textContent = "Start";
    }
  });

  document.addEventListener("mousemove", (e) => {
    if (document.pointerLockElement !== renderer.domElement) return;
    // Mouse right = look right; mouse up = look up.
    state.player.yaw -= e.movementX * SETTINGS.mouseSensitivity;
    state.player.pitch -= e.movementY * SETTINGS.mouseSensitivity;
    state.player.pitch = clamp(state.player.pitch, -SETTINGS.maxPitch, SETTINGS.maxPitch);
  });

  UI.startBtn.addEventListener("click", () => {
    if (state.game.over) {
      resetGame(state);
    }
    setOverlayVisible(false);
    state.game.started = true;
    // Make sure player isn't stuck with a "pressed" space.
    state.input.Space = false;
    requestAimLock();
  });

  // Click anywhere to focus
  window.addEventListener("pointerdown", () => {
    if (!state.game.started) return;
    requestAimLock();
  });

  // Disable right-click menu on the canvas
  renderer.domElement.addEventListener("contextmenu", (e) => {
    e.preventDefault();
  });

  // Right-click to shoot
  renderer.domElement.addEventListener("mousedown", (e) => {
    if (!state.game.started || state.game.over) return;
    // 2 = right button
    if (e.button === 2) {
      e.preventDefault();
      tryPlayerShoot(state);
    }
  });

  let lastT = performance.now();

  function frame() {
    const t = performance.now();
    const dt = Math.min(0.033, (t - lastT) / 1000);
    lastT = t;

    if (state.game.started) {
      integratePlayerMovement(state.player, state.input, dt);
      if (state.input.Space) {
        tryPlayerShoot(state);
      }
      stepEnemyAI(state, dt);
      updateProjectiles(state, dt);
      updateCamera(camera, state.player);
    }

    if (state.effects.muzzleFlash.visible && t > state.effects.muzzleFlashOffAt) {
      state.effects.muzzleFlash.visible = false;
    }
    if (state.effects.enemyFlash.visible && t > state.effects.enemyFlashOffAt) {
      state.effects.enemyFlash.visible = false;
    }

    renderer.render(scene, camera);
    requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);

  resetGame(state);
  setOverlayVisible(true);
}

main();
