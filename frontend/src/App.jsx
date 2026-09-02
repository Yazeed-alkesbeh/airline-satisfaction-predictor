/**
 * Main App component
 * Orchestrates the prediction form with models and results display
 */

import { useEffect, useState } from 'react'
import './App.css'

import { ModelSelector } from './components/ModelSelector'
import { PassengerForm } from './components/PassengerForm'
import { ResultsCard } from './components/ResultsCard'

import { 
  fetchModels, 
  makePrediction,
  askKimi,
  formatValidationErrors 
} from './services/api'
import {
  INITIAL_FORM_DATA,
  INITIAL_FEEDBACK_DATA,
} from './services/constants'

const ANALYSIS_CACHE_KEY = 'airline-ai-analysis-cache-v1'

function App() {
  const [models, setModels] = useState([])
  const [selectedModel, setSelectedModel] = useState('')
  const [formData, setFormData] = useState(INITIAL_FORM_DATA)
  const [feedback, setFeedback] = useState(INITIAL_FEEDBACK_DATA)
  const [result, setResult] = useState(null)
  const [loadingModels, setLoadingModels] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [apiError, setApiError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [aiAnswer, setAiAnswer] = useState('')
  const [customPrompt, setCustomPrompt] = useState('Analyze the passenger feedback and explain the main complaint, the likely root cause, and the most important service improvement area based on the prediction result.')
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState('')
  const [aiCache, setAiCache] = useState(() => {
    try {
      const cached = localStorage.getItem(ANALYSIS_CACHE_KEY)
      return cached ? JSON.parse(cached) : {}
    } catch {
      return {}
    }
  })

  useEffect(() => {
    try {
      localStorage.setItem(ANALYSIS_CACHE_KEY, JSON.stringify(aiCache))
    } catch {
      // Ignore storage failures and continue without cached data.
    }
  }, [aiCache])

  // Load models on component mount
  useEffect(() => {
    async function loadModels() {
      try {
        const data = await fetchModels()
        setModels(data.models || [])
        setSelectedModel(data.best_model || '')
      } catch (error) {
        setApiError('Unable to load model list from the backend.')
      } finally {
        setLoadingModels(false)
      }
    }

    loadModels()
  }, [])

  const handleFormChange = (fieldName, value) => {
    setFormData((previous) => ({
      ...previous,
      [fieldName]: value,
    }))

    // Clear field error when user modifies field
    if (fieldErrors[fieldName]) {
      setFieldErrors((previous) => ({
        ...previous,
        [fieldName]: undefined,
      }))
    }
  }

  const handleFeedbackChange = (fieldName, value) => {
    setFeedback((previous) => ({
      ...previous,
      [fieldName]: value,
    }))
  }

  const handleRangeChange = (fieldName, value) => {
    handleFormChange(fieldName, value)
  }

  const handleSubmit = async () => {
    setSubmitting(true)
    setApiError('')
    setFieldErrors({})

    try {
      const payload = {
        ...formData,
        model_name: selectedModel || undefined,
        save_for_improvement: feedback.consent_to_use_data,
        metadata: {
          passenger_name: feedback.passenger_name,
          airline_name: feedback.airline_name,
          destination: feedback.destination,
          travel_reason: feedback.travel_reason,
          booking_channel: feedback.booking_channel,
          overall_service_rating: feedback.overall_service_rating,
          comment: feedback.comment,
        },
      }

      const result = await makePrediction(payload)
      setResult(result)
      setAiAnswer('')
      setAiError('')
    } catch (error) {
      if (error.status === 422 && Array.isArray(error.detail)) {
        setFieldErrors(formatValidationErrors(error.detail))
      } else {
        setApiError(error.detail || 'Prediction failed.')
      }
    } finally {
      setSubmitting(false)
    }
  }

  const buildFullPassengerSummary = () => {
    const serviceRatings = Object.entries(formData)
      .filter(([key, value]) => {
        if (key === 'model_name' || key === 'save_for_improvement') return false
        return value !== undefined && value !== null && value !== ''
      })
      .map(([key, value]) => `${key}: ${value}`)
      .join('\n')

    const extraDetails = [
      `Passenger name: ${feedback.passenger_name || 'Not provided'}`,
      `Airline name: ${feedback.airline_name || 'Not provided'}`,
      `Destination: ${feedback.destination || 'Not provided'}`,
      `Travel reason: ${feedback.travel_reason || 'Not provided'}`,
      `Booking channel: ${feedback.booking_channel || 'Not provided'}`,
      `Overall service rating: ${feedback.overall_service_rating || 'Not provided'}`,
      `Additional comment: ${feedback.comment || 'No additional comment provided'}`,
      `Consent to use data: ${feedback.consent_to_use_data ? 'Yes' : 'No'}`,
    ].join('\n')

    const predictionDetails = result
      ? `\n\nPrediction result:\nPrediction: ${result.prediction}\nProbability: ${result.probability}\nModel used: ${result.model_used || selectedModel || 'N/A'}`
      : '\n\nPrediction result: Not available yet. Please predict satisfaction first.'

    return `Passenger information and trip details:\n${serviceRatings}\n\nFeedback details:\n${extraDetails}${predictionDetails}`
  }

  const getAnalysisCacheKey = () => `${selectedModel || 'no-model'}::${JSON.stringify(result || {})}::${buildFullPassengerSummary()}`

  const handleAiAnalyze = async () => {
    const summary = buildFullPassengerSummary()
    const cacheKey = `${customPrompt || 'default'}::${selectedModel || 'no-model'}::${JSON.stringify(result || {})}::${summary}`

    if (aiCache[cacheKey]) {
      setAiAnswer(aiCache[cacheKey])
    }

    setAiLoading(true)
    setAiError('')

    try {
      const response = await askKimi({
        message: customPrompt ? `${customPrompt}\n\n${summary}` : summary,
        image_url: null,
      })
      setAiAnswer(response.answer)
      setAiCache((previous) => ({
        ...previous,
        [cacheKey]: response.answer,
      }))
    } catch (error) {
      setAiError(error.detail || 'AI analysis failed.')
    } finally {
      setAiLoading(false)
    }
  }


  return (
    <div className="page-shell">
      <div className="header-block">
        <p className="eyebrow">Airline passenger satisfaction</p>
        <h1>Prediction form</h1>
      </div>

      <ModelSelector
        models={models}
        selectedModel={selectedModel}
        loading={loadingModels}
        onSelect={setSelectedModel}
      />

      <PassengerForm
        formData={formData}
        feedback={feedback}
        fieldErrors={fieldErrors}
        apiError={apiError}
        submitting={submitting}
        aiAnswer={aiAnswer}
        aiLoading={aiLoading}
        aiError={aiError}
        customPrompt={customPrompt}
        result={result}
        onFormChange={handleFormChange}
        onFeedbackChange={handleFeedbackChange}
        onRangeChange={handleRangeChange}
        onSubmit={handleSubmit}
        onAiAnalyze={handleAiAnalyze}
        onCustomPromptChange={setCustomPrompt}
      />

      <ResultsCard result={result} />
    </div>
  )
}

export default App
