import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  // Disable optimization for static export
  reactStrictMode: true,
};

export default nextConfig;
