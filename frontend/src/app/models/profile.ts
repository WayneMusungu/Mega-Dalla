import { User } from "./auth";

export interface Profile{
    id?: number;
    user?: User;
    email?: string;
    bio: string;
    phone_number: any;
    url?: string;
}
export class Prof{
    constructor(
       
        public id: number,
        public user: User,
        public email: string,
        public bio: string,
        public phone_number:any,
        public url: string,
    ){}
    
}