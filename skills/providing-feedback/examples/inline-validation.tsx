import React, { useState, useEffect } from 'react';

/**
 * Inline Form Validation Examples
 *
 * Demonstrates real-time form validation with inline error messages
 * and field-level feedback
 */

// Real-time Form Validation Component
export function FormWithInlineValidation() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    username: '',
    phone: '',
    website: ''
  });

  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validation rules
  const validationRules = {
    email: {
      required: true,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: 'Please enter a valid email address'
    },
    password: {
      required: true,
      minLength: 8,
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      message: 'Password must be at least 8 characters with uppercase, lowercase, and number'
    },
    confirmPassword: {
      required: true,
      match: 'password',
      message: 'Passwords do not match'
    },
    username: {
      required: true,
      minLength: 3,
      maxLength: 20,
      pattern: /^[a-zA-Z0-9_]+$/,
      message: 'Username must be 3-20 characters, alphanumeric and underscore only'
    },
    phone: {
      pattern: /^\+?[\d\s-()]+$/,
      minLength: 10,
      message: 'Please enter a valid phone number'
    },
    website: {
      pattern: /^https?:\/\/.+\..+/,
      message: 'Please enter a valid URL starting with http:// or https://'
    }
  };

  // Validate single field
  const validateField = (name, value) => {
    const rules = validationRules[name];
    if (!rules) return '';

    // Required check
    if (rules.required && !value) {
      return `${name.charAt(0).toUpperCase() + name.slice(1)} is required`;
    }

    // Pattern check
    if (rules.pattern && value && !rules.pattern.test(value)) {
      return rules.message;
    }

    // Min length check
    if (rules.minLength && value && value.length < rules.minLength) {
      return `Must be at least ${rules.minLength} characters`;
    }

    // Max length check
    if (rules.maxLength && value && value.length > rules.maxLength) {
      return `Must be no more than ${rules.maxLength} characters`;
    }

    // Match check (for confirm password)
    if (rules.match && value !== formData[rules.match]) {
      return rules.message;
    }

    return '';
  };

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    // Real-time validation if field has been touched
    if (touched[name]) {
      const error = validateField(name, value);
      setErrors(prev => ({ ...prev, [name]: error }));
    }
  };

  // Handle field blur
  const handleBlur = (e) => {
    const { name, value } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));

    // Validate on blur
    const error = validateField(name, value);
    setErrors(prev => ({ ...prev, [name]: error }));
  };

  // Validate entire form
  const validateForm = () => {
    const newErrors = {};
    Object.keys(formData).forEach(key => {
      const error = validateField(key, formData[key]);
      if (error) newErrors[key] = error;
    });
    return newErrors;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Mark all fields as touched
    const allTouched = {};
    Object.keys(formData).forEach(key => {
      allTouched[key] = true;
    });
    setTouched(allTouched);

    // Validate all fields
    const newErrors = validateForm();
    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      setIsSubmitting(true);

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));

      console.log('Form submitted:', formData);
      // Show success message
      toast.success('Form submitted successfully!');

      setIsSubmitting(false);
    } else {
      // Focus first error field
      const firstErrorField = Object.keys(newErrors)[0];
      document.getElementById(firstErrorField)?.focus();

      // Show error toast
      toast.error('Please fix the errors before submitting');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="validation-form">
      <h2>Registration Form</h2>

      {/* Email Field */}
      <FormField
        id="email"
        label="Email Address"
        type="email"
        value={formData.email}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.email}
        touched={touched.email}
        required
      />

      {/* Username Field */}
      <FormField
        id="username"
        label="Username"
        type="text"
        value={formData.username}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.username}
        touched={touched.username}
        required
        helpText="3-20 characters, letters, numbers, and underscore only"
      />

      {/* Password Field */}
      <FormField
        id="password"
        label="Password"
        type="password"
        value={formData.password}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.password}
        touched={touched.password}
        required
        strength={calculatePasswordStrength(formData.password)}
      />

      {/* Confirm Password Field */}
      <FormField
        id="confirmPassword"
        label="Confirm Password"
        type="password"
        value={formData.confirmPassword}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.confirmPassword}
        touched={touched.confirmPassword}
        required
      />

      {/* Phone Field (Optional) */}
      <FormField
        id="phone"
        label="Phone Number"
        type="tel"
        value={formData.phone}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.phone}
        touched={touched.phone}
        helpText="Optional"
      />

      {/* Website Field (Optional) */}
      <FormField
        id="website"
        label="Website"
        type="url"
        value={formData.website}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.website}
        touched={touched.website}
        helpText="Optional - Include http:// or https://"
      />

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="btn-primary submit-btn"
      >
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}

