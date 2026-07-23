"use client";

import { useEffect, useRef } from "react";

export default function ParticleOrb() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = 300);
    let height = (canvas.height = 300);

    const particles: {
      x: number;
      y: number;
      z: number;
      radius: number;
      color: string;
      angle: number;
      speed: number;
    }[] = [];

    const numParticles = 180;
    for (let i = 0; i < numParticles; i++) {
      particles.push({
        x: (Math.random() - 0.5) * 180,
        y: (Math.random() - 0.5) * 180,
        z: (Math.random() - 0.5) * 180,
        radius: Math.random() * 2 + 1,
        color: i % 2 === 0 ? "rgba(99, 102, 241, " : "rgba(16, 185, 129, ",
        angle: Math.random() * Math.PI * 2,
        speed: 0.008 + Math.random() * 0.005,
      });
    }

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      particles.forEach((p) => {
        p.angle += p.speed;
        const cos = Math.cos(p.angle);
        const sin = Math.sin(p.angle);

        const rx = p.x * cos - p.z * sin;
        const rz = p.z * cos + p.x * sin;

        const scale = 200 / (200 + rz);
        const projX = width / 2 + rx * scale;
        const projY = height / 2 + p.y * scale;

        const alpha = Math.max(0.2, (rz + 100) / 200);

        ctx.beginPath();
        ctx.arc(projX, projY, p.radius * scale, 0, Math.PI * 2);
        ctx.fillStyle = `${p.color}${alpha})`;
        ctx.fill();
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  return (
    <div className="relative flex items-center justify-center">
      <div className="absolute w-48 h-48 bg-indigo-600/20 rounded-full blur-3xl animate-pulse" />
      <canvas ref={canvasRef} className="relative z-10 w-[300px] h-[300px]" />
    </div>
  );
}