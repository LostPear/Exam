import apiClient from './client'

// 获取用户列表
export const getUsers = (params) => {
  return apiClient.get('/users/', { params })
}

// 获取单个用户
export const getUser = (id) => {
  return apiClient.get(`/users/${id}/`)
}

// 更新用户
export const updateUser = (id, data) => {
  return apiClient.put(`/users/${id}/`, data)
}

// 删除用户
export const deleteUser = (id) => {
  return apiClient.delete(`/users/${id}/`)
}

// 获取用户统计信息
export const getUserStats = (id) => {
  return apiClient.get(`/users/${id}/stats/`)
}
