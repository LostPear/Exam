import { defineStore } from 'pinia'
import { loginApi, logoutApi, registerApi, meApi, updateProfileApi } from '../services/auth'
import type { LoginRequest, RegisterRequest, User, UpdateProfileRequest } from '../types/auth'

interface AuthState {
  token: string | null
  currentUser: User | null
  loading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token'),
    currentUser: null,
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(payload: LoginRequest) {
      this.loading = true
      this.error = null
      try {
        const { token, user } = await loginApi(payload)
        this.token = token || null
        this.currentUser = user
        if (token) localStorage.setItem('token', token)
      } catch (e: any) {
        this.error = e?.message || '登录失败'
        throw e
      } finally {
        this.loading = false
      }
    },
    async register(payload: RegisterRequest) {
      this.loading = true
      this.error = null
      try {
        await registerApi(payload)
      } catch (e: any) {
        this.error = e?.message || '注册失败'
        throw e
      } finally {
        this.loading = false
      }
    },
    async fetchMe() {
      try {
        const me = await meApi()
        this.currentUser = me
      } catch (e) {
        // ignore
      }
    },
    async logout() {
      await logoutApi()
      this.token = null
      this.currentUser = null
      localStorage.removeItem('token')
    },
    async updateProfile(payload: UpdateProfileRequest) {
      const user = await updateProfileApi(payload)
      this.currentUser = user
    },
  },
})
