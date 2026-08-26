import { useState, useEffect } from "react";

interface RiotPlayer {
  summonerName: string;
  championName: string;
  team: "chaos" | "order";
  position: "TOP" | "JUNGLE" | "MIDDLE" | "BOTTOM" | "UTILITY";
}

interface LiveGameData {
  activePlayer: {
    riotId: string;
    level: number;
  };
  allPlayers: RiotPlayer[];
}
export function useRiotPolling() {
  const [gameData, setGameData] = useState<LiveGameData | null>(null);

  useEffect(() => {
    const poll = async () => {
      try {
        const res = await fetch("/api/riot");
        if (!res.ok) return setGameData(null);

        // Cast raw json to your type
        const data: LiveGameData = await res.json();
        setGameData(data);
      } catch {
        setGameData(null);
      }
    };

    const interval = setInterval(poll, 2000);
    return () => clearInterval(interval);
  }, []);
  return { gameData: gameData, isLive: !!gameData };
}
