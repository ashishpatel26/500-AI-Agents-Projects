import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function RobotAssistant({ mousePosition }) {
  const groupRef = useRef();
  const headRef = useRef();
  const eyeLeftRef = useRef();
  const eyeRightRef = useRef();

  useFrame((state) => {
    if (groupRef.current && mousePosition) {
      // Smooth follow mouse
      const targetX = (mousePosition.x / window.innerWidth) * 2 - 1;
      const targetY = -(mousePosition.y / window.innerHeight) * 2 + 1;
      
      groupRef.current.rotation.y = THREE.MathUtils.lerp(
        groupRef.current.rotation.y,
        targetX * 0.5,
        0.05
      );
      
      groupRef.current.rotation.x = THREE.MathUtils.lerp(
        groupRef.current.rotation.x,
        targetY * 0.3,
        0.05
      );
    }

    // Floating animation
    if (groupRef.current) {
      groupRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.8) * 0.3;
    }

    // Eye blink animation
    if (eyeLeftRef.current && eyeRightRef.current) {
      const blink = Math.sin(state.clock.elapsedTime * 3) > 0.95 ? 0.1 : 1;
      eyeLeftRef.current.scale.y = blink;
      eyeRightRef.current.scale.y = blink;
    }

    // Head bob
    if (headRef.current) {
      headRef.current.rotation.z = Math.sin(state.clock.elapsedTime * 2) * 0.05;
    }
  });

  return (
    <group ref={groupRef} position={[4, 0, 0]}>
      {/* Head */}
      <group ref={headRef}>
        <mesh>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial
            color="#1a1a2e"
            metalness={0.8}
            roughness={0.2}
            emissive="#00f0ff"
            emissiveIntensity={0.2}
          />
        </mesh>

        {/* Antenna */}
        <mesh position={[0, 0.7, 0]}>
          <cylinderGeometry args={[0.03, 0.03, 0.4, 8]} />
          <meshStandardMaterial
            color="#00f0ff"
            emissive="#00f0ff"
            emissiveIntensity={1}
          />
        </mesh>
        <mesh position={[0, 0.95, 0]}>
          <sphereGeometry args={[0.08, 16, 16]} />
          <meshStandardMaterial
            color="#00f0ff"
            emissive="#00f0ff"
            emissiveIntensity={2}
            toneMapped={false}
          />
        </mesh>

        {/* Eyes */}
        <mesh ref={eyeLeftRef} position={[-0.25, 0.15, 0.51]}>
          <boxGeometry args={[0.15, 0.15, 0.02]} />
          <meshStandardMaterial
            color="#00f0ff"
            emissive="#00f0ff"
            emissiveIntensity={3}
            toneMapped={false}
          />
        </mesh>
        <mesh ref={eyeRightRef} position={[0.25, 0.15, 0.51]}>
          <boxGeometry args={[0.15, 0.15, 0.02]} />
          <meshStandardMaterial
            color="#00f0ff"
            emissive="#00f0ff"
            emissiveIntensity={3}
            toneMapped={false}
          />
        </mesh>

        {/* Mouth */}
        <mesh position={[0, -0.2, 0.51]}>
          <boxGeometry args={[0.4, 0.05, 0.02]} />
          <meshStandardMaterial
            color="#a855f7"
            emissive="#a855f7"
            emissiveIntensity={2}
          />
        </mesh>
      </group>

      {/* Body */}
      <mesh position={[0, -1.2, 0]}>
        <boxGeometry args={[1.2, 1.5, 0.8]} />
        <meshStandardMaterial
          color="#1a1a2e"
          metalness={0.8}
          roughness={0.2}
          emissive="#a855f7"
          emissiveIntensity={0.1}
        />
      </mesh>

      {/* Chest panel */}
      <mesh position={[0, -1.2, 0.41]}>
        <boxGeometry args={[0.6, 0.8, 0.05]} />
        <meshStandardMaterial
          color="#00f0ff"
          emissive="#00f0ff"
          emissiveIntensity={0.5}
          transparent
          opacity={0.8}
        />
      </mesh>

      {/* Arms */}
      <mesh position={[-0.8, -1.2, 0]} rotation={[0, 0, 0.3]}>
        <cylinderGeometry args={[0.15, 0.15, 1.2, 8]} />
        <meshStandardMaterial
          color="#1a1a2e"
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>
      <mesh position={[0.8, -1.2, 0]} rotation={[0, 0, -0.3]}>
        <cylinderGeometry args={[0.15, 0.15, 1.2, 8]} />
        <meshStandardMaterial
          color="#1a1a2e"
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>

      {/* Holographic rings */}
      <HolographicRings />
    </group>
  );
}

function HolographicRings() {
  const ringsRef = useRef();

  useFrame((state) => {
    if (ringsRef.current) {
      ringsRef.current.rotation.y = state.clock.elapsedTime * 2;
    }
  });

  return (
    <group ref={ringsRef}>
      {[1, 1.5, 2].map((radius, i) => (
        <mesh key={i} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[radius, 0.02, 16, 100]} />
          <meshBasicMaterial
            color="#00f0ff"
            transparent
            opacity={0.3 - i * 0.1}
          />
        </mesh>
      ))}
    </group>
  );
}

export default RobotAssistant;