// Reusable Form Field Component
function FormField({
  id,
  label,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  touched,
  required,
  helpText,
  strength
}) {
  const hasError = touched && error;
  const isValid = touched && !error && value;

  return (
    <div className={`form-field ${hasError ? 'field-error' : ''} ${isValid ? 'field-valid' : ''}`}>
      <label htmlFor={id} className="field-label">
        {label}
        {required && <span className="required-mark">*</span>}
      </label>

      <div className="field-wrapper">
        <input
          id={id}
          name={id}
          type={type}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          className="field-input"
          aria-invalid={hasError}
          aria-describedby={hasError ? `${id}-error` : helpText ? `${id}-help` : undefined}
        />

        {/* Status icon */}
        <div className="field-icon">
          {hasError && <span className="icon-error">✕</span>}
          {isValid && <span className="icon-success">✓</span>}
        </div>
      </div>

      {/* Password strength indicator */}
      {strength !== undefined && value && (
        <PasswordStrength strength={strength} />
      )}

      {/* Help text */}
      {helpText && !hasError && (
        <div id={`${id}-help`} className="field-help">
          {helpText}
        </div>
      )}

      {/* Error message */}
      {hasError && (
        <div
          id={`${id}-error`}
          className="field-error-message"
          role="alert"
          aria-live="polite"
        >
          {error}
        </div>
      )}
    </div>
  );
}

// Password Strength Indicator
function PasswordStrength({ strength }) {
  const getStrengthLabel = () => {
    if (strength < 2) return 'Weak';
    if (strength < 3) return 'Fair';
    if (strength < 4) return 'Good';
    return 'Strong';
  };

  const getStrengthColor = () => {
    if (strength < 2) return '#ef4444';
    if (strength < 3) return '#f59e0b';
    if (strength < 4) return '#3b82f6';
    return '#10b981';
  };

  return (
    <div className="password-strength">
      <div className="strength-bars">
        {[1, 2, 3, 4].map(level => (
          <div
            key={level}
            className={`strength-bar ${strength >= level ? 'active' : ''}`}
            style={{
              backgroundColor: strength >= level ? getStrengthColor() : '#e5e7eb'
            }}
          />
        ))}
      </div>
      <span className="strength-label" style={{ color: getStrengthColor() }}>
        {getStrengthLabel()}
      </span>
    </div>
  );
}

// Calculate password strength
function calculatePasswordStrength(password) {
  if (!password) return 0;

  let strength = 0;

  // Length
  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;

  // Character types
  if (/[a-z]/.test(password)) strength += 0.5;
  if (/[A-Z]/.test(password)) strength += 0.5;
  if (/\d/.test(password)) strength += 0.5;
  if (/[^a-zA-Z0-9]/.test(password)) strength += 0.5;

  return Math.min(4, strength);
}

// Async Validation Example (Username availability)
export function AsyncValidationField() {
  const [username, setUsername] = useState('');
  const [isChecking, setIsChecking] = useState(false);
  const [isAvailable, setIsAvailable] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!username || username.length < 3) {
      setIsAvailable(null);
      setError('');
      return;
    }

    const timer = setTimeout(async () => {
      setIsChecking(true);
      setError('');

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Simulate availability check
      const unavailableUsernames = ['admin', 'test', 'user', 'demo'];
      const available = !unavailableUsernames.includes(username.toLowerCase());

      setIsAvailable(available);
      if (!available) {
        setError('Username is already taken');
      }
      setIsChecking(false);
    }, 500); // Debounce for 500ms

    return () => clearTimeout(timer);
  }, [username]);

  return (
    <div className="form-field">
      <label htmlFor="async-username" className="field-label">
        Choose Username
      </label>

      <div className="field-wrapper">
        <input
          id="async-username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="field-input"
          placeholder="Enter desired username"
        />

        <div className="field-icon">
          {isChecking && <span className="spinner-small">⟳</span>}
          {!isChecking && isAvailable === true && <span className="icon-success">✓</span>}
          {!isChecking && isAvailable === false && <span className="icon-error">✕</span>}
        </div>
      </div>

      {isChecking && (
        <div className="field-help">Checking availability...</div>
      )}

      {!isChecking && isAvailable === true && (
        <div className="field-success">Username is available!</div>
      )}

      {!isChecking && error && (
        <div className="field-error-message" role="alert">
          {error}
        </div>
      )}
    </div>
  );
}

