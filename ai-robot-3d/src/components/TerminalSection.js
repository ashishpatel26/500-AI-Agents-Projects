import React, { useState, useEffect } from 'react';

function TerminalSection() {
  const [displayedText, setDisplayedText] = useState('');
  const [currentLine, setCurrentLine] = useState(0);
  
  const lines = React.useMemo(() => [
    '> Initializing AI Neural Network...',
    '> Loading quantum processors... [OK]',
    '> Establishing neural connections... [OK]',
    '> Calibrating robotic systems... [OK]',
    '> System ready. Welcome to the future.',
  ], []);

  useEffect(() => {
    if (currentLine < lines.length) {
      const line = lines[currentLine];
      let charIndex = 0;

      const typeInterval = setInterval(() => {
        if (charIndex <= line.length) {
          setDisplayedText(prev => {
            const allPreviousLines = lines.slice(0, currentLine).join('\n');
            const currentTyping = line.slice(0, charIndex);
            return allPreviousLines + (allPreviousLines ? '\n' : '') + currentTyping;
          });
          charIndex++;
        } else {
          clearInterval(typeInterval);
          setTimeout(() => {
            setCurrentLine(prev => prev + 1);
          }, 500);
        }
      }, 50);

      return () => clearInterval(typeInterval);
    }
  }, [currentLine, lines]);

  return (
    <div className="glass-effect rounded-2xl p-8 font-mono text-sm">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-3 h-3 rounded-full bg-red-500"></div>
        <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
        <div className="w-3 h-3 rounded-full bg-green-500"></div>
        <span className="ml-4 text-gray-400">terminal.ai</span>
      </div>
      
      <div className="bg-black/50 rounded-lg p-6 min-h-[200px]">
        <pre className="text-green-400 whitespace-pre-wrap">
          {displayedText}
          <span className="animate-pulse">_</span>
        </pre>
      </div>
    </div>
  );
}

export default TerminalSection;
