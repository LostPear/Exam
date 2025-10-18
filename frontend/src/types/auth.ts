export interface User {
  id: number
  username: string
  email: string
  is_admin?: boolean
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
}

export interface UpdateProfileRequest {
  email?: string
  username?: string
  password?: string
}
