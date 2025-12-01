/**
 * Inline Validation Example
 *
 * Demonstrates:
 * - Real-time validation with debouncing
 * - Password strength meter
 * - Username availability check (async)
 * - Progressive enhancement (on-blur → on-change after error)
 * - Success indicators
 * - Accessibility (aria-live announcements)
 */

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useState, useEffect, useCallback } from 'react';

// Validation schema
const registrationSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),

  email: z.string()
    .email('Invalid email address')
    .toLowerCase(),

  password: z.string()
    .min(8, 'Password must be at least 8 characters'),

  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type RegistrationData = z.infer<typeof registrationSchema>;

// Password strength calculation
type PasswordStrength = 'weak' | 'medium' | 'strong' | 'very-strong';

function calculatePasswordStrength(password: string): PasswordStrength {
  let score = 0;

  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;

  if (score >= 5) return 'very-strong';
  if (score >= 4) return 'strong';
  if (score >= 2) return 'medium';
  return 'weak';
}

// Debounce utility
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default function InlineValidationForm() {
  const [passwordStrength, setPasswordStrength] = useState<PasswordStrength>('weak');
  const [usernameStatus, setUsernameStatus] = useState<'idle' | 'checking' | 'available' | 'taken'>('idle');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting, touchedFields },
  } = useForm<RegistrationData>({
    resolver: zodResolver(registrationSchema),
    mode: 'onBlur', // Initial validation on blur
    reValidateMode: 'onChange', // After error, switch to on-change
  });

  // Watch password for strength meter
  const password = watch('password', '');
  const username = watch('username', '');

  // Debounce username for availability check
  const debouncedUsername = useDebounce(username, 500);

  // Update password strength on change
  useEffect(() => {
    if (password) {
      setPasswordStrength(calculatePasswordStrength(password));
    }
  }, [password]);

  // Check username availability (debounced)
  useEffect(() => {
    if (debouncedUsername && debouncedUsername.length >= 3) {
      checkUsernameAvailability(debouncedUsername);
    } else {
      setUsernameStatus('idle');
    }
  }, [debouncedUsername]);

  const checkUsernameAvailability = async (username: string) => {
    setUsernameStatus('checking');

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Simulate availability check
      const taken = ['admin', 'user', 'test', 'demo'].includes(username.toLowerCase());

      setUsernameStatus(taken ? 'taken' : 'available');
    } catch (error) {
      setUsernameStatus('idle');
    }
  };

  const onSubmit = async (data: RegistrationData) => {
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));

      console.log('Form submitted:', data);
      setIsSubmitted(true);
    } catch (error) {
      console.error('Submission error:', error);
    }
  };

  if (isSubmitted) {
    return (
      <div className="success-message" role="alert">
        <h2>Registration Successful!</h2>
        <p>Welcome to our platform!</p>
      </div>
    );
  }

  const strengthColors = {
    weak: '#ef4444',
    medium: '#f59e0b',
    strong: '#3b82f6',
    'very-strong': '#22c55e',
  };

  const strengthLabels = {
    weak: 'Weak',
    medium: 'Medium',
    strong: 'Strong',
    'very-strong': 'Very Strong',
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <h2>Create Account</h2>

      {/* Username with Availability Check */}
      <div className="field">
        <label htmlFor="username">
          Username <span aria-label="required">*</span>
        </label>
        <div className="input-with-status">
          <input
            id="username"
            type="text"
            {...register('username')}
            aria-invalid={errors.username || usernameStatus === 'taken' ? 'true' : 'false'}
            aria-describedby="username-status username-error"
            className={
              errors.username || usernameStatus === 'taken'
                ? 'error'
                : usernameStatus === 'available'
                ? 'valid'
                : ''
            }
          />
          {usernameStatus === 'checking' && (
            <span className="input-icon">⏳</span>
          )}
          {usernameStatus === 'available' && !errors.username && (
            <span className="input-icon success">✓</span>
          )}
          {usernameStatus === 'taken' && (
            <span className="input-icon error">✗</span>
          )}
        </div>

        <div id="username-status" aria-live="polite" aria-atomic="true">
          {usernameStatus === 'checking' && (
            <span className="status-message">Checking availability...</span>
          )}
          {usernameStatus === 'available' && !errors.username && (
            <span className="success-message">✓ Username available</span>
          )}
          {usernameStatus === 'taken' && (
            <span className="error-message">Username already taken</span>
          )}
        </div>

        {errors.username && (
          <span id="username-error" className="error-message" role="alert">
            {errors.username.message}
          </span>
        )}
      </div>

      {/* Email */}
      <div className="field">
        <label htmlFor="email">
          Email Address <span aria-label="required">*</span>
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          aria-invalid={errors.email ? 'true' : 'false'}
          aria-describedby={errors.email ? 'email-error' : undefined}
          placeholder="name@example.com"
          className={errors.email ? 'error' : touchedFields.email && !errors.email ? 'valid' : ''}
        />
        {errors.email && (
          <span id="email-error" className="error-message" role="alert">
            {errors.email.message}
          </span>
        )}
        {touchedFields.email && !errors.email && (
          <span className="success-message">✓ Valid email</span>
        )}
      </div>

      {/* Password with Strength Meter */}
      <div className="field">
        <label htmlFor="password">
          Password <span aria-label="required">*</span>
        </label>
        <input
          id="password"
          type="password"
          {...register('password')}
          aria-invalid={errors.password ? 'true' : 'false'}
          aria-describedby="password-error password-strength password-requirements"
          className={errors.password ? 'error' : ''}
        />

        {/* Password Strength Meter */}
        {password && (
          <div
            id="password-strength"
            className="strength-meter"
            aria-live="polite"
            aria-atomic="true"
          >
            <div
              className="strength-bar"
              style={{
                width: `${
                  passwordStrength === 'weak'
                    ? '25%'
                    : passwordStrength === 'medium'
                    ? '50%'
                    : passwordStrength === 'strong'
                    ? '75%'
                    : '100%'
                }`,
                backgroundColor: strengthColors[passwordStrength],
              }}
            />
            <span
              className="strength-label"
              style={{ color: strengthColors[passwordStrength] }}
            >
              {strengthLabels[passwordStrength]}
            </span>
          </div>
        )}

        {/* Password Requirements Checklist */}
        <ul id="password-requirements" className="requirements-list">
          <li className={password.length >= 8 ? 'met' : 'unmet'}>
            {password.length >= 8 ? '✓' : '✗'} At least 8 characters
          </li>
          <li className={/[A-Z]/.test(password) ? 'met' : 'unmet'}>
            {/[A-Z]/.test(password) ? '✓' : '✗'} Contains uppercase letter
          </li>
          <li className={/[a-z]/.test(password) ? 'met' : 'unmet'}>
            {/[a-z]/.test(password) ? '✓' : '✗'} Contains lowercase letter
          </li>
          <li className={/[0-9]/.test(password) ? 'met' : 'unmet'}>
            {/[0-9]/.test(password) ? '✓' : '✗'} Contains number
          </li>
          <li className={/[!@#$%^&*]/.test(password) ? 'met' : 'unmet'}>
            {/[!@#$%^&*]/.test(password) ? '✓' : '✗'} Contains special character
          </li>
        </ul>

        {errors.password && (
          <span id="password-error" className="error-message" role="alert">
            {errors.password.message}
          </span>
        )}
      </div>

      {/* Confirm Password */}
      <div className="field">
        <label htmlFor="confirmPassword">
          Confirm Password <span aria-label="required">*</span>
        </label>
        <input
          id="confirmPassword"
          type="password"
          {...register('confirmPassword')}
          aria-invalid={errors.confirmPassword ? 'true' : 'false'}
          aria-describedby={errors.confirmPassword ? 'confirmPassword-error' : undefined}
          className={
            errors.confirmPassword
              ? 'error'
              : touchedFields.confirmPassword && !errors.confirmPassword
              ? 'valid'
              : ''
          }
        />
        {errors.confirmPassword && (
          <span id="confirmPassword-error" className="error-message" role="alert">
            {errors.confirmPassword.message}
          </span>
        )}
        {touchedFields.confirmPassword && !errors.confirmPassword && (
          <span className="success-message">✓ Passwords match</span>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting || usernameStatus === 'checking'}
        className="submit-button"
      >
        {isSubmitting ? 'Creating Account...' : 'Create Account'}
      </button>
    </form>
  );
}

/**
 * CSS Styles (example)
 *
 * .input-with-status {
 *   position: relative;
 * }
 *
 * .input-icon {
 *   position: absolute;
 *   right: 12px;
 *   top: 50%;
 *   transform: translateY(-50%);
 * }
 *
 * .strength-meter {
 *   margin-top: 0.5rem;
 *   height: 4px;
 *   background: #e5e7eb;
 *   border-radius: 2px;
 *   position: relative;
 *   margin-bottom: 0.5rem;
 * }
 *
 * .strength-bar {
 *   height: 100%;
 *   border-radius: 2px;
 *   transition: width 0.3s ease, background-color 0.3s ease;
 * }
 *
 * .strength-label {
 *   font-size: 0.875rem;
 *   font-weight: 600;
 *   margin-left: 0.5rem;
 * }
 *
 * .requirements-list {
 *   margin: 0.5rem 0;
 *   padding: 0;
 *   list-style: none;
 *   font-size: 0.875rem;
 * }
 *
 * .requirements-list li {
 *   margin: 0.25rem 0;
 * }
 *
 * .requirements-list li.met {
 *   color: #22c55e;
 * }
 *
 * .requirements-list li.unmet {
 *   color: #9ca3af;
 * }
 *
 * .status-message {
 *   font-size: 0.875rem;
 *   color: #6b7280;
 * }
 */
