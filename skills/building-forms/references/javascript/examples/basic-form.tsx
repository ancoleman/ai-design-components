/**
 * Basic Contact Form Example
 *
 * Demonstrates:
 * - React Hook Form with Zod validation
 * - Accessible form patterns (WCAG 2.1 AA)
 * - Error handling and success states
 * - On-blur validation with progressive enhancement
 * - Modern UX patterns (inline validation, success indicators)
 */

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useState } from 'react';

// Validation schema
const contactSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(50, 'Name must be less than 50 characters'),

  email: z.string()
    .email('Please enter a valid email address')
    .toLowerCase(),

  subject: z.string()
    .min(5, 'Subject must be at least 5 characters')
    .max(100, 'Subject must be less than 100 characters'),

  message: z.string()
    .min(20, 'Message must be at least 20 characters')
    .max(1000, 'Message must be less than 1000 characters'),

  newsletter: z.boolean().default(false),
});

type ContactFormData = z.infer<typeof contactSchema>;

export default function ContactForm() {
  const [isSubmitted, setIsSubmitted] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isValid, touchedFields },
    reset,
    watch,
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
    mode: 'onBlur', // Validate on blur (recommended)
    reValidateMode: 'onChange', // After first error, validate on change
    defaultValues: {
      newsletter: false,
    },
  });

  const messageLength = watch('message')?.length || 0;

  const onSubmit = async (data: ContactFormData) => {
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));

      console.log('Form submitted:', data);

      // Show success state
      setIsSubmitted(true);

      // Reset form after 3 seconds
      setTimeout(() => {
        reset();
        setIsSubmitted(false);
      }, 3000);
    } catch (error) {
      console.error('Submission error:', error);
    }
  };

  if (isSubmitted) {
    return (
      <div className="success-message" role="alert">
        <h2>Thank you for contacting us!</h2>
        <p>We'll get back to you within 24 hours.</p>
      </div>
    );
  }

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate // Use custom validation, not browser default
      aria-labelledby="form-title"
    >
      <h2 id="form-title">Contact Us</h2>

      {/* Name Field */}
      <div className="field">
        <label htmlFor="name">
          Name <span aria-label="required">*</span>
        </label>
        <input
          id="name"
          type="text"
          {...register('name')}
          aria-invalid={errors.name ? 'true' : 'false'}
          aria-describedby={errors.name ? 'name-error' : undefined}
          className={errors.name ? 'error' : touchedFields.name && !errors.name ? 'valid' : ''}
        />
        {errors.name && (
          <span id="name-error" className="error-message" role="alert">
            {errors.name.message}
          </span>
        )}
        {touchedFields.name && !errors.name && (
          <span className="success-message" aria-live="polite">
            ✓ Valid name
          </span>
        )}
      </div>

      {/* Email Field */}
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
          <span className="success-message" aria-live="polite">
            ✓ Valid email
          </span>
        )}
      </div>

      {/* Subject Field */}
      <div className="field">
        <label htmlFor="subject">
          Subject <span aria-label="required">*</span>
        </label>
        <input
          id="subject"
          type="text"
          {...register('subject')}
          aria-invalid={errors.subject ? 'true' : 'false'}
          aria-describedby={errors.subject ? 'subject-error' : undefined}
          className={errors.subject ? 'error' : touchedFields.subject && !errors.subject ? 'valid' : ''}
        />
        {errors.subject && (
          <span id="subject-error" className="error-message" role="alert">
            {errors.subject.message}
          </span>
        )}
      </div>

      {/* Message Field with Character Count */}
      <div className="field">
        <label htmlFor="message">
          Message <span aria-label="required">*</span>
        </label>
        <textarea
          id="message"
          rows={5}
          {...register('message')}
          aria-invalid={errors.message ? 'true' : 'false'}
          aria-describedby={errors.message ? 'message-error message-count' : 'message-count'}
          maxLength={1000}
          className={errors.message ? 'error' : touchedFields.message && !errors.message ? 'valid' : ''}
        />
        <p id="message-count" aria-live="polite" className="character-count">
          {messageLength} / 1000 characters
        </p>
        {errors.message && (
          <span id="message-error" className="error-message" role="alert">
            {errors.message.message}
          </span>
        )}
      </div>

      {/* Newsletter Checkbox */}
      <div className="field checkbox-field">
        <label htmlFor="newsletter">
          <input
            id="newsletter"
            type="checkbox"
            {...register('newsletter')}
          />
          Subscribe to newsletter
        </label>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="submit-button"
      >
        {isSubmitting ? 'Sending...' : 'Send Message'}
      </button>

      {/* Required fields note */}
      <p className="required-note">
        <span aria-label="asterisk">*</span> Required fields
      </p>
    </form>
  );
}

/**
 * CSS Styles (example)
 *
 * .field {
 *   margin-bottom: 1.5rem;
 * }
 *
 * .field label {
 *   display: block;
 *   margin-bottom: 0.5rem;
 *   font-weight: 600;
 * }
 *
 * .field input,
 * .field textarea {
 *   width: 100%;
 *   padding: 0.75rem;
 *   border: 1px solid #d1d5db;
 *   border-radius: 0.375rem;
 *   font-size: 1rem;
 * }
 *
 * .field input.error,
 * .field textarea.error {
 *   border-color: #ef4444;
 * }
 *
 * .field input.valid,
 * .field textarea.valid {
 *   border-color: #22c55e;
 * }
 *
 * .field input:focus,
 * .field textarea:focus {
 *   outline: 2px solid #3b82f6;
 *   outline-offset: 2px;
 * }
 *
 * .error-message {
 *   display: block;
 *   margin-top: 0.25rem;
 *   color: #ef4444;
 *   font-size: 0.875rem;
 * }
 *
 * .success-message {
 *   display: block;
 *   margin-top: 0.25rem;
 *   color: #22c55e;
 *   font-size: 0.875rem;
 * }
 *
 * .character-count {
 *   margin-top: 0.25rem;
 *   font-size: 0.875rem;
 *   color: #6b7280;
 * }
 *
 * .submit-button {
 *   padding: 0.75rem 1.5rem;
 *   background-color: #3b82f6;
 *   color: white;
 *   border: none;
 *   border-radius: 0.375rem;
 *   font-size: 1rem;
 *   font-weight: 600;
 *   cursor: pointer;
 * }
 *
 * .submit-button:hover {
 *   background-color: #2563eb;
 * }
 *
 * .submit-button:disabled {
 *   background-color: #9ca3af;
 *   cursor: not-allowed;
 * }
 *
 * .required-note {
 *   margin-top: 1rem;
 *   font-size: 0.875rem;
 *   color: #6b7280;
 * }
 */
