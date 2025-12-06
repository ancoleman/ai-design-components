import React, { useState, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Zod schema for settings
const settingsSchema = z.object({
  emailNotifications: z.boolean(),
  pushNotifications: z.boolean(),
  smsNotifications: z.boolean(),
  newsletter: z.boolean(),
  theme: z.enum(['light', 'dark', 'auto']),
  language: z.string(),
  timezone: z.string(),
  privacy: z.enum(['public', 'friends', 'private']),
  notificationFrequency: z.array(z.string()).min(1, 'Select at least one option'),
});

type SettingsFormData = z.infer<typeof settingsSchema>;

// Simulate API call to save settings
const saveSettings = async (data: SettingsFormData): Promise<void> => {
  await new Promise(resolve => setTimeout(resolve, 500));
  console.log('Settings saved:', data);
};

export function SettingsForm() {
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');

  // Initialize with default/loaded settings
  const {
    control,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<SettingsFormData>({
    resolver: zodResolver(settingsSchema),
    defaultValues: {
      emailNotifications: true,
      pushNotifications: false,
      smsNotifications: false,
      newsletter: true,
      theme: 'auto',
      language: 'en',
      timezone: 'America/New_York',
      privacy: 'friends',
      notificationFrequency: ['daily'],
    },
  });

  // Watch all form values for auto-save
  const formValues = watch();

  // Auto-save on change with debounce
  useEffect(() => {
    const timeoutId = setTimeout(async () => {
      try {
        setSaveStatus('saving');
        setIsSaving(true);
        await saveSettings(formValues);
        setSaveStatus('saved');
        setLastSaved(new Date());

        // Reset status after 2 seconds
        setTimeout(() => setSaveStatus('idle'), 2000);
      } catch (error) {
        setSaveStatus('error');
        console.error('Error saving settings:', error);
      } finally {
        setIsSaving(false);
      }
    }, 1000); // Debounce for 1 second

    return () => clearTimeout(timeoutId);
  }, [formValues]);

  const onSubmit = async (data: SettingsFormData) => {
    // Manual save (if needed)
    console.log('Manual save:', data);
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      {/* Header with Save Status */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Settings</h2>
        <div className="flex items-center gap-2">
          {saveStatus === 'saving' && (
            <div className="flex items-center text-sm text-blue-600">
              <svg className="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Saving...
            </div>
          )}
          {saveStatus === 'saved' && (
            <div className="flex items-center text-sm text-green-600">
              <svg className="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Saved
            </div>
          )}
          {saveStatus === 'error' && (
            <div className="flex items-center text-sm text-red-600">
              <svg className="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Error saving
            </div>
          )}
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Notifications Section */}
        <div className="border-b pb-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-700">Notifications</h3>

          {/* Toggle Switches */}
          <div className="space-y-4">
            <Controller
              name="emailNotifications"
              control={control}
              render={({ field }) => (
                <div className="flex items-center justify-between">
                  <div>
                    <label htmlFor="emailNotifications" className="text-sm font-medium text-gray-700">
                      Email Notifications
                    </label>
                    <p className="text-xs text-gray-500">Receive notifications via email</p>
                  </div>
                  <button
                    type="button"
                    id="emailNotifications"
                    role="switch"
                    aria-checked={field.value}
                    onClick={() => field.onChange(!field.value)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                      field.value ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        field.value ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              )}
            />

            <Controller
              name="pushNotifications"
              control={control}
              render={({ field }) => (
                <div className="flex items-center justify-between">
                  <div>
                    <label htmlFor="pushNotifications" className="text-sm font-medium text-gray-700">
                      Push Notifications
                    </label>
                    <p className="text-xs text-gray-500">Receive push notifications on your device</p>
                  </div>
                  <button
                    type="button"
                    id="pushNotifications"
                    role="switch"
                    aria-checked={field.value}
                    onClick={() => field.onChange(!field.value)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                      field.value ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        field.value ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              )}
            />

            <Controller
              name="smsNotifications"
              control={control}
              render={({ field }) => (
                <div className="flex items-center justify-between">
                  <div>
                    <label htmlFor="smsNotifications" className="text-sm font-medium text-gray-700">
                      SMS Notifications
                    </label>
                    <p className="text-xs text-gray-500">Receive notifications via text message</p>
                  </div>
                  <button
                    type="button"
                    id="smsNotifications"
                    role="switch"
                    aria-checked={field.value}
                    onClick={() => field.onChange(!field.value)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                      field.value ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        field.value ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              )}
            />

            <Controller
              name="newsletter"
              control={control}
              render={({ field }) => (
                <div className="flex items-center justify-between">
                  <div>
                    <label htmlFor="newsletter" className="text-sm font-medium text-gray-700">
                      Newsletter
                    </label>
                    <p className="text-xs text-gray-500">Subscribe to our weekly newsletter</p>
                  </div>
                  <button
                    type="button"
                    id="newsletter"
                    role="switch"
                    aria-checked={field.value}
                    onClick={() => field.onChange(!field.value)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                      field.value ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        field.value ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              )}
            />
          </div>
        </div>

        {/* Appearance Section */}
        <div className="border-b pb-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-700">Appearance</h3>

          {/* Theme Radio Group */}
          <Controller
            name="theme"
            control={control}
            render={({ field }) => (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Theme
                </label>
                <div className="space-y-2">
                  {(['light', 'dark', 'auto'] as const).map((theme) => (
                    <label key={theme} className="flex items-center">
                      <input
                        type="radio"
                        value={theme}
                        checked={field.value === theme}
                        onChange={() => field.onChange(theme)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                      />
                      <span className="ml-2 text-sm text-gray-700 capitalize">{theme}</span>
                    </label>
                  ))}
                </div>
              </div>
            )}
          />
        </div>

        {/* Localization Section */}
        <div className="border-b pb-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-700">Localization</h3>

          {/* Language Select */}
          <div className="mb-4">
            <Controller
              name="language"
              control={control}
              render={({ field }) => (
                <div>
                  <label htmlFor="language" className="block text-sm font-medium text-gray-700 mb-1">
                    Language
                  </label>
                  <select
                    id="language"
                    {...field}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    <option value="ja">Japanese</option>
                  </select>
                </div>
              )}
            />
          </div>

          {/* Timezone Select */}
          <div>
            <Controller
              name="timezone"
              control={control}
              render={({ field }) => (
                <div>
                  <label htmlFor="timezone" className="block text-sm font-medium text-gray-700 mb-1">
                    Timezone
                  </label>
                  <select
                    id="timezone"
                    {...field}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="America/New_York">Eastern Time</option>
                    <option value="America/Chicago">Central Time</option>
                    <option value="America/Denver">Mountain Time</option>
                    <option value="America/Los_Angeles">Pacific Time</option>
                    <option value="Europe/London">London</option>
                    <option value="Europe/Paris">Paris</option>
                    <option value="Asia/Tokyo">Tokyo</option>
                  </select>
                </div>
              )}
            />
          </div>
        </div>

        {/* Privacy Section */}
        <div className="border-b pb-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-700">Privacy</h3>

          {/* Privacy Radio Group */}
          <Controller
            name="privacy"
            control={control}
            render={({ field }) => (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Profile Visibility
                </label>
                <div className="space-y-2">
                  <label className="flex items-start">
                    <input
                      type="radio"
                      value="public"
                      checked={field.value === 'public'}
                      onChange={() => field.onChange('public')}
                      className="h-4 w-4 mt-0.5 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <div className="ml-2">
                      <span className="text-sm font-medium text-gray-700">Public</span>
                      <p className="text-xs text-gray-500">Anyone can see your profile</p>
                    </div>
                  </label>
                  <label className="flex items-start">
                    <input
                      type="radio"
                      value="friends"
                      checked={field.value === 'friends'}
                      onChange={() => field.onChange('friends')}
                      className="h-4 w-4 mt-0.5 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <div className="ml-2">
                      <span className="text-sm font-medium text-gray-700">Friends Only</span>
                      <p className="text-xs text-gray-500">Only your friends can see your profile</p>
                    </div>
                  </label>
                  <label className="flex items-start">
                    <input
                      type="radio"
                      value="private"
                      checked={field.value === 'private'}
                      onChange={() => field.onChange('private')}
                      className="h-4 w-4 mt-0.5 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <div className="ml-2">
                      <span className="text-sm font-medium text-gray-700">Private</span>
                      <p className="text-xs text-gray-500">Only you can see your profile</p>
                    </div>
                  </label>
                </div>
              </div>
            )}
          />
        </div>

        {/* Notification Frequency Section */}
        <div>
          <h3 className="text-lg font-semibold mb-4 text-gray-700">Notification Frequency</h3>

          {/* Checkbox Group */}
          <Controller
            name="notificationFrequency"
            control={control}
            render={({ field }) => (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Send me notifications
                </label>
                <div className="space-y-2">
                  {['instant', 'daily', 'weekly'].map((frequency) => (
                    <label key={frequency} className="flex items-center">
                      <input
                        type="checkbox"
                        value={frequency}
                        checked={field.value.includes(frequency)}
                        onChange={(e) => {
                          const newValue = e.target.checked
                            ? [...field.value, frequency]
                            : field.value.filter((v) => v !== frequency);
                          field.onChange(newValue);
                        }}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span className="ml-2 text-sm text-gray-700 capitalize">{frequency}</span>
                    </label>
                  ))}
                </div>
                {errors.notificationFrequency && (
                  <p className="mt-1 text-sm text-red-600">{errors.notificationFrequency.message}</p>
                )}
              </div>
            )}
          />
        </div>
      </form>

      {/* Last Saved Info */}
      {lastSaved && (
        <p className="mt-6 text-xs text-gray-500 text-center">
          Last saved at {lastSaved.toLocaleTimeString()}
        </p>
      )}
    </div>
  );
}
