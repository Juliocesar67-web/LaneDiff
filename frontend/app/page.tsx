"use client";
import { useRiotPolling } from "@/hooks/useRiotPolling";
import Image from "next/image";
import { useState, useEffect } from "react";

export default function Home() {
  const { gameData, isLive } = useRiotPolling();
  useEffect(() => {
    console.log(gameData, isLive);
  }, [isLive]);
  return (
    <div className="bg-[#2F184B] h-screen">
      <h1>Hello world</h1>
    </div>
  );
}
