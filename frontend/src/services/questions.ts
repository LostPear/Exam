import { api } from './api'
import type { Question, ExamPaper, PracticeQuestionRequest, ExamPaperRequest, AnswerSubmission } from '../types/questions'

export async function listQuestionsApi(): Promise<Question[]> {
  const { data } = await api.get('/admin/questions/')
  return data
}

export async function createQuestionApi(payload: { content: string; options: string[]; answer: number }): Promise<void> {
  await api.post('/admin/questions/', payload)
}

export async function updateQuestionApi(id: number, payload: { content?: string; options?: string[]; answer?: number }): Promise<void> {
  await api.put(`/admin/questions/${id}/`, payload)
}

export async function deleteQuestionApi(id: number): Promise<void> {
  await api.delete(`/admin/questions/${id}/`)
}

export async function importQuestionsApi(formData: FormData): Promise<void> {
  await api.post('/admin/questions/import/', formData)
}

export async function getPracticeQuestionApi(params: PracticeQuestionRequest): Promise<Question> {
  const { data } = await api.get('/practice/question/', { params })
  return data
}

export async function submitPracticeAnswerApi(payload: AnswerSubmission): Promise<{ correct: boolean }> {
  const { data } = await api.post('/practice/answer/', payload)
  return data
}

export async function getExamPaperApi(params: ExamPaperRequest): Promise<ExamPaper> {
  const { data } = await api.post('/exam/paper/', params)
  return data
}

export async function submitExamAnswerApi(payload: AnswerSubmission): Promise<void> {
  await api.post('/exam/answer/', payload)
}

export async function finishExamApi(paperId: number): Promise<void> {
  await api.post(`/exam/${paperId}/finish/`)
}
