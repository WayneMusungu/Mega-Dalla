export interface signupModel{
    email: string,
    username: string,
    password: string,
    is_vendor: boolean,
    is_customer:boolean,
}
export interface loginModel{
    username: string,
    password: string
}
export class Userr{
    constructor(
       
        public id: number,
        public email: string,
        public username: string,
        public is_vendor: boolean,
        public is_customer:boolean,
    ){}
    
}
export interface User{
    id: number;
    username: string,
    email: string,
    is_vendor?: boolean,
    is_customer?: boolean,
    password?: string,
}