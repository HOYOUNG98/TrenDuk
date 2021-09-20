module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "https://api.trenduk-go.com/:path*",
      },
    ];
  },
};
