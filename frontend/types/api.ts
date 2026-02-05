
export class ApiErrorResponse extends Error {
    detail: string | { [key:string]: string };
    statusCode: number;
  
    constructor(message: string, detail: string | { [key:string]: string }, statusCode: number) {
      super(message);
      this.detail = detail;
      this.statusCode = statusCode;
      this.name = 'ApiErrorResponse';
      // This is to make `instanceof` work correctly in TypeScript
      Object.setPrototypeOf(this, ApiErrorResponse.prototype);
    }
  }
  
  export interface ApiSuccessResponse<T> {
    data: T;
    message: string;
  }
  
  export interface PaginationParams {
    page?: number;
    per_page?: number;
  }
  
  export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    per_page: number;
    pages: number;
  }
