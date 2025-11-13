import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';

function NeuralNetwork3D() {
  const groupRef = useRef();
  const particlesRef = useRef();
  const linesRef = useRef();

  // Create neural network nodes
  const nodes = useMemo(() => {
    const temp = [];
    const layers = 5;
    const nodesPerLayer = 8;
    
    for (let layer = 0; layer < layers; layer++) {
      for (let i = 0; i < nodesPerLayer; i++) {
        const angle = (i / nodesPerLayer) * Math.PI * 2;
        const radius = 3 + Math.sin(layer * 0.5) * 0.5;
        temp.push({
          position: [
            Math.cos(angle) * radius,
            (layer - layers / 2) * 1.5,
            Math.sin(angle) * radius
          ],
          layer,
          index: i
        });
      }
    }
    return temp;
  }, []);

  // Create connections between nodes
  const connections = useMemo(() => {
    const temp = [];
    nodes.forEach((node, i) => {
      nodes.forEach((otherNode, j) => {
        if (i < j && Math.abs(node.layer - otherNode.layer) === 1) {
          if (Math.random() > 0.3) {
            temp.push([node.position, otherNode.position]);
          }
        }
      });
    });
    return temp;
  }, [nodes]);

  // Animate the neural network
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.15;
      groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.1;
    }

    // Animate particles
    if (particlesRef.current) {
      particlesRef.current.children.forEach((particle, i) => {
        const time = state.clock.elapsedTime;
        particle.scale.setScalar(1 + Math.sin(time * 2 + i) * 0.3);
      });
    }
  });

  return (
    <group ref={groupRef}>
      {/* Neural nodes */}
      <group ref={particlesRef}>
        {nodes.map((node, i) => (
          <mesh key={i} position={node.position}>
            <sphereGeometry args={[0.08, 16, 16]} />
            <meshStandardMaterial
              color="#00f0ff"
              emissive="#00f0ff"
              emissiveIntensity={2}
              toneMapped={false}
            />
            {/* Glow effect */}
            <mesh scale={1.5}>
              <sphereGeometry args={[0.08, 16, 16]} />
              <meshBasicMaterial
                color="#00f0ff"
                transparent
                opacity={0.3}
              />
            </mesh>
          </mesh>
        ))}
      </group>

      {/* Connections */}
      <group ref={linesRef}>
        {connections.map((connection, i) => {
          return (
            <line key={i}>
              <bufferGeometry>
                <bufferAttribute
                  attach="attributes-position"
                  count={2}
                  array={new Float32Array([...connection[0], ...connection[1]])}
                  itemSize={3}
                />
              </bufferGeometry>
              <lineBasicMaterial
                color="#a855f7"
                transparent
                opacity={0.3}
                linewidth={1}
              />
            </line>
          );
        })}
      </group>

      {/* Ambient particles */}
      <ParticleField />
    </group>
  );
}

function ParticleField() {
  const particlesRef = useRef();
  
  const particles = useMemo(() => {
    const temp = [];
    for (let i = 0; i < 200; i++) {
      temp.push({
        position: [
          (Math.random() - 0.5) * 20,
          (Math.random() - 0.5) * 20,
          (Math.random() - 0.5) * 20
        ],
        speed: Math.random() * 0.5 + 0.2
      });
    }
    return temp;
  }, []);

  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.children.forEach((particle, i) => {
        particle.position.y += Math.sin(state.clock.elapsedTime + i) * 0.01;
        particle.position.x += Math.cos(state.clock.elapsedTime * 0.5 + i) * 0.005;
      });
    }
  });

  return (
    <group ref={particlesRef}>
      {particles.map((particle, i) => (
        <mesh key={i} position={particle.position}>
          <sphereGeometry args={[0.02, 8, 8]} />
          <meshBasicMaterial
            color={i % 3 === 0 ? "#00f0ff" : i % 3 === 1 ? "#a855f7" : "#ec4899"}
            transparent
            opacity={0.6}
          />
        </mesh>
      ))}
    </group>
  );
}

export default NeuralNetwork3D;
