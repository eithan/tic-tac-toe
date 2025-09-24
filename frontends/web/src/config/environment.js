// Environment configuration for different deployment stages
const getApiUrl = () => {
  const environment = import.meta.env.MODE;
  
  switch (environment) {
    case 'development':
      return import.meta.env.VITE_API_URL || 'http://localhost:8000';
    case 'production':
      return import.meta.env.VITE_API_URL || 'https://your-backend-url.run.app';
    default:
      return 'http://localhost:8000';
  }
};

export const config = {
  API_BASE_URL: getApiUrl(),
  ENVIRONMENT: import.meta.env.MODE,
  IS_PRODUCTION: import.meta.env.MODE === 'production',
  IS_DEVELOPMENT: import.meta.env.MODE === 'development'
};
