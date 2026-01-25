// Generic API response wrapper
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

// API error response
export interface ApiError {
  error: string;
  message: string;
  statusCode: number;
}

// API error class for better error handling
export class ApiErrorResponse extends Error {
  statusCode: number;
  error: string;

  constructor(error: ApiError) {
    super(error.message);
    this.name = "ApiErrorResponse";
    this.statusCode = error.statusCode;
    this.error = error.error;
  }
}
