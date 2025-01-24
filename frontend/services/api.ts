import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
});

export const submitReview = async (repository: string, pullRequestNumber: number) => {
  const response = await api.post('/api/review', {
    repository,
    pull_request_number: pullRequestNumber,
  });
  return response.data;
};

export const getReviewStatus = async (taskId: string) => {
  const response = await api.get(`/api/review/${taskId}`);
  return response.data;
};

export const login = async (username: string, password: string) => {
  const response = await api.post('/api/token', {
    username,
    password,
  });
  return response.data;
};

// Add auth interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}); 