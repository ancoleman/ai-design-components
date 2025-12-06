import React from 'react';
import { useForm, useWatch, Controller, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Dynamic schema that adapts based on user type and business type
const createFormSchema = (userType?: string, businessType?: string) => {
  const baseSchema = z.object({
    userType: z.enum(['individual', 'business'], {
      required_error: 'Please select a user type',
    }),
  });

  // Individual-specific fields
  const individualSchema = z.object({
    firstName: z.string().min(2, 'First name required'),
    lastName: z.string().min(2, 'Last name required'),
    dateOfBirth: z.string().min(1, 'Date of birth required'),
  });

  // Business-specific fields
  const businessSchema = z.object({
    businessType: z.enum(['llc', 'corporation', 'nonprofit'], {
      required_error: 'Please select a business type',
    }),
    businessName: z.string().min(2, 'Business name required'),
    taxId: z.string().regex(/^\d{2}-\d{7}$/, 'Tax ID must be in format XX-XXXXXXX'),
  });

  // LLC-specific fields
  const llcSchema = z.object({
    owners: z.array(
      z.object({
        name: z.string().min(1, 'Owner name required'),
        percentage: z.number().min(1).max(100),
      })
    ).min(1, 'At least one owner required'),
  });

  // Corporation-specific fields
  const corporationSchema = z.object({
    stockSymbol: z.string().optional(),
    boardMembers: z.array(
      z.object({
        name: z.string().min(1, 'Board member name required'),
        title: z.string().min(1, 'Title required'),
      })
    ).min(1, 'At least one board member required'),
  });

  // Nonprofit-specific fields
  const nonprofitSchema = z.object({
    missionStatement: z.string().min(10, 'Mission statement required (min 10 characters)'),
    ein: z.string().regex(/^\d{2}-\d{7}$/, 'EIN must be in format XX-XXXXXXX'),
  });

  // Common fields for both types
  const commonSchema = z.object({
    email: z.string().email('Invalid email'),
    phone: z.string().regex(/^\+?[\d\s-()]+$/, 'Invalid phone number'),
    country: z.string().min(1, 'Country required'),
    state: z.string().optional(),
  });

  // Build schema based on selections
  if (userType === 'individual') {
    return baseSchema.merge(individualSchema).merge(commonSchema);
  }

  if (userType === 'business') {
    let businessFullSchema = baseSchema.merge(businessSchema).merge(commonSchema);

    if (businessType === 'llc') {
      businessFullSchema = businessFullSchema.merge(llcSchema) as any;
    } else if (businessType === 'corporation') {
      businessFullSchema = businessFullSchema.merge(corporationSchema) as any;
    } else if (businessType === 'nonprofit') {
      businessFullSchema = businessFullSchema.merge(nonprofitSchema) as any;
    }

    return businessFullSchema;
  }

  return baseSchema.merge(commonSchema);
};

// Type for the most complete form
type FormData = z.infer<ReturnType<typeof createFormSchema>>;

export function ConditionalForm() {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    setValue,
  } = useForm<FormData>({
    resolver: zodResolver(createFormSchema()),
    mode: 'onChange',
  });

  // Watch fields to show/hide conditional sections
  const userType = useWatch({ control, name: 'userType' });
  const businessType = useWatch({ control, name: 'businessType' as any });
  const country = useWatch({ control, name: 'country' });

  // Field arrays for dynamic lists
  const {
    fields: ownerFields,
    append: appendOwner,
    remove: removeOwner,
  } = useFieldArray({
    control,
    name: 'owners' as any,
  });

  const {
    fields: boardFields,
    append: appendBoard,
    remove: removeBoard,
  } = useFieldArray({
    control,
    name: 'boardMembers' as any,
  });

  const onSubmit = async (data: FormData) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log('Form submitted:', data);
    alert('Registration submitted successfully!');
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Account Registration</h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* User Type Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            I am registering as <span className="text-red-500">*</span>
          </label>
          <div className="space-y-2">
            <label className="flex items-start p-3 border rounded-md hover:bg-gray-50 cursor-pointer">
              <input
                type="radio"
                value="individual"
                {...register('userType')}
                className="h-4 w-4 mt-0.5 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <div className="ml-3">
                <span className="text-sm font-medium text-gray-700">Individual</span>
                <p className="text-xs text-gray-500">Personal account for individual use</p>
              </div>
            </label>
            <label className="flex items-start p-3 border rounded-md hover:bg-gray-50 cursor-pointer">
              <input
                type="radio"
                value="business"
                {...register('userType')}
                className="h-4 w-4 mt-0.5 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <div className="ml-3">
                <span className="text-sm font-medium text-gray-700">Business</span>
                <p className="text-xs text-gray-500">Business or organization account</p>
              </div>
            </label>
          </div>
          {errors.userType && (
            <p className="mt-1 text-sm text-red-600">{errors.userType.message}</p>
          )}
        </div>

        {/* Individual-Specific Fields */}
        {userType === 'individual' && (
          <div className="p-4 bg-blue-50 rounded-md space-y-4">
            <h3 className="font-semibold text-gray-700">Personal Information</h3>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
                  First Name <span className="text-red-500">*</span>
                </label>
                <input
                  id="firstName"
                  {...register('firstName' as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {errors.firstName && (
                  <p className="mt-1 text-sm text-red-600">{(errors.firstName as any).message}</p>
                )}
              </div>

              <div>
                <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
                  Last Name <span className="text-red-500">*</span>
                </label>
                <input
                  id="lastName"
                  {...register('lastName' as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {errors.lastName && (
                  <p className="mt-1 text-sm text-red-600">{(errors.lastName as any).message}</p>
                )}
              </div>
            </div>

            <div>
              <label htmlFor="dateOfBirth" className="block text-sm font-medium text-gray-700 mb-1">
                Date of Birth <span className="text-red-500">*</span>
              </label>
              <input
                id="dateOfBirth"
                type="date"
                {...register('dateOfBirth' as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {errors.dateOfBirth && (
                <p className="mt-1 text-sm text-red-600">{(errors.dateOfBirth as any).message}</p>
              )}
            </div>
          </div>
        )}

        {/* Business-Specific Fields */}
        {userType === 'business' && (
          <div className="p-4 bg-green-50 rounded-md space-y-4">
            <h3 className="font-semibold text-gray-700">Business Information</h3>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Business Type <span className="text-red-500">*</span>
              </label>
              <select
                {...register('businessType' as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a type...</option>
                <option value="llc">LLC</option>
                <option value="corporation">Corporation</option>
                <option value="nonprofit">Nonprofit</option>
              </select>
              {errors.businessType && (
                <p className="mt-1 text-sm text-red-600">{(errors.businessType as any).message}</p>
              )}
            </div>

            <div>
              <label htmlFor="businessName" className="block text-sm font-medium text-gray-700 mb-1">
                Business Name <span className="text-red-500">*</span>
              </label>
              <input
                id="businessName"
                {...register('businessName' as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {errors.businessName && (
                <p className="mt-1 text-sm text-red-600">{(errors.businessName as any).message}</p>
              )}
            </div>

            <div>
              <label htmlFor="taxId" className="block text-sm font-medium text-gray-700 mb-1">
                Tax ID <span className="text-red-500">*</span>
                <span className="text-xs text-gray-500 ml-1">(Format: XX-XXXXXXX)</span>
              </label>
              <input
                id="taxId"
                {...register('taxId' as any)}
                placeholder="12-3456789"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {errors.taxId && (
                <p className="mt-1 text-sm text-red-600">{(errors.taxId as any).message}</p>
              )}
            </div>

            {/* LLC-Specific Fields */}
            {businessType === 'llc' && (
              <div className="p-3 bg-white rounded-md border border-gray-200">
                <h4 className="font-semibold text-gray-700 mb-3">LLC Owners</h4>
                {ownerFields.map((field, index) => (
                  <div key={field.id} className="flex gap-2 mb-2">
                    <div className="flex-1">
                      <input
                        {...register(`owners.${index}.name` as any)}
                        placeholder="Owner name"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="w-24">
                      <input
                        type="number"
                        {...register(`owners.${index}.percentage` as any, { valueAsNumber: true })}
                        placeholder="%"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <button
                      type="button"
                      onClick={() => removeOwner(index)}
                      className="px-3 py-2 text-red-600 hover:bg-red-50 rounded-md"
                    >
                      Remove
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => appendOwner({ name: '', percentage: 0 })}
                  className="mt-2 px-4 py-2 text-sm text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50"
                >
                  Add Owner
                </button>
              </div>
            )}

            {/* Corporation-Specific Fields */}
            {businessType === 'corporation' && (
              <div className="p-3 bg-white rounded-md border border-gray-200">
                <div className="mb-3">
                  <label htmlFor="stockSymbol" className="block text-sm font-medium text-gray-700 mb-1">
                    Stock Symbol (if publicly traded)
                  </label>
                  <input
                    id="stockSymbol"
                    {...register('stockSymbol' as any)}
                    placeholder="AAPL"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <h4 className="font-semibold text-gray-700 mb-3">Board Members</h4>
                {boardFields.map((field, index) => (
                  <div key={field.id} className="flex gap-2 mb-2">
                    <div className="flex-1">
                      <input
                        {...register(`boardMembers.${index}.name` as any)}
                        placeholder="Board member name"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="flex-1">
                      <input
                        {...register(`boardMembers.${index}.title` as any)}
                        placeholder="Title"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <button
                      type="button"
                      onClick={() => removeBoard(index)}
                      className="px-3 py-2 text-red-600 hover:bg-red-50 rounded-md"
                    >
                      Remove
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => appendBoard({ name: '', title: '' })}
                  className="mt-2 px-4 py-2 text-sm text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50"
                >
                  Add Board Member
                </button>
              </div>
            )}

            {/* Nonprofit-Specific Fields */}
            {businessType === 'nonprofit' && (
              <div className="p-3 bg-white rounded-md border border-gray-200">
                <div className="mb-3">
                  <label htmlFor="missionStatement" className="block text-sm font-medium text-gray-700 mb-1">
                    Mission Statement <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    id="missionStatement"
                    rows={3}
                    {...register('missionStatement' as any)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.missionStatement && (
                    <p className="mt-1 text-sm text-red-600">{(errors.missionStatement as any).message}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="ein" className="block text-sm font-medium text-gray-700 mb-1">
                    EIN (Employer Identification Number) <span className="text-red-500">*</span>
                  </label>
                  <input
                    id="ein"
                    {...register('ein' as any)}
                    placeholder="12-3456789"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.ein && (
                    <p className="mt-1 text-sm text-red-600">{(errors.ein as any).message}</p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Common Contact Fields (shown for both types) */}
        {userType && (
          <div className="space-y-4">
            <h3 className="font-semibold text-gray-700">Contact Information</h3>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email <span className="text-red-500">*</span>
              </label>
              <input
                id="email"
                type="email"
                {...register('email')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                Phone <span className="text-red-500">*</span>
              </label>
              <input
                id="phone"
                type="tel"
                {...register('phone')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {errors.phone && (
                <p className="mt-1 text-sm text-red-600">{errors.phone.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="country" className="block text-sm font-medium text-gray-700 mb-1">
                Country <span className="text-red-500">*</span>
              </label>
              <select
                id="country"
                {...register('country')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a country...</option>
                <option value="US">United States</option>
                <option value="CA">Canada</option>
                <option value="UK">United Kingdom</option>
                <option value="AU">Australia</option>
              </select>
              {errors.country && (
                <p className="mt-1 text-sm text-red-600">{errors.country.message}</p>
              )}
            </div>

            {/* Conditional State Field (only for US and CA) */}
            {(country === 'US' || country === 'CA') && (
              <div>
                <label htmlFor="state" className="block text-sm font-medium text-gray-700 mb-1">
                  State/Province
                </label>
                <select
                  id="state"
                  {...register('state')}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select a state...</option>
                  {country === 'US' && (
                    <>
                      <option value="CA">California</option>
                      <option value="NY">New York</option>
                      <option value="TX">Texas</option>
                      <option value="FL">Florida</option>
                    </>
                  )}
                  {country === 'CA' && (
                    <>
                      <option value="ON">Ontario</option>
                      <option value="QC">Quebec</option>
                      <option value="BC">British Columbia</option>
                      <option value="AB">Alberta</option>
                    </>
                  )}
                </select>
              </div>
            )}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!userType}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
        >
          Submit Registration
        </button>
      </form>
    </div>
  );
}
