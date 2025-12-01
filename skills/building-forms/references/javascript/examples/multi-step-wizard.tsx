/**
 * Multi-Step Registration Wizard
 *
 * Demonstrates:
 * - Multi-step form with state management
 * - Step-by-step validation
 * - Progress indicator
 * - Navigation between steps
 * - Data persistence across steps
 * - Final submission with all data
 */

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useState } from 'react';

// Step 1: Personal Information
const step1Schema = z.object({
  firstName: z.string().min(2, 'First name must be at least 2 characters'),
  lastName: z.string().min(2, 'Last name must be at least 2 characters'),
  email: z.string().email('Invalid email address').toLowerCase(),
  phone: z.string().regex(/^\d{10}$/, 'Phone must be 10 digits'),
});

// Step 2: Address
const step2Schema = z.object({
  street: z.string().min(5, 'Street address must be at least 5 characters'),
  city: z.string().min(2, 'City must be at least 2 characters'),
  state: z.string().length(2, 'State must be 2 characters').toUpperCase(),
  zipCode: z.string().regex(/^\d{5}$/, 'ZIP code must be 5 digits'),
});

// Step 3: Account
const step3Schema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

// Complete schema (all steps combined)
const completeSchema = z.object({
  ...step1Schema.shape,
  ...step2Schema.shape,
  ...step3Schema.shape,
});

type FormData = z.infer<typeof completeSchema>;

const STEPS = [
  { number: 1, title: 'Personal Info', schema: step1Schema },
  { number: 2, title: 'Address', schema: step2Schema },
  { number: 3, title: 'Account', schema: step3Schema },
];

