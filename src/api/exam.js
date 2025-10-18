import apiClient from './client'

// 创建考试
export const createExam = (data) => {
  return apiClient.post('/exams/', data)
}

// 获取考试详情
export const getExam = (id) => {
  return apiClient.get(`/exams/${id}/`)
}

// 提交考试答案
export const submitExam = (id, answers) => {
  return apiClient.post(`/exams/${id}/submit/`, { answers })
}

// 获取考试结果
export const getExamResult = (id) => {
  return apiClient.get(`/exams/${id}/result/`)
}

// 获取用户考试历史
export const getExamHistory = (params) => {
  return apiClient.get('/exams/history/', { params })
}
