export interface Customer {
  id: number;
  customer_code: string;
  customer_name: string;
  contact_person?: string | null;
  email?: string | null;
  phone_number?: string | null;
  billing_address?: string | null;
  shipping_address?: string | null;
  credit_limit: number;
  payment_terms?: string | null;
}

export interface CustomerErrors{
  customer_code: string;
  customer_name: string;
}