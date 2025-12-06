import React, { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Zod schemas for each step
const step1Schema = z.object({
  firstName: z.string().min(2, 'First name required'),
  lastName: z.string().min(2, 'Last name required'),
  email: z.string().email('Invalid email'),
});

const step2Schema = z.object({
  company: z.string().min(2, 'Company name required'),
  jobTitle: z.string().min(2, 'Job title required'),
  phone: z.string().regex(/^\+?[\d\s-()]+$/, 'Invalid phone number'),
});

const step3Schema = z.object({
  skills: z.array(
    z.object({
      name: z.string().min(1, 'Skill name required'),
      level: z.enum(['beginner', 'intermediate', 'advanced']),
    })
  ).min(1, 'Add at least one skill'),
});

// Combined schema for final validation
const wizardSchema = z.object({
  ...step1Schema.shape,
  ...step2Schema.shape,
  ...step3Schema.shape,
});

type WizardFormData = z.infer<typeof wizardSchema>;

const steps = [
  { id: 1, name: 'Personal Info', schema: step1Schema },
  { id: 2, name: 'Professional Info', schema: step2Schema },
  { id: 3, name: 'Skills', schema: step3Schema },
  { id: 4, name: 'Review', schema: wizardSchema },
];

export function MultiStepWizard() {
  const [currentStep, setCurrentStep] = useState(1);

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    trigger,
    getValues,
  } = useForm<WizardFormData>({
    resolver: zodResolver(wizardSchema),
    defaultValues: {
      skills: [{ name: '', level: 'beginner' }],
    },
    mode: 'onBlur',
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'skills',
  });

  // Validate current step before proceeding
  const validateStep = async (step: number): Promise<boolean> => {
    let fieldsToValidate: (keyof WizardFormData)[] = [];

    if (step === 1) fieldsToValidate = ['firstName', 'lastName', 'email'];
    if (step === 2) fieldsToValidate = ['company', 'jobTitle', 'phone'];
    if (step === 3) fieldsToValidate = ['skills'];

    const result = await trigger(fieldsToValidate as any);
    return result;
  };

  const handleNext = async () => {
    const isValid = await validateStep(currentStep);
    if (isValid) {
      setCurrentStep(prev => Math.min(prev + 1, steps.length));
    }
  };

  const handlePrevious = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const onSubmit = async (data: WizardFormData) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log('Wizard completed:', data);
    alert('Registration completed successfully!');
  };

  const formData = getValues();

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      {/* Progress Indicator */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          {steps.map((step, index) => (
            <React.Fragment key={step.id}>
              <div className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                    currentStep >= step.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {step.id}
                </div>
                <span className="text-xs mt-1 text-gray-600">{step.name}</span>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={`flex-1 h-1 mx-2 ${
                    currentStep > step.id ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Step 1: Personal Info */}
        {currentStep === 1 && (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold mb-4">Personal Information</h3>

            <div>
              <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
                First Name
              </label>
              <input
                id="firstName"
                {...register('firstName')}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.firstName ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.firstName && (
                <p className="mt-1 text-sm text-red-600">{errors.firstName.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
                Last Name
              </label>
              <input
                id="lastName"
                {...register('lastName')}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.lastName ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.lastName && (
                <p className="mt-1 text-sm text-red-600">{errors.lastName.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                id="email"
                type="email"
                {...register('email')}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.email ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>
          </div>
        )}

        {/* Step 2: Professional Info */}
        {currentStep === 2 && (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold mb-4">Professional Information</h3>

            <div>
              <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-1">
                Company
              </label>
              <input
                id="company"
                {...register('company')}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.company ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.company && (
                <p className="mt-1 text-sm text-red-600">{errors.company.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="jobTitle" className="block text-sm font-medium text-gray-700 mb-1">
                Job Title
              </label>
              <input
                id="jobTitle"
                {...register('jobTitle')}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.jobTitle ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.jobTitle && (
                <p className="mt-1 text-sm text-red-600">{errors.jobTitle.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                Phone Number
              </label>
              <input
                id="phone"
                type="tel"
                {...register('phone')}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.phone ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.phone && (
                <p className="mt-1 text-sm text-red-600">{errors.phone.message}</p>
              )}
            </div>
          </div>
        )}

        {/* Step 3: Skills */}
        {currentStep === 3 && (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold mb-4">Your Skills</h3>

            {fields.map((field, index) => (
              <div key={field.id} className="flex gap-2 items-start">
                <div className="flex-1">
                  <label htmlFor={`skills.${index}.name`} className="block text-sm font-medium text-gray-700 mb-1">
                    Skill Name
                  </label>
                  <input
                    id={`skills.${index}.name`}
                    {...register(`skills.${index}.name` as const)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.skills?.[index]?.name && (
                    <p className="mt-1 text-sm text-red-600">{errors.skills[index]?.name?.message}</p>
                  )}
                </div>

                <div className="flex-1">
                  <label htmlFor={`skills.${index}.level`} className="block text-sm font-medium text-gray-700 mb-1">
                    Level
                  </label>
                  <select
                    id={`skills.${index}.level`}
                    {...register(`skills.${index}.level` as const)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>

                <button
                  type="button"
                  onClick={() => remove(index)}
                  disabled={fields.length === 1}
                  className="mt-7 px-3 py-2 text-red-600 hover:bg-red-50 rounded-md disabled:opacity-50"
                >
                  Remove
                </button>
              </div>
            ))}

            {errors.skills && typeof errors.skills.message === 'string' && (
              <p className="text-sm text-red-600">{errors.skills.message}</p>
            )}

            <button
              type="button"
              onClick={() => append({ name: '', level: 'beginner' })}
              className="px-4 py-2 text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50"
            >
              Add Skill
            </button>
          </div>
        )}

        {/* Step 4: Review */}
        {currentStep === 4 && (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold mb-4">Review Your Information</h3>

            <div className="bg-gray-50 p-4 rounded-md space-y-3">
              <div>
                <h4 className="font-semibold text-gray-700">Personal Information</h4>
                <p>Name: {formData.firstName} {formData.lastName}</p>
                <p>Email: {formData.email}</p>
              </div>

              <div>
                <h4 className="font-semibold text-gray-700">Professional Information</h4>
                <p>Company: {formData.company}</p>
                <p>Job Title: {formData.jobTitle}</p>
                <p>Phone: {formData.phone}</p>
              </div>

              <div>
                <h4 className="font-semibold text-gray-700">Skills</h4>
                <ul className="list-disc list-inside">
                  {formData.skills?.map((skill, index) => (
                    <li key={index}>
                      {skill.name} - {skill.level}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-6">
          <button
            type="button"
            onClick={handlePrevious}
            disabled={currentStep === 1}
            className="px-6 py-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          {currentStep < steps.length ? (
            <button
              type="button"
              onClick={handleNext}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Next
            </button>
          ) : (
            <button
              type="submit"
              className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Submit
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
