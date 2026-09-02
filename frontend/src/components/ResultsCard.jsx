/**
 * ResultsCard component - displays prediction results
 */

import './ResultsCard.css'

export function ResultsCard({ result = null }) {
  if (!result) {
    return null
  }

  const isSatisfied = result.prediction === 'satisfied'
  const confidencePercentage = Math.round(result.probability * 100)

  return (
    <aside className={`result-card ${isSatisfied ? 'satisfied' : 'neutral'}`}>
      <p className="result-label">Prediction</p>
      <h3>{isSatisfied ? 'Satisfied' : 'Neutral or dissatisfied'}</h3>
      <div className="probability-box">
        <span>Confidence</span>
        <strong>{confidencePercentage}%</strong>
      </div>
      <p className="result-meta">Model used: {result.model_used}</p>
    </aside>
  )
}
