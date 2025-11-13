import React, { useEffect, useRef } from 'react';

function FloatingCard({ title, description, delay = 0, icon }) {
  const cardRef = useRef();

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (cardRef.current) {
        const rect = cardRef.current.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        const rotateX = (y / rect.height) * 10;
        const rotateY = (x / rect.width) * 10;
        
        cardRef.current.style.transform = `
          perspective(1000px)
          rotateX(${-rotateX}deg)
          rotateY(${rotateY}deg)
          translateZ(20px)
        `;
      }
    };

    const handleMouseLeave = () => {
      if (cardRef.current) {
        cardRef.current.style.transform = `
          perspective(1000px)
          rotateX(0deg)
          rotateY(0deg)
          translateZ(0px)
        `;
      }
    };

    const card = cardRef.current;
    if (card) {
      card.addEventListener('mousemove', handleMouseMove);
      card.addEventListener('mouseleave', handleMouseLeave);
    }

    return () => {
      if (card) {
        card.removeEventListener('mousemove', handleMouseMove);
        card.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, []);

  return (
    <div
      ref={cardRef}
      className="glass-effect rounded-2xl p-8 transition-all duration-300 hover:scale-105 cursor-pointer"
      style={{
        animationDelay: `${delay}s`,
        transformStyle: 'preserve-3d',
      }}
    >
      <div className="relative z-10">
        {icon && (
          <div className="text-6xl mb-4 gradient-text font-bold">
            {icon}
          </div>
        )}
        <h3 className="text-2xl font-bold mb-4 text-white font-['Orbitron']">
          {title}
        </h3>
        <p className="text-gray-300 leading-relaxed">
          {description}
        </p>
      </div>
      
      {/* Animated border */}
      <div className="absolute inset-0 rounded-2xl overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 opacity-20"></div>
        <div className="absolute inset-[2px] bg-black/40 rounded-2xl"></div>
      </div>

      {/* Glow effect on hover */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-cyan-500/0 via-purple-500/0 to-pink-500/0 hover:from-cyan-500/20 hover:via-purple-500/20 hover:to-pink-500/20 transition-all duration-500"></div>
    </div>
  );
}

export default FloatingCard;
