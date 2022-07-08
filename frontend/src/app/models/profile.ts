import { User } from "./auth.model";

export interface Profile{
    id: number;
    user: User;
    email: string;
    bio: string;
}