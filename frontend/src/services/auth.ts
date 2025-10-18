import { api } from './api'
import type { LoginRequest, RegisterRequest, User, UpdateProfileRequest } from '../types/auth'

export async function loginApi(payload: LoginRequest): Promise<{ token?: string; user: User }> {
  const { data } = await api.post('/auth/login/', payload)
  return data
}

export async function registerApi(payload: RegisterRequest): Promise<void> {
  await api.post('/auth/register/', payload)
}

export async function meApi(): Promise<User> {
  const { data } = await api.get('/auth/me/')
  return data
}

export async function logoutApi(): Promise<void> {
  await api.post('/auth/logout/')
}

export async function updateProfileApi(payload: UpdateProfileRequest): Promise<User> {
  const { data } = await api.put('/auth/me/', payload)
  return data
}
