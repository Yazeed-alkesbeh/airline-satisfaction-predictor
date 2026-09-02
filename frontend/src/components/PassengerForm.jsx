/**
 * PassengerForm component - main prediction form
 */

import {
  SERVICE_FIELDS,
  GENDER_OPTIONS,
  CUSTOMER_TYPE_OPTIONS,
  TRAVEL_TYPE_OPTIONS,
  CLASS_OPTIONS,
  TRAVEL_REASON_OPTIONS,
  BOOKING_CHANNEL_OPTIONS,
} from '../services/constants'
import './PassengerForm.css'

export function PassengerForm({
  formData = {},
  feedback = {},
  fieldErrors = {},
  apiError = '',
  submitting = false,
  aiAnswer = '',
  aiLoading = false,
  aiError = '',
  customPrompt = '',
  result = null,
  onFormChange = () => {},
  onFeedbackChange = () => {},
  onRangeChange = () => {},
  onSubmit = () => {},
  onAiAnalyze = () => {},
  onCustomPromptChange = () => {},
}) {
  const handleSubmit = (event) => {
    event.preventDefault()
    onSubmit()
  }

  return (
    <form className="form-layout" onSubmit={handleSubmit}>
      {/* Passenger Info Section */}
      <section className="panel">
        <h2>Passenger info</h2>
        <div className="field-grid">
          <label className="field">
            <span>Gender</span>
            <select
              name="Gender"
              value={formData.Gender || ''}
              onChange={(e) => onFormChange('Gender', e.target.value)}
            >
              {GENDER_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Customer Type</span>
            <select
              name="Customer Type"
              value={formData['Customer Type'] || ''}
              onChange={(e) => onFormChange('Customer Type', e.target.value)}
            >
              {CUSTOMER_TYPE_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Age</span>
            <input
              type="number"
              name="Age"
              min="7"
              max="85"
              value={formData.Age || ''}
              onChange={(e) => onFormChange('Age', Number(e.target.value))}
            />
          </label>

          <label className="field">
            <span>Type of Travel</span>
            <select
              name="Type of Travel"
              value={formData['Type of Travel'] || ''}
              onChange={(e) => onFormChange('Type of Travel', e.target.value)}
            >
              {TRAVEL_TYPE_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Class</span>
            <select
              name="Class"
              value={formData.Class || ''}
              onChange={(e) => onFormChange('Class', e.target.value)}
            >
              {CLASS_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
        </div>
      </section>

      {/* Flight Info Section */}
      <section className="panel">
        <h2>Flight info</h2>
        <div className="field-grid">
          <label className="field">
            <span>Flight Distance</span>
            <input
              type="number"
              name="Flight Distance"
              min="31"
              max="4983"
              value={formData['Flight Distance'] || ''}
              onChange={(e) => onFormChange('Flight Distance', Number(e.target.value))}
            />
          </label>

          <label className="field">
            <span>Departure Delay in Minutes</span>
            <input
              type="number"
              name="Departure Delay in Minutes"
              min="0"
              max="1600"
              value={formData['Departure Delay in Minutes'] || ''}
              onChange={(e) => onFormChange('Departure Delay in Minutes', Number(e.target.value))}
            />
          </label>
        </div>
      </section>

      {/* Service Ratings Section */}
      <section className="panel">
        <h2>Service ratings</h2>
        <div className="field-grid ratings-grid">
          {SERVICE_FIELDS.map((fieldName) => (
            <div key={fieldName} className="rating-field">
              <div className="rating-header">
                <label htmlFor={fieldName}>{fieldName}</label>
                <span className="rating-value">{formData[fieldName] || 0}</span>
              </div>
              <input
                id={fieldName}
                type="range"
                min={fieldName === 'Baggage handling' ? 1 : 0}
                max="5"
                step="1"
                value={formData[fieldName] || 0}
                onChange={(e) => onRangeChange(fieldName, Number(e.target.value))}
              />
              {fieldErrors[fieldName] && (
                <small className="error-text">{fieldErrors[fieldName]}</small>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Feedback Section */}
      <section className="panel">
        <h2>Data collection for future model improvement</h2>
        <div className="field-grid">
          <label className="field">
            <span>Passenger name</span>
            <input
              type="text"
              name="passenger_name"
              value={feedback.passenger_name || ''}
              onChange={(e) => onFeedbackChange('passenger_name', e.target.value)}
              placeholder="e.g. Ahmed Ali"
            />
          </label>

          <label className="field">
            <span>Airline name</span>
            <input
              type="text"
              name="airline_name"
              value={feedback.airline_name || ''}
              onChange={(e) => onFeedbackChange('airline_name', e.target.value)}
              placeholder="e.g. Emirates"
            />
          </label>

          <label className="field">
            <span>Destination</span>
            <input
              type="text"
              name="destination"
              value={feedback.destination || ''}
              onChange={(e) => onFeedbackChange('destination', e.target.value)}
              placeholder="e.g. Dubai"
            />
          </label>

          <label className="field">
            <span>Travel reason</span>
            <select
              name="travel_reason"
              value={feedback.travel_reason || ''}
              onChange={(e) => onFeedbackChange('travel_reason', e.target.value)}
            >
              {TRAVEL_REASON_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Booking channel</span>
            <select
              name="booking_channel"
              value={feedback.booking_channel || ''}
              onChange={(e) => onFeedbackChange('booking_channel', e.target.value)}
            >
              {BOOKING_CHANNEL_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Overall service rating</span>
            <input
              type="number"
              min="1"
              max="5"
              step="1"
              name="overall_service_rating"
              value={feedback.overall_service_rating || ''}
              onChange={(e) => onFeedbackChange('overall_service_rating', Number(e.target.value))}
            />
          </label>

          <label className="field wide-field">
            <span>Additional comment</span>
            <textarea
              name="comment"
              rows="3"
              value={feedback.comment || ''}
              onChange={(e) => onFeedbackChange('comment', e.target.value)}
              placeholder="Tell us about your trip experience..."
            />
          </label>
        </div>

        <label className="checkbox-row">
          <input
            type="checkbox"
            name="consent_to_use_data"
            checked={feedback.consent_to_use_data || false}
            onChange={(e) => onFeedbackChange('consent_to_use_data', e.target.checked)}
          />
          <span>I agree to save this response for future model improvement.</span>
        </label>
      </section>

      {apiError && <div className="inline-error">{apiError}</div>}

      <div className="submit-row">
        <button type="submit" disabled={submitting}>
          {submitting ? 'Predicting…' : 'Predict satisfaction'}
        </button>
      </div>

      <section className="panel">
        <h2>AI complaint assistant</h2>

        <div className="field-grid">
          <label className="field wide-field">
            <span>Optional custom prompt</span>
            <textarea
              rows="3"
              value={customPrompt}
              onChange={(e) => onCustomPromptChange(e.target.value)}
              placeholder="Edit or replace the prompt here..."
            />
          </label>
        </div>

        {aiError && <div className="inline-error">{aiError}</div>}

        {aiAnswer && (
          <div className="panel" style={{ marginTop: '1rem' }}>
            <h3>AI answer</h3>
            <p>{aiAnswer}</p>
          </div>
        )}

        <div className="submit-row">
          <button
            type="button"
            onClick={onAiAnalyze}
            disabled={aiLoading || !result}
            title={!result ? 'Predict satisfaction first to enable analysis.' : ''}
          >
            {aiLoading ? 'Analyzing…' : 'Analyze'}
          </button>
        </div>
      </section>
    </form>
  )
}
