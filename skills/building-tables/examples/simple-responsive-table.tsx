import React from 'react';

/**
 * Simple Responsive Table Example
 *
 * Transforms from table layout (desktop) to card layout (mobile)
 * using CSS media queries and Tailwind responsive utilities.
 */

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  joinDate: string;
}

const users: User[] = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin', joinDate: '2025-01-15' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'Editor', joinDate: '2025-03-22' },
  { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'Viewer', joinDate: '2025-06-10' },
];

export function SimpleResponsiveTable() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Users</h1>

      {/* Desktop: Table */}
      <div className="hidden md:block overflow-x-auto border rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Join Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y">
            {users.map((user) => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap font-medium">{user.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-600">{user.email}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                    {user.role}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-600">{user.joinDate}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <button className="text-blue-600 hover:text-blue-800 mr-2">Edit</button>
                  <button className="text-red-600 hover:text-red-800">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile: Cards */}
      <div className="md:hidden space-y-4">
        {users.map((user) => (
          <div key={user.id} className="border rounded-lg p-4 bg-white shadow-sm">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-semibold text-lg">{user.name}</h3>
                <p className="text-sm text-gray-600">{user.email}</p>
              </div>
              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                {user.role}
              </span>
            </div>

            <div className="text-sm text-gray-600 mb-3">
              Joined: {user.joinDate}
            </div>

            <div className="flex gap-2">
              <button className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg">
                Edit
              </button>
              <button className="flex-1 px-4 py-2 bg-white border border-red-500 text-red-500 rounded-lg">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="mt-4 text-sm text-gray-600">
        Total: {users.length} users
      </div>
    </div>
  );
}

export default SimpleResponsiveTable;
