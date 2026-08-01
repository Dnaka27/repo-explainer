const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export class ApiError extends Error {
  constructor(code, message) {
    super(message)
    this.code = code
  }
}

export async function analyzeRepo(repoUrl) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_url: repoUrl }),
  })

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const error = data?.error ?? { code: 'UNKNOWN_ERROR', message: 'Erro desconhecido.' }
    throw new ApiError(error.code, error.message)
  }

  return data
}
