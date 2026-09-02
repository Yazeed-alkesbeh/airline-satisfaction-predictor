/**
 * Frontend constants and configuration
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const INITIAL_FORM_DATA = {
  Gender: 'Female',
  'Customer Type': 'Loyal Customer',
  Age: 35,
  'Type of Travel': 'Business travel',
  Class: 'Eco',
  'Flight Distance': 1600,
  'Inflight wifi service': 4,
  'Departure/Arrival time convenient': 4,
  'Ease of Online booking': 4,
  'Gate location': 3,
  'Food and drink': 3,
  'Online boarding': 4,
  'Seat comfort': 4,
  'Inflight entertainment': 4,
  'On-board service': 4,
  'Leg room service': 4,
  'Baggage handling': 4,
  'Checkin service': 3,
  'Inflight service': 4,
  Cleanliness: 4,
  'Departure Delay in Minutes': 15,
}

export const INITIAL_FEEDBACK_DATA = {
  passenger_name: '',
  airline_name: 'Emirates',
  destination: 'Dubai',
  travel_reason: 'Business',
  booking_channel: 'Website',
  overall_service_rating: 4,
  comment: '',
  consent_to_use_data: true,
}

export const SERVICE_FIELDS = [
  'Inflight wifi service',
  'Departure/Arrival time convenient',
  'Ease of Online booking',
  'Gate location',
  'Food and drink',
  'Online boarding',
  'Seat comfort',
  'Inflight entertainment',
  'On-board service',
  'Leg room service',
  'Baggage handling',
  'Checkin service',
  'Inflight service',
  'Cleanliness',
]

export const TRAVEL_REASON_OPTIONS = [
  'Business',
  'Leisure',
  'Family',
  'Other',
]

export const BOOKING_CHANNEL_OPTIONS = [
  'Website',
  'Mobile App',
  'Call center',
  'Travel agency',
]

export const GENDER_OPTIONS = [
  'Male',
  'Female',
]

export const CUSTOMER_TYPE_OPTIONS = [
  'Loyal Customer',
  'disloyal Customer',
]

export const TRAVEL_TYPE_OPTIONS = [
  'Personal Travel',
  'Business travel',
]

export const CLASS_OPTIONS = [
  'Business',
  'Eco',
  'Eco Plus',
]
