import { User } from "./auth";

export interface Profile{
    id: number;
    user: User;
    email: string;
    bio: string;
}