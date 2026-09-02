/**
 * ModelSelector component - displays available models and their metrics
 */

import './ModelSelector.css'

export function ModelSelector({
  models = [],
  selectedModel = '',
  loading = false,
  onSelect = () => {},
}) {
  const selectedModelStats = models.find((model) => model.name === selectedModel)

  return (
    <div className="selector-row">
      <label className="selector-label" htmlFor="model-select">
        Model
      </label>
      <select
        id="model-select"
        value={selectedModel}
        onChange={(event) => onSelect(event.target.value)}
        disabled={loading || !models.length}
      >
        {models.map((model) => (
          <option key={model.name} value={model.name}>
            {model.name}
          </option>
        ))}
      </select>
      {selectedModelStats && (
        <div className="model-metrics">
          <span>F1: {selectedModelStats.f1.toFixed(3)}</span>
          <span>Accuracy: {selectedModelStats.accuracy.toFixed(3)}</span>
        </div>
      )}
    </div>
  )
}
