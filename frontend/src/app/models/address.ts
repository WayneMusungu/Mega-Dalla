import { User } from "./auth";

export interface Address{
    // user: User;
    street_address: string;
    apartment_address: string;
    country: string;
    zip: string;
    address_type: string;
    default: boolean;
}