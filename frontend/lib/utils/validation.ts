// Basic email validation regex
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const isValidEmail = (email: string): boolean => {
  return emailRegex.test(email);
};

export const isStrongPassword = (password: string): boolean => {
  // Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.
  const strongPasswordRegex = new RegExp(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})"
  );
  return strongPasswordRegex.test(password);
};

export const isNotEmpty = (value: string | undefined | null): boolean => {
  return value !== undefined && value !== null && value.trim() !== '';
};

export const isPositiveNumber = (value: number | undefined | null): boolean => {
  return value !== undefined && value !== null && typeof value === 'number' && value > 0;
};

export const getEmailError = (email: string): string | undefined => {
    if (!isNotEmpty(email)) {
      return "Email is required.";
    }
    if (!isValidEmail(email)) {
      return "Please enter a valid email address.";
    }
    return undefined;
  };
  
  export const getPasswordError = (password: string): string | undefined => {
    if (!isNotEmpty(password)) {
      return "Password is required.";
    }
    if (!isStrongPassword(password)) {
      return "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.";
    }
    return undefined;
  };
  
  export const getTaskTitleError = (title: string): string | undefined => {
    if (!isNotEmpty(title)) {
      return "Title is required.";
    }
    return undefined;
  };
  
  export const getTaskDescriptionError = (description: string): string | undefined => {
    if (!isNotEmpty(description)) {
      return "Description is required.";
    }
    return undefined;
  };