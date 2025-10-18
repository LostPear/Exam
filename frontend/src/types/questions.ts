export interface Question {
  id: number
  content: string
  options: string[]
  answer: number
}

export interface ExamPaper {
  id: number
  questions: Question[]
}

export interface PracticeQuestionRequest {
  mode: 'sequential' | 'random'
}

export interface ExamPaperRequest {
  count: number
}

export interface AnswerSubmission {
  question_id: number
  selected_option: number
  paper_id?: number
}
