/**
 * Async Validation Example: Username Availability Check
 *
 * Demonstrates:
 * - Async validation (API call to check username)
 * - Debouncing to prevent excessive API calls
 * - Loading states during validation
 * - Real-time feedback
 * - Error handling for network failures
 */

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useState, useCallback } from 'react';
import { debounce } from 'lodash';

// Validation schema with async refinement
const signupSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters')
    .regex(/^[a-zA-Z0-9_-]+$/, 'Username can only contain letters, numbers, underscores, and hyphens'),

  email: z.string().email('Please enter a valid email address'),

  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Must contain at least one number'),
});

type SignupFormData = z.infer<typeof signupSchema>;

export default function AsyncValidationForm() {
  const [isCheckingUsername, setIsCheckingUsername] = useState(false);
  const [usernameAvailable, setUsernameAvailable] = useState<boolean | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
    clearErrors,
    watch,
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
    mode: 'onBlur',
    reValidateMode: 'onChange',
  });

  // Mock API call to check username availability
  const checkUsernameAPI = async (username: string): Promise<boolean> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800));

    // Simulate some taken usernames
    const takenUsernames = ['admin', 'user', 'test', 'demo', 'support'];
    return !takenUsernames.includes(username.toLowerCase());
  };

  // Debounced username check (500ms delay)
  const debouncedCheckUsername = useCallback(
    debounce(async (username: string) => {
      if (username.length < 3) {
        setUsernameAvailable(null);
        return;
      }

      setIsCheckingUsername(true);

      try {
        const available = await checkUsernameAPI(username);
        setUsernameAvailable(available);

        if (!available) {
          setError('username', {
            type: 'manual',
            message: 'This username is already taken. Please choose another.',
          });
        } else {
          clearErrors('username');
        }
      } catch (error) {
        console.error('Username check failed:', error);
        setError('username', {
          type: 'manual',
          message: 'Could not verify username. Please try again.',
        });
      } finally {
        setIsCheckingUsername(false);
      }
    }, 500),
    []
  );

  // Watch username field for changes
  const username = watch('username');

  // Trigger check on username change
  React.useEffect(() => {
    if (username) {
      debouncedCheckUsername(username);
    } else {
      setUsernameAvailable(null);
    }
  }, [username, debouncedCheckUsername]);

  const onSubmit = async (data: SignupFormData) => {
    // Final check before submission
    const available = await checkUsernameAPI(data.username);
    if (!available) {
      setError('username', {
        type: 'manual',
        message: 'Username is no longer available',
      });
      return;
    }

    console.log('Form submitted:', data);
    // Submit to API...
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <h2>Sign Up</h2>

      {/* Username with async validation */}
      <div style={{ marginBottom: '24px' }}>
        <label htmlFor="username" style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          Username *
        </label>
        <div style={{ position: 'relative' }}>
          <input
            id="username"
            {...register('username')}
            placeholder="Choose a username"
            aria-invalid={errors.username ? 'true' : 'false'}
            aria-describedby={errors.username ? 'username-error' : undefined}
            style={{
              width: '100%',
              padding: '12px',
              border: `2px solid ${
                errors.username ? '#EF4444' :
                usernameAvailable === true ? '#10B981' :
                '#D1D5DB'
              }`,
              borderRadius: '8px',
              fontSize: '16px',
            }}
          />

          {/* Loading indicator */}
          {isCheckingUsername && (
            <div style={{
              position: 'absolute',
              right: '12px',
              top: '50%',
              transform: 'translateY(-50%)',
            }}>
              <div className="spinner" style={{
                width: '20px',
                height: '20px',
                border: '2px solid #D1D5DB',
                borderTopColor: '#3B82F6',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
              }} />
            </div>
          )}

          {/* Success indicator */}
          {usernameAvailable === true && !isCheckingUsername && (
            <div style={{
              position: 'absolute',
              right: '12px',
              top: '50%',
              transform: 'translateY(-50%)',
              color: '#10B981',
              fontSize: '20px',
            }}>
              ✓
            </div>
          )}
        </div>

        {/* Error message */}
        {errors.username && (
          <p id="username-error" role="alert" style={{
            color: '#EF4444',
            fontSize: '14px',
            marginTop: '8px',
          }}>
            {errors.username.message}
          </p>
        )}

        {/* Success message */}
        {usernameAvailable === true && !errors.username && (
          <p style={{
            color: '#10B981',
            fontSize: '14px',
            marginTop: '8px',
          }}>
            ✓ Username is available!
          </p>
        )}
      </div>

      {/* Email */}
      <div style={{ marginBottom: '24px' }}>
        <label htmlFor="email" style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          Email *
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          placeholder="you@example.com"
          aria-invalid={errors.email ? 'true' : 'false'}
          aria-describedby={errors.email ? 'email-error' : undefined}
          style={{
            width: '100%',
            padding: '12px',
            border: `2px solid ${errors.email ? '#EF4444' : '#D1D5DB'}`,
            borderRadius: '8px',
            fontSize: '16px',
          }}
        />
        {errors.email && (
          <p id="email-error" role="alert" style={{
            color: '#EF4444',
            fontSize: '14px',
            marginTop: '8px',
          }}>
            {errors.email.message}
          </p>
        )}
      </div>

      {/* Password */}
      <div style={{ marginBottom: '24px' }}>
        <label htmlFor="password" style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          Password *
        </label>
        <input
          id="password"
          type="password"
          {...register('password')}
          placeholder="At least 8 characters"
          aria-invalid={errors.password ? 'true' : 'false'}
          aria-describedby={errors.password ? 'password-error' : undefined}
          style={{
            width: '100%',
            padding: '12px',
            border: `2px solid ${errors.password ? '#EF4444' : '#D1D5DB'}`,
            borderRadius: '8px',
            fontSize: '16px',
          }}
        />
        {errors.password && (
          <p id="password-error" role="alert" style={{
            color: '#EF4444',
            fontSize: '14px',
            marginTop: '8px',
          }}>
            {errors.password.message}
          </p>
        )}
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={isSubmitting || isCheckingUsername}
        style={{
          width: '100%',
          padding: '12px 24px',
          backgroundColor: '#3B82F6',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          fontSize: '16px',
          fontWeight: '500',
          cursor: 'pointer',
          opacity: (isSubmitting || isCheckingUsername) ? 0.6 : 1,
        }}
      >
        {isSubmitting ? 'Creating Account...' : 'Sign Up'}
      </button>
    </form>
  );
}

// Add CSS animation for spinner
const styles = `
@keyframes spin {
  to { transform: rotate(360deg); }
}
`;
```