export default function MultiStepWizard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<Partial<FormData>>({});
  const [isCompleted, setIsCompleted] = useState(false);

  const currentStepSchema = STEPS[currentStep - 1].schema;

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    trigger,
  } = useForm({
    resolver: zodResolver(currentStepSchema as any),
    mode: 'onBlur',
    defaultValues: formData,
  });

  const nextStep = async (data: any) => {
    // Save current step data
    setFormData((prev) => ({ ...prev, ...data }));

    if (currentStep < STEPS.length) {
      setCurrentStep((prev) => prev + 1);
    } else {
      // Final step - submit all data
      await submitForm({ ...formData, ...data });
    }
  };

  const previousStep = () => {
    if (currentStep > 1) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const submitForm = async (data: FormData) => {
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1500));

      console.log('Complete form data:', data);

      setIsCompleted(true);
    } catch (error) {
      console.error('Submission error:', error);
    }
  };

  if (isCompleted) {
    return (
      <div className="success-container" role="alert">
        <h2>Registration Complete!</h2>
        <p>Welcome, {formData.firstName}!</p>
        <p>A confirmation email has been sent to {formData.email}.</p>
      </div>
    );
  }

  return (
    <div className="wizard-container">
      {/* Progress Indicator */}
      <nav aria-label="Registration progress">
        <ol className="progress-steps">
          {STEPS.map((step) => (
            <li
              key={step.number}
              className={`step ${currentStep === step.number ? 'active' : ''} ${
                currentStep > step.number ? 'completed' : ''
              }`}
              aria-current={currentStep === step.number ? 'step' : undefined}
            >
              <span className="step-number">{step.number}</span>
              <span className="step-title">{step.title}</span>
            </li>
          ))}
        </ol>
      </nav>

      {/* Step announcement for screen readers */}
      <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
        Step {currentStep} of {STEPS.length}: {STEPS[currentStep - 1].title}
      </div>

      <form onSubmit={handleSubmit(nextStep)} noValidate>
        <h2>Step {currentStep}: {STEPS[currentStep - 1].title}</h2>

        {/* Step 1: Personal Information */}
        {currentStep === 1 && (
          <>
            <div className="field">
              <label htmlFor="firstName">First Name *</label>
              <input
                id="firstName"
                type="text"
                {...register('firstName')}
                aria-invalid={errors.firstName ? 'true' : 'false'}
                aria-describedby={errors.firstName ? 'firstName-error' : undefined}
              />
              {errors.firstName && (
                <span id="firstName-error" className="error-message" role="alert">
                  {errors.firstName.message as string}
                </span>
              )}
            </div>

            <div className="field">
              <label htmlFor="lastName">Last Name *</label>
              <input
                id="lastName"
                type="text"
                {...register('lastName')}
                aria-invalid={errors.lastName ? 'true' : 'false'}
                aria-describedby={errors.lastName ? 'lastName-error' : undefined}
              />
              {errors.lastName && (
                <span id="lastName-error" className="error-message" role="alert">
                  {errors.lastName.message as string}
                </span>
              )}
            </div>

            <div className="field">
              <label htmlFor="email">Email Address *</label>
              <input
                id="email"
                type="email"
                {...register('email')}
                aria-invalid={errors.email ? 'true' : 'false'}
                aria-describedby={errors.email ? 'email-error' : undefined}
                placeholder="name@example.com"
              />
              {errors.email && (
                <span id="email-error" className="error-message" role="alert">
                  {errors.email.message as string}
                </span>
              )}
            </div>

            <div className="field">
              <label htmlFor="phone">Phone Number *</label>
              <input
                id="phone"
                type="tel"
                {...register('phone')}
                aria-invalid={errors.phone ? 'true' : 'false'}
                aria-describedby={errors.phone ? 'phone-error phone-help' : 'phone-help'}
                placeholder="5551234567"
              />
              <span id="phone-help" className="help-text">10 digits, no dashes</span>
              {errors.phone && (
                <span id="phone-error" className="error-message" role="alert">
                  {errors.phone.message as string}
                </span>
              )}
            </div>
          </>
        )}

        {/* Step 2: Address */}
        {currentStep === 2 && (
          <>
            <div className="field">
              <label htmlFor="street">Street Address *</label>
              <input
                id="street"
                type="text"
                {...register('street')}
                aria-invalid={errors.street ? 'true' : 'false'}
                aria-describedby={errors.street ? 'street-error' : undefined}
              />
              {errors.street && (
                <span id="street-error" className="error-message" role="alert">
                  {errors.street.message as string}
                </span>
              )}
            </div>

            <div className="field">
              <label htmlFor="city">City *</label>
              <input
                id="city"
                type="text"
                {...register('city')}
                aria-invalid={errors.city ? 'true' : 'false'}
                aria-describedby={errors.city ? 'city-error' : undefined}
              />
              {errors.city && (
                <span id="city-error" className="error-message" role="alert">
                  {errors.city.message as string}
                </span>
              )}
            </div>

            <div className="field-row">
              <div className="field">
                <label htmlFor="state">State *</label>
                <input
                  id="state"
                  type="text"
                  {...register('state')}
                  aria-invalid={errors.state ? 'true' : 'false'}
                  aria-describedby={errors.state ? 'state-error state-help' : 'state-help'}
                  placeholder="CA"
                  maxLength={2}
                />
                <span id="state-help" className="help-text">2 letter code</span>
                {errors.state && (
                  <span id="state-error" className="error-message" role="alert">
                    {errors.state.message as string}
                  </span>
                )}
              </div>

              <div className="field">
                <label htmlFor="zipCode">ZIP Code *</label>
                <input
                  id="zipCode"
                  type="text"
                  {...register('zipCode')}
                  aria-invalid={errors.zipCode ? 'true' : 'false'}
                  aria-describedby={errors.zipCode ? 'zipCode-error' : undefined}
                  placeholder="12345"
                  maxLength={5}
                />
                {errors.zipCode && (
                  <span id="zipCode-error" className="error-message" role="alert">
                    {errors.zipCode.message as string}
                  </span>
                )}
              </div>
            </div>
          </>
        )}

        {/* Step 3: Account */}
        {currentStep === 3 && (
          <>
            <div className="field">
              <label htmlFor="username">Username *</label>
              <input
                id="username"
                type="text"
                {...register('username')}
                aria-invalid={errors.username ? 'true' : 'false'}
                aria-describedby={errors.username ? 'username-error username-help' : 'username-help'}
              />
              <span id="username-help" className="help-text">3-20 characters, letters, numbers, and underscores only</span>
              {errors.username && (
                <span id="username-error" className="error-message" role="alert">
                  {errors.username.message as string}
                </span>
              )}
            </div>

            <div className="field">
              <label htmlFor="password">Password *</label>
              <input
                id="password"
                type="password"
                {...register('password')}
                aria-invalid={errors.password ? 'true' : 'false'}
                aria-describedby={errors.password ? 'password-error password-help' : 'password-help'}
              />
              <span id="password-help" className="help-text">
                Min 8 characters, with uppercase and number
              </span>
              {errors.password && (
                <span id="password-error" className="error-message" role="alert">
                  {errors.password.message as string}
                </span>
              )}
            </div>

            <div className="field">
              <label htmlFor="confirmPassword">Confirm Password *</label>
              <input
                id="confirmPassword"
                type="password"
                {...register('confirmPassword')}
                aria-invalid={errors.confirmPassword ? 'true' : 'false'}
                aria-describedby={errors.confirmPassword ? 'confirmPassword-error' : undefined}
              />
              {errors.confirmPassword && (
                <span id="confirmPassword-error" className="error-message" role="alert">
                  {errors.confirmPassword.message as string}
                </span>
              )}
            </div>
          </>
        )}

        {/* Navigation Buttons */}
        <div className="button-group">
          {currentStep > 1 && (
            <button
              type="button"
              onClick={previousStep}
              className="button button-secondary"
            >
              ← Previous
            </button>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="button button-primary"
          >
            {isSubmitting ? 'Processing...' : currentStep === STEPS.length ? 'Complete Registration' : 'Next →'}
          </button>
        </div>
      </form>
    </div>
  );
}

/**
 * CSS Styles (example)
 *
 * .wizard-container {
 *   max-width: 600px;
 *   margin: 0 auto;
 *   padding: 2rem;
 * }
 *
 * .progress-steps {
 *   display: flex;
 *   justify-content: space-between;
 *   margin-bottom: 2rem;
 *   padding: 0;
 *   list-style: none;
 * }
 *
 * .step {
 *   display: flex;
 *   flex-direction: column;
 *   align-items: center;
 *   flex: 1;
 *   position: relative;
 * }
 *
 * .step::before {
 *   content: '';
 *   position: absolute;
 *   top: 20px;
 *   left: 50%;
 *   right: -50%;
 *   height: 2px;
 *   background: #e5e7eb;
 *   z-index: -1;
 * }
 *
 * .step:last-child::before {
 *   display: none;
 * }
 *
 * .step.completed::before {
 *   background: #22c55e;
 * }
 *
 * .step-number {
 *   width: 40px;
 *   height: 40px;
 *   border-radius: 50%;
 *   background: #e5e7eb;
 *   display: flex;
 *   align-items: center;
 *   justify-content: center;
 *   font-weight: 600;
 *   margin-bottom: 0.5rem;
 * }
 *
 * .step.active .step-number {
 *   background: #3b82f6;
 *   color: white;
 * }
 *
 * .step.completed .step-number {
 *   background: #22c55e;
 *   color: white;
 * }
 *
 * .field-row {
 *   display: grid;
 *   grid-template-columns: 1fr 1fr;
 *   gap: 1rem;
 * }
 *
 * .button-group {
 *   display: flex;
 *   gap: 1rem;
 *   margin-top: 2rem;
 * }
 *
 * .button-secondary {
 *   background: white;
 *   color: #3b82f6;
 *   border: 1px solid #3b82f6;
 * }
 *
 * .sr-only {
 *   position: absolute;
 *   width: 1px;
 *   height: 1px;
 *   padding: 0;
 *   margin: -1px;
 *   overflow: hidden;
 *   clip: rect(0, 0, 0, 0);
 *   white-space: nowrap;
 *   border-width: 0;
 * }
 */