// Dynamic Field Validation (Credit Card)
export function CreditCardValidation() {
  const [cardNumber, setCardNumber] = useState('');
  const [cardType, setCardType] = useState(null);

  const detectCardType = (number) => {
    const cleanNumber = number.replace(/\s/g, '');

    if (/^4/.test(cleanNumber)) return 'visa';
    if (/^5[1-5]/.test(cleanNumber)) return 'mastercard';
    if (/^3[47]/.test(cleanNumber)) return 'amex';
    if (/^6(?:011|5)/.test(cleanNumber)) return 'discover';

    return null;
  };

  const formatCardNumber = (value) => {
    const cleanValue = value.replace(/\s/g, '');
    const chunks = cleanValue.match(/.{1,4}/g) || [];
    return chunks.join(' ');
  };

  const handleCardNumberChange = (e) => {
    const value = e.target.value.replace(/\s/g, '');
    if (/^\d*$/.test(value) && value.length <= 16) {
      const formatted = formatCardNumber(value);
      setCardNumber(formatted);
      setCardType(detectCardType(value));
    }
  };

  return (
    <div className="form-field">
      <label htmlFor="card-number" className="field-label">
        Card Number
      </label>

      <div className="field-wrapper">
        <input
          id="card-number"
          type="text"
          value={cardNumber}
          onChange={handleCardNumberChange}
          placeholder="1234 5678 9012 3456"
          className="field-input"
          maxLength={19}
        />

        {cardType && (
          <div className="card-type-icon">
            {cardType === 'visa' && '💳 Visa'}
            {cardType === 'mastercard' && '💳 Mastercard'}
            {cardType === 'amex' && '💳 Amex'}
            {cardType === 'discover' && '💳 Discover'}
          </div>
        )}
      </div>

      {cardNumber.length === 19 && (
        <div className="field-success">Valid card number format</div>
      )}
    </div>
  );
}

// Styles
const styles = `
  .validation-form {
    max-width: 500px;
    margin: 0 auto;
    padding: 24px;
  }

  .form-field {
    margin-bottom: 20px;
  }

  .field-label {
    display: block;
    margin-bottom: 6px;
    font-weight: 500;
    font-size: 14px;
    color: #374151;
  }

  .required-mark {
    color: #ef4444;
    margin-left: 4px;
  }

  .field-wrapper {
    position: relative;
  }

  .field-input {
    width: 100%;
    padding: 8px 36px 8px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 16px;
    transition: all 0.2s;
  }

  .field-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .field-error .field-input {
    border-color: #ef4444;
    background-color: #fef2f2;
  }

  .field-error .field-input:focus {
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
  }

  .field-valid .field-input {
    border-color: #10b981;
    background-color: #f0fdf4;
  }

  .field-icon {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
  }

  .icon-error {
    color: #ef4444;
  }

  .icon-success {
    color: #10b981;
  }

  .field-help {
    margin-top: 4px;
    font-size: 14px;
    color: #6b7280;
  }

  .field-error-message {
    margin-top: 4px;
    font-size: 14px;
    color: #ef4444;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .field-success {
    margin-top: 4px;
    font-size: 14px;
    color: #10b981;
  }

  /* Password strength */
  .password-strength {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
  }

  .strength-bars {
    display: flex;
    gap: 4px;
    flex: 1;
  }

  .strength-bar {
    height: 4px;
    flex: 1;
    border-radius: 2px;
    transition: background-color 0.3s;
  }

  .strength-label {
    font-size: 12px;
    font-weight: 500;
  }

  /* Spinner */
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .spinner-small {
    display: inline-block;
    animation: spin 1s linear infinite;
  }

  /* Submit button */
  .submit-btn {
    width: 100%;
    padding: 12px;
    margin-top: 24px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
  }

  .submit-btn:hover:not(:disabled) {
    background: #2563eb;
  }

  .submit-btn:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }

  /* Card type icon */
  .card-type-icon {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 14px;
  }
`;