import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Simulate async username check
const checkUsernameAvailability = async (username: string): Promise<boolean> => {
  await new Promise(resolve => setTimeout(resolve, 1000));
  // Simulate taken usernames
  const takenUsernames = ['admin', 'user', 'test', 'demo'];
  return !takenUsernames.includes(username.toLowerCase());
};

// Zod schema with custom async validation
const formSchema = z.object({
  username: z
    .string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters')
    .regex(/^[a-zA-Z0-9_-]+$/, 'Username can only contain letters, numbers, underscores, and hyphens'),
  email: z.string().email('Invalid email address'),
  website: z
    .string()
    .url('Must be a valid URL')
    .or(z.literal('')),
  bio: z
    .string()
    .max(500, 'Bio must be less than 500 characters')
    .optional(),
});

type FormData = z.infer<typeof formSchema>;

// Field validation state
type FieldStatus = 'idle' | 'validating' | 'valid' | 'invalid';

export function InlineValidationForm() {
  const [usernameStatus, setUsernameStatus] = useState<FieldStatus>('idle');
  const [usernameError, setUsernameError] = useState<string>('');

  const {
    register,
    handleSubmit,
    formState: { errors, dirtyFields },
    watch,
    trigger,
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: 'onBlur', // Validate on blur
    reValidateMode: 'onChange', // Re-validate on change after first validation
  });

  const watchedUsername = watch('username');
  const watchedBio = watch('bio');

  // Debounced async username validation
  React.useEffect(() => {
    if (!watchedUsername || watchedUsername.length < 3) {
      setUsernameStatus('idle');
      return;
    }

    // Check schema validation first
    const schemaValidation = formSchema.shape.username.safeParse(watchedUsername);
    if (!schemaValidation.success) {
      setUsernameStatus('idle');
      return;
    }

    setUsernameStatus('validating');
    setUsernameError('');

    const timeoutId = setTimeout(async () => {
      try {
        const isAvailable = await checkUsernameAvailability(watchedUsername);
        if (isAvailable) {
          setUsernameStatus('valid');
          setUsernameError('');
        } else {
          setUsernameStatus('invalid');
          setUsernameError('Username is already taken');
        }
      } catch (error) {
        setUsernameStatus('invalid');
        setUsernameError('Error checking username availability');
      }
    }, 500); // Debounce for 500ms

    return () => clearTimeout(timeoutId);
  }, [watchedUsername]);

  const onSubmit = async (data: FormData) => {
    // Final check for username availability
    if (usernameStatus !== 'valid') {
      setUsernameError('Please wait for username validation to complete');
      return;
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log('Form submitted:', data);
    alert('Profile created successfully!');
  };

  // Get status icon for username field
  const getUsernameStatusIcon = () => {
    if (usernameStatus === 'validating') {
      return (
        <svg className="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      );
    }
    if (usernameStatus === 'valid') {
      return (
        <svg className="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
      );
    }
    if (usernameStatus === 'invalid') {
      return (
        <svg className="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      );
    }
    return null;
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Create Profile</h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Username Field with Async Validation */}
        <div>
          <label
            htmlFor="username"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Username
          </label>
          <div className="relative">
            <input
              id="username"
              type="text"
              {...register('username')}
              className={`w-full px-3 py-2 pr-10 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.username || usernameStatus === 'invalid'
                  ? 'border-red-500'
                  : usernameStatus === 'valid'
                  ? 'border-green-500'
                  : 'border-gray-300'
              }`}
              aria-invalid={errors.username || usernameStatus === 'invalid' ? 'true' : 'false'}
              aria-describedby="username-error username-status"
            />
            {/* Status Icon */}
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              {getUsernameStatusIcon()}
            </div>
          </div>

          {/* Error Messages */}
          {errors.username && (
            <p id="username-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.username.message}
            </p>
          )}
          {usernameError && !errors.username && (
            <p id="username-error" className="mt-1 text-sm text-red-600" role="alert">
              {usernameError}
            </p>
          )}

          {/* Success Message */}
          {usernameStatus === 'valid' && (
            <p id="username-status" className="mt-1 text-sm text-green-600">
              Username is available!
            </p>
          )}

          {/* Loading Message */}
          {usernameStatus === 'validating' && (
            <p id="username-status" className="mt-1 text-sm text-blue-600">
              Checking availability...
            </p>
          )}
        </div>

        {/* Email Field with Real-time Validation */}
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Email Address
          </label>
          <div className="relative">
            <input
              id="email"
              type="email"
              {...register('email')}
              onBlur={() => trigger('email')}
              className={`w-full px-3 py-2 pr-10 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.email
                  ? 'border-red-500'
                  : dirtyFields.email && !errors.email
                  ? 'border-green-500'
                  : 'border-gray-300'
              }`}
              aria-invalid={errors.email ? 'true' : 'false'}
              aria-describedby={errors.email ? 'email-error' : undefined}
            />
            {/* Success Icon */}
            {dirtyFields.email && !errors.email && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            )}
          </div>
          {errors.email && (
            <p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.email.message}
            </p>
          )}
        </div>

        {/* Website Field (Optional) */}
        <div>
          <label
            htmlFor="website"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Website <span className="text-gray-500 text-xs">(optional)</span>
          </label>
          <div className="relative">
            <input
              id="website"
              type="url"
              {...register('website')}
              onBlur={() => trigger('website')}
              placeholder="https://example.com"
              className={`w-full px-3 py-2 pr-10 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.website
                  ? 'border-red-500'
                  : dirtyFields.website && !errors.website
                  ? 'border-green-500'
                  : 'border-gray-300'
              }`}
              aria-invalid={errors.website ? 'true' : 'false'}
              aria-describedby={errors.website ? 'website-error' : undefined}
            />
            {/* Success Icon */}
            {dirtyFields.website && !errors.website && watch('website') && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            )}
          </div>
          {errors.website && (
            <p id="website-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.website.message}
            </p>
          )}
        </div>

        {/* Bio Field with Character Count */}
        <div>
          <label
            htmlFor="bio"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Bio <span className="text-gray-500 text-xs">(optional)</span>
          </label>
          <textarea
            id="bio"
            rows={4}
            {...register('bio')}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.bio ? 'border-red-500' : 'border-gray-300'
            }`}
            aria-invalid={errors.bio ? 'true' : 'false'}
            aria-describedby="bio-error bio-count"
          />
          <div className="flex justify-between items-center mt-1">
            <div>
              {errors.bio && (
                <p id="bio-error" className="text-sm text-red-600" role="alert">
                  {errors.bio.message}
                </p>
              )}
            </div>
            <p
              id="bio-count"
              className={`text-sm ${
                (watchedBio?.length || 0) > 500 ? 'text-red-600' : 'text-gray-500'
              }`}
            >
              {watchedBio?.length || 0} / 500
            </p>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={usernameStatus === 'validating' || usernameStatus === 'invalid'}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Create Profile
        </button>
      </form>
    </div>
  );
}
