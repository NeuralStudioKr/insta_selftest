/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Railway 배포를 위한 설정
  output: 'standalone',
  // API 프록시 (개발 환경용, 프로덕션에서는 직접 API URL 사용)
  async rewrites() {
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: process.env.NEXT_PUBLIC_API_URL + '/api/:path*',
        },
      ];
    }
    return [];
  },
};

module.exports = nextConfig;
