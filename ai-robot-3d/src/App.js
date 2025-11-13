import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import NeuralNetwork3D from './components/NeuralNetwork3D';
import RobotAssistant from './components/RobotAssistant';
import FloatingCard from './components/FloatingCard';
import MatrixRain from './components/MatrixRain';
import TerminalSection from './components/TerminalSection';
import './index.css';

function App() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e) => {
    setMousePosition({ x: e.clientX, y: e.clientY });
  };

  return (
    <div 
      className="relative min-h-screen bg-gradient-to-br from-black via-gray-900 to-black overflow-hidden"
      onMouseMove={handleMouseMove}
    >
      {/* Matrix Rain Background */}
      <MatrixRain />

      {/* Scan line effect */}
      <div className="fixed top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-50 scan-line pointer-events-none z-10"></div>

      {/* 3D Canvas */}
      <div className="fixed top-0 left-0 w-full h-full z-0">
        <Canvas>
          <PerspectiveCamera makeDefault position={[0, 0, 10]} />
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} intensity={1} color="#00f0ff" />
          <pointLight position={[-10, -10, -10]} intensity={0.5} color="#a855f7" />
          
          <Suspense fallback={null}>
            <NeuralNetwork3D />
            <RobotAssistant mousePosition={mousePosition} />
          </Suspense>
          
          <OrbitControls 
            enableZoom={false} 
            enablePan={false}
            autoRotate
            autoRotateSpeed={0.5}
          />
        </Canvas>
      </div>

      {/* Content Overlay */}
      <div className="relative z-20 min-h-screen">
        {/* Hero Section */}
        <section className="min-h-screen flex flex-col items-center justify-center px-6 text-center">
          <div className="animate-float">
            <h1 className="text-7xl md:text-9xl font-black mb-6 gradient-text font-['Orbitron'] tracking-wider">
              AI NEXUS
            </h1>
            <p className="text-xl md:text-3xl text-gray-300 mb-8 font-light tracking-wide">
              Next-Generation Artificial Intelligence Platform
            </p>
            <div className="flex gap-4 justify-center flex-wrap">
              <button className="glass-effect px-8 py-4 rounded-full text-white font-semibold hover:scale-110 transition-transform neon-border">
                Launch System
              </button>
              <button className="glass-effect px-8 py-4 rounded-full text-white font-semibold hover:scale-110 transition-transform border border-white/20">
                Learn More
              </button>
            </div>
          </div>

          {/* Scroll indicator */}
          <div className="absolute bottom-10 animate-bounce">
            <div className="w-6 h-10 border-2 border-cyan-500 rounded-full flex items-start justify-center p-2">
              <div className="w-1 h-3 bg-cyan-500 rounded-full animate-pulse"></div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="min-h-screen py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-5xl md:text-6xl font-bold text-center mb-16 gradient-text font-['Orbitron']">
              CORE CAPABILITIES
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <FloatingCard
                icon="🧠"
                title="Neural Processing"
                description="Advanced deep learning algorithms powered by quantum neural networks for unprecedented computational intelligence."
                delay={0}
              />
              <FloatingCard
                icon="🤖"
                title="Autonomous Systems"
                description="Self-learning robotic frameworks that adapt and evolve in real-time to complex environmental challenges."
                delay={0.2}
              />
              <FloatingCard
                icon="⚡"
                title="Quantum Computing"
                description="Harness the power of quantum mechanics for exponentially faster processing and problem-solving capabilities."
                delay={0.4}
              />
              <FloatingCard
                icon="🔮"
                title="Predictive Analytics"
                description="Machine learning models that forecast trends and patterns with unprecedented accuracy and reliability."
                delay={0.6}
              />
              <FloatingCard
                icon="🌐"
                title="Global Network"
                description="Distributed AI infrastructure spanning continents, ensuring low-latency access and maximum uptime."
                delay={0.8}
              />
              <FloatingCard
                icon="🔒"
                title="Secure Architecture"
                description="Military-grade encryption and blockchain-verified transactions protect your data at every layer."
                delay={1}
              />
            </div>
          </div>
        </section>

        {/* Terminal Section */}
        <section className="min-h-screen py-20 px-6 flex items-center">
          <div className="max-w-4xl mx-auto w-full">
            <h2 className="text-5xl md:text-6xl font-bold text-center mb-16 gradient-text font-['Orbitron']">
              SYSTEM STATUS
            </h2>
            <TerminalSection />
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              {[
                { value: '99.9%', label: 'Uptime' },
                { value: '10M+', label: 'Operations/sec' },
                { value: '256', label: 'Quantum Qubits' },
                { value: '<1ms', label: 'Response Time' },
              ].map((stat, i) => (
                <div key={i} className="glass-effect rounded-2xl p-8 text-center hover:scale-105 transition-transform">
                  <div className="text-5xl font-bold gradient-text mb-2 font-['Orbitron']">
                    {stat.value}
                  </div>
                  <div className="text-gray-400 text-lg">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-12 px-6 border-t border-white/10">
          <div className="max-w-7xl mx-auto text-center">
            <p className="text-gray-400 mb-4">
              © 2025 AI NEXUS. Powered by Quantum Neural Networks.
            </p>
            <div className="flex gap-6 justify-center text-sm text-gray-500">
              <button className="hover:text-cyan-500 transition-colors">Privacy</button>
              <button className="hover:text-cyan-500 transition-colors">Terms</button>
              <button className="hover:text-cyan-500 transition-colors">Documentation</button>
              <button className="hover:text-cyan-500 transition-colors">Contact</button>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
