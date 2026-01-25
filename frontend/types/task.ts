// Task type definition
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string; // ISO 8601 format
  updatedAt: string; // ISO 8601 format
  userId: string;
}

// Task form data for create/update operations
export interface TaskFormData {
  title: string;
  description?: string;
}

// Task update data (all fields optional)
export interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
}
