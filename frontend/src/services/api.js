/**
 * API client for backend communication
 */

import { API_BASE_URL } from './constants'

/**
 * Fetch available models and their metrics
 */
export async function fetchModels() {
  const response = await fetch(`${API_BASE_URL}/api/models`)
  if (!response.ok) {
    throw new Error('Failed to fetch models')
  }
  const data = await response.json()
  return data
}

/**
 * Make a prediction request
 * @param {Object} payload - Prediction request payload
 * @returns {Promise<Object>} Prediction result
 */
export async function makePrediction(payload) {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  const data = await response.json()

  if (!response.ok) {
    const error = new Error('Prediction failed')
    error.status = response.status
    error.detail = data.detail
    throw error
  }

  return data
}

/**
 * Ask the Kimi assistant to analyze a complaint or image URL.
 * @param {Object} payload
 * @returns {Promise<Object>}
 */
export async function askKimi(payload = {}) {
  const response = await fetch(`${API_BASE_URL}/api/assistant`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: payload.message || '',
      image_url: payload.image_url || null,
      max_tokens: payload.max_tokens || 1000,
      temperature: payload.temperature || 0.7,
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    const error = new Error('AI analysis failed')
    error.status = response.status
    error.detail = data.detail || 'AI analysis failed.'
    throw error
  }

  return data
}

/**
 * Format validation errors from API response
 * @param {Array} errorDetail - Error details from API
 * @returns {Object} Formatted field errors
 */
export function formatValidationErrors(errorDetail) {
  const formatted = {}
  
  if (Array.isArray(errorDetail)) {
    errorDetail.forEach((item) => {
      const fieldName = item.loc?.[1]
      if (fieldName) {
        formatted[fieldName] = item.msg
      }
    })
  }
  
  return formatted
}
