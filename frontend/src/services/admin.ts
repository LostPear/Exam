import { api } from './api'
import type { User } from '../types/auth'

export async function listUsersApi(): Promise<User[]> {
  const { data } = await api.get('/admin/users/')
  return data
}

export async function toggleAdminApi(userId: number, isAdmin: boolean): Promise<void> {
  await api.post(`/admin/users/${userId}/toggle_admin/`, { is_admin: isAdmin })
}
