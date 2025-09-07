import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  try {

    const response = await fetch(`${process.env.BACKEND_API_URL}/meta/last-update`, {
      headers: {
        Authorization: `Bearer ${process.env.ENDPOINT_API_KEY}`,
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to fetch last update" },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
