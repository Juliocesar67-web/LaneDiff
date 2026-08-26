import { NextResponse } from "next/server";

export async function GET() {
  try {
    // 1. Tell Node.js to allow Riot's self-signed SSL certificate locally
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

    // 2. Perform server-to-server fetch (bypasses browser CORS)
    const res = await fetch(
      "https://127.0.0.1:2999/liveclientdata/allgamedata",
    );

    if (!res.ok) {
      return NextResponse.json({ live: false }, { status: 404 });
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    // League client is closed or not in an active game
    return NextResponse.json({ live: false }, { status: 503 });
  }
}
